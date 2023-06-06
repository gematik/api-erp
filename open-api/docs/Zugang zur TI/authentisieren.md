Hier dokumentiert die gematik die Nutzung der Schnittstellen, um sich
mit der Telematikinfrastruktur zu verbinden. Das betrifft zum einen die
Authentifizierung als Nutzer oder Institution durch den Identity
Provider (IDP) und zum anderen den verschlüsselten Datentransport auf
Anwendungsebene (["VAU-Transport](#anchor-vau-transport)").

# Endpunkte des E-Rezept Fachdienstes

Für den Verbindungsaufbau mit dem E-Rezept Fachdienst stehen
verschiedene Endpunkte zur verfügung, je nach Entwicklungsumgebung.
Angegeben werden jeweils der Endpunkt für den Fachdienst und den IDP:

**PU**

-   erp.zentral.erp.splitdns.ti-dienste.de

-   idp.zentral.idp.splitdns.ti-dienste.de

**RU**

-   erp-ref.zentral.erp.splitdns.ti-dienste.de

-   idp-ref.zentral.idp.splitdns.ti-dienste.de

**RU-DEV**

-   erp-dev.zentral.erp.splitdns.ti-dienste.de

-   idp-ref.zentral.idp.splitdns.ti-dienste.de

Für die Entwicklung in der RU-DEV ist der Scope in der Anfrage-URL
umzustellen. Als Parameter der Anfrage ist statt
`&scope=e-rezept+openid` ist `&scope=e-rezept-dev+openid` anzugeben.
Siehe Schritt 37 im [Rbelflow für
Primärsysteme^](https://gematik.github.io/ref-idp-server/tokenFlowPs.html).

Die jeweiligen Konfigurationen können sich je nach Entwicklungsstand
unterscheiden. Aktuelle Informationen zu den jeweiligen Umgebungen
finden Sie [hier](https://wiki.gematik.de/display/RUAAS/E-Rezept@RU).

# Http-Header in Requests an Dienste der Telematikinfrastruktur

Zur Steuerung der Funktionsaufrufe, für Sicherheitsprüfungen und die
Protokollierung sind verpflichtende http-Header in allen http-Requests
an den IDP-Dienst und den E-Rezept-Fachdienst erforderlich. Da mit dem
VAU-Transport ein "innerer" und ein "äußerer" http-Request an den
E-Rezept-Fachdienst gesendet werden, ist auf das korrekte Setzen innen
und außen zu achten. Die folgende Tabelle listet die notwendigen
http-Header auf.

<table>
<colgroup>
<col style="width: 60%" />
<col style="width: 20%" />
<col style="width: 20%" />
</colgroup>
<thead>
<tr class="header">
<th style="text-align: right;">http-Header</th>
<th style="text-align: center;">äußerer Request ("/VAU")</th>
<th style="text-align: center;">innerer Request</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td style="text-align: right;"><p>Authorization</p></td>
<td style="text-align: center;"><p>-</p></td>
<td style="text-align: center;"><p>x</p></td>
</tr>
<tr class="even">
<td style="text-align: right;"><p>User-Agent</p></td>
<td style="text-align: center;"><p>x</p></td>
<td style="text-align: center;"><p>optional</p></td>
</tr>
<tr class="odd">
<td style="text-align: right;"><p>X-erp-user</p></td>
<td style="text-align: center;"><p>x</p></td>
<td style="text-align: center;"><p>-</p></td>
</tr>
<tr class="even">
<td style="text-align: right;"><p>X-erp-resource</p></td>
<td style="text-align: center;"><p>x</p></td>
<td style="text-align: center;"><p>-</p></td>
</tr>
<tr class="odd">
<td style="text-align: right;"><p>X-AccessCode</p></td>
<td style="text-align: center;"><p>-</p></td>
<td style="text-align: center;"><p>x</p></td>
</tr>
<tr class="even">
<td style="text-align: right;"><p>SOAPAction (nur für
Konnektor)</p></td>
<td style="text-align: center;"><p>n/a</p></td>
<td style="text-align: center;"><p>x</p></td>
</tr>
</tbody>
</table>

Der Aufbau von User-Agent hat nach A\_20015-01 zu erfolgen:
&lt;Produktname&gt;/&lt;Produktversion&gt;
&lt;Herstellername&gt;/&lt;client\_id&gt;

Die Standard http-Header wie bspw. `Accept-*`, `Connection`, `Host`,
`Content-Type`, `Content-Length` usw. sind gemäß Standard ebenfalls zu
setzen.

# Als Nutzer der Telematikinfrastruktur authentifiziert werden

Die Telematikinfrastruktur gestattet keinen Zugriff auf Dienste ohne
eine Identifikation der Nutzer. Dies dient der Durchsetzung von
Zugriffsregeln und der Protokollierung des Zugriffs auf medizinische
Daten von Versicherten. Mit der Authentifizierung der Nutzer erfolgt
keine Profilbildung, Sessiondaten werden temporär verwaltet und nach
Beendigung einer Sesssion unverzüglich gelöscht. Die Protokollierung von
Zugriffen auf medizinische Daten erfolgt in Abhängigkeit der genutzten
Schnittstellen in den jeweils aufgerufenen Services sowie in
Abhängigkeit der fachlichen Anforderungen gemäß
gematik-Spezifikationen.  

Die Authentifizierung übernimmt mit der Einführung des E-Rezepts ein
zentraler Identity Provider (IDP). Der IDP erkennt Nutzer anhand ihrer
kartenbasierten Identitäten und stellt die Identitätsmerkmale (Name,
KVNR bzw. Telematik-ID) der Zertifikate auf der Karte in ID\_TOKEN und
ACCESS\_TOKEN für die Nutzung im E-Rezept-Fachdienst bereit.

## Ablauf des Authentifizierungsprotokolls

Leistungserbringerinstitutionen (Praxen, Apotheken, Krankenhäuser)
weisen sich gegenüber der Telematikinfrastruktur mit der Identität des
Praxisausweises SMC-B aus. Die Authentifizierung erfolgt gegenüber dem
Identity Provider (IDP) unter Nutzung der Konnektorschnittstelle.

Das Primärsystem adressiert Anfragen an den IDP über eine bekannt zu
machende Adresse **z.B.** `idp.zentral.idp.splitdns.ti-dienste.de` bzw.
`idp.app.ti-dienste.de`, dabei veröffentlicht der IDP sein
DiscoveryDocument mit den Informationen zu verschiedenen Endpunkten zur
Tokenausstellung unter einer "/.well-known"-Adresse, d.h.
`idp.ti-dienste.de/.well-known/openid-configuration`.

Die folgende Abbildung zeigt den detaillierten Ablauf mit allen
beteiligten Komponenten. Das Primärsystem gliedert sich in die
E-Rezept-Fachlogik und ein Authenticator-Modul. Letzteres übernimmt die
Authentisierung mittels der kartenbasierten Identität unter Nutzung der
Konnektorschnittstellen. Der IDP authentifiziert den Nutzer anhand der
kartenbasierten Identität und einer Signatur durch das Schlüsselmaterial
auf der Karte (SMC-B) und stellt bei Erfolg einen Zugriffstoken
(ACCESS\_TOKEN) für den Zugriff auf den Fachdienst aus.

![width=100%](../images/workflowAuthentication.svg)

Die Ablaufbeschreibung [Rbelflow für
Primärsysteme^](https://gematik.github.io/ref-idp-server/tokenFlowPs.html)
gibt ein konkretes Beispiel mit Request- und Response-Parametern für die
Authentifizierung mittels SMC-B einer Test-Apotheke
"3-SMC-B-Testkarte-883110000xxxxxx" (siehe auch "professionOID":
"1.2.276.0.76.4.54" = "Öffentliche Apotheke").

Die folgenden Schritte sind von besonderer Bedeutung und werden kurz
erläutert.

<table>
<colgroup>
<col style="width: 0%" />
<col style="width: 0%" />
<col style="width: 98%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p><strong>Step</strong></p></td>
<td style="text-align: left;"><p><strong>eRp (Fachlogik) / AM
(Auth-Modul)</strong></p></td>
<td style="text-align: left;"><p><strong>Beschreibung</strong></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>1 - 5</p></td>
<td style="text-align: left;"><p>AM/eRP</p></td>
<td style="text-align: left;"><p>Laden des Discovery Documents (DD) vom
IDP (Diese Operation wird vorbereitend sowohl vom Auth-Modul, wie auch
von der Fachlogik und dem Fachdienst durchgeführt)<br />
[<a
href="https://idp.zentral.idp.splitdns.ti-dienste.de/.well-known/openid-configuration">https://idp.zentral.idp.splitdns.ti-dienste.de/.well-known/openid-configuration</a>]
<strong>Schritt 1 im Rbel-Flow</strong>, Prüfung der Signatur des DD
gegen das Signatur-Zertifikat im <code>x5c</code>-Feld des
Response-Header und Verifikation des Zertifikates gegen den
Vertrauensraum der TI und eine Prüfung der technischen Rolle (siehe
unten <a
href="#anchor-verify-certificate">Konnektor-Aufruf</a>,</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>6 - 8</p></td>
<td style="text-align: left;"><p>eRp</p></td>
<td style="text-align: left;"><p>Erzeugung eines CODE_VERIFIER (128
zufällige Zeichen aus der Menge [A-Z] / [a-z] / [0-9] / "-" / "." / "_"
/ "~") und bilden der CODE_CHALLENGE als dessen sha256-Hashwert sowie,
Erzeugung einer <code>nonce</code> und eines <code>state</code>.
<code>Nonce</code> ist ein optionaler Zufallswert, <code>state</code>
kann beliebig gewählt werden, also ebenso eine Zufallszahl oder eine
session-id etc.<br />
Um das CHALLENGE_TOKEN zu beziehen, werden CODE_CHALLENGE,
<code>state</code> und ggf. <code>Nonce</code> an das
Authenticator-Modul übergeben und in der Fachlogik für spätere Prüfungen
zwischengespeichert.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>AuthorizationCode über
Handshake mit Kartenidentität beziehen</strong></p></td>
<td style="text-align: left;"><p>9 - 12</p></td>
<td style="text-align: left;"><p>AM</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>Lesen des X509-Signatur-Zertifikats zum
<code>puk_idp_sig</code> des IDP und des IDP-Verschlüsselungsschlüssels
<code>puk_idp_enc</code> von <a
href="http://url.des.idp/idpSig/jwk.json">http://url.des.idp/idpSig/jwk.json</a>
und <a
href="http://url.des.idp/idpEnc/jwk.json">http://url.des.idp/idpEnc/jwk.json</a>
oder aus dem JWK-Set <a
href="http://url.des.idp/jwks">http://url.des.idp/jwks</a>
<strong>Schritt 3 + 5 im Rbel-Flow</strong></p></td>
<td style="text-align: left;"><p>13 - 17</p></td>
<td style="text-align: left;"><p>AM</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>Senden der in Schritt 8 übergebenen
Werte (als URL-Parameter wie z.B. <em>code_challenge</em>) an den
authorization_endpoint des IDP, ,+ dieser antwortet mit dem
CHALLENGE_TOKEN und dem <code>user_consent</code> <strong>Schritt 7 im
Rbel-Flow</strong>,<br />
Die Signatur des CHALLENGE_TOKEN wird mittels <code>puk_idp_sig</code>
geprüft. Es erfolgt eine Verifikation des Zertifikates gegen den
Vertrauensraum der TI und eine Prüfung der technischen Rolle (siehe
unten <a
href="#anchor-verify-certificate">Konnektor-Aufruf</a>,.</p></td>
<td style="text-align: left;"><p>18 - 19</p></td>
<td style="text-align: left;"><p>AM</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>Anzeige des <code>user_consent</code>
und Bestätigung durch den Nutzer, dass die genannten personenbezogenen
Attribute vom IDP verarbeitet und dem Fachdienst übermittelt werden
dürfen. Die erfolgte Nutzereinwilligung für diesen <code>scope</code>
kann gespeichert werden.</p></td>
<td style="text-align: left;"><p>20</p></td>
<td style="text-align: left;"><p>AM</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>Zertifikat der
Authentisierungs-Identität C.HCI.AUT von der SMC-B lesen (siehe unten <a
href="#anchor-read-aut">Konnektor-Aufruf</a>)</p></td>
<td style="text-align: left;"><p>21</p></td>
<td style="text-align: left;"><p>AM</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>Berechnen des HASH-Werts der
empfangenen Challenge und Signieren des Challenge-HASH mit PrK.HCI.AUT
der SMC-B (siehe unten <a
href="#anchor-sign-challenge">Konnektor-Aufruf</a>)</p></td>
<td style="text-align: left;"><p>22</p></td>
<td style="text-align: left;"><p>AM</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>JWE-Verschlüsselung der signierten
Challenge als njwt und des Zertifikats C.HCI.AUT mit
<code>puk_idp_enc</code> aus dem Discovery Document.</p></td>
<td style="text-align: left;"><p>23 - 27</p></td>
<td style="text-align: left;"><p>AM</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>Senden der verschlüsselten Challenge
und des verschlüsselten Zertifikats an den authorization_endpoint des
IDP<br />
<strong>Schritt 9 im Rbel-Flow</strong><br />
</p></td>
<td style="text-align: left;"><p>28</p></td>
<td style="text-align: left;"><p>AM</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>Die Response
(<code>AuthorizationCode</code> und Redirect zum Tausch des
<code>AuthorizationCode</code> gegen einen ACCESS_TOKEN) wird an die
Fachlogik zurückgegeben.<br />
</p></td>
<td style="text-align: left;"><p><strong>Authentifizierung des Nutzers
abgeschlossen, im Folgenden wird der ACCESS_TOKEN für den Zugriff am
E-Rezept-Fachdienst mit Hilfe des AuthorizationCodes
abgerufen.</strong></p></td>
<td style="text-align: left;"><p>29 - 32</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>eRp</p></td>
<td style="text-align: left;"><p>Generierung eines
<code>Token-Key</code> (AES256) zur verschlüsselten Kommunikation mit
dem IDP, anschließend wird dem Redirect gefolgt, um den
<code>AuthorizationCode</code> gegen ein AccessToken zu
tauschen.</p></td>
<td style="text-align: left;"><p>33 - 37</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>eRp</p></td>
<td style="text-align: left;"><p>Der Aufruf übergibt den zuvor
erhaltenen <code>AuthorizationCode</code> und den zusammen mit dem
CODE_VERIFIER verschlüsselten <code>Token-Key</code>.<br />
<strong>Schritt 11 im Rbel-Flow</strong><br />
Der IDP prüft die Signatur des <code>AuthorizationCode</code>, um die
Gültigkeit des Codes zu verifizieren und antwortet mit einem
verschlüsselten AccessToken für den Zugriff auf den E-Rezept-Fachdienst
und mit einem verschlüsselten ID_TOKEN.</p></td>
<td style="text-align: left;"><p>38 - 41</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>eRp</p></td>
<td style="text-align: left;"><p>Das ACCESS_TOKEN und das ID_TOKEN
werden mit Hilfe des <code>Token-Key</code> entschlüsselt. Die Signatur
des ID_TOKEN wird gegen den <code>puk_idp_sig</code> überprüft. Es
erfolgt eine Verifikation des Zertifikates gegen den Vertrauensraum der
TI und eine Prüfung der technischen Rolle (siehe unten <a
href="#anchor-verify-certificate">Konnektor-Aufruf</a>,. Die enthaltene
Nonce gegen den im Schritt 1 erzeugten Wert abgeglichen. Anschließend
wird das ACCESS_TOKEN zum Zugriff auf den Fachdienst verwendet.</p></td>
<td style="text-align: left;"><p>42 - 44</p></td>
</tr>
</tbody>
</table>

### Vorbereitende Schritte für die Authentifizierung mittels der SMC-B

1.  Dem Nutzer soll der vom IDP bereitgestellte UserConsent angezeigt
    werden. Stimmt der Nutzer der Bereitstellung der Daten für den
    E-Rezept-Fachdienst nicht zu, muss der Authentifizierungsvorgang
    abgebrochen werden, da der Fachdienst ohne diese Informationen den
    E-Rezept-Workflow nicht umsetzen kann.

2.  Die vom IDP in der obigen Response übermittelte Challenge beinhaltet
    ein Challenge-Token
    `{"iss":"https://idp.zentral.idp.splitdns.ti-dienste.de","response_type":"code","snc":"syQAvJmxPnRtLjT6uPVERb_RF7MmVzhS1sP8FbHjhLM","code_challenge_method":"S256","token_type":"challenge","nonce":"887766","client_id":"gematikTestPs","scope":"openid e-rezept","state":"xxxstatexxx","redirect_uri":"http://test-ps.gematik.de/erezept","exp":1616686048,"iat":1616685868,"code_challenge":"Ca3Ve8jSsBQOBFVqQvLs1E-dGV1BXg2FTvrd-Tg19Vg","jti":"5e5ad23ae3e7d8aa"}`
    in Base64-Codierung
    `eyJpc3MiOiJodHRwczovL2lkcC56ZW50cmFsLmlkcC5zcGxpdGRucy50aS1kaWVuc3RlLmRlIiwicmVzcG9uc2VfdHlwZSI6ImNvZGUiLCJzbmMiOiJzeVFBdkpteFBuUnRMalQ2dVBWRVJiX1JGN01tVnpoUzFzUDhGYkhqaExNIiwiY29kZV9jaGFsbGVuZ2VfbWV0aG9kIjoiUzI1NiIsInRva2VuX3R5cGUiOiJjaGFsbGVuZ2UiLCJub25jZSI6Ijg4Nzc2NiIsImNsaWVudF9pZCI6ImdlbWF0aWtUZXN0UHMiLCJzY29wZSI6Im9wZW5pZCBlLXJlemVwdCIsInN0YXRlIjoieHh4c3RhdGV4eHgiLCJyZWRpcmVjdF91cmkiOiJodHRwOi8vdGVzdC1wcy5nZW1hdGlrLmRlL2VyZXplcHQiLCJleHAiOjE2MTY2ODYwNDgsImlhdCI6MTYxNjY4NTg2OCwiY29kZV9jaGFsbGVuZ2UiOiJDYTNWZThqU3NCUU9CRlZxUXZMczFFLWRHVjFCWGcyRlR2cmQtVGcxOVZnIiwianRpIjoiNWU1YWQyM2FlM2U3ZDhhYSJ9`.
    Da die Signatur immer über einen Hashwert der zu signierenden Daten
    erfolgt, muss dieser Hashwert vom Clientsystem berechnet werden. Als
    kryptografisches Verfahren kommt hier SHA-256 zum Einsatz. Aus dem
    obigen Beispiel `eyJpc3MiOiJodHRwczovL2lkcC56ZW50cmFsLmlkcC5...`
    ergibt sich folgender Hashwert:
    `dd775a30757431a62bbe12301898511f5d9d5145a58dbd5d6cbae2481b36993f`

### Request zum Auslesen des Zertifikats der SMC-B über Konnektor (read\_certificate)

Der Konnektor authentifiziert Nutzer anhand einer kartengebundenen,
kryptografischen Identität. Die Karte hält den privaten Schlüssel zu
dieser Identität, welcher für die Signatur über eine Challenge des IDP
genutzt wird. Zur Prüfung der Signatur benötigt der IDP das Zertifikat
dieser Identität. Dieses enthält den öffentlichen Schlüssel für die
kryptografische Signaturprüfung sowie weitere Nutzerinformationen (Name,
KVNR/Telematik-ID, fachliche Rolle), die der IDP in
Identitätsbestätigungen zur Nutzung gegenüber dem E-Rezept-Fachdienst
attestiert. Der Abruf des Zertifikats erfolgt über die
Konnektor-Operation `ReadCertificate`.

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
SOAPAction: &quot;http://ws.gematik.de/conn/CertificateService/v7.4#ReadCardCertificate&quot;</code></pre></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>Payload</strong></p></td>
<td style="text-align: left;"><div class="sourceCode" id="cb2"><pre
class="sourceCode xml"><code class="sourceCode xml"><span id="cb2-1"><a href="#cb2-1" aria-hidden="true" tabindex="-1"></a>&lt;<span class="kw">S:Envelope</span><span class="ot"> xmlns:S=</span><span class="st">&quot;http://schemas.xmlsoap.org/soap/envelope/&quot;</span>&gt;</span>
<span id="cb2-2"><a href="#cb2-2" aria-hidden="true" tabindex="-1"></a>    &lt;<span class="kw">S:Body</span>&gt;</span>
<span id="cb2-3"><a href="#cb2-3" aria-hidden="true" tabindex="-1"></a>        &lt;<span class="kw">ns8:ReadCardCertificate</span><span class="ot"> xmlns:ns2=</span><span class="st">&quot;http://ws.gematik.de/conn/CertificateServiceCommon/v2.0&quot;</span></span>
<span id="cb2-4"><a href="#cb2-4" aria-hidden="true" tabindex="-1"></a><span class="ot">            xmlns:ns3=</span><span class="st">&quot;urn:oasis:names:tc:dss:1.0:core:schema&quot;</span></span>
<span id="cb2-5"><a href="#cb2-5" aria-hidden="true" tabindex="-1"></a><span class="ot">            xmlns:ns4=</span><span class="st">&quot;http://www.w3.org/2000/09/xmldsig#&quot;</span></span>
<span id="cb2-6"><a href="#cb2-6" aria-hidden="true" tabindex="-1"></a><span class="ot">            xmlns:ns5=</span><span class="st">&quot;http://ws.gematik.de/conn/ConnectorCommon/v5.0&quot;</span></span>
<span id="cb2-7"><a href="#cb2-7" aria-hidden="true" tabindex="-1"></a><span class="ot">            xmlns:ns6=</span><span class="st">&quot;http://ws.gematik.de/tel/error/v2.0&quot;</span></span>
<span id="cb2-8"><a href="#cb2-8" aria-hidden="true" tabindex="-1"></a><span class="ot">            xmlns:ns7=</span><span class="st">&quot;urn:oasis:names:tc:SAML:1.0:assertion&quot;</span></span>
<span id="cb2-9"><a href="#cb2-9" aria-hidden="true" tabindex="-1"></a><span class="ot">            xmlns:ns8=</span><span class="st">&quot;http://ws.gematik.de/conn/CertificateService/v7.4&quot;</span></span>
<span id="cb2-10"><a href="#cb2-10" aria-hidden="true" tabindex="-1"></a><span class="ot">            xmlns:ns9=</span><span class="st">&quot;http://ws.gematik.de/conn/ConnectorContext/v2.0&quot;</span>&gt;</span>
<span id="cb2-11"><a href="#cb2-11" aria-hidden="true" tabindex="-1"></a>            &lt;<span class="kw">ns5:CardHandle</span>&gt;smc-b_2&lt;/<span class="kw">ns5:CardHandle</span>&gt;</span>
<span id="cb2-12"><a href="#cb2-12" aria-hidden="true" tabindex="-1"></a>            &lt;<span class="kw">ns9:Context</span>&gt;</span>
<span id="cb2-13"><a href="#cb2-13" aria-hidden="true" tabindex="-1"></a>                &lt;<span class="kw">ns5:MandantId</span>&gt;Mandant1&lt;/<span class="kw">ns5:MandantId</span>&gt;</span>
<span id="cb2-14"><a href="#cb2-14" aria-hidden="true" tabindex="-1"></a>                &lt;<span class="kw">ns5:ClientSystemId</span>&gt;myPVS&lt;/<span class="kw">ns5:ClientSystemId</span>&gt;</span>
<span id="cb2-15"><a href="#cb2-15" aria-hidden="true" tabindex="-1"></a>                &lt;<span class="kw">ns5:WorkplaceId</span>&gt;WP1&lt;/<span class="kw">ns5:WorkplaceId</span>&gt;</span>
<span id="cb2-16"><a href="#cb2-16" aria-hidden="true" tabindex="-1"></a>            &lt;/<span class="kw">ns9:Context</span>&gt;</span>
<span id="cb2-17"><a href="#cb2-17" aria-hidden="true" tabindex="-1"></a>            &lt;<span class="kw">ns8:CertRefList</span>&gt;</span>
<span id="cb2-18"><a href="#cb2-18" aria-hidden="true" tabindex="-1"></a>                &lt;<span class="kw">ns8:CertRef</span>&gt;C.AUT&lt;/<span class="kw">ns8:CertRef</span>&gt;</span>
<span id="cb2-19"><a href="#cb2-19" aria-hidden="true" tabindex="-1"></a>            &lt;/<span class="kw">ns8:CertRefList</span>&gt;</span>
<span id="cb2-20"><a href="#cb2-20" aria-hidden="true" tabindex="-1"></a>        &lt;/<span class="kw">ns8:ReadCardCertificate</span>&gt;</span>
<span id="cb2-21"><a href="#cb2-21" aria-hidden="true" tabindex="-1"></a>    &lt;/<span class="kw">S:Body</span>&gt;</span>
<span id="cb2-22"><a href="#cb2-22" aria-hidden="true" tabindex="-1"></a>&lt;/<span class="kw">S:Envelope</span>&gt;</span></code></pre></div>
<div class="note">
<p>In <code>&lt;ns8:CertRef&gt;C.AUT&lt;/ns8:CertRef&gt;</code> wird
angegeben, dass das Zertifikat zur Authentisierung gegenüber dem IDP aus
der SMC-B ausgelesen werden soll.</p>
</div></td>
</tr>
</tbody>
</table>

**Response**

    HTTP/1.1 200 OK
    Content-Type: text/xml;charset=utf-8

    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
        <soap:Body>
            <ns3:ReadCardCertificateResponse xmlns="http://ws.gematik.de/conn/ConnectorCommon/v5.0"
                xmlns:ns2="http://ws.gematik.de/conn/ConnectorContext/v2.0"
                xmlns:ns3="http://ws.gematik.de/conn/CertificateService/v7.4"
                xmlns:ns4="http://ws.gematik.de/tel/error/v2.0"
                xmlns:ns5="http://ws.gematik.de/conn/CertificateServiceCommon/v2.0"
                xmlns:ns6="http://www.w3.org/2000/09/xmldsig#"
                xmlns:ns7="urn:oasis:names:tc:dss:1.0:core:schema"
                xmlns:ns8="urn:oasis:names:tc:SAML:1.0:assertion">
                <Status>
                    <Result>OK</Result>
                </Status>
                <ns5:X509DataInfoList>
                    <ns5:X509DataInfo>
                        <ns5:X509Data>
                            <ns5:X509Certificate>MIIFcTCCBFmgAwIBAgIHAXumDkbX3zANBgkqhkiG9w0BAQsFADCBmjELMAkGA1UEBhMCREUxHzAdBgNVBAoMFmdlbWF0aWsgR21iSCBOT1QtVkFMSUQxSDBGBgNVBAsMP0luc3RpdHV0aW9uIGRlcyBHZXN1bmRoZWl0c3dlc2Vucy1DQSBkZXIgVGVsZW1hdGlraW5mcmFzdHJ1a3R1cjEgMB4GA1UEAwwXR0VNLlNNQ0ItQ0EyNCBURVNULU9OTFkwHhcNMjAwNjEwMDAwMDAwWhcNMjUwNjA5MjM1OTU5WjCB+DELMAkGA1UEBhMCREUxFDASBgNVBAcMC03DvGhsaGF1c2VuMQ4wDAYDVQQRDAU5OTk3NDEeMBwGA1UECQwVTGFuZ2Vuc2FsemFlciBTdHIuIDI1MSowKAYDVQQKDCEzLVNNQy1CLVRlc3RrYXJ0ZS04ODMxMTAwMDAxMjkwNjgxHTAbBgNVBAUTFDgwMjc2ODgzMTEwMDAwMTI5MDY4MRQwEgYDVQQEDAtCbGFua2VuYmVyZzEWMBQGA1UEKgwNRG9taW5pay1QZXRlcjEqMCgGA1UEAwwhQXBvdGhla2UgYW0gU3BvcnR6ZW50cnVtVEVTVC1PTkxZMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAjVMEf2TTXlfkuCDyiMpo96jA5XRvkaHTy+4qTcDR1awUP4yemfKsB1BTWMMSDrA1/2YdnlZJeynEnQi0K4LWMvTcq+CRGi4ghcIokb2TURZXZ1K6FTJHqITojp9ZRaNTap+kIpOZCmSRa7ftRzEgooPjG6C+7XxUViczlVE17UJMPavWQfY2+A1M/0vx9Jbi7wPmXCMuEvj7yEAVRCGQExVxzbLZPE7FS/vlXcwkFtmnMUVWiQFFXlVLG7uUc9CQFvTXPT5ppDhxAmVeUBLNXKruDkpSeuq3sCi93ln9hXXw/xPeNAAehtvxFp6eMGf5LEVGvZj8v51qu4eDPaKtJwIDAQABo4IBWjCCAVYwEwYDVR0lBAwwCgYIKwYBBQUHAwIwDgYDVR0PAQH/BAQDAgWgMB0GA1UdDgQWBBSEkJ1lgmhiHfVZyKKyVw2Qd86PPDA4BggrBgEFBQcBAQQsMCowKAYIKwYBBQUHMAGGHGh0dHA6Ly9laGNhLmdlbWF0aWsuZGUvb2NzcC8wDAYDVR0TAQH/BAIwADAgBgNVHSAEGTAXMAoGCCqCFABMBIEjMAkGByqCFABMBE0wHwYDVR0jBBgwFoAUeunhb+oUWRYF7gPp0/0hq97p2Z4wgYQGBSskCAMDBHsweaQoMCYxCzAJBgNVBAYTAkRFMRcwFQYDVQQKDA5nZW1hdGlrIEJlcmxpbjBNMEswSTBHMBcMFcOWZmZlbnRsaWNoZSBBcG90aGVrZTAJBgcqghQATAQ2EyEzLVNNQy1CLVRlc3RrYXJ0ZS04ODMxMTAwMDAxMjkwNjgwDQYJKoZIhvcNAQELBQADggEBAGwmbkXMdRrIZwTzUVsdH6RUB7cc3+CcDN0NqLSOM7sdCQrr5NfzcK2dzhc77KVzviZbvz6MxfEq47Y/dPMmtVlU0Amw5bbnYT4WnadjrLOHnKCxLFssrfo0izB7IJvBswMQl/KnUXbk/X57KcNKTYOfuCVVVt+yET63N4qp9YOPiMdCHxu+BUvgwmOgr/enRnh+HgCYVQtzLmDXimBcneRoZg3XgukoMQPd5TlVlZAF1JZ6W8uGN+LEiddnHdzYFVInest3xMzwHj4T3lXLCkr6oc9jvwKe2A2qsBvcbEFDR0mi0CW9NjfJ05v/52GKZZZyjEnFjnHJ1J5r1DlD5S8=
                            </ns5:X509Certificate>
                        </ns5:X509Data>
                    </ns5:X509DataInfo>
                </ns5:X509DataInfoList>
            </ns3:ReadCardCertificateResponse>
        </soap:Body>
    </soap:Envelope>

Der Konnektor liefert das Zertifikat in `<ns5:X509Certificate>` zurück,
wie es auf der Karte gespeichert ist, ASN.1 DER codiert in
Base64-Darstellung.

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
[small]#Die Anfrage wurde erfolgreich bearbeitet.#</code></pre></td>
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

### Zertifikat mittels Konnektoroperation verifizieren (verifyCertificate)

Der Konnektor prüft das übergebene Zertifikat gegen den Vertrauensraum
der Telematikinfrastruktur, dabei führt er eine Online-Prüfung des
Sperrstatus durch und liefert das Ergebnis der Prüfung sowie die im
Zertifikat enthaltene technische Rolle. Diese technische Rolle muss das
Primärsystem im Anschluß gegen die Rolle des erwarteten Dienstes
abgleichen.

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
SOAPAction: &quot;http://ws.gematik.de/conn/CertificateService/v6.0#VerifyCertificate&quot;</code></pre>
<div class="important">
<p>Die Länge des Soap-Requests, muss entsprechend im Header mit der
Eigenschaft <code>Content-Length</code> gesetzt werden.</p>
</div></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>Payload</strong></p></td>
<td style="text-align: left;"><div class="sourceCode" id="cb2"><pre
class="sourceCode xml"><code class="sourceCode xml"><span id="cb2-1"><a href="#cb2-1" aria-hidden="true" tabindex="-1"></a>&lt;<span class="kw">SOAP-ENV:Envelope</span><span class="ot"> xmlns:SOAP-ENV=</span><span class="st">&quot;http://schemas.xmlsoap.org/soap/envelope/&quot;</span></span>
<span id="cb2-2"><a href="#cb2-2" aria-hidden="true" tabindex="-1"></a><span class="ot">    xmlns:SOAP-ENC=</span><span class="st">&quot;http://schemas.xmlsoap.org/soap/encoding/&quot;</span></span>
<span id="cb2-3"><a href="#cb2-3" aria-hidden="true" tabindex="-1"></a><span class="ot">    xmlns:xsi=</span><span class="st">&quot;http://www.w3.org/2001/XMLSchema-instance&quot;</span></span>
<span id="cb2-4"><a href="#cb2-4" aria-hidden="true" tabindex="-1"></a><span class="ot">    xmlns:xsd=</span><span class="st">&quot;http://www.w3.org/2001/XMLSchema&quot;</span></span>
<span id="cb2-5"><a href="#cb2-5" aria-hidden="true" tabindex="-1"></a><span class="ot">    xmlns:m0=</span><span class="st">&quot;http://ws.gematik.de/conn/ConnectorContext/v2.0&quot;</span></span>
<span id="cb2-6"><a href="#cb2-6" aria-hidden="true" tabindex="-1"></a><span class="ot">    xmlns:m1=</span><span class="st">&quot;http://ws.gematik.de/conn/ConnectorCommon/v5.0&quot;</span></span>
<span id="cb2-7"><a href="#cb2-7" aria-hidden="true" tabindex="-1"></a><span class="ot">    xmlns:m2=</span><span class="st">&quot;http://ws.gematik.de/conn/CertificateServiceCommon/v2.0&quot;</span>&gt;</span>
<span id="cb2-8"><a href="#cb2-8" aria-hidden="true" tabindex="-1"></a>    &lt;<span class="kw">SOAP-ENV:Body</span>&gt;</span>
<span id="cb2-9"><a href="#cb2-9" aria-hidden="true" tabindex="-1"></a>        &lt;<span class="kw">m:VerifyCertificate</span><span class="ot"> xmlns:m=</span><span class="st">&quot;http://ws.gematik.de/conn/CertificateService/v6.0&quot;</span>&gt;</span>
<span id="cb2-10"><a href="#cb2-10" aria-hidden="true" tabindex="-1"></a>            &lt;<span class="kw">m0:Context</span>&gt;</span>
<span id="cb2-11"><a href="#cb2-11" aria-hidden="true" tabindex="-1"></a>                &lt;<span class="kw">m1:MandantId</span>&gt;Mandant1&lt;/<span class="kw">m1:MandantId</span>&gt;</span>
<span id="cb2-12"><a href="#cb2-12" aria-hidden="true" tabindex="-1"></a>                &lt;<span class="kw">m1:ClientSystemId</span>&gt;ClientID1&lt;/<span class="kw">m1:ClientSystemId</span>&gt;</span>
<span id="cb2-13"><a href="#cb2-13" aria-hidden="true" tabindex="-1"></a>                &lt;<span class="kw">m1:WorkplaceId</span>&gt;CATS&lt;/<span class="kw">m1:WorkplaceId</span>&gt;</span>
<span id="cb2-14"><a href="#cb2-14" aria-hidden="true" tabindex="-1"></a>            &lt;/<span class="kw">m0:Context</span>&gt;</span>
<span id="cb2-15"><a href="#cb2-15" aria-hidden="true" tabindex="-1"></a>            &lt;<span class="kw">m2:X509Certificate</span>&gt;MIICsTCCAligAwIBAgIHA61I5ACUjTAKBggqhkjOPQQDAjCBhDELMAkGA1UEBhMCREUxHzAdBgNV</span>
<span id="cb2-16"><a href="#cb2-16" aria-hidden="true" tabindex="-1"></a>BAoMFmdlbWF0aWsgR21iSCBOT1QtVkFMSUQxMjAwBgNVBAsMKUtvbXBvbmVudGVuLUNBIGRlciBU</span>
<span id="cb2-17"><a href="#cb2-17" aria-hidden="true" tabindex="-1"></a>ZWxlbWF0aWtpbmZyYXN0cnVrdHVyMSAwHgYDVQQDDBdHRU0uS09NUC1DQTEwIFRFU1QtT05MWTAe</span>
<span id="cb2-18"><a href="#cb2-18" aria-hidden="true" tabindex="-1"></a>Fw0yMDA4MDQwMDAwMDBaFw0yNTA4MDQyMzU5NTlaMEkxCzAJBgNVBAYTAkRFMSYwJAYDVQQKDB1n</span>
<span id="cb2-19"><a href="#cb2-19" aria-hidden="true" tabindex="-1"></a>ZW1hdGlrIFRFU1QtT05MWSAtIE5PVC1WQUxJRDESMBAGA1UEAwwJSURQIFNpZyAxMFowFAYHKoZI</span>
<span id="cb2-20"><a href="#cb2-20" aria-hidden="true" tabindex="-1"></a>zj0CAQYJKyQDAwIIAQEHA0IABJZQrG1NWxIB3kz/6Z2zojlkJqN3vJXZ3EZnJ6JXTXw5ZDFZ5Xjw</span>
<span id="cb2-21"><a href="#cb2-21" aria-hidden="true" tabindex="-1"></a>Wmtgfomv3VOV7qzI5ycUSJysMWDEu3mqRcajge0wgeowHQYDVR0OBBYEFJ8DVLAZWT+BlojTD4MT</span>
<span id="cb2-22"><a href="#cb2-22" aria-hidden="true" tabindex="-1"></a>/Na+ES8YMDgGCCsGAQUFBwEBBCwwKjAoBggrBgEFBQcwAYYcaHR0cDovL2VoY2EuZ2VtYXRpay5k</span>
<span id="cb2-23"><a href="#cb2-23" aria-hidden="true" tabindex="-1"></a>ZS9vY3NwLzAMBgNVHRMBAf8EAjAAMCEGA1UdIAQaMBgwCgYIKoIUAEwEgUswCgYIKoIUAEwEgSMw</span>
<span id="cb2-24"><a href="#cb2-24" aria-hidden="true" tabindex="-1"></a>HwYDVR0jBBgwFoAUKPD45qnId8xDRduartc6g6wOD6gwLQYFKyQIAwMEJDAiMCAwHjAcMBowDAwK</span>
<span id="cb2-25"><a href="#cb2-25" aria-hidden="true" tabindex="-1"></a>SURQLURpZW5zdDAKBggqghQATASCBDAOBgNVHQ8BAf8EBAMCB4AwCgYIKoZIzj0EAwIDRwAwRAIg</span>
<span id="cb2-26"><a href="#cb2-26" aria-hidden="true" tabindex="-1"></a>VBPhAwyX8HAVH0O0b3+VazpBAWkQNjkEVRkv+EYX1e8CIFdn4O+nivM+XVi9xiKK4dW1R7MD334O</span>
<span id="cb2-27"><a href="#cb2-27" aria-hidden="true" tabindex="-1"></a>pOPTFjeEhIVV&lt;/<span class="kw">m2:X509Certificate</span>&gt;</span>
<span id="cb2-28"><a href="#cb2-28" aria-hidden="true" tabindex="-1"></a>        &lt;/<span class="kw">m:VerifyCertificate</span>&gt;</span>
<span id="cb2-29"><a href="#cb2-29" aria-hidden="true" tabindex="-1"></a>    &lt;/<span class="kw">SOAP-ENV:Body</span>&gt;</span>
<span id="cb2-30"><a href="#cb2-30" aria-hidden="true" tabindex="-1"></a>&lt;/<span class="kw">SOAP-ENV:Envelope</span>&gt;</span></code></pre></div>
<div class="note">
<p>Das zu prüfende Zertifikat in Base64-DER-Codierung ist mit
<code>&lt;m2:X509Certificate&gt;&lt;/m2:X509Certificate&gt;</code>
identifiziert.</p>
</div></td>
</tr>
</tbody>
</table>

**Response**

    HTTP/1.1 200 OK
    Content-Type: text/xml;charset=utf-8
    <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
        <SOAP-ENV:Header/>
        <SOAP-ENV:Body>
            <ns4:VerifyCertificateResponse xmlns:ns2="http://ws.gematik.de/conn/ConnectorCommon/v5.0"
                xmlns:ns3="http://ws.gematik.de/tel/error/v2.0"
                xmlns:ns4="http://ws.gematik.de/conn/CertificateService/v6.0">
                <ns2:Status>
                    <ns2:Result>OK</ns2:Result>
                </ns2:Status>
                <ns4:VerificationStatus>
                    <ns4:VerificationResult>VALID</ns4:VerificationResult>
                    </ns4:VerificationStatus>
                    <ns4:RoleList>
                        <ns4:Role>1.2.276.0.76.4.260</ns4:Role>
                    </ns4:RoleList>
                </ns4:VerifyCertificateResponse>
            </SOAP-ENV:Body>
        </SOAP-ENV:Envelope>

In `<ns4:VerificationResult></ns4:VerificationResult>` wird das
Prüfergebnis des Zertifikats \[VALID = gültig, INCONCLUSIVE =
offline-gültig ohne Sperrstatus, INVALID = ungültig\] angegeben

in `<ns4:Role>VALID</<ns4:Role>` ist die technische Rolle hinterlegt,
wie im Zertifikat angegeben.

Aufgrund der im Feld befindlichen unterschiedlichen Konnektorversionen
ist ggfs. nicht in allen Installationen die aktuell gültige Liste der
OIDs gemäß gemSpec\_OID bekannt. Daher kann es vorkommen, dass einige
Konnektorversionen die Zertifikate als ungültig betrachten. Die gematik
arbeitet an einer Lösung, die Primärsystemen die Implementierung des
PKI-Stacks in einer Übergangsphase erspart.

Die Gültigkeitsprüfung von ECC-Zertifikaten unterstützt der Konnektor
erst in der Version PTV4 ("ePA 1.0").

### Signatur mit SMC-B erzeugen (external\_authenticate)

Das vom IDP bereitgestellte Challenge-Token muss mit der AUT-Identität
der SMC-B signiert werden. Das Primärsystem berechnet den Hashwert der
Challenge im vom IDP vorgegebenen SHA-256-Verfahren und ruft für diesen
Hashwert die Konnektor-Operation `ExternalAuthenticate` auf.  
Für das obige Challenge-Beispiel ergibt sich der folgende SHA-256-Wert:
`dd775a30757431a62bbe12301898511f5d9d5145a58dbd5d6cbae2481b36993f` in
HEX-Darstellung, welcher dann Base64-codiert werden muss (ergibt
`3XdaMHV0MaYrvhIwGJhRH12dUUWljb1dbLriSBs2mT8=`).

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
SOAPAction: &quot;http://ws.gematik.de/conn/SignatureService/v7.4#ExternalAuthenticate&quot;</code></pre></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>Payload</strong></p></td>
<td style="text-align: left;"><div class="sourceCode" id="cb2"><pre
class="sourceCode xml"><code class="sourceCode xml"><span id="cb2-1"><a href="#cb2-1" aria-hidden="true" tabindex="-1"></a>&lt;<span class="kw">soap-env:Envelope</span><span class="ot"> xmlns:soap-env=</span><span class="st">&quot;http://schemas.xmlsoap.org/soap/envelope/&quot;</span>&gt;</span>
<span id="cb2-2"><a href="#cb2-2" aria-hidden="true" tabindex="-1"></a>    &lt;<span class="kw">soap-env:Body</span>&gt;</span>
<span id="cb2-3"><a href="#cb2-3" aria-hidden="true" tabindex="-1"></a>        &lt;<span class="kw">ns0:ExternalAuthenticate</span><span class="ot"> xmlns:ns0=</span><span class="st">&quot;http://ws.gematik.de/conn/SignatureService/v7.4&quot;</span>&gt;</span>
<span id="cb2-4"><a href="#cb2-4" aria-hidden="true" tabindex="-1"></a>            &lt;<span class="kw">ns1:CardHandle</span><span class="ot"> xmlns:ns1=</span><span class="st">&quot;http://ws.gematik.de/conn/ConnectorCommon/v5.0&quot;</span>&gt;smc-b_2&lt;/<span class="kw">ns1:CardHandle</span>&gt;</span>
<span id="cb2-5"><a href="#cb2-5" aria-hidden="true" tabindex="-1"></a>            &lt;<span class="kw">ns2:Context</span><span class="ot"> xmlns:ns2=</span><span class="st">&quot;http://ws.gematik.de/conn/ConnectorContext/v2.0&quot;</span>&gt;</span>
<span id="cb2-6"><a href="#cb2-6" aria-hidden="true" tabindex="-1"></a>                &lt;<span class="kw">ns3:MandantId</span><span class="ot"> xmlns:ns3=</span><span class="st">&quot;http://ws.gematik.de/conn/ConnectorCommon/v5.0&quot;</span>&gt;Mandant1&lt;/<span class="kw">ns3:MandantId</span>&gt;</span>
<span id="cb2-7"><a href="#cb2-7" aria-hidden="true" tabindex="-1"></a>                &lt;<span class="kw">ns4:ClientSystemId</span><span class="ot"> xmlns:ns4=</span><span class="st">&quot;http://ws.gematik.de/conn/ConnectorCommon/v5.0&quot;</span>&gt;myPVS&lt;/<span class="kw">ns4:ClientSystemId</span>&gt;</span>
<span id="cb2-8"><a href="#cb2-8" aria-hidden="true" tabindex="-1"></a>                &lt;<span class="kw">ns5:WorkplaceId</span><span class="ot"> xmlns:ns5=</span><span class="st">&quot;http://ws.gematik.de/conn/ConnectorCommon/v5.0&quot;</span>&gt;WP1&lt;/<span class="kw">ns5:WorkplaceId</span>&gt;</span>
<span id="cb2-9"><a href="#cb2-9" aria-hidden="true" tabindex="-1"></a>            &lt;/<span class="kw">ns2:Context</span>&gt;</span>
<span id="cb2-10"><a href="#cb2-10" aria-hidden="true" tabindex="-1"></a>            &lt;<span class="kw">ns0:BinaryString</span>&gt;</span>
<span id="cb2-11"><a href="#cb2-11" aria-hidden="true" tabindex="-1"></a>                &lt;<span class="kw">ns7:Base64Data</span><span class="ot"> xmlns:ns7=</span><span class="st">&quot;urn:oasis:names:tc:dss:1.0:core:schema&quot;</span>&gt;3XdaMHV0MaYrvhIwGJhRH12dUUWljb1dbLriSBs2mT8=&lt;/<span class="kw">ns7:Base64Data</span>&gt;</span>
<span id="cb2-12"><a href="#cb2-12" aria-hidden="true" tabindex="-1"></a>            &lt;/<span class="kw">ns0:BinaryString</span>&gt;</span>
<span id="cb2-13"><a href="#cb2-13" aria-hidden="true" tabindex="-1"></a>        &lt;/<span class="kw">ns0:ExternalAuthenticate</span>&gt;</span>
<span id="cb2-14"><a href="#cb2-14" aria-hidden="true" tabindex="-1"></a>    &lt;/<span class="kw">soap-env:Body</span>&gt;</span>
<span id="cb2-15"><a href="#cb2-15" aria-hidden="true" tabindex="-1"></a>&lt;/<span class="kw">soap-env:Envelope</span>&gt;</span></code></pre></div>
<div class="note">
<p>Entsprechend der Mandantenkonfiguration wird in
<code>&lt;ns1:CardHandle&gt;&lt;/ns1:CardHandle&gt;</code> die SMC-B
referenziert, welche der IDP authentifizieren soll.</p>
</div>
<div class="note">
<p>In <code>&lt;ns7:Base64Data&gt;&lt;/ns7:Base64Data&gt;</code>
befindet sich der zu signierende Hashwert zur Challenge
(Base64-Darstellung des Challengetoken, das zuvor vom IDP bezogen
wurde).</p>
</div></td>
</tr>
</tbody>
</table>

**Response**

    HTTP/1.1 200 OK
    Content-Type: text/xml;charset=utf-8
    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
        <soap:Body>
            <ns4:ExternalAuthenticateResponse xmlns="http://ws.gematik.de/conn/ConnectorCommon/v5.0"
                xmlns:ns2="http://ws.gematik.de/conn/ConnectorContext/v2.0"
                xmlns:ns3="urn:oasis:names:tc:dss:1.0:core:schema"
                xmlns:ns4="http://ws.gematik.de/conn/SignatureService/v7.4"
                xmlns:ns5="http://www.w3.org/2000/09/xmldsig#"
                xmlns:ns6="http://ws.gematik.de/tel/error/v2.0"
                xmlns:ns7="http://uri.etsi.org/01903/v1.3.2#"
                xmlns:ns8="http://ws.gematik.de/conn/CertificateServiceCommon/v2.0"
                xmlns:ns9="urn:oasis:names:tc:SAML:1.0:assertion"
                xmlns:ns10="http://www.w3.org/2001/04/xmlenc#"
                xmlns:ns11="http://uri.etsi.org/02231/v2#"
                xmlns:ns12="urn:oasis:names:tc:dss-x:1.0:profiles:verificationreport:schema#"
                xmlns:ns13="urn:oasis:names:tc:dss-x:1.0:profiles:SignaturePolicy:schema#"
                xmlns:ns14="urn:oasis:names:tc:SAML:2.0:assertion">
                <Status>
                    <Result>OK</Result>
                </Status>
                <ns3:SignatureObject>
                    <ns3:Base64Signature Type="urn:ietf:rfc:3447">iSCNtUJUaH3uameymaYdplnmn5iq6k90a8i/TvSRvYOjw3x7zXn6+74LoVDc1xWNplmy6fzZejoIZAPxAJ0wBGQWFbdpD6ZLdOqC+Cm3BXUEXHeW2swfI6KfUwfWj43pujBTdzYI6JYG08sL63fxuY9eeGndzuWCDvHQVK0bPPjxq0K/fHx+PFQ1DxuNr5jbDaCBKOegPvcPXOFBY8dRGW0fu/T8baEpm5ACNGmX3vIqC3SWsP7M1TcTbEwxh82vMc0iOkIVDa2LKJAk5H4gSBBAGJahsFD3N3fnKgdLr81HiEQaoIyb+uEIVvaemz8yQ59dAIv3Hrb0Em5k/faHDQ==</ns3:Base64Signature>
                </ns3:SignatureObject>
            </ns4:ExternalAuthenticateResponse>
        </soap:Body>
    </soap:Envelope>

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

`<ns3:Base64Signature></ns3:Base64Signature>` enthält die Signatur, die
mittels Konnektor und dem privaten Schlüssel der SMC-B erstellt wurde.

**Nutzung der Gesundheitskarte**  
Versicherte weisen sich gegenüber der Telematikinfrastruktur mit der
Identität der elektronischen Gesundheitskarte aus. Der Ablauf ist analog
zu dem oben ausgeführt Ablauf für Primärsysteme. Das E-Rezept-FdV
bündelt dabei (wie das Primärsystem) in Stufe 1 die E-Rezept-Fachlogik
und die Funktion des Authenticator-Moduls. Die Signatur der Challenge
erfolgt bei Nutzung der elektronischen Gesundheitskarte bspw. über die
NFC-Schnittstelle des Mobilgeräts. Dabei wird das Schlüsselmaterial
PRK.CH.AUT für Private-Key und C.CH.AUT für das Zertifikat inkl.
PublicKey verwendet.

# Verschlüsselter Transportkanal zur Vertrauenswürdigen Ausführungsumgebung ("VAU-Transport")

Der Einsatz moderner Transportverschlüsselung ab TLS 1.2 schützt vor der
Einsicht sensibler Daten beim Transport über das Internet. Dabei sind
sowohl die Daten des HTTP-Body als auch die aufgerufene URL und die
HTTP-Header verschlüsselt. In modernen Cloud-Infrastrukturen enden
solche TLS-Verbindungen meist an einem Internetgateway, müssen jedoch in
einer Serverinfrastruktur häufig zu dahinterliegenden Applicationservern
und -diensten weitertransportiert werden.

Um sensible Daten bis hinein in einen vertrauenswürdigen
Ausführungskontext verschlüsselt zu transportieren, erfolgt der Zugang
zum E-Rezept-Fachdienst mit einer zusätzlichen Transportverschlüsselung
für eine kryptografische Identität der vertrauenswürdigen
Ausführungsumgebung (VAU). Dabei werden die Daten des HTTP-Body für den
Verarbeitungskontext der VAU um einen symmetrischen Antwortschlüssel
ergänzt und anschließend asymmetrisch verschlüsselt. Dieser
verschlüsselte HTTP-Request wird dann mittels TLS transportverschlüsselt
an den E-Rezept-Fachdienst übergeben.

![width=80%](../images/api_vau_transport.png)

Das Diagramm inkl. der konkreten Ablaufbeschreibung befindet sich auch
im Spezifikationsdokument \[gemSpec\_Krypt\] in Kapitel 7.

-   <https://github.com/gematik/ref-erp-client-cs/>

-   <https://github.com/ere-health/architecture>

-   <https://github.com/ere-health/ere-ps-app>

-   <https://github.com/ere-health/front-end-ere.health>

-   <https://bitbucket.org/andreas_hallof/vau-protokoll/src/master/erp>

Die VAU des E-Rezept-Fachdienstes erzeugt eine HTTP-Response
entsprechend des Workflows im E-Rezept und verschlüsselt diese Response
symmetrisch mit dem vom Client bereitgestellten Antwortschlüssel. Die
verschlüsselte Response wird anschließend mittels TLS
transportverschlüsselt an den Client zurückgegeben.

Ein zusätzlich in den Aufrufen vom E-Rezept-Fachdienst generiertes,
wechselndes Nutzerpseudonym wirkt zusätzlich Überlastungsangriffen
entgegen, indem Aufrufe ohne Nutzerpseudonym mit einer geringeren
Priorität bearbeitet werden.

Die zusätzliche Verschlüsselung erfolgt mit dem AES-GCM-Verfahren, die
über ein AuthenticationTag am Ende des Bitstroms die Integrität des
transportierten Ciphertextes sicherstellt. Der AES-Schlüssel ergibt sich
zufällig aus der Ableitung über den öffentlichen ECC-Schlüssel des
VAU-ENC-Zertifikats. Sind der verwendete **Random** oder die **X**- und
**Y**-Koordinaten des ECC-Schlüssels dabei nicht exakt 32 Byte groß,
werden die Daten zwar korrekt verschlüsselt, aber das AuthenticationTag
passt am Ende nicht zum Ciphertext - der Fachdienst muss das dann gemäß
AES-Spezifikation als "manipuliert" ablehnen und antwortet mit einer
Fehlermeldung
`vau decryption failed: AesGcmException can't finalize AES-GCM decryption;`

Die folgenden beispielhaften Code-Zeilen prüfen auf eine exakte Länge:

    //sharedSecretBytes muss 32 Byte groß sein entweder vorn abschneiden oder mit 0 auffüllen
    if (sharedSecretBytes.Length > 32) {
        sharedSecretBytes = sharedSecretBytes.Skip(sharedSecretBytes.Length - 32).ToArray();
    } else if (sharedSecretBytes.Length < 32) {
        sharedSecretBytes = Enumerable.Repeat((byte) 0, 32 -
          sharedSecretBytes.Length).Concat(sharedSecretBytes).ToArray();
    }

Ein Java-Beispiel stellen wir in der folgenden Datei
[VAUClientCrypto.java^](../samples/snippets/VAUClientCrypto.java)
bereit, in der dieses Problem mit der Methode `pad32(byte[] input)`
behandelt wird.

## Kennzeichnung des verschlüsselten Inhalts für Routing

Der E-Rezept-Fachdienst benötigt eine Kennzeichnung im äußeren
http-Request, um den verschlüsselten Inhalt an den fachlich zuständigen
VAU-Kontext zu routen. Um eine Überlastung nutzerrollen- und
workflowspezifischer VAU-Kontexte zu vermeiden, werden die http-Header
`X-erp-user` und `X-erp-resource` genutzt. Die folgende Tabelle zeigt
die Belegung der Header zur Nutzung durch die entsprechenden
E-Rezept-Nutzer (in den Beispielen der verschiedenen UseCases sind die
jeweiligen Header-Belegungen für den äußeren http-Request angegeben):

<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p><strong>Leistungserbringer (PVS, AVS
,KIS)</strong></p></td>
<td style="text-align: left;"><p><strong>Versicherte
(E-Rezept-App)</strong></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><code>X-erp-user: l</code><br />
Dieser Header mit Wert "l" (kleines "L") signalisiert dem
E-Rezept-Fachdienst einen Zugriff durch Leistungserbringer</p></td>
<td style="text-align: left;"><p><code>X-erp-user: v</code><br />
Dieser Header mit Wert "v" (kleines "V") signalisiert dem
E-Rezept-Fachdienst einen Zugriff durch Versicherte</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><code>X-erp-resource: Task</code><br />
<code>X-erp-resource: Communication</code><br />
Der Header mit diesem Wert signalisiert den Zugriff auf eine bestimmte
FHIR-Ressource, z.B. Task. Es wird immer nur eine Ressource genannt, da
Zugriffe auch immer nur an eine Ressource adressiert werden. Hinweis:
Beim Zugriff auf das CapabilityStatement mit GET /metadata wird
entsprechend <code>X-erp-resource: metadata</code> angegeben. Die
Auswertung erfolgt <strong>Case-Sensitiv</strong></p></td>
<td style="text-align: left;"><p><code>X-erp-resource: Task</code><br />
<code>X-erp-resource: MedicationDispense</code><br />
<code>X-erp-resource: Communication</code><br />
<code>X-erp-resource: AuditEvent</code></p></td>
</tr>
</tbody>
</table>

## Verbindungsaufbau zum E-Rezept-Fachdienst

Zunächst muss das Verschlüsselungszertifikat der VAU vom
E-Rezept-Fachdienst abgerufen werden.

<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p><strong>URI</strong></p></td>
<td style="text-align: left;"><p><a
href="https://erp.zentral.erp.splitdns.ti-dienste.de/VAUCertificate">https://erp.zentral.erp.splitdns.ti-dienste.de/VAUCertificate</a></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>Method</strong></p></td>
<td style="text-align: left;"><p>GET</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>HTTP Header</strong></p></td>
<td style="text-align: left;"><p>X-erp-user: l</p>
<div class="note">
<p>Der Header <code>X-erp-user</code> signalisiert dem
E-Rezept-Fachdienst einen Zugriff aus der Leistungserbringerumgebung
[<code>l</code> - kleines "L"] (muss in jedem Header angegeben
werden).</p>
</div></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>Payload</strong></p></td>
<td style="text-align: left;"><pre><code>-</code></pre></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>Response</strong></p></td>
<td style="text-align: left;"><div class="sourceCode" id="cb2"><pre
class="sourceCode json"><code class="sourceCode json"><span id="cb2-1"><a href="#cb2-1" aria-hidden="true" tabindex="-1"></a><span class="er">HTTP/1.1</span> <span class="er">200</span> <span class="er">OK</span></span>
<span id="cb2-2"><a href="#cb2-2" aria-hidden="true" tabindex="-1"></a><span class="er">Content-Type:</span> <span class="er">application/pkix-cert</span></span>
<span id="cb2-3"><a href="#cb2-3" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb2-4"><a href="#cb2-4" aria-hidden="true" tabindex="-1"></a><span class="er">1100110001111111000000011011000010100111100001111000010010111001...</span></span></code></pre></div></td>
</tr>
</tbody>
</table>

Der E-Rezept-Fachdienst stellt zusätzlich eine frische OCSP-Response für
die erweiterte Prüfung des Verschlüsselungszertifikats bereit.

<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p><strong>URI</strong></p></td>
<td style="text-align: left;"><p><a
href="https://erp.zentral.erp.splitdns.ti-dienste.de/VAUCertificateOCSPResponse">https://erp.zentral.erp.splitdns.ti-dienste.de/VAUCertificateOCSPResponse</a></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>Method</strong></p></td>
<td style="text-align: left;"><p>GET</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>HTTP Header</strong></p></td>
<td style="text-align: left;"><p>X-erp-user: l</p>
<div class="note">
<p>Der Header <code>X-erp-user</code> signalisiert dem
E-Rezept-Fachdienst einen Zugriff aus der Leistungserbringerumgebung
[<code>l</code> - kleines "L"] (muss in jedem Header angegeben
werden).</p>
</div></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>Payload</strong></p></td>
<td style="text-align: left;"><pre><code>-</code></pre></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>Response</strong></p></td>
<td style="text-align: left;"><div class="sourceCode" id="cb2"><pre
class="sourceCode json"><code class="sourceCode json"><span id="cb2-1"><a href="#cb2-1" aria-hidden="true" tabindex="-1"></a><span class="er">HTTP/1.1</span> <span class="er">200</span> <span class="er">OK</span></span>
<span id="cb2-2"><a href="#cb2-2" aria-hidden="true" tabindex="-1"></a><span class="er">Content-Type:</span> <span class="er">application/ocsp-response</span></span>
<span id="cb2-3"><a href="#cb2-3" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb2-4"><a href="#cb2-4" aria-hidden="true" tabindex="-1"></a><span class="er">100100100110001011110001110111011000110000101111101100100111011...</span></span></code></pre></div></td>
</tr>
</tbody>
</table>

## Request versenden

Für den verschlüsselten VAU-Transport wird der zu transportierende
HTTP-Request für die VAU in mehreren Schritten aufbereitet. Als Beispiel
wird im Folgenden die Abfrage aller E-Rezepte eines Versicherten
verwendet.

    GET /Task HTTP/1.1
    Host: erp.zentral.erp.splitdns.ti-dienste.de
    Authorization: Bearer eyJraWQ.ewogImL2pA10Qql22ddtutrvx4FsDlz.rHQjEmB1lLmpqn9J
    User-Agent: E-Rezept FdV/1.0.0 gematik GmbH/GEMxxxxxxxxxxxxxxxxx
    Accept: application/fhir+json;charset=utf-8

Der zu verschlüsselnde http-Request muss vollständig und syntaktisch
korrekt gemäß [RFC-2616](https://datatracker.ietf.org/doc/html/rfc2616)
erstellt werden (d.h. inkl. aller verpflichtenden http-Header und ggfs.
http-Body *new line*-getrennt).

Zunächst müssen im Client eine zufällige Request-ID (z.B.
`b69f01734f34376ddcdbdbe9af18a06f`) und ein symmetrischer
Antwortschlüssel (z.B. `16bac90134c635e4ec85fae0e4885d9f`) generiert
werden.  
Als nächstes wird die folgende leerzeichengetrennte Zeichenkette `p` für
die anschließende Verschlüsselung gebildet:
`p="1" + " " + ACCESS_TOKEN + " " + Request-ID + " " + Antwortschlüssel + " " + HTTP-Request`,
mit obigem Beispiel ergibt sich für `p`:

    "1 eyJraWQ.ewogImL2pA10Qql22ddtutrvx4FsDlz.rHQjEmB1lLmpqn9J b69f01734f34376ddcdbdbe9af18a06f 16bac90134c635e4ec85fae0e4885d9f GET /Task HTTP/1.1
    Host: erp.zentral.erp.splitdns.ti-dienste.de
    Authorization: Bearer eyJraWQ.ewogImL2pA10Qql22ddtutrvx4FsDlz.rHQjEmB1lLmpqn9J
    User-Agent: E-Rezept FdV/1.0.0 gematik GmbH/GEMxxxxxxxxxxxxxxxxx
    Accept: application/fhir+json;charset=utf-8"

Diese Zeichenkette wird nun mit dem ECIES-Verfahrens \[SEC1-2009\] und
dem öffentlichen Schlüssel aus dem zuvor abgerufenen
Verschlüsselungszertifikat der VAU hybrid verschlüsselt. Sei
`1101110011011110000101101000111000010101100110111011111100011111111110001101110010011010010110000101000001011000000100`
ein unvollständiges Beispiel für das Ergebnis der
Verschlüsselungsoperation. Dieses wird nun als Payload im HTTP-Body des
folgenden Requests an den E-Rezept-Fachdienst übergeben.

<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p><strong>URI</strong></p></td>
<td style="text-align: left;"><p><a
href="https://erp.zentral.erp.splitdns.ti-dienste.de/VAU/0">https://erp.zentral.erp.splitdns.ti-dienste.de/VAU/0</a></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>Method</strong></p></td>
<td style="text-align: left;"><p>POST</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>HTTP Header</strong></p></td>
<td
style="text-align: left;"><p><code>Content-Type: application/octet-stream</code><br />
X-erp-user: l</p>
<div class="note">
<p>Der Header <code>X-erp-user</code> signalisiert dem
E-Rezept-Fachdienst einen Zugriff aus der Leistungserbringerumgebung
[<code>l</code> - kleines "L"] (muss in jedem Header angegeben
werden).</p>
</div></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>HTTP Body</strong></p></td>
<td
style="text-align: left;"><p><code>1101110011011110000101101000111000010101100110111011111100011111111110001101110010011010010110000101000001011000000100</code></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>Response</strong></p></td>
<td style="text-align: left;"><div class="sourceCode" id="cb1"><pre
class="sourceCode json"><code class="sourceCode json"><span id="cb1-1"><a href="#cb1-1" aria-hidden="true" tabindex="-1"></a><span class="er">HTTP/1.1</span> <span class="er">200</span> <span class="er">OK</span></span>
<span id="cb1-2"><a href="#cb1-2" aria-hidden="true" tabindex="-1"></a><span class="er">Content-Type:</span> <span class="er">application/octet-stream</span></span>
<span id="cb1-3"><a href="#cb1-3" aria-hidden="true" tabindex="-1"></a><span class="er">Userpseudonym:</span> <span class="er">5a049a2c1654e685247e2d20136445d9-632f841a029564ce000f29675d192513</span></span>
<span id="cb1-4"><a href="#cb1-4" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb1-5"><a href="#cb1-5" aria-hidden="true" tabindex="-1"></a><span class="er">001111101111100110001001001111010110010010111110101100100011110...</span></span></code></pre></div></td>
</tr>
</tbody>
</table>

Die `0` am Ende der URL des Requests steht für ein (dem Client nicht
bekanntes) Nutzerpseudonym, nach der ersten Antwort der VAU des
E-Rezept-Fachdienstes kann das vom Fachdienst mitgeteilte
`Userpseudonym`
`5a049a2c1654e685247e2d20136445d9-632f841a029564ce000f29675d192513`
anstelle der `0` verwendet werden, um Folgezugriffe höher zu
priorisieren.

## Response verarbeiten

Nach dem erfolgreichen Abschluss der Bearbeitung des Requests durch die
VAU des E-Rezept-Fachdienstes erhält der Client die verschlüsselte
HTTP-Response der VAU in einer äußeren "VAU-Transport"-HTTP-Response.
Der HTTP-Statuscode 200 signalisiert dabei die korrekte Verarbeitung und
Erstellung der verschlüsselten Antwort. Die innere HTTP-Response des
fachlichen Ergebnisses aus der VAU kann dabei einen abweichenden
HTTP-Statuscode beinhalten, wenn aufgrund der Daten oder Verarbeitung
innerhalb der VAU Fehlerzustände eintreten oder ungültige Daten
übergeben wurden. Sei
`001111101111100110001001001111010110010010111110101100100011110...` die
verschlüsselte Response zum obigen Beispiel. Die Entschlüsselung mit dem
für den Request generierten Antwortschlüssel
\`16bac90134c635e4ec85fae0e4885d9f\`mittels AES-GCM liefert die innere
HTTP-Response der VAU als leerzeichengetrennte Zeichenkette:

    1 b69f01734f34376ddcdbdbe9af18a06f HTTP/1.1 200 OK
    Content-Type: application/fhir+json;charset=utf-8
    Content-Location: https://erp.zentral.erp.splitdns.ti-dienste.de/Bundle/f5ba6eaf-9052-42f6-ac4e-fadceed7293b

    {
      "resourceType": "Bundle",
      "id": "f5ba6eaf-9052-42f6-ac4e-fadceed7293b",
      "meta": {
        "lastUpdated": "2020-03-01T07:02:37.836+00:00"
      },
      "type": "searchset",
      "total": 2,
      "link": [{
        "relation": "self",
        "url": "https://erp.zentral.erp.splitdns.ti-dienste.de/Task/"
      }],
      "entry": [{
        "fullUrl": "https://erp.zentral.erp.splitdns.ti-dienste.de/Task/160.123.456.789.123.58",
        "resource": {
          "resourceType": "Task",
          "id":"160.123.456.789.123.58",
          "meta": {
            "profile":  [
                "https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_PR_Task"
            ]
          },
          "extension":  [{
            "url": "https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_EX_PrescriptionType",
            "valueCoding": {
              "system": "https://gematik.de/fhir/erp/CodeSystem/GEM_ERP_CS_FlowType",
              "code": "160",
              "display": "Muster 16 (Apothekenpflichtige Arzneimittel)"
            }
          }, {
            "url": "https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_EX_AcceptDate",
            "valueDateTime": "2020-03-02T08:25:05+00:00"
          }, {
            "url": "https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_EX_ExpiryDate",
            "valueDateTime": "2020-05-02T08:25:05+00:00"
          }],
          "identifier":  [{
            "system": "https://gematik.de/fhir/erp/NamingSystem/GEM_ERP_NS_PrescriptionId",
            "value": "160.123.456.789.123.58"
          }, {
            "system": "https://gematik.de/fhir/erp/NamingSystem/GEM_ERP_NS_AccessCode",
            "value": "777bea0e13cc9c42ceec14aec3ddee2263325dc2c6c699db115f58fe423607ea"
          }, {
            "system": "https://gematik.de/fhir/erp/NamingSystem/GEM_ERP_NS_Secret",
            "value": "c36ca26502892b371d252c99b496e31505ff449aca9bc69e231c58148f6233cf"
          }],
          "status": "in-progress",
          "intent": "order",
          "for": {
            "identifier": {
              "system": "http://fhir.de/sid/gkv/kvid-10",
              "value": "X123456789"
            }
          },
          "authoredOn": "2020-03-02T08:25:05+00:00",
          "lastModified": "2020-03-02T08:45:05+00:00",
          "performerType":  [{
            "coding":  [{
              "system": "urn:ietf:rfc:3986",
              "code": "urn:oid:1.2.276.0.76.4.54",
              "display": "Öffentliche Apotheke"
            }]
          }],
          "input":  [{
            "type": {
              "coding":  [{
                "system": "https://gematik.de/fhir/erp/CodeSystem/GEM_ERP_CS_DocumentType",
                "code": "1",
                "display": "Health Care Provider Prescription"
              }]
            },
            "valueReference": {
              "reference": "Bundle/KbvPrescriptionExample"
            }
          }]
        },
        "search": {
          "mode": "match"
        }
      }]
    }

Die innere HTTP-Response hat die folgende Struktur "1" + " " +
ursprüngliche-Request-ID + " " + Response-Header-und-Body

Ein Splitten der inneren Struktur anhand des Leerzeichens " " könnte
dazu führen, dass auch der Payload im inneren HTTP-Response-Body
zerstückelt wird. Robuster ist das Prüfen auf Vorhandensein der
ursprünglichen Request-ID und anschließendes Entfernen des von der VAU
hinzugefügten Präfixes `"1" + " " + ursprüngliche-Request-ID + " "`. Nun
kann die innere HTTP-Response standardgemäß weiterverarbeitet werden.
