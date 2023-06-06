# Beschreibung des Features

Mit diesem Anwendungsfall kann ein Versicherten sein ein E-Rezept im
E-Rezept-FdV digital an eine Apotheke zu übermitteln, ohne sich selber
in der App am E-Rezept-Fachdienst anmelden zu müssen.

Hierzu scannt der Versicherte zunächst den QR-Code des ausgedruckten
E-Rezeptes in das E-Rezept-FdV ein. Hierdurch liegen die notwendigen
Einlöseinformationen TaskID und AccessCode im E-Rezept-FdV vor.

Möchte der Versicherte ein Medikament reservieren, liefern lassen oder
online bestellen, hat er die Möglichkeit eine entsprechende Apotheke
auszuwählen, die diesen Service bietet. Zur Übermittlung des E-Rezeptes
ist es zwingend notwendig, dass der Versicherte seine Adress- und
Kontaktangaben in der Nachricht hinterlegt. Über diese kann der Versand
erfolgen oder die Apotheke sich mit dem Versicherten in Verbindung
setzen.

Der Versicherte übermittelt seine Nachricht nicht über den
E-Rezept-Fachdienst, sondern sendet die E-Rezept-Einlöseinformationen
für die Apotheke verschlüsselt an einen REST-Service. Dieser kann von
der Apotheke oder einem Dienstleister bereitgestellt werden. Die
verschlüsselten Informationen (E-Rezept-Token und für die Transaktion
notwendigen Informationen) werden an das AVS der ausgewählten Apotheke
weitergeleitet.

Die Apotheke kann die verschlüsselten Informationen mit dem Konnektor
entschlüsseln und so mithilfe des E-Rezept-Tokens mit dem
E-Rezept-Fachdienst kommunizieren, um das E-Rezept abzurufen und zu
bearbeiten. Sobald das Rezept bearbeitet wurde, kann die Apotheke sich
über den angegebenen Kontaktweg mit dem Versicherten in Verbindung
setzen.

# Anwendungsfall Bereitstellung der Zusatzinformationen im APOVZD durch die Apotheke

![width=100%](../images/../images/puml_az_apovzd.png)

Jede Apotheke, die an diesem Dienst teilnehmen möchte, stellt eine
REST-API an denen im APOVZD veröffentlichten URLs zur Verfügung. Diese
Funktion kann auch von einem Dienstleister erbracht werden. Hierfür kann
sich eine Apotheke für diesen Service bei einem Apothekendienstleister
registrieren, der einem dann die URLs zur Verfügung stellt. Die
Spezifikation und API-Beschreibung der Dienstleister wird von der
gematik nicht vorgenommen.

Für das Einlösen eines E-Rezeptes über diesen Weg sind drei
Belieferungsoptionen vorgesehen:

-   Abholung in der Apotheke

-   Lieferung zum Versicherten durch Vor-Ort-Apotheke

-   Versand zum Versicherten durch Online-Apotheke

Für jeden dieser Optionen ist jeweils eine URL/ ein Endpunkt
bereitzustellen. Die Endpunkte werden genutzt, um die verschlüsselten
Informationen (E-Rezept-Token und Zusatzinformationen) an die Apotheke
für den entsprechenden Belieferungsweg weiterzuleiten.

Um diesen Dienst anzubieten, muss mindestens eine der
Belieferungsoptionen genutzt werden. Hierfür müssen die URLs im APOVZD
über das AVS hinterlegt und gepflegt werden. Das APOVZD stellt hierfür
eine Schnittstelle (Upload-Container) bereit, um die Informationen
übertragen zu können.

## Datensatz des AVS für Belieferungs URLs

Für jeden Belieferungsweg wird eine URL hinterlegt. Das AVS erstellt
dazu folgende Daten zur Verfügung, die im Apothekenverzeichnis
hinterlegt werden:

    {
        "shipment": "https://beispielurlVersand.de/<ti_id>?req=<transactionID>",
        "delivery": "https://beispielurlBote.de/",
        "onPremise": "https://beispielurlAbholung.de/"
    }

Folgende Platzhalter können in der URL verwendet werden:

<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>Platzhalter</p></td>
<td style="text-align: left;"><p>Bedeutung</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>&lt;ti_id&gt;</p></td>
<td style="text-align: left;"><p>Telematik-ID der adressierten
Apotheke</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>&lt;transactionID&gt;</p></td>
<td style="text-align: left;"><p>Die Transaktions-ID wird durch das
E-Rezept-FdV für jede Nachricht erzeugt.</p></td>
</tr>
</tbody>
</table>

Das AVS signiert den Datensatz mit dem Konnektor und der zugehörigen
SMC-B. Die Signatur des Datensatzes erfolgt mit dem Konnektor mit der
Signaturidentität der SMC-B C.HCI.OSIG gemäß \[RFC5652\] mit Profil
CAdES-BES (\[CAdES\]) als Enveloping-Signatur.

Der Aufruf erfolgt als http-POST-Operation auf eine SOAP-Schnittstelle.

**Request**

