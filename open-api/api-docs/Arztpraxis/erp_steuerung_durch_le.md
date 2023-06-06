Hier dokumentiert die gematik die Nutzung der Schnittstellen rund um das
E-Rezept Feature "Workflow-Steuerung durch Leistungserbringer". Hierbei
handelt es sich um eine besondere Versorgungssituation, bei der ein
E-Rezept direkt vom verordnenden Leistungserbringer an die abgebende
Apotheke zugewiesen und übermittelt werden kann. Der wesentliche
Unterschied gegenüber der bisherigen Prozessdefinition für den
Workflowtype 160 (bzw. 200 für PKV) besteht in der Übergabe der
Einlöseinformationen an die Apotheke durch den verordnenden
Leistungserbringer.

Für diesen Workflow wird das gleiche Datenmodell, wie für Workflow 160
genutzt. Ebenso wird das gleiche Datenmodell für den
Verordnungsdatensatz der KBV verwendet. Es werden lediglich je ein neuer
Flowtype für GKV `169` und PKV `209` zur Erkennung des abweichenden
Prozessablaufs und zur Nutzung in der Berechnung der Rezept-ID
eingeführt.

# Profilierung

Für diesen Anwendungsfall wird die FHIR-Resource "Task" profiliert. Das
Profil kann als JSON oder XML hier eingesehen werden:
<https://simplifier.net/erezept-workflow/gem_erp_pr_task>.

Die für diese Anwendung wichtigen Attribute und Besonderheiten durch die
Profilierung der Ressourcen werden durch das "must be supported"-Flag
gekennzeichnet. Sie werden in der folgenden Tabelle kurz
zusammengefasst:

<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p><strong>Name</strong></p></td>
<td style="text-align: left;"><p><strong>Beschreibung</strong></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>identifier:PrescriptionID</p></td>
<td style="text-align: left;"><p>Rezept-ID; eindeutig für jedes
Rezept</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>identifier:AccessCode</p></td>
<td style="text-align: left;"><p>Vom E-Rezept-Fachdienst generierter
Berechtigungs-Code</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>identifier:Secret</p></td>
<td style="text-align: left;"><p>Vom E-Rezept-Fachdienst generierter
Berechtigungs-Code</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>status</p></td>
<td style="text-align: left;"><p>Status des E-Rezepts</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>intent</p></td>
<td style="text-align: left;"><p>Intension des Tasks. Fixer
Wert="order"</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>for</p></td>
<td style="text-align: left;"><p>Krankenversichertennummer</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>authoredOn</p></td>
<td style="text-align: left;"><p>Erstellungszeitpunkt des Tasks</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>lastModified</p></td>
<td style="text-align: left;"><p>Letzte Änderung am Task</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>performerType</p></td>
<td style="text-align: left;"><p>Institution, in der das Rezept
eingelöst werden soll</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>input</p></td>
<td style="text-align: left;"><p>Verweis auf das für den Patient und den
Leistungserbringer erstellten Bundle</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>output</p></td>
<td style="text-align: left;"><p>Verweis auf das
Quittungs-Bundle</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>extension:flowType</p></td>
<td style="text-align: left;"><p>Gibt den Typ des Rezeptes an</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>extension:expiryDate</p></td>
<td style="text-align: left;"><p>Verfallsdatum</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>extension:acceptDate</p></td>
<td style="text-align: left;"><p>Datum, bis zu welchem die Krankenkasse
spätestens die Kosten übernimmt</p></td>
</tr>
</tbody>
</table>

In den folgenden Kapiteln wird erläutert, wann und wie die Befüllung
dieser Attribute erfolgt.

# Anwendungsfall Workflow 169 (209) durch Verordnenden erzeugen

