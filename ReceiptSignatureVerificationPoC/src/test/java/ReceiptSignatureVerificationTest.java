import de.gematik.pki.certificate.CertificateProfile;
import de.gematik.pki.certificate.TucPki018Verifier;
import de.gematik.pki.exception.GemPkiException;
import de.gematik.pki.tsl.TslInformationProvider;
import de.gematik.test.erp.TestEnvironment;
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
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

@Slf4j
public class ReceiptSignatureVerificationTest {

    private static final String PRODUCT_TYPE = "eRp_FD";
    private static final String X_API_KEY = "ewOktIm6KMGEo7hPI4Nwtg==";

    private static byte[] signature;
    private static TslInformationProvider tslInformationProvider;
    private static String ocspForwarderUrl;
    private static String xApiKey;

    @BeforeAll
    static void setup() throws IOException, GemPkiException {
        val content =  Files.readString(Path.of("src/test/resources/ReceiptSignature.base64"));
        signature = Base64.getDecoder().decode(content);
        assertNotNull(signature, "Signatur kann nicht geladen oder dekodiert werden");

        val environment = TestEnvironment.valueFrom(
                Optional.ofNullable(System.getProperty("TestEnvironment")).orElse("RU")
            ).orElseThrow(() -> new RuntimeException("Test Environment is undefined"));
        log.debug("Testenvironment {}", environment.name());

        tslInformationProvider = environment.getTslInformationProvider();
        ocspForwarderUrl = environment.getOcspForwarderUrl();

        xApiKey = Optional.ofNullable(System.getProperty("XApiKey")).orElse(X_API_KEY);
    }

    @Test
    void embeddedOcspResp() {
        // Parsen der Quittungssignatur. Es werden Informationen zum Signaturzertifikat, Aussteller-Zertifikat, eingebetteten OCSP-Response
        // und zur Signatur selbst ausgelesen
        val cmsParser = new CMSParser(signature, tslInformationProvider, PRODUCT_TYPE);

        // Prüfen des Signaturzertifikat mit Hilfe der GemPkiLib
        performTucPki018(cmsParser.getSignerCert(), cmsParser.getOcspResp().orElseThrow());

        // Prüfen der Signatur
        assertTrue(cmsParser.verifySignature());

    }

    @Test
    void withOnlineOcspResp() {
        // Parsen der Quittungssignatur. Es werden Informationen zum Signaturzertifikat, Aussteller-Zertifikat
        // und zur Signatur selbst ausgelesen
        val cmsParser = new CMSParser(signature, tslInformationProvider, PRODUCT_TYPE);

        // Abruf der OCSP-Resp vom OCSP-Forwarder vom E-Rezept Fachdienst für das Signaturzertifikates
        val ocspResp = OcspUtils.getOcspResp(ocspForwarderUrl,
                xApiKey,
                cmsParser.getIssuerCert(),
                cmsParser.getSignerCert().getSerialNumber());

        // Prüfen des Signaturzertifikat mit Hilfe der GemPkiLib
        performTucPki018(cmsParser.getSignerCert(), ocspResp);

        // Prüfen der Signatur
        assertTrue(cmsParser.verifySignature());
    }

    @SneakyThrows
    private void performTucPki018(final X509Certificate signerCert, final OCSPResp ocspResp) {
        val tucPki018Verifier = TucPki018Verifier.builder()
                .productType(PRODUCT_TYPE)
                .withOcspCheck(true)
                // Übergabe der Trusted Service Provider der TSL
                .tspServiceList(tslInformationProvider.getTspServices())
                .certificateProfiles(List.of(CertificateProfile.C_FD_OSIG))
                // Übergabe der Ocsp-Response
                .ocspRespCache(OcspUtils.generateOcspRespCache(ocspResp, signerCert.getSerialNumber()))
                .build();

        tucPki018Verifier.performTucPki18Checks(signerCert);
    }
}