<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p><strong>URI</strong></p></td>
<td style="text-align: left;"><p><a
href="https://192.168.x.y/Konnektorservice">https://192.168.x.y/Konnektorservice</a></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>Method</strong></p></td>
<td style="text-align: left;"><p>POST</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>HTTP Header</strong></p></td>
<td style="text-align: left;"><pre><code>Content-Type: text/xml; charset=UTF-8
Content-Length: 1234
SOAPAction: &quot;http://ws.gematik.de/conn/SignatureService/v7.4#SignDocument&quot;</code></pre></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>Payload</strong></p></td>
<td style="text-align: left;"><div class="sourceCode" id="cb2"><pre
class="sourceCode xml"><code class="sourceCode xml"><span id="cb2-1"><a href="#cb2-1" aria-hidden="true" tabindex="-1"></a><span class="fu">&lt;?xml</span><span class="ot"> version=</span><span class="st">&#39;1.0&#39;</span><span class="ot"> encoding=</span><span class="st">&#39;UTF-8&#39;</span><span class="fu">?&gt;</span></span>
<span id="cb2-2"><a href="#cb2-2" aria-hidden="true" tabindex="-1"></a>&lt;<span class="kw">S:Envelope</span><span class="ot"> xmlns:S=</span><span class="st">&quot;http://schemas.xmlsoap.org/soap/envelope/&quot;</span>&gt;</span>
<span id="cb2-3"><a href="#cb2-3" aria-hidden="true" tabindex="-1"></a>    &lt;<span class="kw">S:Body</span>&gt;</span>
<span id="cb2-4"><a href="#cb2-4" aria-hidden="true" tabindex="-1"></a>        &lt;<span class="kw">ns5:SignDocument</span><span class="ot"> xmlns:ns2=</span><span class="st">&quot;http://ws.gematik.de/conn/ConnectorCommon/v5.0&quot;</span></span>
<span id="cb2-5"><a href="#cb2-5" aria-hidden="true" tabindex="-1"></a><span class="ot">            xmlns:ns3=</span><span class="st">&quot;urn:oasis:names:tc:dss:1.0:core:schema&quot;</span></span>
<span id="cb2-6"><a href="#cb2-6" aria-hidden="true" tabindex="-1"></a><span class="ot">            xmlns:ns4=</span><span class="st">&quot;http://www.w3.org/2000/09/xmldsig#&quot;</span></span>
<span id="cb2-7"><a href="#cb2-7" aria-hidden="true" tabindex="-1"></a><span class="ot">            xmlns:ns5=</span><span class="st">&quot;http://ws.gematik.de/conn/SignatureService/v7.5&quot;</span></span>
<span id="cb2-8"><a href="#cb2-8" aria-hidden="true" tabindex="-1"></a><span class="ot">            xmlns:ns6=</span><span class="st">&quot;urn:oasis:names:tc:dss-x:1.0:profiles:SignaturePolicy:schema#&quot;</span></span>
<span id="cb2-9"><a href="#cb2-9" aria-hidden="true" tabindex="-1"></a><span class="ot">            xmlns:ns7=</span><span class="st">&quot;http://ws.gematik.de/tel/error/v2.0&quot;</span></span>
<span id="cb2-10"><a href="#cb2-10" aria-hidden="true" tabindex="-1"></a><span class="ot">            xmlns:ns8=</span><span class="st">&quot;urn:oasis:names:tc:dss-x:1.0:profiles:verificationreport:schema#&quot;</span></span>
<span id="cb2-11"><a href="#cb2-11" aria-hidden="true" tabindex="-1"></a><span class="ot">            xmlns:ns9=</span><span class="st">&quot;http://uri.etsi.org/01903/v1.3.2#&quot;</span></span>
<span id="cb2-12"><a href="#cb2-12" aria-hidden="true" tabindex="-1"></a><span class="ot">            xmlns:ns10=</span><span class="st">&quot;http://uri.etsi.org/02231/v2#&quot;</span></span>
<span id="cb2-13"><a href="#cb2-13" aria-hidden="true" tabindex="-1"></a><span class="ot">            xmlns:ns11=</span><span class="st">&quot;http://ws.gematik.de/conn/ConnectorContext/v2.0&quot;</span></span>
<span id="cb2-14"><a href="#cb2-14" aria-hidden="true" tabindex="-1"></a><span class="ot">            xmlns:ns12=</span><span class="st">&quot;http://ws.gematik.de/conn/CertificateServiceCommon/v2.0&quot;</span></span>
<span id="cb2-15"><a href="#cb2-15" aria-hidden="true" tabindex="-1"></a><span class="ot">            xmlns:ns13=</span><span class="st">&quot;urn:oasis:names:tc:SAML:1.0:assertion&quot;</span></span>
<span id="cb2-16"><a href="#cb2-16" aria-hidden="true" tabindex="-1"></a><span class="ot">            xmlns:ns14=</span><span class="st">&quot;urn:oasis:names:tc:SAML:2.0:assertion&quot;</span></span>
<span id="cb2-17"><a href="#cb2-17" aria-hidden="true" tabindex="-1"></a><span class="ot">            xmlns:ns15=</span><span class="st">&quot;http://www.w3.org/2001/04/xmlenc#&quot;</span>&gt;</span>
<span id="cb2-18"><a href="#cb2-18" aria-hidden="true" tabindex="-1"></a>            &lt;<span class="kw">ns2:CardHandle</span>&gt;8cbd273f-a644-4986-a64a-4ee7994b77cc&lt;/<span class="kw">ns2:CardHandle</span>&gt;</span>
<span id="cb2-19"><a href="#cb2-19" aria-hidden="true" tabindex="-1"></a>            &lt;<span class="kw">ns5:Crypt</span>&gt;RSA&lt;/<span class="kw">ns5:Crypt</span>&gt;</span>
<span id="cb2-20"><a href="#cb2-20" aria-hidden="true" tabindex="-1"></a>            &lt;<span class="kw">ns11:Context</span>&gt;</span>
<span id="cb2-21"><a href="#cb2-21" aria-hidden="true" tabindex="-1"></a>                &lt;<span class="kw">ns2:MandantId</span>&gt;Mandant1&lt;/<span class="kw">ns2:MandantId</span>&gt;</span>
<span id="cb2-22"><a href="#cb2-22" aria-hidden="true" tabindex="-1"></a>                &lt;<span class="kw">ns2:ClientSystemId</span>&gt;CS1&lt;/<span class="kw">ns2:ClientSystemId</span>&gt;</span>
<span id="cb2-23"><a href="#cb2-23" aria-hidden="true" tabindex="-1"></a>                &lt;<span class="kw">ns2:WorkplaceId</span>&gt;AP1&lt;/<span class="kw">ns2:WorkplaceId</span>&gt;</span>
<span id="cb2-24"><a href="#cb2-24" aria-hidden="true" tabindex="-1"></a>                &lt;<span class="kw">ns2:UserId</span>&gt;user1&lt;/<span class="kw">ns2:UserId</span>&gt;</span>
<span id="cb2-25"><a href="#cb2-25" aria-hidden="true" tabindex="-1"></a>            &lt;/<span class="kw">ns11:Context</span>&gt;</span>
<span id="cb2-26"><a href="#cb2-26" aria-hidden="true" tabindex="-1"></a>            &lt;<span class="kw">ns5:TvMode</span>&gt;NONE&lt;/<span class="kw">ns5:TvMode</span>&gt;</span>
<span id="cb2-27"><a href="#cb2-27" aria-hidden="true" tabindex="-1"></a>            &lt;<span class="kw">ns5:JobNumber</span>&gt;NHH-436&lt;/<span class="kw">ns5:JobNumber</span>&gt;</span>
<span id="cb2-28"><a href="#cb2-28" aria-hidden="true" tabindex="-1"></a>            &lt;<span class="kw">ns5:SignRequest</span><span class="ot"> RequestID=</span><span class="st">&quot;c82e6614-c891-40aa-9b8b-fa17a54f03b8&quot;</span>&gt;</span>
<span id="cb2-29"><a href="#cb2-29" aria-hidden="true" tabindex="-1"></a>                &lt;<span class="kw">ns5:OptionalInputs</span>&gt;</span>
<span id="cb2-30"><a href="#cb2-30" aria-hidden="true" tabindex="-1"></a>                    &lt;<span class="kw">ns3:SignatureType</span>&gt;urn:ietf:rfc:5652&lt;/<span class="kw">ns3:SignatureType</span>&gt;</span>
<span id="cb2-31"><a href="#cb2-31" aria-hidden="true" tabindex="-1"></a>                    &lt;<span class="kw">ns5:IncludeEContent</span>&gt;true&lt;/<span class="kw">ns5:IncludeEContent</span>&gt;</span>
<span id="cb2-32"><a href="#cb2-32" aria-hidden="true" tabindex="-1"></a>                &lt;/<span class="kw">ns5:OptionalInputs</span>&gt;</span>
<span id="cb2-33"><a href="#cb2-33" aria-hidden="true" tabindex="-1"></a>                &lt;<span class="kw">ns5:Document</span><span class="ot"> ShortText=</span><span class="st">&quot;a CMSDocument2Sign&quot;</span><span class="ot"> ID=</span><span class="st">&quot;CMS-Doc1&quot;</span>&gt;</span>
<span id="cb2-34"><a href="#cb2-34" aria-hidden="true" tabindex="-1"></a>                    &lt;<span class="kw">ns3:Base64Data</span><span class="ot"> MimeType=</span><span class="st">&quot;text/plain; charset=utf-8&quot;</span>&gt;eyJzaGlwbWVudCI6Imh0dHBzOi8vYmVpc3BpZWx1cmxWZXJzYW5kLmRlLzMtMTAuMy4xMjM0NTY3MDAwLjEwLjk5OT9yZXE9MTIzNDU2IiwiZGVsaXZlcnkiOiJodHRwczovL2JlaXNwaWVsdXJsQm90ZS5kZS8iLCJvblByZW1pc2UiOiJodHRwczovL2JlaXNwaWVsdXJsQWJob2x1bmcuZGUvIn0=&lt;/<span class="kw">ns3:Base64Data</span>&gt;</span>
<span id="cb2-35"><a href="#cb2-35" aria-hidden="true" tabindex="-1"></a>                &lt;/<span class="kw">ns5:Document</span>&gt;</span>
<span id="cb2-36"><a href="#cb2-36" aria-hidden="true" tabindex="-1"></a>                &lt;<span class="kw">ns5:IncludeRevocationInfo</span>&gt;false&lt;/<span class="kw">ns5:IncludeRevocationInfo</span>&gt;</span>
<span id="cb2-37"><a href="#cb2-37" aria-hidden="true" tabindex="-1"></a>            &lt;/<span class="kw">ns5:SignRequest</span>&gt;</span>
<span id="cb2-38"><a href="#cb2-38" aria-hidden="true" tabindex="-1"></a>        &lt;/<span class="kw">ns5:SignDocument</span>&gt;</span>
<span id="cb2-39"><a href="#cb2-39" aria-hidden="true" tabindex="-1"></a>    &lt;/<span class="kw">S:Body</span>&gt;</span>
<span id="cb2-40"><a href="#cb2-40" aria-hidden="true" tabindex="-1"></a>&lt;/<span class="kw">S:Envelope</span>&gt;</span></code></pre></div>
<div class="note">
<p>Mit der Referenz
<code>&lt;m2:SignatureType&gt;urn:ietf:rfc:5652&lt;/m2:SignatureType&gt;</code>
auf den RFC-5652 erfolgt die Erzeugung der nonQES als CMS-Signatur
(CAdES).</p>
</div>
<div class="note">
<p>Mit
<code>&lt;m:IncludeEContent&gt;true&lt;/m:IncludeEContent&gt;</code>
wird der Konnektor angewiesen, eine enveloping-Signatur zu erzeugen.
D.h. der signierte Datensatz ist (<code>true</code>) Bestandteil des
erzeugten Signaturobjekts.</p>
</div>
<div class="note">
<p>In
<code>&lt;ns5:Document ID="CMS-Doc1" ShortText="a CMSDocument2sign"&gt;</code>
erfolgt die Übergabe des mittels nonQES zu signierenden Datensatzes in
Base64-codierter Form.<br />
<strong><em>ShortText nicht länger als 30 Zeichen!</em></strong></p>
</div></td>
</tr>
</tbody>
</table>

