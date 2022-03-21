package de.gematik.test.erp.ocsp;

import de.gematik.pki.ocsp.OcspRespCache;
import kong.unirest.Unirest;
import kong.unirest.UnirestException;
import lombok.NonNull;
import lombok.SneakyThrows;
import lombok.extern.log4j.Log4j;
import lombok.extern.slf4j.Slf4j;
import lombok.val;
import org.bouncycastle.asn1.DEROctetString;
import org.bouncycastle.asn1.ocsp.OCSPObjectIdentifiers;
import org.bouncycastle.asn1.x509.Extension;
import org.bouncycastle.asn1.x509.Extensions;
import org.bouncycastle.cert.ocsp.CertificateID;
import org.bouncycastle.cert.ocsp.OCSPReq;
import org.bouncycastle.cert.ocsp.OCSPReqBuilder;
import org.bouncycastle.cert.ocsp.OCSPResp;
import org.bouncycastle.cert.ocsp.jcajce.JcaCertificateID;
import org.bouncycastle.operator.jcajce.JcaDigestCalculatorProviderBuilder;

import java.math.BigInteger;
import java.security.cert.X509Certificate;

@Slf4j
public class OcspUtils {

    private static final int OCSP_GRACE_PERIOD_SECONDS = 120;

    @SneakyThrows
    public static OCSPResp getOcspResp(
            @NonNull String url,
            @NonNull String xApiKey,
            @NonNull X509Certificate certificate,
            @NonNull BigInteger serialNumber) {

        log.debug("Ocsp Forwarder Url: {}", url);
        log.debug("X-Api-key: {}", xApiKey);

        val ocspReq = generateOCSPRequest(certificate, serialNumber);
        val httpResponse =
                Unirest.post(url)
                        .header("X-api-key", xApiKey)
                        .header("Content-Type", "application/ocsp-request")
                        .header("accept", "application/ocsp-response")
                        .body(ocspReq.getEncoded())
                        .asBytes();
        if(httpResponse.getStatus() != 200) {
            log.error("StatusCode: {}, Message: {}", httpResponse.getStatus(), httpResponse.getStatusText());
            throw new UnirestException(httpResponse.getStatusText() + " with XApiKey " + xApiKey);
        }
        return new OCSPResp(httpResponse.getBody());
    }

    @SneakyThrows
    private static OCSPReq generateOCSPRequest(
            X509Certificate certificate, @NonNull BigInteger serialNumber) {
        val nonce = BigInteger.valueOf(System.currentTimeMillis());
        val ext =
                new Extension(
                        OCSPObjectIdentifiers.id_pkix_ocsp_nonce,
                        true,
                        new DEROctetString(nonce.toByteArray()));

        val ocspReqBuilder =
                new OCSPReqBuilder()
                        .addRequest(
                                new JcaCertificateID(
                                        new JcaDigestCalculatorProviderBuilder()
                                                .setProvider("BC")
                                                .build()
                                                .get(CertificateID.HASH_SHA1),
                                        certificate,
                                        serialNumber))
                        .setRequestExtensions(new Extensions(new Extension[] {ext}));
        return ocspReqBuilder.build();
    }

    public static OcspRespCache generateOcspRespCache(
            @NonNull OCSPResp ocspResp, @NonNull BigInteger signerSerialNumber) {

        val ocspCache = new OcspRespCache(OCSP_GRACE_PERIOD_SECONDS);
        ocspCache.saveResponse(signerSerialNumber, ocspResp);
        return ocspCache;
    }
}
