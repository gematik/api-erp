package de.gematik.test.erp.cms;

import de.gematik.pki.tsl.TslInformationProvider;
import de.gematik.pki.tsl.TspService;
import eu.europa.esig.dss.spi.DSSRevocationUtils;
import lombok.Getter;
import lombok.NonNull;
import lombok.SneakyThrows;
import lombok.extern.slf4j.Slf4j;
import lombok.val;
import org.bouncycastle.asn1.ASN1Sequence;
import org.bouncycastle.asn1.cms.CMSObjectIdentifiers;
import org.bouncycastle.asn1.x500.X500Name;
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

import java.io.ByteArrayInputStream;
import java.security.Security;
import java.security.cert.CertificateFactory;
import java.security.cert.X509Certificate;
import java.util.List;
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

    @SneakyThrows
    public CMSParser(byte[] data, @NonNull TslInformationProvider tslInformationProvider){

        val parser = new CMSSignedDataParser(new JcaDigestCalculatorProviderBuilder().setProvider("BC").build(), data);
        parser.getSignedContent().drain();

        this.signer = parser.getSignerInfos().getSigners().stream().findFirst().orElseThrow();
        this.signerCert = getSignerCert(parser);
        this.issuerCert = getIssuerCert(parser, tslInformationProvider);
        this.ocspResp = getOCSPResp(parser);
    }

    private boolean matchTspService(TspService tspService, X509CertificateHolder cert){
        val serviceName = tspService.getTspServiceType()
                .getServiceInformation()
                .getServiceName();
        val x500Name = serviceName.getName().stream()
                .map(x1 -> new X500Name(x1.getValue()))
                .findFirst();
        if(x500Name.isEmpty()){
            return false;
        }
        return cert.getIssuer().equals(x500Name.orElseThrow());
    }


    @SneakyThrows
    @SuppressWarnings("unchecked")
    private X509Certificate getIssuerCert(CMSSignedDataParser parser, TslInformationProvider tslInformationProvider) {
        val certStore = parser.getCertificates();
        val cert = (X509CertificateHolder)certStore.getMatches(signer.getSID()).stream()
                .findFirst().orElseThrow();

        return tslInformationProvider.getFilteredTspServices(List.of("http://uri.etsi.org/TrstSvc/Svctype/CA/PKC")).stream()
                .filter(tspService -> matchTspService(tspService, cert))
                .map(x -> x.getTspServiceType().getServiceInformation()
                        .getServiceDigitalIdentity().getDigitalId().stream()
                        .findFirst().orElseThrow().getX509Certificate())
                .map(this::loadX509Certificate)
                .findFirst().orElseThrow();
    }

    @SneakyThrows
    private X509Certificate loadX509Certificate(byte[] input) {
        val certFactory = CertificateFactory.getInstance("X.509");
        val in = new ByteArrayInputStream(input);
        return (X509Certificate)certFactory.generateCertificate(in);
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
            return signer.verify(new JcaSimpleSignerInfoVerifierBuilder().setProvider("BC").build(signerCert));
        } catch (CMSException | OperatorCreationException e) {
            log.error(e.getMessage());
            return false;
        }
    }
}