**Response**

    <?xml version="1.0"?>
    <S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/">
        <S:Body>
            <ns10:SignDocumentResponse xmlns:ns2="http://www.w3.org/2001/04/xmlenc#"
                xmlns:ns3="http://www.w3.org/2000/09/xmldsig#"
                xmlns:ns4="http://uri.etsi.org/01903/v1.3.2#"
                xmlns:ns5="http://uri.etsi.org/02231/v2#"
                xmlns:ns6="urn:oasis:names:tc:dss-x:1.0:profiles:verificationreport:schema#"
                xmlns:ns7="urn:oasis:names:tc:dss:1.0:core:schema"
                xmlns:ns8="http://ws.gematik.de/conn/ConnectorCommon/v5.0"
                xmlns:ns9="http://ws.gematik.de/tel/error/v2.0"
                xmlns:ns10="http://ws.gematik.de/conn/SignatureService/v7.5"
                xmlns:ns11="http://ws.gematik.de/conn/ConnectorContext/v2.0"
                xmlns:ns12="urn:oasis:names:tc:dss-x:1.0:profiles:SignaturePolicy:schema#"
                xmlns:ns13="http://ws.gematik.de/conn/CertificateServiceCommon/v2.0"
                xmlns:ns14="urn:oasis:names:tc:SAML:2.0:assertion"
                xmlns:ns15="urn:oasis:names:tc:SAML:1.0:assertion">
                <ns10:SignResponse RequestID="c82e6614-c891-40aa-9b8b-fa17a54f03b8">
                    <ns8:Status>
                        <ns8:Result>OK</ns8:Result>
                    </ns8:Status>
                    <ns10:OptionalOutputs>
                        <ns10:DocumentWithSignature ShortText="a CMSDocument2Sign" ID="CMS-Doc1">
                            <ns7:Base64Data></ns7:Base64Data>
                        </ns10:DocumentWithSignature>
                    </ns10:OptionalOutputs>
                    <ns7:SignatureObject>
                        <ns7:Base64Signature Type="urn:ietf:rfc:5652">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</ns7:Base64Signature>
                    </ns7:SignatureObject>
                </ns10:SignResponse>
            </ns10:SignDocumentResponse>
        </S:Body>
    </S:Envelope>

