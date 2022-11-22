public class example_encryption {
    val info = ASN1EncodableVector().apply
    {
        recipientCerts.forEach { recipientCert ->
            add(
                DERSequence(
                    ASN1EncodableVector().apply {
                        add(DERIA5String("3-10.3.1234567000.10.999", true))

                        add(RecipientIdentifier(IssuerAndSerialNumber(JcaX509CertificateHolder(recipientCert).toASN1Structure())))
                    }
                )
            )
        }
    }
    // ...
    recipientCerts.forEach{ recipientCert ->
        if (recipientCert.sigAlgOID == oidEcdsaWithSHA256) {
            edGen.addRecipientInfoGenerator(
                JceKeyAgreeRecipientInfoGenerator(
                    CMSAlgorithm.ECDH_SHA256KDF,
                    kp.private,
                    kp.public,
                    CMSAlgorithm.AES256_GCM
                )
                    .setProvider(BCProvider)
                    .addRecipient(recipientCert)
            );
        } else {
            edGen.addRecipientInfoGenerator(
                JceKeyTransRecipientInfoGenerator(
                    recipientCert,
                    JceAsymmetricKeyWrapper(
                        OAEPParameterSpec("SHA-256", "MGF1", MGF1ParameterSpec.SHA256, PSource.PSpecified.DEFAULT),
                        recipientCert.publicKey
                    )
                ).setProvider(BCProvider)
            )
        }
    }
}