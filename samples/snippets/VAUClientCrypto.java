package com.ibm.erp.perftest.crypto;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.math.BigInteger;
import java.nio.ByteBuffer;
import java.nio.charset.StandardCharsets;
import java.security.InvalidAlgorithmParameterException;
import java.security.InvalidKeyException;
import java.security.Key;
import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.NoSuchAlgorithmException;
import java.security.PrivateKey;
import java.security.SecureRandom;
import java.security.Security;
import java.security.interfaces.ECPublicKey;
import java.security.spec.InvalidKeySpecException;

import javax.crypto.BadPaddingException;
import javax.crypto.Cipher;
import javax.crypto.IllegalBlockSizeException;
import javax.crypto.KeyAgreement;
import javax.crypto.NoSuchPaddingException;
import javax.crypto.spec.GCMParameterSpec;
import javax.crypto.spec.SecretKeySpec;

import org.apache.commons.codec.binary.Hex;
import org.bouncycastle.crypto.DerivationParameters;
import org.bouncycastle.crypto.digests.SHA256Digest;
import org.bouncycastle.crypto.generators.HKDFBytesGenerator;
import org.bouncycastle.crypto.params.HKDFParameters;
import org.bouncycastle.jce.ECNamedCurveTable;
import org.bouncycastle.jce.provider.BouncyCastleProvider;
import org.bouncycastle.jce.spec.ECNamedCurveParameterSpec;

/**
 * Utility class for the client side encryption of the ERP VAU protocol (see gemSpec_Krypt#A_20161-01 and A_20174 ).
 */
public class VAUClientCrypto {

	private final byte[] INFO_ECIS_VAU_TRANSPORT = "ecies-vau-transport".getBytes();
	
	// 128-bit Request-Id
	private final int REQUEST_ID_LENGTH = 16;
	
	// Byte length for the 128-bit (8 x 16) AES key
	private final int RESPONSE_KEY_LENGTH = 16;

	// Byte length for the IV
	private final int IV_LENGTH = 12;
	
	// Bit length for the 16 byte AES Authentication Tag 
	private final int AUTHENTICATION_TAG_BITS = 16 * 8;
	
	public VAUClientCrypto() {
		Security.addProvider(new BouncyCastleProvider());
	}

	public String generateRequestId() {
		byte[] key = new byte[REQUEST_ID_LENGTH];
		new SecureRandom().nextBytes(key);
		return Hex.encodeHexString(key);
	}

	/**
	 * Generates a 128-bit (8 x 16) AES key
	 * 
	 * @return
	 */
	public SecretKeySpec generateResponseKey() {
		byte[] key = new byte[RESPONSE_KEY_LENGTH];
		new SecureRandom().nextBytes(key);
		return new SecretKeySpec(key, "AES");
	}

	public byte[] encrypt(Key vauPublicKey, String plaintext)
			throws NoSuchAlgorithmException, InvalidKeyException, InvalidAlgorithmParameterException,
			NoSuchPaddingException, IllegalBlockSizeException, BadPaddingException, IOException {

		ECNamedCurveParameterSpec parameterSpec = ECNamedCurveTable.getParameterSpec("brainpoolp256r1");
		KeyPairGenerator keyPairGenerator = KeyPairGenerator.getInstance("ECDH");
		keyPairGenerator.initialize(parameterSpec);

		KeyPair keyPair = keyPairGenerator.generateKeyPair();
		PrivateKey privateKey = keyPair.getPrivate();

		KeyAgreement ka = KeyAgreement.getInstance("ECDH");
		ka.init(privateKey);
		ka.doPhase(vauPublicKey, true);
		byte[] sharedSecret = ka.generateSecret();

		// Als Schlüsselableitungsfunktion MUSS er die HKDF nach [RFC-5869] auf Basis
		// von SHA-256 verwenden.
		byte[] derivedSharedSecret = deriveKey(sharedSecret);

		byte[] iv = new byte[IV_LENGTH];
		new SecureRandom().nextBytes(iv);
		GCMParameterSpec spec = new GCMParameterSpec(AUTHENTICATION_TAG_BITS, iv);
		Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
		cipher.init(Cipher.ENCRYPT_MODE, new SecretKeySpec(derivedSharedSecret, "AES"), spec);
		byte[] cipherText = cipher.doFinal(plaintext.getBytes());

		ECPublicKey ecPublicKey = (ECPublicKey) keyPair.getPublic();
		BigInteger x = ecPublicKey.getW().getAffineX();
		BigInteger y = ecPublicKey.getW().getAffineY();

		ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
		outputStream.write(0x01);
		outputStream.write(pad32(x.toByteArray()));
		outputStream.write(pad32(y.toByteArray()));
		outputStream.write(iv);
		outputStream.write(cipherText);

		return outputStream.toByteArray();
	}

	public String decrypt(SecretKeySpec responseKey, byte[] encryptedInnerResponse)
			throws NoSuchAlgorithmException, NoSuchPaddingException, InvalidKeyException, IllegalBlockSizeException,
			BadPaddingException, InvalidKeySpecException, InvalidAlgorithmParameterException {

		ByteBuffer byteBuffer = ByteBuffer.wrap(encryptedInnerResponse);
		byte[] iv = new byte[IV_LENGTH];
		byteBuffer.get(iv);
		byte[] cipherText = new byte[byteBuffer.remaining()];
		byteBuffer.get(cipherText);

		Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
		GCMParameterSpec spec = new GCMParameterSpec(AUTHENTICATION_TAG_BITS, iv);
		cipher.init(Cipher.DECRYPT_MODE, responseKey, spec);
		byte[] decryptedResponse = cipher.doFinal(cipherText);

		return new String(decryptedResponse, StandardCharsets.UTF_8);
	}

	/**
	 *  Die Koordinaten sind (wie üblich) vorne mit chr(0) zu padden solange bis sie eine Kodierungslänge von 32 Byte erreichen.
	 *  See gemSpec_Krypt#A_20161-01
	 */
	private byte[] pad32(byte[] input) {

		// this requires some rework or analysis - in some cases I noticed the X/Y
		// coordinates from EC Key had 33 bytes instead of 32.
		if (input[0] == 0 && input.length > 32) {
			byte[] tmp = new byte[input.length - 1];
			System.arraycopy(input, 1, tmp, 0, tmp.length);
			input = tmp;
		}
		
		if (input.length < 32) {
			byte[] tmp = new byte[32];
			System.arraycopy(input, 0, tmp, 32-input.length, input.length);
			input = tmp;
		}

		if (input.length == 32) {
			return input;
		}

		throw new IllegalArgumentException("Must be 32 bytes! But was "+input.length);
	}

	private byte[] deriveKey(byte[] sharedSecret) {
		HKDFBytesGenerator hkdf = new HKDFBytesGenerator(new SHA256Digest());

		int keyLengthBytes = 16;
		byte[] derivedSharedSecret = new byte[keyLengthBytes];
		DerivationParameters param = new HKDFParameters(sharedSecret, null, INFO_ECIS_VAU_TRANSPORT);
		hkdf.init(param);
		hkdf.generateBytes(derivedSharedSecret, 0, keyLengthBytes);
		return derivedSharedSecret;
	}
}