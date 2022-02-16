# PoC - Verifikation E-Rezept Quittungssignatur außerhalb der TI

## PoC - Introduction
Dieser PoC implementiert beispielhaft die Verifizierung der E-Rezept Quittung außerhalb 
der TI gemäß der Beschreibung nach "Signaturen der Abrechnungsinformationen" der Gematik [1]. 
Für diesen PoC wurden Testdaten (bespw. Quittungssignatur, TSL) aus der Testumgebung der RU verwendet.
Bei der Quittungssignatur handelt es sich um einen nonQES Datensatz, der mit Hilfe des Signaturzertifikates,
einer gültigen OCSP-Response und einer TSL der TI
geprüft werden kann. 
Die Implementierung kommt ohne Konnektor oder Basis Consumer aus und soll Apothekenrechenzentren 
und Dienstleistern der Krankenkassen helfen, eigene Implementierungen umzusetzen. 

## Voraussetzungen
Für die Kommunikation mit dem OCSP-Forwarder des E-Rezept Fachdiensts muss bei der Gematik ein
gültiger API-Key angefragt und beim Fachdienst hinterlegt werden. Dieser API-Key ist notwendig, um
eine OCSP-Response für das verwendetete Signaturzertifikat abzufragen. 


## Ablauf
Als Ausgangssituation kann eine E-Rezept Quittungssignatur vom E-Rezept Fachdienst
mit eingebetteter OCSP-Response oder ohne eingebetteter OCSP-Response vorliegen. 
Für das letztere Szenario muss eine gültige OCSP-Response für das Signaturzertifikat vom 
OCSP-Responder der Komponenten-PKI der TI abgerufen werden. 

Für diese beiden Szenarien umfasst der PoC zwei JUnit Testfälle, welche jeweils als Einstiegspunkte 
der Verifikation dienen. Die Testfälle befinden sich in der Klasse *ReceiptSignatureVerificationTest*.

### Verifikation mit eingebetteter OCSP-Response (embeddedOcspResp)
1. Base64 Quittungssignatur aus der Datei *ReceiptSignature.base64* laden.
   
2. Parsen der Signatur (Quittingssignatur). Hierzu werden Informationen zum 
   Signaturzertifikat, Ausstellerzertifikat (Issuer), eingebetteten OCSP-Response und zur 
   eigentlichen Signatur selbst ausgelesen. 
   
3. Mit Hilfe der GemPkiLib der Gematik wird TUC_PKI_018 mit Angaben zum
   Produkttypen, einer gültigen TSL der TI, der eingebetteten OCSP-Response, den relevanten 
   Zertifikatsprofilen und dem
   Signaturzertifikat ausgeführt. Sofern Abweichungen bei der Ausführung von TUC_PKI_018
   festgestellt werden, werden Exceptions mit weiterführenden Informationen geworfen.
   Hinweis: TUC_PKI_018 ist der technische Use Case zu Zertifikatsprüfung in der TI. 
   Für weitere Informationen zu TUC_PKI_018 siehe [gemSpec_PKI]
   
4. Verifikation der eigentlichen Quittungssignatur.

### Verifikation mit Online OCSP-Response (withOnlineOcspResp)

1. Base64 Quittungssignatur aus der Datei *ReceiptSignature.base64* laden. 

2. Parsen der Signatur (Quittingssignatur). Hierzu werden Informationen zum
   Signaturzertifikat, Ausstellerzertifikat (Issuer) und zur
   eigentlichen Signatur selbst ausgelesen.
   
3. Abruf einer passenden und aktuell gültigen OCSP-Response vom E-Rezept Fachdienst beim Endpunkt /ocspf.
   Hierfür wird ein OCSP-Request auf Basis der SerialNumber des Signaturzertifikats und des Hash-Werts
   des Issuer Zertifikats erzeugt [3] und mittels https an den OCSP-Forwarder des E-Rezept Fachdienst
   geschickt. Damit der Fachdienst das Request nicht abweist, muss im Header ein gültiger X-api-key 
   übertragen werden. Ein Beispiel zu diesem Request ist der Klasse *OCSPUtils* 
   zu entnehmen. 

4. Mit Hilfe der GemPkiLib der Gematik wird TUC_PKI_018 mit Angaben zum
   Produkttypen, einer gültigen TSL, der Online OCSP-Response, den relevanten
   Zertifikatsprofilen und dem
   Signaturzertifikat ausgeführt und das Signaturzertifikat gegen die TSL der TI 
   und die OCSP-Response geprüft. Sofern Abweichungen bei der Ausführung von TUC_PKI_018
   festgestellt werden, werden Exceptions mit weiterführenden Informationen geworfen.

5. Verifikation der eigentlichen Quittungssignatur.

## Testdaten

- E-Rezept-Quittung *ReceiptSignature.base64*: Beispieldatensatz aus der RU mit eingebetteter OCSP-Response
- TSL *ECC-RSA_TSL-ref.xml*: Für den PoC wurde aus der RU eine gültige TSL unter 
  https://download-ref.tsl.ti-dienste.de heruntergeladen und im Projekt hinterlegt. 
  Mit Hilfe dieser RU TSL kann die Signatur der Beispiel Quittung geprüft werden. Für den 
  Produktivbetrieb muss regelmäßig eine gültige TSL der TI unter https://download.tsl.ti-dienste.de/
  heruntergeladen werden

## Anforderungen / Maven Abhängigkeiten
- gemLibPki 0.5.2 [2]
- bouncycastle bcprov-jdk15on 1.70
- konghq unirest-java 3.13.6
- lombok 1.18.22
- openjdk 17.x (openjdk 17.0.1 war die Entwicklungsversion, sicherlich funktionieren auch ältere Versionen)
- Maven

## Ausführung
``` 
mvn clean test
``` 

## Referenzen

1. [1] Signaturen der Abrechnungsinformationen_V1.2.0.pdf im Order doc
2. [2] https://github.com/gematik/ref-GemLibPki
3. [3] https://datatracker.ietf.org/doc/html/rfc6960#section-4.1
 