Das Ergebnis der erfolgreichen nonQES wird Base64-codiert in
`<ns7:SignatureObject>` zurückgegeben. Darin enthalten ist eine
PKCS#7-Datei in HEX-Codierung, die mit einem ASN1-Decoder angesehen
werden kann.

<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>Code</p></td>
<td style="text-align: left;"><p>Type Success</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>200</p></td>
<td style="text-align: left;"><pre><code> OK +
[small]#Die Anfrage wurde erfolgreich bearbeitet. Die angeforderte Ressource wurde vor dem Senden der Antwort erstellt.#</code></pre></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>Code</p></td>
<td style="text-align: left;"><p>Type Error</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>400</p></td>
<td style="text-align: left;"><pre><code> Bad Request  +
[small]#Die Anfrage-Nachricht war fehlerhaft aufgebaut.#</code></pre></td>
</tr>
</tbody>
</table>

## Übertragen an den Upload-Container des AVS

Das APOVZD stellt eine Schnittstelle (Upload-Container) bereit.

Der beigestellte Upload-Container stellt im Internet einen REST-Service
gemäß \[ADAS-A2B-eRezept\] unter der folgenden URL zur Verfügung,
welcher die POST-Operation zur Einlieferung der Endpunkte durch das AVS
unterstützt:

    https://datahub.ngda.de/erx2gem/<version>/configuration/erx2url/?n_id=<N-ID>

