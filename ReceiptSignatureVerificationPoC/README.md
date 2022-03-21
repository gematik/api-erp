# PoC - Verifikation E-Rezept Quittungssignatur außerhalb der TI

## PoC - Introduction
Dieser PoC implementiert beispielhaft die Verifizierung der E-Rezept Quittungssignatur außerhalb 
der TI gemäß der Beschreibung nach "Signaturen der Abrechnungsinformationen" der Gematik [1]. 
Für diesen PoC wurden Testdaten (bespw. Quittungssignatur, TSL) aus der Testumgebung der RU verwendet.
Bei der Quittungssignatur handelt es sich um einen nonQES Datensatz, der mit Hilfe des Signaturzertifikates,
einer gültigen OCSP-Response und einer TSL der TI
geprüft werden kann. 
Die Implementierung kommt ohne Konnektor oder Basis Consumer aus und soll Dienstleistern der Krankenkassen helfen, 
eigene Implementierungen umzusetzen. 

Hinweis: Der bereitgestellte PoC ist nicht für den Produktiveinsatz entwickelt worden. 

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

1. Parsen der Quittingssignatur aus der Datei *ReceiptSignature.base64*. Hierzu werden Informationen zum 
   Signaturzertifikat, Ausstellerzertifikat (Issuer), ggf. eingebetteten OCSP-Response und zur 
   Signatur selbst ausgelesen. 

2. Sofern erforderlich, wird eine aktuell gültige OCSP-Response vom E-Rezept Fachdienst 
   beim Endpunkt /ocspf abgerufen.
   Hierfür wird ein OCSP-Request an den OCSP-Forwarder des E-Rezept Fachdienst
   geschickt. Damit der Fachdienst das Request akzeptiert, muss im Header ein gültiger X-Api-Key
   übergeben werden. Ein Beispiel zu diesem Request ist der Klasse *OCSPUtils*
   zu entnehmen.

3. Mit Hilfe der GemLibPki der Gematik wird TUC_PKI_018 mit Angaben zum
   Produkttypen, einer gültigen TSL der TI, der eingebetteten oder der abgerufenden OCSP-Response, dem 
   Zertifikatsprofil C_FD_OSIG und dem
   Signaturzertifikat ausgeführt. Sofern Abweichungen bei der Ausführung von TUC_PKI_018
   festgestellt werden, werden Exceptions mit weiterführenden Informationen geworfen.
   Hinweis: TUC_PKI_018 ist der technische Use Case zu Zertifikatsprüfung in der TI. 
   Für weitere Informationen zu TUC_PKI_018 siehe [gemSpec_PKI].
   
4. Verifikation der Signatur.

## Testdaten

- E-Rezept-Quittung *ReceiptSignature.base64*: Beispieldatensatz aus der RU mit eingebetteter OCSP-Response
- X-Api-Key: Der bereitgestellt X-Api-Key hat nur eine Gültigkeit für die RU und ist auch nur für die Nutzung des 
Endpunkts /ocspf gedacht. 

## Anforderungen / Maven Abhängigkeiten
- GemLibPki 0.5.3 [2]
- bouncycastle bcprov-jdk15on 1.70
- konghq unirest-java 3.13.6
- lombok 1.18.22
- openjdk 17.x
- Maven

## Ausführung
``` 
mvn -DTestEnvironment=[RU|TU|PU] -DXApiKey=[] clean test
``` 

### Beispiele:
``` 
mvn -DTestEnvironment=RU -DXApiKey=ewOktIm6KMGEo7hPI4Nwtg== clean test
``` 

## Referenzen

1. [1] Signaturen der Abrechnungsinformationen_V1.2.0.pdf im Order doc
2. [2] https://github.com/gematik/ref-GemLibPki
3. [3] https://datatracker.ietf.org/doc/html/rfc6960#section-4.1
 
