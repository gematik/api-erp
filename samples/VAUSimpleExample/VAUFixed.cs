using System;
using System.Security.Cryptography;
using Org.BouncyCastle.Math;

namespace VAUSimpleExample {
    public class VAUFixed : VAU {
        protected override KeyCoords GetVauPublicKeyXY() {
            return new() {
                X = new BigInteger(CertPublicKeyX, 16),
                Y = new BigInteger(CertPublicKeyY, 16)
            };
        }

        protected override ECParameters GenerateNewECDHKey() {
            ECParameters myexportParametersFix = new ECParameters {
                Curve = ECCurve.NamedCurves.brainpoolP256r1,
                Q = {
                    X = HexStringToByteArray(EphemeralPublicKeyX), Y = HexStringToByteArray(EphemeralPublicKeyY)
                },
                D = HexStringToByteArray(EccPrivateKey),
            };
            return myexportParametersFix;
        }

        protected override byte[] GetIv() {
            return HexStringToByteArray(IVBytes);
        }

        public const string CertPublicKeyX = "8634212830dad457ca05305e6687134166b9c21a65ffebf555f4e75dfb048888";
        public const string CertPublicKeyY = "66e4b6843624cbda43c97ea89968bc41fd53576f82c03efa7d601b9facac2b29";

        public const string Message = "Hallo Test";

        public const string EccPrivateKey = "5bbba34d47502bd588ed680dfa2309ca375eb7a35ddbbd67cc7f8b6b687a1c1d";
        public const string EphemeralPublicKeyX = "754e548941e5cd073fed6d734578a484be9f0bbfa1b6fa3168ed7ffb22878f0f";
        public const string EphemeralPublicKeyY = "9aef9bbd932a020d8828367bd080a3e72b36c41ee40c87253f9b1b0beb8371bf";

        public const string IVBytes = "257db4604af8ae0dfced37ce";

        public static string CipherText =
            "01 754e548941e5cd073fed6d734578a484be9f0bbfa1b6fa3168ed7ffb22878f0f 9aef9bbd932a020d8828367bd080a3e72b36c41ee40c87253f9b1b0beb8371bf 257db4604af8ae0dfced37ce 86c2b491c7a8309e750b 4e6e307219863938c204dfe85502ee0a"
                .Replace(" ", "").ToUpperInvariant();

        public static void DemoBspAusGemSpecCrypt() {
            {
                var gesamtoutput = new VAUFixed().Encrypt(Message);
                var byteArrayToHexString = ByteArrayToHexString(gesamtoutput);
                Console.Out.WriteLine("IST =" + byteArrayToHexString);
                Console.Out.WriteLine("SOLL=" + CipherText);
                var gleich = CipherText == byteArrayToHexString;
                Console.Out.WriteLine($"GLEICH={gleich}\n\n");
            }

            {
                var gesamtoutput = new VAU().Encrypt(Message);
                var byteArrayToHexString = ByteArrayToHexString(gesamtoutput);
                Console.Out.WriteLine("IST =" + byteArrayToHexString);
            }
        }
    }
}