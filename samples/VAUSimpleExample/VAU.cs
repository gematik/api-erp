using System;
using System.IO;
using System.Linq;
using System.Net;
using System.Security.Cryptography;
using System.Security.Cryptography.X509Certificates;
using System.Text;
using Org.BouncyCastle.Asn1.TeleTrust;
using Org.BouncyCastle.Asn1.X9;
using Org.BouncyCastle.Crypto;
using Org.BouncyCastle.Crypto.Agreement;
using Org.BouncyCastle.Crypto.Digests;
using Org.BouncyCastle.Crypto.Engines;
using Org.BouncyCastle.Crypto.Generators;
using Org.BouncyCastle.Crypto.Modes;
using Org.BouncyCastle.Crypto.Parameters;
using Org.BouncyCastle.Math;
using Org.BouncyCastle.Security;

namespace VAUSimpleExample {
    public class VAU {
        readonly SecureRandom _random = new();

        public byte[] GetRandom(int cntBytes) {
            byte[] keyBytes = new byte[cntBytes];
            _random.NextBytes(keyBytes);
            return keyBytes;
        }

        protected virtual byte[] GetIv() {
            byte[] keyBytes = new byte[96 / 8];
            _random.NextBytes(keyBytes);
            return keyBytes;
        }

        protected virtual ECParameters GenerateNewECDHKey() {
            //eigener Key
            ECDsa key = ECDsa.Create(ECCurve.NamedCurves.brainpoolP256r1);
            var myexportParameters = key.ExportParameters(true);
            return myexportParameters;
        }

        protected virtual KeyCoords GetVauPublicKeyXY() {
            string VAUzertifikat = "https://fd.erezept-instanz1.titus.ti-dienste.de/VAUCertificate";

            var zert = new WebClient().DownloadData(VAUzertifikat);
            var z = new X509Certificate2(zert);

            var bc = DotNetUtilities.FromX509Certificate(z);
            var x = (ECPublicKeyParameters) bc.GetPublicKey();

            return new KeyCoords {
                X = new BigInteger(1, x.Q.XCoord.GetEncoded()),
                Y = new BigInteger(1, x.Q.YCoord.GetEncoded())
            };
        }

        /// <summary>
        /// verschlüsselt einen Request für die VAU
        /// </summary>
        /// <param name="message"></param>
        /// <returns></returns>
        public byte[] Encrypt(string message) {
            X9ECParameters x9EC = ECNamedCurveTable.GetByOid(TeleTrusTObjectIdentifiers.BrainpoolP256R1);
            ECDomainParameters ecDomain = new ECDomainParameters(x9EC.Curve, x9EC.G, x9EC.N, x9EC.H, x9EC.GetSeed());

            ECParameters myECDHKey = GenerateNewECDHKey();
            ECPrivateKeyParameters myPrivate = new ECPrivateKeyParameters(new BigInteger(1, myECDHKey.D), ecDomain);
            Console.Out.WriteLine("MY public X=" + ByteArrayToHexString(myECDHKey.Q.X));
            Console.Out.WriteLine("MY public Y=" + ByteArrayToHexString(myECDHKey.Q.Y));
            Console.Out.WriteLine("MY private =" + ByteArrayToHexString(myECDHKey.D));

            KeyCoords vauPublicKeyXY = GetVauPublicKeyXY();
            var point = x9EC.Curve.CreatePoint(vauPublicKeyXY.X, vauPublicKeyXY.Y);
            ECPublicKeyParameters vauPublicKey = new ECPublicKeyParameters(point, ecDomain);
            Console.Out.WriteLine("VAU X=" + vauPublicKeyXY.X.ToString(16));
            Console.Out.WriteLine("VAU Y=" + vauPublicKeyXY.Y.ToString(16));

            //SharedSecret
            IBasicAgreement aKeyAgree = new ECDHBasicAgreement();
            aKeyAgree.Init(myPrivate);
            BigInteger sharedSecret = aKeyAgree.CalculateAgreement(vauPublicKey);
            byte[] sharedSecretBytes = sharedSecret.ToByteArray().ToArray();

            //sharedSecretBytes muss 32 Byte groß sein entweder vorn abschneiden oder mit 0 auffüllen
            if (sharedSecretBytes.Length > 32) {
                sharedSecretBytes = sharedSecretBytes.Skip(sharedSecretBytes.Length - 32).ToArray();
            } else if (sharedSecretBytes.Length < 32) {
                sharedSecretBytes = Enumerable.Repeat((byte) 0, 32 - sharedSecretBytes.Length).Concat(sharedSecretBytes).ToArray();
            }
            Console.Out.WriteLine($"SharedSecret={ByteArrayToHexString(sharedSecretBytes)} {sharedSecretBytes.Length}");

            //HKDF
            byte[] info = Encoding.UTF8.GetBytes("ecies-vau-transport");
            HkdfBytesGenerator hkdfBytesGenerator = new HkdfBytesGenerator(new Sha256Digest());
            hkdfBytesGenerator.Init(new HkdfParameters(sharedSecretBytes, new byte[0], info));
            byte[] aes128Key_CEK = new byte[16];
            hkdfBytesGenerator.GenerateBytes(aes128Key_CEK, 0, aes128Key_CEK.Length);
            Console.Out.WriteLine("Schlüsselableitung AES128Key=" + ByteArrayToHexString(aes128Key_CEK));

            //AES CGM
            byte[] input = Encoding.UTF8.GetBytes(message);
            byte[] outputAESCGM = new byte[input.Length + 16];

            //random IV
            var iv = GetIv();
            Console.Out.WriteLine("IV =" + ByteArrayToHexString(iv));

            var cipher = new GcmBlockCipher(new AesEngine());
            var parameters = new AeadParameters(new KeyParameter(aes128Key_CEK), 128, iv);
            cipher.Init(true, parameters);
            var len = cipher.ProcessBytes(input, 0, input.Length, outputAESCGM, 0);
            var final = cipher.DoFinal(outputAESCGM, len);

            Console.Out.WriteLine(len + final);

            using var mem = new MemoryStream();
            mem.WriteByte(0x01); //Version
            mem.Write(myECDHKey.Q.X, 0, myECDHKey.Q.X.Length); //XKoordinate VAU Zert
            mem.Write(myECDHKey.Q.Y, 0, myECDHKey.Q.Y.Length); //YKoordinate VAU Zert
            mem.Write(iv, 0, iv.Length);
            mem.Write(outputAESCGM, 0, outputAESCGM.Length);
            var gesamtoutput = mem.ToArray();
            return gesamtoutput;
        }