Ein Leistungserbringer will mit seinem Primärsystem ein E-Rezept für den
Workflow 169 (209) erzeugen. Hierfür erstellt das Primärsystem ein
FHIR-Bundle gemäß der KBV-Profilierung des E-Rezepts (siehe
<https://simplifier.net/erezept>) mit workflowspezifischen Parametern.
Für die Bereitstellung an den Versicherten wird auf dem
E-Rezept-Fachdienst ein Task erstellt, dessen Identifier als Rezept-ID
in das FHIR-Bundle eingebettet wird. Nach der qualifizierten
elektronischen Signatur des Bundles wird dieses im Task ergänzt und der
Workflow des E-Rezepts mit der Aktivierung des Tasks gestartet.

Der Aufruf erfolgt als http-`POST`-Operation. Im Aufruf muss das während
der Authentisierung erhaltene ACCESS\_TOKEN im http-Request-Header
`Authorization` übergeben werden. Im http-RequestBody MUSS der
Konfigurationsparameter des Workflows `flowType` übergeben werden. Der
E-Rezept-Fachdienst speichert den Task unter einer generierten ID,
welche im Response-Header `Location` zurückgemeldet wird und zusätzlich
ist im http-ResponseBody des Task der serverseitig generierte AccessCode
als Identifier enthalten.

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
href="https://erp.zentral.erp.splitdns.ti-dienste.de/Task/$create">https://erp.zentral.erp.splitdns.ti-dienste.de/Task/$create</a></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>Method</strong></p></td>
<td style="text-align: left;"><p>POST</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>HTTP Header</strong></p></td>
<td style="text-align: left;"><pre><code>Content-Type: application/fhir+xml; charset=UTF-8
Authorization: Bearer eyJraWQ.ewogImL2pA10Qql22ddtutrvx4FsDlz.rHQjEmB1lLmpqn9J</code></pre>
<div class="note">
<p>Mit dem ACCESS_TOKEN im <code>Authorization</code>-Header weist sich
der Zugreifende als Leistungserbringer aus, im Token ist seine Rolle
enthalten. Die Base64-Darstellung des Tokens ist stark gekürzt.</p>
</div>
<div class="note">
<p>Im http-Header des äußeren http-Requests an die VAU (POST /VAU) sind
die Header <code>X-erp-user: l</code> und
<code>X-erp-resource: Task</code> zu setzen.</p>
</div></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>Payload</strong></p></td>
<td style="text-align: left;"><div class="sourceCode" id="cb2"><pre
class="sourceCode xml"><code class="sourceCode xml"><span id="cb2-1"><a href="#cb2-1" aria-hidden="true" tabindex="-1"></a>&lt;<span class="kw">Parameters</span><span class="ot"> xmlns=</span><span class="st">&quot;http://hl7.org/fhir&quot;</span>&gt;</span>
<span id="cb2-2"><a href="#cb2-2" aria-hidden="true" tabindex="-1"></a>    &lt;<span class="kw">parameter</span>&gt;</span>
<span id="cb2-3"><a href="#cb2-3" aria-hidden="true" tabindex="-1"></a>        &lt;<span class="kw">name</span><span class="ot"> value=</span><span class="st">&quot;workflowType&quot;</span>/&gt;</span>
<span id="cb2-4"><a href="#cb2-4" aria-hidden="true" tabindex="-1"></a>        &lt;<span class="kw">valueCoding</span>&gt;</span>
<span id="cb2-5"><a href="#cb2-5" aria-hidden="true" tabindex="-1"></a>            &lt;<span class="kw">system</span><span class="ot"> value=</span><span class="st">&quot;https://gematik.de/fhir/erp/CodeSystem/GEM_ERP_CS_FlowType&quot;</span>/&gt;</span>
<span id="cb2-6"><a href="#cb2-6" aria-hidden="true" tabindex="-1"></a>            &lt;<span class="kw">code</span><span class="ot"> value=</span><span class="st">&quot;169&quot;</span>/&gt;</span>
<span id="cb2-7"><a href="#cb2-7" aria-hidden="true" tabindex="-1"></a>        &lt;/<span class="kw">valueCoding</span>&gt;</span>
<span id="cb2-8"><a href="#cb2-8" aria-hidden="true" tabindex="-1"></a>    &lt;/<span class="kw">parameter</span>&gt;</span>
<span id="cb2-9"><a href="#cb2-9" aria-hidden="true" tabindex="-1"></a>&lt;/<span class="kw">Parameters</span>&gt;</span></code></pre></div>
<p>Der Parameter <code>&lt;code value="169"/&gt;</code> steuert den Typ
des dem Task zugrunde liegenden Workflows. In diesem Fall obliegt die
Einlösehoheit (als Zuweisung an eine bestimmte Apotheke) beim
Verordnenden Leistungserbringer.</p></td>
</tr>
</tbody>
</table>

**Response**

    HTTP/1.1 201 Created
    Content-Type: application/fhir+xml; charset=UTF-8

    <Task xmlns="http://hl7.org/fhir">
        <id value="169.000.004.839.514.95"/>
        <meta>
            <profile value="https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_PR_Task|1.2"/>
        </meta>
        <extension url="https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_EX_PrescriptionType">
            <valueCoding>
                <system value="https://gematik.de/fhir/erp/CodeSystem/GEM_ERP_CS_FlowType" />
                <code value="169" />
                <display value="Muster 16 (Direkte Zuweisung)" />
            </valueCoding>
        </extension>
        <extension url="https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_EX_AcceptDate">
            <valueDate value="2022-06-30" />
        </extension>
        <extension url="https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_EX_ExpiryDate">
            <valueDate value="2022-06-30" />
        </extension>
        <identifier>
            <system value="https://gematik.de/fhir/erp/NamingSystem/GEM_ERP_NS_PrescriptionId" />
            <value value="169.000.004.839.514.95" />
        </identifier>
        <identifier>
            <system value="https://gematik.de/fhir/erp/NamingSystem/GEM_ERP_NS_AccessCode" />
            <value value="777bea0e13cc9c42ceec14aec3ddee2263325dc2c6c699db115f58fe423607ea" />
        </identifier>
        <status value="draft" />
        <intent value="order" />
        <authoredOn value="2022-03-18T15:26:00+00:00" />
        <performerType>
            <coding>
                <system value="urn:ietf:rfc:3986" />
                <code value="urn:oid:1.2.276.0.76.4.54" />
                <display value="Öffentliche Apotheke" />
            </coding>
        </performerType>
    </Task>

An der Stelle `<code value="169" />` hat der E-Rezept-Fachdienst den
Übergabeparameter zur Konfiguration des des Workflows übernommen.

Der Identifier in `<value value="169.000.004.839.514.95" />` stellt die
10 Jahre lang eineindeutige Rezept-ID dar.

Im Parameter
`<value value="777bea0e13cc9c42ceec14aec3ddee2263325dc2c6c699db115f58fe423607ea" />`
befindet sich der serverseitig generierte `AccessCode`, der für
nachfolgende Zugriffe auf diesen Task in einem http-Request für die
Berechtigungsprüfung mitgegeben werden muss.

Der Wert `<code value="urn:oid:1.2.276.0.76.4.54" />` entspricht dem
intendierten Institutionstyp, in welchen der Versicherte für die
Einlösung des Rezepts gelenkt werden soll

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
<td style="text-align: left;"><p>201</p></td>
<td style="text-align: left;"><pre><code> Created +
[small]#Die Anfrage wurde erfolgreich bearbeitet. Die angeforderte Ressource wurde vor dem Senden der Antwort erstellt. Das `Location`-Header-Feld enthält die Adresse der erstellten Ressource.#</code></pre></td>
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
<tr class="odd">
<td style="text-align: left;"><p>401</p></td>
<td style="text-align: left;"><p>Unauthorized<br />
<span class="small">Die Anfrage kann nicht ohne gültige
Authentifizierung durchgeführt werden. Wie die Authentifizierung
durchgeführt werden soll, wird im "WWW-Authenticate"-Header-Feld der
Antwort übermittelt.</span></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>403</p></td>
<td style="text-align: left;"><p>Forbidden<br />
<span class="small">Die Anfrage wurde mangels Berechtigung des Clients
nicht durchgeführt, bspw. weil der authentifizierte Benutzer nicht
berechtigt ist.</span></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>405</p></td>
<td style="text-align: left;"><p>Method Not Allowed<br />
<span class="small">Die Anfrage darf nur mit anderen HTTP-Methoden (zum
Beispiel GET statt POST) gestellt werden. Gültige Methoden für die
betreffende Ressource werden im "Allow"-Header-Feld der Antwort
übermittelt.</span></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>408</p></td>
<td style="text-align: left;"><p>Request Timeout<br />
<span class="small">Innerhalb der vom Server erlaubten Zeitspanne wurde
keine vollständige Anfrage des Clients empfangen.</span></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>429</p></td>
<td style="text-align: left;"><p>Too Many Requests<br />
<span class="small">Der Client hat zu viele Anfragen in einem bestimmten
Zeitraum gesendet.</span></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>500</p></td>
<td style="text-align: left;"><p>Server Errors<br />
<span class="small">Unerwarteter Serverfehler</span></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>512</p></td>
<td style="text-align: left;"><p>OCSP Backend Error<br />
<span class="small">Innerhalb der vom Server erlaubten Zeitspanne wurde
keine gültige Antwort des OCSP-Responders geliefert.</span></p></td>
</tr>
</tbody>
</table>

# Anwendungsfall E-Rezept durch Verordnenden einstellen

Nach der erfolgreichen qualifizierten Signatur kann nun der Task im
Fachdienst aktiviert werden, indem das Ergebnis der erfolgreichen
QES-Erstellung als Base64-codierter Datensatz an den E-Rezept-Fachdienst
geschickt wird.

Der Aufruf erfolgt als http-`POST`-Operation auf die FHIR-Opertation
`$activate` des referenziereten Tasks. Im Aufruf muss das während der
Authentisierung erhaltene ACCESS\_TOKEN im http-Request-Header
`Authorization` und der beim Erzeugen des Tasks generierte `AccessCode`
übergeben werden. Im http-RequestBody muss das codierte, QES-signierte
E-Rezept enthalten sein. Der E-Rezept-Fachdienst aktualisiert bei
gültiger QES den Task und erzeugt eine Signatur über den Datensatz, die
als signierte Kopie des KBV-`Bundle` für den Abruf durch den
Versicherten gespeichert wird.

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
href="https://erp.zentral.erp.splitdns.ti-dienste.de/Task/169.000.004.839.514.95/$activate">https://erp.zentral.erp.splitdns.ti-dienste.de/Task/169.000.004.839.514.95/$activate</a></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>Method</strong></p></td>
<td style="text-align: left;"><p>POST</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>HTTP Header</strong></p></td>
<td style="text-align: left;"><pre><code>Content-Type: application/fhir+xml; charset=UTF-8
X-AccessCode: 777bea0e13cc9c42ceec14aec3ddee2263325dc2c6c699db115f58fe423607ea
Authorization: Bearer eyJraWQ.ewogImL2pA10Qql22ddtutrvx4FsDlz.rHQjEmB1lLmpqn9J</code></pre>
<div class="note">
<p>Im http-Header des äußeren http-Requests an die VAU (POST /VAU) sind
die Header <code>X-erp-user: l</code> und
<code>X-erp-resource: Task</code> zu setzen.</p>
</div></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>Payload</strong></p></td>
<td style="text-align: left;"><div class="sourceCode" id="cb2"><pre
class="sourceCode xml"><code class="sourceCode xml"><span id="cb2-1"><a href="#cb2-1" aria-hidden="true" tabindex="-1"></a>&lt;<span class="kw">Parameters</span><span class="ot"> xmlns=</span><span class="st">&quot;http://hl7.org/fhir&quot;</span>&gt;</span>
<span id="cb2-2"><a href="#cb2-2" aria-hidden="true" tabindex="-1"></a>    &lt;<span class="kw">parameter</span>&gt;</span>
<span id="cb2-3"><a href="#cb2-3" aria-hidden="true" tabindex="-1"></a>        &lt;<span class="kw">name</span><span class="ot"> value=</span><span class="st">&quot;ePrescription&quot;</span> /&gt;</span>
<span id="cb2-4"><a href="#cb2-4" aria-hidden="true" tabindex="-1"></a>        &lt;<span class="kw">resource</span>&gt;</span>
<span id="cb2-5"><a href="#cb2-5" aria-hidden="true" tabindex="-1"></a>            &lt;<span class="kw">Binary</span>&gt;</span>
<span id="cb2-6"><a href="#cb2-6" aria-hidden="true" tabindex="-1"></a>                &lt;<span class="kw">contentType</span><span class="ot"> value=</span><span class="st">&quot;application/pkcs7-mime&quot;</span> /&gt;</span>
<span id="cb2-7"><a href="#cb2-7" aria-hidden="true" tabindex="-1"></a>                &lt;<span class="kw">data</span><span class="ot"> value=</span><span class="st">&quot;MIJTfQYJKoZIhvcNAQcCoIJTbjCCU2oCAQUxDzANBglghkgBZQMEAg...&quot;</span> /&gt;</span>
<span id="cb2-8"><a href="#cb2-8" aria-hidden="true" tabindex="-1"></a>            &lt;/<span class="kw">Binary</span>&gt;</span>
<span id="cb2-9"><a href="#cb2-9" aria-hidden="true" tabindex="-1"></a>        &lt;/<span class="kw">resource</span>&gt;</span>
<span id="cb2-10"><a href="#cb2-10" aria-hidden="true" tabindex="-1"></a>    &lt;/<span class="kw">parameter</span>&gt;</span>
<span id="cb2-11"><a href="#cb2-11" aria-hidden="true" tabindex="-1"></a>&lt;/<span class="kw">Parameters</span>&gt;</span></code></pre></div>
<div class="note">
<p>Bei ` &lt;data value="*" /&gt;` handelt es sich um die
base64-codierte Repräsentation der enveloping-Signatur mit dem
enthaltenen E-Rezept-Bundle. Der codierte base64-String ist hier aus
Gründen der Lesbarkeit nicht vollständig dargestellt. Das vollständige
Beispiel findet sich im Unterordner der <a
href="../samples/qes/signed">Beispiele</a> in der Datei
<code>4fe2013d-ae94-441a-a1b1-78236ae65680_S_SECUN_secu_kon_4.8.2_4.1.3.p7</code></p>
</div></td>
</tr>
</tbody>
</table>

**Response**

    HTTP/1.1 200 OK
    Content-Type: application/fhir+xml;charset=utf-8

    <Task xmlns="http://hl7.org/fhir">
        <id value="169.000.004.839.514.95" />
        <meta>
            <profile value="https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_PR_Task|1.2" />
        </meta>
        <extension url="https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_EX_PrescriptionType">
            <valueCoding>
                <system value="https://gematik.de/fhir/erp/CodeSystem/GEM_ERP_CS_FlowType" />
                <code value="169" />
                <display value="Muster 16 (Direkte Zuweisung)" />
            </valueCoding>
        </extension>
        <extension url="https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_EX_AcceptDate">
            <valueDate value="2022-06-30" />
        </extension>
        <extension url="https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_EX_ExpiryDate">
            <valueDate value="2022-06-30" />
        </extension>
        <identifier>
            <system value="https://gematik.de/fhir/erp/NamingSystem/GEM_ERP_NS_PrescriptionId" />
            <value value="169.000.004.839.514.95" />
        </identifier>
        <identifier>
            <system value="https://gematik.de/fhir/erp/NamingSystem/GEM_ERP_NS_AccessCode" />
            <value value="777bea0e13cc9c42ceec14aec3ddee2263325dc2c6c699db115f58fe423607ea" />
        </identifier>
        <status value="ready" />
        <intent value="order" />
        <for>
            <identifier>
                <system value="http://fhir.de/sid/gkv/kvid-10" />
                <value value="X123456789" />
            </identifier>
        </for>
        <authoredOn value="2022-03-18T15:26:00+00:00" />
        <lastModified value="2022-03-18T15:27:00+00:00" />
        <performerType>
            <coding>
                <system value="urn:ietf:rfc:3986" />
                <code value="urn:oid:1.2.276.0.76.4.54" />
                <display value="Öffentliche Apotheke" />
            </coding>
        </performerType>
        <input>
            <type>
                <coding>
                    <system value="https://gematik.de/fhir/erp/CodeSystem/GEM_ERP_CS_DocumentType" />
                    <code value="1" />
                    <display value="Health Care Provider Prescription" />
                </coding>
            </type>
            <valueReference>
                <reference value="281a985c-f25b-4aae-91a6-41ad744080b0" />
            </valueReference>
        </input>
        <input>
            <type>
                <coding>
                    <system value="https://gematik.de/fhir/erp/CodeSystem/GEM_ERP_CS_DocumentType" />
                    <code value="2" />
                    <display value="Patient Confirmation" />
                </coding>
            </type>
            <valueReference>
                <reference value="f8c2298f-7c00-4a68-af29-8a2862d55d43" />
            </valueReference>
        </input>
    </Task>

Der E-Rezept-Fachdienst prüft die Gültigkeit der qualifizierten Signatur
des übergebenen FHIR-Bundles. Bei Gültigkeit wird der Task aktiviert und
die Zuordnung des Task zum Patienten auf Basis der KVNR im Task unter
`<value value="X123456789"` hinterlegt.

Das signierte FHIR-Bundle wird als Ganzes gespeichert und steht inkl.
der Signatur für den Abruf durch einen berechtigten, abgebenden
Leistungserbringer zur Verfügung. Der Verweis erfolgt über die ID des
Bundles in `<reference value="281a985c-f25b-4aae-91a6-41ad744080b0" />`,
der Abruf erfolgt immer über den Task.

Für den Versicherten wird eine Kopie des Bundles im JSON-Format inkl.
serverseitiger Signatur bereitgestellt, die an der Stelle
`<reference value="f8c2298f-7c00-4a68-af29-8a2862d55d43" />`
referenziert wird.

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
[small]#Die Anfrage wurde erfolgreich bearbeitet und das Ergebnis der Anfrage wird in der Antwort übertragen.#</code></pre></td>
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
<tr class="odd">
<td style="text-align: left;"><p>401</p></td>
<td style="text-align: left;"><p>Unauthorized<br />
<span class="small">Die Anfrage kann nicht ohne gültige
Authentifizierung durchgeführt werden. Wie die Authentifizierung
durchgeführt werden soll, wird im "WWW-Authenticate"-Header-Feld der
Antwort übermittelt.</span></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>403</p></td>
<td style="text-align: left;"><p>Forbidden<br />
<span class="small">Die Anfrage wurde mangels Berechtigung des Clients
nicht durchgeführt, bspw. weil der authentifizierte Benutzer nicht
berechtigt ist.</span></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>404</p></td>
<td style="text-align: left;"><p>Not found<br />
<span class="small">Die adressierte Ressource wurde nicht gefunden, die
übergebene ID ist ungültig.</span></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>405</p></td>
<td style="text-align: left;"><p>Method Not Allowed<br />
<span class="small">Die Anfrage darf nur mit anderen HTTP-Methoden (zum
Beispiel GET statt POST) gestellt werden. Gültige Methoden für die
betreffende Ressource werden im "Allow"-Header-Feld der Antwort
übermittelt.</span></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>408</p></td>
<td style="text-align: left;"><p>Request Timeout<br />
<span class="small">Innerhalb der vom Server erlaubten Zeitspanne wurde
keine vollständige Anfrage des Clients empfangen.</span></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>429</p></td>
<td style="text-align: left;"><p>Too Many Requests<br />
<span class="small">Der Client hat zu viele Anfragen in einem bestimmten
Zeitraum gesendet.</span></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>500</p></td>
<td style="text-align: left;"><p>Server Errors<br />
<span class="small">Unerwarteter Serverfehler</span></p></td>
</tr>
</tbody>
</table>

# Anwendungsfall E-Rezept-Token an Apotheke übermitteln

Als verordnender Leistungserbringer möchte ich die Einlöseinformationen
(Task-ID und AccessCode) eines E-Rezepts direkt an eine Apotheke
versenden. Für das Übermitteln der Einlöseinformationen verwende ich die
TI-Fachanwendung KIM.

Voraussetzung für die Verwendung des KIM-Dienstes ist, das alle
beteiligten Parteien über eine eine einsatzfähige KIM Installation
verfügen. Dazu gehört ein konfiguriertes und einsatzfähiges
KIM-Clientmodul und die Regristierung bei einem KIM-Anbieter. (Siehe
Voraussetzungen zur Nutzung der Fachanwendung KIM:
<https://github.com/gematik/api-kim/blob/main/docs/Primaersystem.adoc#voraussetzungen>).

## Ablauf der Erstellung einer KIM Nachricht

### KIM-Nachricht generieren und Empfänger ermitteln

Im ersten Schritt wird eine Nachricht im Primärsystem erstellt. Der
verordnende Leistungserbringer verfasst einen Nachrichtentext und kann
wählen, ob eine Zustellbestätigung erfolgen soll. Das E-Rezept Token
wird automatisch in die Nachricht eingefügt.  
Die Nachricht kann nur an Empfänger versendet werden, für die ein
Eintrag im Verzeichnisdienst (inklusive KIM Adresse) der TI vorhanden
ist. Der KIM-Header "To" muss mit einer Email-Adresse aus dem
Verzeichnisdienst befüllt werden. Das Primärsystem kann hierzu eine
Abfrage der Empfänger-Adressen durchführen und agiert dabei als
LDAP-Client gegenüber dem LDAP-Server (Verzeichnisdienst). Der Konnektor
dient dabei als LDAP-Proxy.

### KIM-Nachricht versenden

Der Versand von KIM-Nachrichten erfolgt über das Clientmodul, das die
Nachricht für jeden Empfänger zuerst signiert und anschließend
verschlüsselt. Die KIM-Nachricht wird als "message/rfc822"-MIME Einheit
erzeugt und in eine "multipart/mixed"-MIME-Nachricht verpackt. Die
Message-IDs der Nachrichten dürfen keine datenschutzrelevanten
Informationen - wie z. B. FQDNs - enthalten. Die E-Mail-Nachricht muss
anschließend über das Clientmodul versendet werden. Die Signatur erfolgt
über das Primärsystem mit einem Aufruf der Signaturschnittstelle des
Konnektors. Zur Signatur wird der S-MIME-Standard verwendet. Die
Nachricht wird durch das Clientmodul automatisch mit dem öffentlichen
Schlüssel des SMC-B-Zertifikats des Empfängers verschlüsselt und mit der
SMC-B der Absenders signiert.  

Beim Aufbau der SMTP-Verbindung ist es erforderlich,
Kartenverwaltungsinformationen zur SMC-B mitzuliefern, die zum
Integritätsschutz der Nachricht verwendet werden sollen. Dazu müssen
MandantId, ClientsystemId und WorkplaceId, der Kartensitzung der
erforderlichen SMC-B, über den SMTP-Benutzernamen dem Clientmodul
mitgeteilt werden. Weitere Informationen zur SMTP-Kommunikation finden
Sie hier:
<https://github.com/gematik/api-kim/blob/main/docs/Primaersystem.adoc#43-nachrichten-versenden>  

Eine beispielhafte verschlüsselte KIM-Nachricht kann hier eingesehen
werden: <https://github.com/gematik/api-kim/tree/main/samples>  

### KIM-Nachricht empfangen

Das Clientmodul des Empfängers erhält die KIM-Nachricht und
entschlüsselt diese, sofern die dafür erforderliche Smartcard/HSM im
System registriert und freigeschaltet ist. Damit wird sichergestellt,
dass der Zugriff auf die Nachrichten nur durch autorisierte Personen
erfolgt. Die Kommunikation zwischen dem Primärsystem und dem
KIM-Clientmodul erfolgt mittels des POP3-Standards. Das Primärsystem
übergibt dem Clientmodul alle zum Nachrichtenempfang erforderlichen
Informationen. Das Primärsystem muss sich zur POP3-Authentifizierung
gegenüber dem KIM-Dienst ausweisen können. Hierfür wird im Primärsystem
ein POP3-Benutzername und Passwort persistiert.  
Das Clientmodul leitet die POP3-Anfragen des Primärsystems an den
KIM-Fachdienst (MTA) weiter und entschlüsselt abgeholte Nachrichten, um
sie in entschlüsselter und verifizierter Form an das Primärsystem
weiterzugeben.  
Enthält eine KIM-Nachricht externe Anhänge die auf einem KAS abgelegt
wurden, so werden diese in KOM-LE 1.5 vom Clientmodul automatisch
heruntergeladen und für das Primärsystem in die KIM-E-Mail eingefügt.  

Eine Übersicht der beteiligten Komponenten sowie Schnittstellen zwischen
Primärsysten, Clientmodul und KIM-Fachdienst kann in der
API-Dokumentation zur KIM Fachanwendung nachgelesen werden:
<https://github.com/gematik/api-kim#systemarchitektur>

## KIM-Nachrichten in der E-Rezept Fachanwendung

Es gibt zwei E-Rezept spezifische Nachrichten, diese unterscheiden sich
durch die X-KIM-Dienstkennung (Siehe
<https://fachportal.gematik.de/toolkit/dienstkennung-kim-kom-le>).

Eine Nachricht dient der direkten Zuweisung eines E-Rezeptes an eine
Apotheke. Die Nachricht beinhaltet einen Mitteilungstext, den
E-Rezept-Token als Link und optional einen Therapieplan als Anhang
(base64 codiert).

### Beispielnachricht für eine Zuweisung eines E-Rezepts an eine Apotheke

    Date: Sun, 20 Jun 2021 11:12:13 +0100
    From: ArztABC@abc.kim.telematik
    To: Apotheke123@xyz.kim.telematik
    Subject: E-Rezept direkte Zuweisung Zytostatikum
    X-KIM-Dienstkennung: eRezept;Zuweisung;V1.0
    Disposition-Notification-To: ArztABC@abc.kim.telematik
    Return-Path: <ArztABC@abc.kim.telematik>
    Message-ID: <th1s1s43me55age1d@abc.kim.telematik>
    MIME-Version: 1.0
    Content-Type: multipart/mixed;boundary=boundarymultipartseparator42

    This is a multi-part message in MIME format.

    --boundarymultipartseparator42
    Content-Type: text/plain;charset=UTF-8

    Sehr geehrte Apotheke
    TextTextTextTextTextTextTextTextText
    TextTextTextTextTextTextTextTextText
    TextTextTextTextTextTextTextTextText

    Mit den besten Gruessen
    Aerztin Mueller
    --boundarymultipartseparator42
    Content-Type: text/plain;charset=UTF-8

    Task/169.774.328.939.869.74/$accept?ac=777bea0e13cc9c42ceec14aec3ddee2263325dc2c6c699db115f58fe423607ea
    --boundarymultipartseparator42
    Content-Type: application/pdf; name="therapieplan.pdf"
    Content-Transfer-Encoding: base64
    Content-Disposition: attachment; filename=therapieplan.pdf

    JVBERi0xLjQKJcDIzNINCjEgMCBvYmoKPDwKL1RpdGxlI
    [...]
     GQzZDMEUxQzRGRUI0NjFCQ0NGOUYzPjw0RDM4MkJGRDRB
     RkM2QzBFMUM0RkVCNDYxQkNDRjlGMz5dCj4+CnN0YXJ0e
     HJlZgoyMDE0CiUlRU9GCg==
     --boundarymultipartseparator42--

`Subject:` enthält den wählbaren Titel der Nachricht. Es dürfen keine
personenbezogenen oder medizinischen Informationen enthalten sein.  

Für die Zuweisung eines E-Rezeptes an die Apotheke muss der Wert
`X-KIM-Dienstkennung` gesetzt sein.  

Aus Gründen der Lesbarkeit wurde der angehängte Therapieplan stark mit
`[...]` gekürzt.

### Nachricht zur freien Kommunikation für bspw. Rückfragen der Apotheke

    Beispiel einer KIM-Message für die freie Kommunikation:
    Date: Mon, 21 Jun 2021 11:12:13 +0100
    From: Apotheke123@xyz.kim.telematik
    To: ArztABC@abc.kim.telematik
    Subject: E-Rezept Kommunikation
    X-KIM-Dienstkennung: eRezept;Kommunikation;V1.0
    Disposition-Notification-To: Apotheke123@xyz.kim.telematik
    Return-Path: <Apotheke123@xyz.kim.telematik>
    Message-ID: <th1s1s43me55ag12a@xyz.kim.telematik>
    MIME-Version: 1.0
    Content-Type: text/plain;charset=UTF-8

    Sehr geehrte Praxis

    TextTextTextTextTextTextTextTextText
    TextTextTextTextTextTextTextTextText
    TextTextTextTextTextTextTextTextText

    Mit den besten Gruessen
    Apotheke 123

`Subject` enthält den wählbaren Titel der Nachricht. Es dürfen keine
personenbezogenen oder medizinischen Informationen enthalten sein.  

Für die Zuweisung eines E-Rezeptes an die Apotheke muss die
`X-KIM-Dienstkennung` gesetzt sein.

# Anwendungsfall E-Rezept durch Versicherten einsehen

Als Versicherter möchte ich meine E-Rezepte einsehen sowie auf die
Dispensierinformationen und das Zugriffsprotokoll zugreifen. Ich bin
nicht berechtigt E-Rezepte mit dem Workflowtyp 169 einer Apotheke
zuzuweisen oder zu löschen.

Der Aufruf erfolgt als http-`GET`-Operation auf die Ressource `/Task`.
Im Aufruf muss das während der Authentisierung erhaltene ACCESS\_TOKEN
im http-Request-Header `Authorization` übergeben werden, der Fachdienst
filtert die Task-Einträge nach der im ACCESS\_TOKEN enthaltenen KVNR des
Versicherten. Werden ein oder mehrere Tasks gefunden, erfolgt die
Rückgabe eines Tasks immer zusammen mit dem entsprechenden, signierten
E-Rezept-Datensatz zu diesem Task, welcher die Verordnungsinformationen
des E-Rezepts enthält. Der E-Rezept-Fachdienst identifiziert die
E-Rezepte auf Basis der Versicherten-ID des Versicherten. Die
AccessCodes werden dem Versicherten für diesen speziellen Rezept-Typ
nicht übermittelt.

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
href="https://erp.zentral.erp.splitdns.ti-dienste.de/Task">https://erp.zentral.erp.splitdns.ti-dienste.de/Task</a></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>Method</strong></p></td>
<td style="text-align: left;"><p>GET</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>HTTP Header</strong></p></td>
<td style="text-align: left;"><pre><code>Authorization: Bearer eyJraWQ.ewogImL2pA10Qql22ddtutrvx4FsDlz.rHQjEmB1lLmpqn9J</code></pre>
<div class="note">
<p>Mit dem ACCESS_TOKEN im <code>Authorization</code>-Header weist sich
der Zugreifende als Versicherter aus, im Token ist seine
Versichertennummer enthalten. Die Base64-Darstellung des Tokens ist
stark gekürzt.</p>
</div>
<div class="note">
<p>Im http-Header des äußeren http-Requests an die VAU (POST /VAU) sind
die Header <code>X-erp-user: v</code> und
<code>X-erp-resource: Task</code> zu setzen.</p>
</div></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>Payload</strong></p></td>
<td style="text-align: left;"><pre><code>-</code></pre></td>
</tr>
</tbody>
</table>

**Response**

    HTTP/1.1 200 OK
    Content-Type: application/fhir+json;charset=utf-8

    {
      "resourceType": "Bundle",
      "id": "f5ba6eaf-9052-42f6-ac4e-fadceed7293b",
      "meta": {
        "lastUpdated": "2020-03-01T07:02:37.836+00:00"
      },
      "type": "collection",
      "total": 2,
      "link": [{
        "relation": "self",
        "url": "https://erp.zentral.erp.splitdns.ti-dienste.de/Task/"
      }],
      "entry": [{
        "fullUrl": "https://erp.zentral.erp.splitdns.ti-dienste.de/Task/169.774.328.939.869.74",
        "resource": {

        "resourceType": "Task",
        "id": "169.774.328.939.869.74",
        "meta": {
            "profile":  [
                "https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_PR_Task|1.2"
            ],
            "tag":  [
                {
                    "display": "Task in READY state activated by (Z)PVS/KIS via $activate operation"
                }]
        },
        "intent": "order",
        "extension":  [{
                "url": "https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_EX_PrescriptionType",
                "valueCoding": {
                    "code": "169",
                    "system": "https://gematik.de/fhir/erp/CodeSystem/GEM_ERP_CS_FlowType",
                    "display": "Muster 16 (Direkte Zuweisung)"
                }},
            {
                "url": "https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_EX_AcceptDate",
                "valueDate": "2022-06-02"
            },{
                "url": "https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_EX_ExpiryDate",
                "valueDate": "2022-06-02"
            }],
        "identifier":  [
            {
                "system": "https://gematik.de/fhir/erp/NamingSystem/GEM_ERP_NS_PrescriptionId",
                "value": "169.774.328.939.869.74"
            }],
        "status": "ready",
        "authoredOn": "2022-03-18T15:26:00+00:00",
        "performerType":  [
            {
                "coding":  [{
                        "code": "urn:oid:1.2.276.0.76.4.54",
                        "system": "urn:ietf:rfc:3986",
                        "display": "Öffentliche Apotheke"
                    }]
            }],
        "for": {
            "identifier": {
                "system": "http://fhir.de/sid/gkv/kvid-10",
                "value": "X123456789"
            }},
        "lastModified": "2022-03-18T15:27:00+00:00",
        "input":  [
            {
                "type": {
                    "coding":  [
                        {
                            "code": "1",
                            "system": "https://gematik.de/fhir/erp/CodeSystem/GEM_ERP_CS_DocumentType",
                            "display": "Health Care Provider Prescription"
                        }]
                },
                "valueReference": {
                    "reference": "281a985c-f25b-4aae-91a6-41ad744080b0"
                }
            },{
                "type": {
                    "coding":  [{
                            "code": "2",
                            "system": "https://gematik.de/fhir/erp/CodeSystem/GEM_ERP_CS_DocumentType",
                            "display": "Patient Confirmation"
                        }]
                },
                "valueReference": {
                    "reference": "f8c2298f-7c00-4a68-af29-8a2862d55d43"
                }}
        ]}
      },{

        "fullUrl": "https://erp.zentral.erp.splitdns.ti-dienste.de/Task/169.000.033.491.280.78",
        "resource": {
        "resourceType": "Task",
        "id": "169.000.033.491.280.78",
        "meta": {
            "profile":  [
                "https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_PR_Task|1.2"
            ]
        },
        "intent": "order",
        "extension":  [{
                "url": "https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_EX_PrescriptionType",
                "valueCoding": {
                    "code": "169",
                    "system": "https://gematik.de/fhir/erp/CodeSystem/GEM_ERP_CS_FlowType",
                    "display": "Muster 16 (Direkte Zuweisung)"
                }},
            {
                "url": "https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_EX_AcceptDate",
                "valueDate": "2022-06-03"
            },{
                "url": "https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_EX_ExpiryDate",
                "valueDate": "2022-06-03"
            }],
        "identifier":  [
            {
                "system": "https://gematik.de/fhir/erp/NamingSystem/GEM_ERP_NS_PrescriptionId",
                "value": "169.000.033.491.280.78"
            }],
        "status": "ready",
        "authoredOn": "2022-03-18T15:26:00+00:00",
        "performerType":  [
            {
                "coding":  [{
                        "code": "urn:oid:1.2.276.0.76.4.54",
                        "system": "urn:ietf:rfc:3986",
                        "display": "Öffentliche Apotheke"
                    }]
            }],
        "for": {
            "identifier": {
                "system": "http://fhir.de/sid/gkv/kvid-10",
                "value": "X123456789"
            }},
        "lastModified": "2022-03-18T15:27:00+00:00",
        "input":  [
            {
                "type": {
                    "coding":  [
                        {
                            "code": "1",
                            "system": "https://gematik.de/fhir/erp/CodeSystem/GEM_ERP_CS_DocumentType",
                            "display": "Health Care Provider Prescription"
                        }]
                },
                "valueReference": {
                    "reference": "281a985c-f25b-4aae-91a6-41ad744080b0"
                }
            },{
                "type": {
                    "coding":  [{
                            "code": "2",
                            "system": "https://gematik.de/fhir/erp/CodeSystem/GEM_ERP_CS_DocumentType",
                            "display": "Patient Confirmation"
                        }]
                },
                "valueReference": {
                    "reference": "f8c2298f-7c00-4a68-af29-8a2862d55d43"
                }
            }
        ]}
      }]
    }

Der Prozesstyp in
`"url": "https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_EX_PrescriptionType"`
referenziert die Workflow-Definition, in diesem Fall den Prozess für
apothekenpflichtige Arzneimittel.

Mit der Angabe `"display": "Öffentliche Apotheke"` kann dem Versicherten
ein Hinweis angezeigt werden, wo er das E-Rezept einlösen kann.

Mit dem Verweis `"reference": "281a985c-f25b-4aae-91a6-41ad744080b0"`
zeigt der Task auf das signierte E-Rezept-Bundle im zurückgegebenen
Bundle.

Aus Gründen der besseren Lesbarkeit ist das E-Rezept-Bundle hier nicht
vollständig dargestellt. Das komplette Beispiel kann hier eingesehen
werden: <https://simplifier.net/eRezept/Bundle-example/~json>.

Bei der Rückgabe an den Versicherten wird der ärztliche Signaturanteil
des E-Rezept-Bundles durch eine serverseitige Signatur in JWS-Format
ersetzt. Aus Gründen der besseren Lesbarkeit mit separaten
Zeilenumbrüchen zwischen den "."-separierten `Header.Payload.Signature`.

<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p><strong>Code</strong></p></td>
<td style="text-align: left;"><p><strong>Type Success</strong></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>200</p></td>
<td style="text-align: left;"><pre><code> OK +
[small]#Die Anfrage wurde erfolgreich bearbeitet. Die angeforderten Ressourcen sind im Response-Body enthalten.#</code></pre></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>Code</strong></p></td>
<td style="text-align: left;"><p><strong>Type Error</strong></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>400</p></td>
<td style="text-align: left;"><pre><code> Bad Request  +
[small]#Die Anfrage-Nachricht war fehlerhaft aufgebaut.#</code></pre></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>401</p></td>
<td style="text-align: left;"><p>Unauthorized<br />
<span class="small">Die Anfrage kann nicht ohne gültige
Authentifizierung durchgeführt werden. Wie die Authentifizierung
durchgeführt werden soll, wird im "WWW-Authenticate"-Header-Feld der
Antwort übermittelt.</span></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>403</p></td>
<td style="text-align: left;"><p>Forbidden<br />
<span class="small">Die Anfrage wurde mangels Berechtigung des Clients
nicht durchgeführt, bspw. weil der authentifizierte Benutzer nicht
berechtigt ist.</span></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>405</p></td>
<td style="text-align: left;"><p>Method Not Allowed<br />
<span class="small">Die Anfrage darf nur mit anderen HTTP-Methoden (zum
Beispiel GET statt POST) gestellt werden. Gültige Methoden für die
betreffende Ressource werden im "Allow"-Header-Feld der Antwort
übermittelt.</span></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>429</p></td>
<td style="text-align: left;"><p>Too Many Requests<br />
<span class="small">Der Client hat zu viele Anfragen in einem bestimmten
Zeitraum gesendet.</span></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>500</p></td>
<td style="text-align: left;"><p>Server Errors<br />
<span class="small">Unerwarteter Serverfehler</span></p></td>
</tr>
</tbody>
</table>