mit

<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>Platzhalter</p></td>
<td style="text-align: left;"><p>Bedeutung</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>&lt;version&gt;</p></td>
<td style="text-align: left;"><p>Versionsnummer der
Schnittstellenspezifikation (gepflegt durch ADAS als openAPI Spec in
SwaggerHub</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>&lt;N-ID&gt;</p></td>
<td style="text-align: left;"><p>N-ID der Apotheke als
Identifier</p></td>
</tr>
</tbody>
</table>

Der Identifier N-ID ist dem AVS aus der Authentifizierungsmethodik der
NGDA bekannt.

Das AVS authentifiziert sich gegenüber dem Upload-Container über einen
durch den NGDA bereitgestellten Authentisierungsendpunkt, der der
Systematik der Authentifizierung für den securPharm-Prozess entspricht.
Es werden zwei abweichende Parameter verwendet:

    clientId=urn-ngda-clients-erxti-m2m
    scope=urn-ngda-services-pharmacy

Das Ergebnis der Authentifizierung ist ein Bearer Token, der bei
Aufrufen des AVS an den Upload-Container im Header übergeben werden
muss. Das AVS übermittelt den signierten Datensatz.

Weitere Informationen finden sich auf der [Webseite der
NGDA](https://ngda.de/loesungen/securpharm.php).

## Apothekenstammdaten im APOVZD

Das APOVZD prüft das Vorhandensein eines Eintrages mit der Telematik-ID
im APOVZD und die Signatur des übermittelten Datensatzes. Bei
erfolgreicher Prüfung wird auf Basis der Telematik-ID aus dem
Signaturzertifikat die übermittelten URLs den Einträgen im APOVZD
zugeordnet.

Die Apothekenstammdaten im APOVZD werden um folgende Informationen
erweitert:

-   ein oder mehrere Verschlüsselungszertifikate der Apotheke
    (C.HCI.ENC)

-   je eine URL für jede Belieferungsoption

-   zusätzliche Type-Angabe, dass dieses Feature von der Apotheke
    unterstützt wird

Das APOVZD synchronisiert die Verschlüsselungszertifikate aus dem VZD
der TI. Bsp:

    cn: gematik006

    organization: gematik

    userCertificate;binary:: MIIFcDCCBFigAwIBAgIDOlcOMA0GCSq...
    userCertificate;binary:: MIIFUTCCBDmgAwIBAgIDQNF0MA0GCqG...

Das APOVZD stellt jedes Zertifikat in einer eigenen
FHIR-Binary-Ressource bereit, wobei jedes Binary eine Referenz auf die
zugehörige LocationApoVzd enthält. Dafür wird das Attribut
Binary.securityContext verwendet. Über die Suche nach Binary mit dem
Suchparameter ?\_securityContext=Location/&lt;location\_id&gt; können
alle Verschlüsselungszertifikate einer Apotheke gefunden und
heruntergeladen werden.

Beispiel eines solchen Binaries:

    {
        "resourceType": "Binary",
        "id": "2928977",
        "meta": {
            "versionId": "1",
            "lastUpdated": "2022-05-05T10:30:29.636+00:00",
            "source": "=thriqhUOEicndJuZ"
        },
        "contentType": "application/pkix-cert",
        "securityContext": {
            "reference": "Location/87e5bda2-cf17-439f-bef5-f705afcd06f1"
        },
        "data": "MIIFUTCCBDmgAwIBAgIDQNF0MA0GCSqGSIb3DQEBCwUAMIGJMQswCQYDVQQGEwJERTEVMBMGA1UECgwMRC1UUlVTVCBHbWJIMUgwRgYDVQQLDD9JbnN0aXR1dGlvbiBkZXMgR2VzdW5kaGVpdHN3ZXNlbnMtQ0EgZGVyIFRlbGVtYXRpa2luZnJhc3RydWt0dXIxGTAXBgNVBAMMEEQtVHJ1c3QuU01DQi1DQTMwHhcNMjExMDExMDM0ODU0WhcNMjYwODE1MDcyOTMxWjBmMQswCQYDVQQGEwJERTEgMB4GA1UECgwXQmV0cmllYnNzdMOkdHRlIGdlbWF0aWsxIDAeBgNVBAUTFzEwLjgwMjc2MDAzMTExMDAwMDAwNTQyMRMwEQYDVQQDDApnZW1hdGlrMDA2MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAmtDDCfvOJL82smWeqCKa1azV3SpMHOhO2P+ot6Yi+DRqANl/0HyUO+b5VGatK1ugqONe9f0jfwUCPKxr33V5dmtJ4F4Ywbjv5rfYhMdTR1XMbrzoOwAFhdve0k42dXbW2NCr8TZLz7xlcKihRphuzGbnGa+XpJriaw7g6fNmdo27Ad4tNIpezqFQWduRJMDnW+89bzOdicLmyKU2k6IK9Wpd8+TjQLtoG32IAxX/+auqf9wYZW9H7mGFBagPxLO7D8cWaaX0K3JtRfCCE2hS7iBd6EqGCeoGz9NFg6aMDLxSOTuEgriTOI/OWSXVpFyAp9amm6KUmdhKegQ0iSvS0wIDAQABo4IB4jCCAd4wHwYDVR0jBBgwFoAUxk6YSKNeL3M/yJih5vVHqDXIhTowcgYFKyQIAwMEaTBnpCYwJDELMAkGA1UEBhMCREUxFTATBgNVBAoMDGdlbWF0aWsgR21iSDA9MDswOTA3MBkMF0JldHJpZWJzc3TDpHR0ZSBnZW1hdGlrMAkGByqCFABMBDoTDzktMi41OC4wMDAwMDA0MDBEBggrBgEFBQcBAQQ4MDYwNAYIKwYBBQUHMAGGKGh0dHA6Ly9ELVRSVVNULVNNQ0ItQ0EzLm9jc3AuZC10cnVzdC5uZXQwUQYDVR0gBEowSDA7BggqghQATASBIzAvMC0GCCsGAQUFBwIBFiFodHRwOi8vd3d3LmdlbWF0aWsuZGUvZ28vcG9saWNpZXMwCQYHKoIUAEwETDBxBgNVHR8EajBoMGagZKBihmBsZGFwOi8vZGlyZWN0b3J5LmQtdHJ1c3QubmV0L0NOPUQtVHJ1c3QuU01DQi1DQTMsTz1ELVRSVVNUJTIwR21iSCxDPURFP2NlcnRpZmljYXRlcmV2b2NhdGlvbmxpc3QwHQYDVR0OBBYEFO4u6BXelEMIzPzPE3Dr+mYUEto/MA4GA1UdDwEB/wQEAwIEMDAMBgNVHRMBAf8EAjAAMA0GCSqGSIb3DQEBCwUAA4IBAQDVUgAkYpXjjeUJbj2fWEXcgiFC0xEk0yAwmY9jK6An0fT+cRC/quTdZx81BR0qt77ROBJ3Sw5CH5+Ai4bjfIsmPOtIFV3qlYWgkldXhUfNHO+pLtdSnlhr7q4MpAoX8pyHrLyMPubJwBSeEHoY6yrW8bm1Pmo3NY/haOGEtuu6oS4hOqUD7kGHFsVpxYQY3gSzVzSv8B2d/pQ6zt6PU2nAYPV+JmRGBXGKPL8ncvZuQK0UsuMpNW0Q7sP6YDxLibjz3631dSjPs5MxIinKVxRPPSm357w8ekTs89oWshDGMuY8Oz7pu4taFHpE3xlzYXhnic0Bj61g6O9YFjcL43No"
    }

Das Synchronisieren vom Upload-Container in das APOVZD erfolgt täglich
zwischen 0 und 6 Uhr. Spätestens ab 6 Uhr ist die Änderung für das
E-Rezept-FdV verfügbar.

Für die europäischen Versandapotheken erfolgt die Pflege der URLs im
APOVZD mittels des Pflegetools der gematik.

# Anwendungsfall Abrufen der Zusatzinformationen im APOVZD durch das E-Rezept-FdV

Als Versicherter möchte ich einer Apotheke meiner Wahl ein E-Rezept
übermitteln. Über eine Verzeichnissuche habe ich die gewünschte Apotheke
gefunden. Mittels der hinterlegten Belieferungsoptionen kann ich
einsehen, wie ich meine Medikamente erhalten kann.

Dem E-Rezept-FdV werden über das APOVZD die URLs innerhalb der
LocationRessource als weitere telecom-Attribute mitgeteilt. Die zu
verwendenden Kontaktinformationen (Webseite, Telefon, E-Mail) erhalten
einen niedrigen "rank" für eine hohe Priorität. Die bis zu drei
Belieferungsoptionen werden mit dem "system": "other" und folgenden
Prioritäten festgelegt:

-   100 = URL für Belieferungsoption "Abholung in der Apotheke"

-   200 = URL für Belieferungsoption "Lieferung zum Versicherten durch
    Vor-Ort-Apotheke" (Botendienst)

-   300 = URL für Belieferungsoption "Versand zum Versicherten durch
    Online-Apotheke"

Beispiel:

    "telecom": [
        {
            "system": "phone",
            "value": "030/400410",
            "rank": 1
        },
        {
            "system": "other",
            "value": "https://www.megaaoptheke.de/reservierung",
            "use": "mobile",
            "rank": 100
        },
        {
            "system": "other",
            "value": "https://www.megaapotheke.de/botendienst",
            "use": "mobile",
            "rank": 200
        },
        {
            "system": "other",
            "value": "https://www.megaapotheke.de/versand",
            "use": "mobile",
            "rank": 300
        }
    ]

Um aus dem E-Rezept-FdV nach Apotheken zu filtern, die dieses Feature
unterstützen, wird ein zusätzlicher Type DELEGATOR aus dem Codesystem
<http://terminology.hl7.org/CodeSystem/v3-RoleCode> eingeführt.

Eine Suche aus dem E-Rezept-FdV kann dann über den URL-Parameter
"?type=&lt;filter&gt;" in Form eines Token-Search gemäß \[FHIR-SEARCH\]
aufgerufen werden, z.B. als
[http://hapi.fhir.org/baseR4/Location?type=http://terminology.hl7.org/CodeSystem/v3-RoleCode|DELEGATOR](http://hapi.fhir.org/baseR4/Location?type=http://terminology.hl7.org/CodeSystem/v3-RoleCode|DELEGATOR)

Sobald eine Apotheke ausgewählt wurde, können zum Verschlüsseln der
Nachricht die entsprechenden Zertifikate (Binary Objekte) im APOVZD mit
dem Suchparameter Location gefunden werden:

    ?_securityContext=Location/<location_id>

(Beispiel-Binary s. [Beispiel APOVZD Zertifikat
Binary](#apovzd-cert-binary))

# Anwendungsfall Bereitstellen der alternativen Zuweisung an einen Dienstleister/Rest-Api durch durch das E-Rezept-FdV

Bis der APOVZD die Funktionalität zur Bereitstellung der URLs für die
Belieferungsoptionen und SMC-B Verschlüsselungszertifikate in der
Testumgebung implementiert hat, können AVS-Hersteller das Zuweisen mit
der Konny-App testen, indem obige Informationen durch den Nutzer in die
Konny-App eingepflegt werden. Siehe [Installation
Konny-App](../attachments/Konny_Zuweisen-ohne-ti2.pdf).

![width=100%](../images/../images/puml_az_patient.png)

Als Versicherter möchte ich mein Rezept an die Apotheke meiner Wahl
übermitteln. Meine App kennt die notwendigen Verschlüsselungszertifikate
der Apotheke und die URL der gewünschten Belieferungsoption.

## Erstellen des Datensatzes

Über Abfragen im FdV sollen folgende Informationen abgefragt und ergänzt
werden:

-   Abweichende Lieferadresse

-   Zusätzliche Hinweise für die Auslieferung

-   Freitext

-   Kontaktinformationen

    -   Telefon

    -   E-Mail

Der folgende Datensatz wird erstellt:

    {
        "version": "2",
        "supplyOptionsType": "delivery",
        "name": "Dr. Maximilian von Muster",
        "address": ["Bundesallee", "312", "12345", "Berlin"],
        "hint": "Bitte im Morsecode klingeln: -.-.",
        "text": "123456",
        "phone": "004916094858168",
        "mail": "max@musterfrau.de",
        "transactionID": "ee63e415-9a99-4051-ab07-257632faf985",
        "taskID": "160.123.456.789.123.58",
        "accessCode": "777bea0e13cc9c42ceec14aec3ddee2263325dc2c6c699db115f58fe423607ea"
    }

## Verschlüsselung des Datensatzes

Der erstellte Datensatz wird hybrid mit allen
Verschlüsslungszertifikaten (C.HCI.ENC) der SMC-Bs der Apotheke
verschlüsselt.

In jeden verschlüsselten Datensatz müssen dabei die
Empfängerinformationen zur Identifikation der richtigen SMC-B durch das
Apothekensystem eingetragen werden. Diese erfolgt analog zur Anwendung
Kommunikation im Medizinwesen (KIM) über die Seriennummer des
verwendeten Zertifikats in der Verschlüsselung.

Das Zielformat der Verschlüsselung ist ein CMS-Objekt, in das
zusätzliche (unsafe = unverschlüsselt) Attribute für die Unterstützung
der Entschlüsselung eingebettet werden. Diese werden unter der OID
oid\_komle-recipient-emails gemäß \[gemSpec\_OID\] gespeichert.

Die Einbettung der Attribute erfolgt in eine ASN.1-Struktur analog zum
KIM-Verfahren. Anstelle der im KIM-Verfahren verwendeten E-Mail-Adresse
des Empfängers wird die Telematik-ID der adressierten Apotheke
eingetragen.

    id-recipientEmails OBJECT IDENTIFIER ::= {1.2.276.0.76.4.173}
    Recipient-emails Attributwerte sind vom ASN.1 Typ RecipientEmails:
    RecipientEmails ::= SET SIZE (1..MAX) OF RecipientEmail
    RecipientEmail ::= SEQUENCE {
        telematikID IA5String, rid RecipientIdentifier
        }

Diese ASN.1-Struktur muss Base64-DER codiert im Aufruf der
Verschlüsselungsoperation übergeben werden.

Das folgende beispielhafte Kommando verschlüsselt einen Datensatz für
ein ENC-Zertifikat inkl. Einbettung der unsafe-Attribute (kotlin-Code).

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

Der erhaltene CMS-Datensatz enthält unter der genannten OID die
Entschlüsselungsinformationen für den Empfänger:

![width=80%](../images/az_cms_encrypted.png)

Abschließend wird der verschlüsselte Datensatz mit einem POST and die
entsprechende URL mittels TLS übermittelt.

# Anwendungsfall Übermittlung der alternativen Zuweisung durch einen Dienstleister/Rest-Api an das AVS

![width=100%](../images/../images/puml_az_apotheke.png)

Als Apotheke erhalte ich eine Benachrichtigung über das AVS, dass eine
neue Zuweisung durch einen Patienten an die Apotheke übermittelt wurde.

Wenn das FdV eine mit dem Zertifikat der SMB-C verschlüsselte Nachricht
an den Dienstleister überträgt, benachrichtigt dieser das AVS. Dieser
Workflow und die Schnittstellen werden nicht von der gematik vorgegeben.
Das AVS kann die Nachricht mit einem Konnektor, in welchem eine der in
der Nachricht referenzierten SMC-Bs registriert ist, entschlüsseln.

## Entschlüsselung der Nachricht

Der übermittelte CMS-Datensatz enthält die notwendigen Informationen zur
Lokalisierung der für die Entschlüsselung zu nutzende SMC-B. Der
Datensatz kann mit der Operation `DecryptDocument` des Konnektors
entschlüsselt werden.

    <S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/"
        xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
        <SOAP-ENV:Header/>
        <S:Body>
            <ns5:DecryptDocument xmlns="http://ws.gematik.de/tel/error/v2.0"
                xmlns:ns2="http://ws.gematik.de/conn/ConnectorCommon/v5.0"
                xmlns:ns3="urn:oasis:names:tc:dss:1.0:core:schema"
                xmlns:ns4="http://www.w3.org/2000/09/xmldsig#"
                xmlns:ns5="http://ws.gematik.de/conn/EncryptionService/v6.1"
                xmlns:ns6="http://ws.gematik.de/conn/ConnectorContext/v2.0"
                xmlns:ns7="urn:oasis:names:tc:SAML:1.0:assertion">
                <ns6:Context>
                    <ns2:MandantId>Mandant1</ns2:MandantId>
                    <ns2:ClientSystemId>CS1</ns2:ClientSystemId>
                    <ns2:WorkplaceId>AP1</ns2:WorkplaceId>
                    <ns2:UserId>user</ns2:UserId>
                </ns6:Context>
                <ns5:PrivateKeyOnCard>
                    <ns2:CardHandle>SMC-B-73</ns2:CardHandle>
                    <ns5:KeyReference/>
                </ns5:PrivateKeyOnCard>
                <ns2:Document>
                    <ns3:Base64Data MimeType="text/plain">MIAGCyqGSIb3DQEJE...</ns3:Base64Data>
                </ns2:Document>
            </ns5:DecryptDocument>
        </S:Body>
    </S:Envelope>

Der entschlüsselte Datensatz enthält folgende Informationen:

    {
        "version": "2",
        "supplyOptionsType": "delivery",
        "name": "Dr. Maximilian von Muster",
        "address": ["Bundesallee", "312", "12345", "Berlin"],
        "hint": "Bitte im Morsecode klingeln: -.-.",
        "text": "123456",
        "phone": "004916094858168",
        "mail": "max@musterfrau.de",
        "transactionID": "ee63e415-9a99-4051-ab07-257632faf985",
        "taskID": "160.123.456.789.123.58",
        "accessCode": "777bea0e13cc9c42ceec14aec3ddee2263325dc2c6c699db115f58fe423607ea"
    }

"transactionID" beinhaltet die von der E-Rezept-App erzeuge UUID zur
eindeutigen Identifikation der Transaktion.

taskID und accessCode werden für den Zugriff auf den E-Rezept-Fachdienst
benötigt.

## Bearbeiten der Anfrage

Der Apotheker kann die Anfrage bearbeiten und mit Task-ID und AccessCode
auf das E-Rezept im E-Rezept-Fachdienst zugreifen. Nachdem der Vorgang
bearbeitet wurde kann die Apotheke den Versicherten über die angegebenen
Kontaktdaten erreichen, z.B. für Bestellbestätigung, Liefertermin, etc.
