/*
Copyright (Change Date see Readme), gematik GmbH

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

*******

For additional notes and disclaimer from gematik and in case of changes
by gematik, find details in the "Readme" file.
*/
package de.gematik.test.erp;

import de.gematik.pki.tsl.TslInformationProvider;
import de.gematik.pki.tsl.TslReader;
import kong.unirest.Unirest;
import lombok.Getter;
import lombok.SneakyThrows;
import lombok.extern.slf4j.Slf4j;
import lombok.val;

import java.nio.file.Path;
import java.util.Arrays;
import java.util.Optional;

import static java.nio.file.StandardCopyOption.REPLACE_EXISTING;

@Slf4j
public enum TestEnvironment {

    RU ("https://download-ref.tsl.ti-dienste.de/ECC/ECC-RSA_TSL-ref.xml", "https://erp-ref.app.ti-dienste.de/ocspf"),
    TU ("https://download-test.tsl.ti-dienste.de/ECC/ECC-RSA_TSL-test.xml", "https://erp-test.app.ti-dienste.de/ocspf"),
    PU ("https://download.tsl.ti-dienste.de/ECC/ECC-RSA_TSL.xml", "https://erp.app.ti-dienste.de/ocspf"),
    ;


    @Getter private final String tslUrl;
    @Getter private final String ocspForwarderUrl;

    TestEnvironment(String tslUrl, String ocspForwarderUrl) {
        this.tslUrl = tslUrl;
        this.ocspForwarderUrl = ocspForwarderUrl;
    }

    public static Optional<TestEnvironment> valueFrom(String environment) {
        return Arrays.stream(TestEnvironment.values())
                .filter(e -> e.name().equalsIgnoreCase(environment))
                .findFirst();
    }

    @SneakyThrows
    public TslInformationProvider getTslInformationProvider() {
        // Download TSL
        val file = Unirest.get(tslUrl)
                .asFile(getFileName(tslUrl), REPLACE_EXISTING)
                .getBody();
        log.info("TSL Url: {}", tslUrl);
        log.info("TSL Download successful");

        val trustStatusListType = TslReader.getTsl(Path.of(file.getAbsolutePath()));
        return new TslInformationProvider(trustStatusListType.orElseThrow());
    }

    private String getFileName(String tslUrl) {
        if(!tslUrl.contains("/")) return tslUrl;
        return tslUrl.substring(tslUrl.lastIndexOf('/') + 1);
    }
}
