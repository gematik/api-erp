import de.gematik.pki.certificate.CertificateProfile;
import de.gematik.pki.certificate.TucPki018Verifier;
import de.gematik.pki.exception.GemPkiException;
import de.gematik.pki.tsl.TslInformationProvider;
import de.gematik.pki.tsl.TslReader;
import de.gematik.test.erp.cms.CMSParser;
import de.gematik.test.erp.ocsp.OcspUtils;
import lombok.SneakyThrows;
import lombok.extern.slf4j.Slf4j;
import lombok.val;
import org.bouncycastle.cert.ocsp.OCSPResp;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.security.cert.X509Certificate;
import java.util.Base64;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

@Slf4j
public class ReceiptSignatureVerificationTest {

    private static final String PRODUCT_TYPE = "eRp_FD";
    private static byte[] signature;
    private static TslInformationProvider tslInformationProvider;

    final String xApiKey = "ewOktIm6KMGEo7hPI4Nwtg==";
    final String ocspForwarderUrl = "https://erp-ref.app.ti-dienste.de/ocspf";

    @BeforeAll
    static void setup() throws IOException, GemPkiException {
        val content =  Files.readString(Path.of("src/test/resources/ReceiptSignature.base64"));
        signature = Base64.getDecoder().decode(content);
        assertNotNull(signature, "Signatur kann nicht geladen oder dekodiert werden");

        val tsl = TslReader.getTsl(Path.of("src/test/resources/ECC-RSA_TSL-ref.xml"));
        tslInformationProvider = new TslInformationProvider(tsl.orElseThrow());
    }

    @Test
    void embeddedOcspResp() {
        // Parsen der Quittungssignatur. Es werden Informationen zum Signaturzertifikat, Aussteller-Zertifikat, eingebetteten OCSP-Response
        // und zur Signatur selbst ausgelesen
        val cmsParser = new CMSParser(signature, tslInformationProvider);

        // Prüfen des Signaturzertifikat mit Hilfe der GemPkiLib
        performTucPki018(cmsParser.getSignerCert(), cmsParser.getOcspResp().orElseThrow());

        // Prüfen der Quittungssignatur
        assertTrue(cmsParser.verifySignature());

    }

    @Test
    void withOnlineOcspResp() {
        // Parsen der Quittungssignatur. Es werden Informationen zum Signaturzertifikat, Aussteller-Zertifikat
        // und zur Signatur selbst ausgelesen
        val cmsParser = new CMSParser(signature, tslInformationProvider);

        // Abruf der OCSP-Resp vom OCSP-Forwarder vom E-Rezept Fachdienst für das Signaturzertifikates
        val ocspResp = OcspUtils.getOcspResp(ocspForwarderUrl,
                xApiKey,
                cmsParser.getIssuerCert(),
                cmsParser.getSignerCert().getSerialNumber());

        // Prüfen des Signaturzertifikat mit Hilfe der GemPkiLib
        performTucPki018(cmsParser.getSignerCert(), ocspResp);

        // Prüfen der Quittungssignatur
        assertTrue(cmsParser.verifySignature());
    }

    @SneakyThrows
    private void performTucPki018(final X509Certificate signerCert, final OCSPResp ocspResp) {
        val tucPki018Verifier = TucPki018Verifier.builder()
                .productType(PRODUCT_TYPE)
                .withOcspCheck(true)
                // Übergabe der Trusted Service Provider der TSL
                .tspServiceList(tslInformationProvider.getTspServices())
                // TODO C_FD_OSIG muss noch verfügbar gemacht werden
                .certificateProfiles(List.of(CertificateProfile.C_FD_SIG))
                // Übergabe der Ocsp-Response
                .ocspRespCache(OcspUtils.generateOcspRespCache(ocspResp, signerCert.getSerialNumber()))
                .build();

        tucPki018Verifier.performTucPki18Checks(signerCert);
    }
}
