package de.gematik.test.erp.cms;

import de.gematik.pki.tsl.TslInformationProvider;
import de.gematik.pki.tsl.TspInformationProvider;
import eu.europa.esig.dss.spi.DSSRevocationUtils;
import lombok.Getter;
import lombok.NonNull;
import lombok.SneakyThrows;
import lombok.extern.slf4j.Slf4j;
import lombok.val;
import org.bouncycastle.asn1.ASN1Sequence;
import org.bouncycastle.asn1.cms.CMSObjectIdentifiers;
import org.bouncycastle.cert.X509CertificateHolder;
import org.bouncycastle.cert.jcajce.JcaX509CertificateConverter;
import org.bouncycastle.cert.ocsp.OCSPResp;
import org.bouncycastle.cms.CMSException;
import org.bouncycastle.cms.CMSSignedDataParser;
import org.bouncycastle.cms.SignerInformation;
import org.bouncycastle.cms.jcajce.JcaSimpleSignerInfoVerifierBuilder;
import org.bouncycastle.jce.provider.BouncyCastleProvider;
import org.bouncycastle.operator.OperatorCreationException;
import org.bouncycastle.operator.jcajce.JcaDigestCalculatorProviderBuilder;

import java.security.Security;
import java.security.cert.X509Certificate;
import java.util.Optional;

@Slf4j
public class CMSParser {

    static {
        val bouncyCastleProvider = new BouncyCastleProvider();
        if(Security.getProvider(bouncyCastleProvider.getName()) == null){
            Security.addProvider(bouncyCastleProvider);
        }
    }

    private final SignerInformation signer;
    @Getter private final X509Certificate signerCert;
    @Getter private final Optional<OCSPResp> ocspResp;
    @Getter private final X509Certificate issuerCert;
    @Getter private final String productType;

    @SneakyThrows
    public CMSParser(byte[] data, @NonNull TslInformationProvider tslInformationProvider, @NonNull String productType){

        this.productType = productType;
        val parser = new CMSSignedDataParser(new JcaDigestCalculatorProviderBuilder().setProvider("BC").build(), data);
        parser.getSignedContent().drain();

        this.signer = parser.getSignerInfos().getSigners().stream().findFirst().orElseThrow();
        this.signerCert = getSignerCert(parser);
        this.issuerCert = getIssuerCert(tslInformationProvider);
        this.ocspResp = getOCSPResp(parser);
    }

    @SneakyThrows
    private X509Certificate getIssuerCert(TslInformationProvider tslInformationProvider) {
        val tspIP = new TspInformationProvider(tslInformationProvider.getTspServices(), productType);
        return tspIP.getTspServiceSubset(this.signerCert).getX509IssuerCert();
    }


    @SneakyThrows
    @SuppressWarnings("unchecked")
    private X509Certificate getSignerCert(CMSSignedDataParser parser){
        val certStore = parser.getCertificates();
        val cert = (X509CertificateHolder)certStore.getMatches(signer.getSID()).stream()
                .findFirst().orElseThrow();
        return new JcaX509CertificateConverter().setProvider( "BC" ).getCertificate( cert );
    }

    @SneakyThrows
    @SuppressWarnings("unchecked")
    private Optional<OCSPResp> getOCSPResp(final CMSSignedDataParser parser){
        val matches = parser.getOtherRevocationInfo(CMSObjectIdentifiers.id_ri_ocsp_response)
                .getMatches(null);
        return matches.stream()
                .filter(o -> o instanceof ASN1Sequence)
                .map(o -> DSSRevocationUtils.getOcspResp((ASN1Sequence) o)).findFirst();
    }


    public boolean verifySignature(){
        try {
            val valid = signer.verify(
                    new JcaSimpleSignerInfoVerifierBuilder()
                            .setProvider("BC")
                            .build(signerCert)
            );
            if(valid) {
                log.info("Signature is valid");
            } else {
                log.info("Signature is invalid");
            }
            return valid;
        } catch (CMSException | OperatorCreationException e) {
            log.error(e.getMessage());
            return false;
        }
    }
}