        public class KeyCoords {
            public BigInteger X { get; set; }
            public BigInteger Y { get; set; }
        }

        public static string ByteArrayToHexString(byte[] bytes) {
            StringBuilder result = new StringBuilder(bytes.Length * 2);
            const string hexAlphabet = "0123456789ABCDEF";

            foreach (byte B in bytes) {
                result.Append(hexAlphabet[B >> 4]);
                result.Append(hexAlphabet[B & 0xF]);
            }

            return result.ToString();
        }

        public static byte[] HexStringToByteArray(string hex) {
            byte[] bytes = new byte[hex.Length / 2];
            int[] hexValue = {
                0x00, 0x01, 0x02, 0x03, 0x04, 0x05,
                0x06, 0x07, 0x08, 0x09, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F
            };

            for (int x = 0, i = 0; i < hex.Length; i += 2, x += 1) {
                bytes[x] = (byte) (hexValue[char.ToUpper(hex[i + 0]) - '0'] << 4 |
                                   hexValue[char.ToUpper(hex[i + 1]) - '0']);
            }
            return bytes;
        }

        /// <summary>
        /// entschlüsselt einen Responde der VAU
        /// </summary>
        /// <param name="message"></param>
        /// <param name="key"></param>
        /// <returns></returns>
        public byte[] DecryptWithKey(byte[] message, byte[] key) {
            const int MAC_BIT_SIZE = 128;
            const int NONCE_BIT_SIZE = 96;
            const int KEY_LENGTH = 128;

            if (key == null || key.Length != KEY_LENGTH / 8) {
                throw new Exception($"Key needs to be {KEY_LENGTH} bit!");
            }
            if (message == null || message.Length == 0) {
                throw new Exception("Message required!");
            }

            using var cipherStream = new MemoryStream(message);
            using var cipherReader = new BinaryReader(cipherStream);
            var nonSecretPayload = cipherReader.ReadBytes(0);
            var nonce = cipherReader.ReadBytes(NONCE_BIT_SIZE / 8);
            var cipher = new GcmBlockCipher(new AesEngine());
            var parameters = new AeadParameters(new KeyParameter(key), MAC_BIT_SIZE, nonce, nonSecretPayload);
            cipher.Init(false, parameters);
            var cipherText = cipherReader.ReadBytes(message.Length - nonce.Length);
            var plainText = new byte[cipher.GetOutputSize(cipherText.Length)];
            try {
                var len = cipher.ProcessBytes(cipherText, 0, cipherText.Length, plainText, 0);
                cipher.DoFinal(plainText, len);
            } catch (InvalidCipherTextException) {
                return null;
            }
            return plainText;
        }
    }
}