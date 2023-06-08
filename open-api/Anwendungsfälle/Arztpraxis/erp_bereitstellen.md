# Anwendungsfall E-Rezept bereitstellen

Mit diesem Use Case stellt ein verordnender (Zahn-)Arzt dem Patienten
ein E-Rezept auf dem E-Rezept-Fachdienst bereit. Die Erzeugung des
E-Rezepts erfolgt unter Nutzung der Verordnungsdatenschnittstelle für
Primärsysteme. Mit dieser wählt der Leistungserbringer die
therapierelevanten Wirkstoffe, Medikamente, o.Ä. aus. Der
Leistungserbringer authentisiert sich gegenüber der
Telematikinfrastruktur mit der Institutionsidentität der SMC-B unter
Nutzung des IdentityProviders (IdP) und des Konnektors. Anschließend
erfolgt das Generieren einer Rezept-ID über das Erzeugen eines Tasks im
E-Rezept-Fachdienst. Die ID der erstellten Ressource Task bettet das
Primärsystem des Leistungserbringers in den lokalen Datensatz ein und
lässt diesen Datensatz vom Konnektor qualifiziert signieren. Zum
Abschluss erfolgt die Aktivierung des im E-Rezept-Fachdienst erstellten
Tasks in den korrekten Status und Ergänzung des qualifiziert signierten
Datensatzes. Der E-Rezept-Fachdienst validiert die QES und erzeugt bei
Gültigkeit der QES sowie Schemakonformität des E-Rezept-Bundles
serverseitig eine Signatur zum Schutz der Integrität der Daten.

Die Qualifizierte elektronischen Signatur QES kann ausschliesslich von
einem (Zahn-)Arzt mit Zugriff auf einen freigeschalteten elektronischen
Heilberufsausweis (HBA) durchgeführt werden. Alle anderen
Teilaktivitäten können auch durch einen Mitarbeiter der medizinischen
Institution (MFA) durchgeführt werden. So ist es bspw. möglich, dass ein
MFA E-Rezepte vorbereitet und lokal im PVS abspeichert. Der (Zahn-)Arzt
erhält Hinweis des PVS, dass ein oder mehrere vorbereitete E-Rezepte auf
eine QES warten und kann zwischen zwei Behandlungsgesprächen (wenn Zeit
ist) die vorbereiteten E-Rezepte signieren.

Das im Verordnungsdatensatz im Attribut authoredOn angegebene Datum muss
identisch mit dem Datum der Erstellung des QES sein. Bei Ungleichheit
lehnt der E-Rezept-Fachdienst das E-Rezept beim Einstellen ab. Sollte
der Verordnungsdatensatz bspw. am Vortag bereits vorbereitet worden
sein, muss das Primärsystem den Wert für authoredOn vor der QES
anpassen.

## Kurzbeschreibung der Abfolge zum Bereitstellen eines E-Rezeptes

1. PrescriptionID und AccessCode vom E-Rezept Fachdienst anfordern ([POST /Task/$create]((../open-api/openapi/openapi_erezpt.yaml/paths/~1Task~1$create/post)))
2. Verordnungsdatensatz erstellen
3. Verordnungsdatensatz signieren
4. Verordnungsdatensatz im E-Rezept Fachdienst einstellen (POST /Task/$activate)

![width=100%](../../../images/api_rezept_einstellen.png)

## Profilierung

Für diesen Anwendungsfall wird die FHIR-Resource "Task" profiliert. Das
Profil kann als JSON oder XML hier eingesehen werden:
<https://simplifier.net/erezept-workflow/gem_erp_pr_task>.

Die für diese Anwendung wichtigen Attribute und Besonderheiten durch die
Profilierung der Ressourcen werden durch das "must be supported"-Flag
gekennzeichnet. Sie werden in der folgenden Tabelle kurz
zusammengefasst:

| Name                      | Beschreibung                                                                 |
|---------------------------|------------------------------------------------------------------------------|
| identifier:PrescriptionID | Rezept-ID; eindeutig für jedes
Rezept                                        |
| identifier:AccessCode     | Vom E-Rezept-Fachdienst generierter
Berechtigungs-Code                       |
| identifier:Secret         | Vom E-Rezept-Fachdienst generierter
Berechtigungs-Code                       |
| status                    | Status des E-Rezepts                                                         |
| intent                    | Intension des Tasks. Fixer
Wert="order"                                      |
| for                       | Krankenversichertennummer                                                    |
| authoredOn                | Erstellungszeitpunkt des Tasks                                               |
| lastModified              | Letzte Änderung am Task                                                      |
| performerType             | Institution, in der das Rezept
eingelöst werden soll                         |
| input                     | Verweis auf das für den Patient und den
Leistungserbringer erstellten Bundle |
| output                    | Verweis auf das
Quittungs-Bundle                                             |
| extension:flowType        | Gibt den Typ des Rezeptes an                                                 |
| extension:expiryDate      | Verfallsdatum                                                                |
| extension:acceptDate      | Datum, bis zu welchem die Krankenkasse
spätestens die Kosten übernimmt       |


In den folgenden Kapiteln wird erläutert, wann und wie die Befüllung
dieser Attribute erfolgt.

## E-Rezept erstellen

[API-Endpunkt: POST /Task/$create](../open-api/openapi/openapi_erezpt.yaml/paths/~1Task~1$create/post)

Ein Leistungserbringer will mit seinem Primärsystem ein E-Rezept
erzeugen. Hierfür erstellt das Primärsystem ein FHIR-Bundle gemäß der
KBV-Profilierung des E-Rezepts (siehe <https://simplifier.net/erezept>).
Für die Bereitstellung an den Versicherten wird auf dem
E-Rezept-Fachdienst ein Task erstellt, dessen Identifier als Rezept-ID
in das FHIR-Bundle eingebettet wird. Nach der qualifizierten
elektronischen Signatur des Bundles wird dieses im Task ergänzt und der
Workflow des E-Rezepts mit der Aktivierung des Tasks gestartet. Im
Aufruf an den E-Rezept-Fachdienst muss das während der Authentisierung
erhaltene ACCESS\_TOKEN im http-Request-Header `Authorization` übergeben
werden. Der E-Rezept-Fachdienst generiert beim Einstellen einen
AccessCode, der fortan bei allen Zugriffen im http-Request-Header
`X-AccessCode` übermittelt werden muss.

Der Aufruf erfolgt als http-`POST`-Operation. Im Aufruf muss das während
der Authentisierung erhaltene ACCESS\_TOKEN im http-Request-Header
`Authorization` übergeben werden. Im http-RequestBody MÜSSEN die
Konfigurationsparameter des Workflows `flowType` und der Typ der
intendierten Leistungserbringerinstitution `healthCareProviderType`
enthalten sein.  
Gültige Werte für den Flowytype sind "160" für "Muster 16
(Apothekenpflichtige Arzneimittel)" und "200" für "PKV
(Apothekenpflichtige Arzneimittel)". Das Rezept für private Versicherte
wird mit dem Flowtype "200" ("PKV (Apothekenpflichtige Arzneimittel)")
gestartet. Zulässige Flowtype-Werte können dem Flowtype-CodeSystem
(<https://simplifier.net/erezept-workflow/flowtype>) entnommen werden.
Der angegebene Flowtype wird in die Task Ressource unter
Task.extension.flowType übernommen und bestimmt den Rezept-Typ.  
Der E-Rezept-Fachdienst speichert den Task unter einer generierten ID,
welche im Response-Header `Location` zurückgemeldet wird und zusätzlich
ist im http-ResponseBody des Task der serverseitig generierte AccessCode
als Identifier enthalten.


Der unter dem Identifier `GEM_ERP_NS_PrescriptionId` hinterlegte
`<identifier><value value="*"/></identifier>` stellt die 10 Jahre lang
eineindeutige Rezept-ID dar.

An Identifier unter `GEM_ERP_NS_AccessCode` ist der serverseitig
generierte `AccessCode`, der für nachfolgende Zugriffe auf diesen Task
in einem http-Request für die Berechtigungsprüfung mitgegeben werden
muss.

Unter `GEM_ERP_CS_FlowType` hat der E-Rezept-Fachdienst den
Übergabeparameter zur Konfiguration des des Workflows übernommen.

Der Wert `urn:oid:1.2.276.0.76.4.54` entspricht dem intendierten
Institutionstyp, in welchen der Versicherte für die Einlösung des
Rezepts gelenkt werden soll (öffentliche Apotheke für Workflow `160`).

## E-Rezept qualifiziert signieren

[API-Endpoint zur Signatur](../open-api/openapi/konnektor.yaml/paths/~1Konnektorservice#SignDocument/post)

Im Primärsystem liegt ein E-Rezept-Datensatz als FHIR-Bundle vor. Das
Primärsystem hat soeben einen Task im E-Rezept-Fachdienst erzeugt, um
eine langlebige Rezept-ID zu erhalten. Der vom Fachdienst
zurückgemeldete `Task.identifier` vom Typ
`https://gematik.de/fhir/erp/NamingSystem/GEM_ERP_NS_PrescriptionId` für
die Rezept-ID wird in den E-Rezept-Datensatz als `Identifier` des
Bundles mit dem gleichen Namingsystem
`https://gematik.de/fhir/erp/NamingSystem/GEM_ERP_NS_PrescriptionId`
eingebettet.

Im Folgenden ist ein Beispiel aus der KBV-Spezifikation des
E-Rezept-Bundles aufgelistet. Die vollständige Definition inkl. aller
Value Sets und Codesysteme findet sich auf der Seite
<https://simplifier.net/eRezept/>

Vollständiges Beispiel entnommen aus [samples/qes](../samples/qes) mit
Dateiname `4fe2013d-ae94-441a-a1b1-78236ae65680*` inkl. der folgenden
Konnektor-Signatur-Beispiele. Daher weicht die Rezept-ID
`PrescriptionID` von den übrigen Beispielen ab.

Das E-Rezept-Bundle in XML-Darstellung muss nun digital
unterschrieben (qualifiziert elektronisch signiert - QES) werden, das
Primärsystem nutzt dafür die Schnittstelle des Konnektors und dieser den
Heilberufsausweis des verordnenden Arztes/Zahnarztes. Um Fehler in der
Signaturprüfung zu vermeiden, wird die Kanonisierung des Dokuments vor
der Signaturerstellung für bestimmte Signaturformate empfohlen (bzw. bei
detached-Signaturen zwingend). Diese Kanonsierung normalisiert das
Dokument nach definierten Regeln, damit das signaturerstellende System
genauso wie das signaturprüfende System ein exakt identisches Dokument
in der Erstellung und Prüfung verwenden. Da es sich hierbei um ein
XML-Dokument handelt, kommen die Kanonisierungsregeln
<https://www.w3.org/TR/2008/REC-xml-c14n11-20080502/> für Canonical XML
Version 1.1 für XML-Dokumente zum Einsatz.

Bei der Verwendung des Signaturformats CAdES-Enveloping ist eine
Kanonisierung nicht erforderlich, da die signierten Daten "innerhalb"
der Signatur transportiert werden.

Der Konnektor wählt standardmäßig ein passendes kryptografisches
Verfahren, es kann jedoch mit dem Parameter `crypt` in SignDocument auch
gemäß der Spezifikation in gemSpec\_Kon#TAB\_KON\_862-01 \[ab
Schemaversion 7.5\] konkret gewählt werden (z.B. ECC, falls das
Verhalten der verschiedenen Algorithmen ausprobiert werden soll).


Der Aufruf erfolgt als http-POST-Operation auf eine SOAP-Schnittstelle.
Für die QES-Erstellung sind mindestens folgende Konnektor-Versionen der
drei Konnektoren notwendig:

-   KoCoBOX MED+ 2.3.24:2.0.0
-   RISE Konnektor 2.1.0:1.0.0
-   secunet Konnektor 2.1.0

## E-Rezept vervollständigen und Task aktivieren

Nach der erfolgreichen qualifizierten Signatur kann nun der Task im
Fachdienst aktiviert werden, indem das Ergebnis der erfolgreichen
QES-Erstellung als Base64-codierter Datensatz an den E-Rezept-Fachdienst
geschickt wird.

Der Aufruf erfolgt als http-`POST`-Operation auf die FHIR-Opertation
`$activate` des referenziereten Tasks. Im Aufruf muss das während der
Authentisierung erhaltene ACCESS\_TOKEN im http-Request-Header
`Authorization` und der beim erzeugen des Tasks generierte `AccessCode`
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
href="https://erp.zentral.erp.splitdns.ti-dienste.de/Task/160.123.456.789.123.58/$activate">https://erp.zentral.erp.splitdns.ti-dienste.de/Task/160.123.456.789.123.58/$activate</a></p></td>
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
<p>Bei dem Wert in
<code>&lt;Binary&gt;&lt;data value="*"/&gt;&lt;/Binary&gt;</code>
handelt es sich um die base64-codierte Repräsentation der
enveloping-Signatur mit dem enthaltenen E-Rezept-Bundle. Der codierte
base64-String ist hier aus Gründen der Lesbarkeit nicht vollständig
dargestellt. Das vollständige Beispiel findet sich im Unterordner der <a
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
        <id value="160.123.456.789.123.58"/>
        <meta>
            <versionId value="2"/>
            <lastUpdated value="2020-02-18T10:05:05.038+00:00"/>
            <source value="#AsYR9plLkvONJAiv"/>
            <profile value="https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_PR_Task|1.2"/>
        </meta>
        <extension url="https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_EX_PrescriptionType">
            <valueCodeableConcept>
                <coding>
                    <system value="https://gematik.de/fhir/erp/CodeSystem/GEM_ERP_CS_FlowType" />
                    <code value="160" />
                    <display value="Muster 16 (Apothekenpflichtige Arzneimittel)" />
                </coding>
            </valueCodeableConcept>
        </extension>
        <extension url="https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_EX_ExpiryDate">
            <valueDateTime value="2020-06-02" />
        </extension>
        <extension url="https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_EX_AcceptDate">
            <valueDateTime value="2020-04-01" />
        </extension>
        <identifier>
            <use value="official"/>
            <system value="https://gematik.de/fhir/erp/NamingSystem/GEM_ERP_NS_PrescriptionId"/>
            <value value="160.123.456.789.123.58"/>
        </identifier>
        <identifier>
            <use value="official"/>
            <system value="https://gematik.de/fhir/erp/NamingSystem/GEM_ERP_NS_AccessCode"/>
            <value value="777bea0e13cc9c42ceec14aec3ddee2263325dc2c6c699db115f58fe423607ea"/>
        </identifier>
        <identifier>
            <use value="official"/>
            <system value="http://fhir.de/sid/gkv/kvid-10"/>
            <value value="X123456789"/>
        </identifier>
        <status value="ready"/>
        <intent value="order"/>
        <authoredOn value="2020-03-02T08:25:05+00:00"/>
        <lastModified value="2020-03-02T08:45:05+00:00"/>
        <performerType>
            <coding>
                <system value="urn:ietf:rfc:3986"/>
                <code value="urn:oid:1.2.276.0.76.4.54"/>
                <display value="Öffentliche Apotheke"/>
            </coding>
        </performerType>
        <input>
            <type>
                <coding>
                    <system value="https://gematik.de/fhir/erp/CodeSystem/GEM_ERP_CS_DocumentType"/>
                    <code value="1"/>
                    <display value="Health Care Provider Prescription"/>
                </coding>
            </type>
            <valueReference>
                <reference value="281a985c-f25b-4aae-91a6-41ad744080b0"/>
            </valueReference>
        </input>
        <input>
            <type>
                <coding>
                    <system value="https://gematik.de/fhir/erp/CodeSystem/GEM_ERP_CS_DocumentType"/>
                    <code value="2"/>
                </coding>
            </type>
            <valueReference>
                <reference value="f8c2298f-7c00-4a68-af29-8a2862d55d43"/>
            </valueReference>
        </input>
    </Task>

Der E-Rezept-Fachdienst prüft die Gültigkeit der qualifizierten Signatur
des übergebenen FHIR-Bundles. Bei Gültigkeit wird der Task aktiviert und
die Zuordnung des Task zum Patienten auf Basis der KVNR im Task unter
dem `value` von `<system value="http://fhir.de/sid/gkv/kvid-10"/>`
hinterlegt.

Das signierte FHIR-Bundle wird als Ganzes gespeichert und steht inkl.
der Signatur für den Abruf durch einen berechtigten, abgebenden
Leistungserbringer zur Verfügung. Der Verweis erfolgt über die ID des
Bundles unter
`<reference value="281a985c-f25b-4aae-91a6-41ad744080b0"/>`, der Abruf
erfolgt immer über den Task.

Für den Versicherten wird eine Kopie des Bundles im JSON-Format inkl.
serverseitiger Signatur bereitgestellt, die an der Stelle
`<reference value="f8c2298f-7c00-4a68-af29-8a2862d55d43"/>` referenziert
wird.

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
<tr class="even">
<td style="text-align: left;"><p>512</p></td>
<td style="text-align: left;"><p>OCSP Backend Error<br />
<span class="small">Innerhalb der vom Server erlaubten Zeitspanne wurde
keine gültige Antwort des OCSP-Responders geliefert.</span></p></td>
</tr>
</tbody>
</table>

# Ein E-Rezept löschen

Als verordnender Leistungserbringer möchte ich ein E-Rezept löschen
können, um den Patienten vor dem Bezug und der Einnahme eines fälschlich
verordneten Medikaments zu schützen.

Der Aufruf erfolgt als http-POST-Operation mit der FHIR-Operation
`$abort`. Im http-Request-Header `Authorization` müssen das während der
Authentisierung erhaltene ACCESS\_TOKEN und der AccessCode im Header
`X-AccessCode` für die Berechtigungsprüfung übergeben werden.

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
href="https://erp.zentral.erp.splitdns.ti-dienste.de/Task/160.123.456.789.123.58/$abort">https://erp.zentral.erp.splitdns.ti-dienste.de/Task/160.123.456.789.123.58/$abort</a></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>Method</strong></p></td>
<td style="text-align: left;"><p>POST</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>HTTP Header</strong></p></td>
<td style="text-align: left;"><pre><code>Authorization: Bearer eyJraWQ.ewogImL2pA10Qql22ddtutrvx4FsDlz.rHQjEmB1lLmpqn9J
X-AccessCode: 777bea0e13cc9c42ceec14aec3ddee2263325dc2c6c699db115f58fe423607ea</code></pre>
<div class="note">
<p>Mit dem ACCESS_TOKEN im <code>Authorization</code>-Header weist sich
der Zugreifende als Leistungerbringer aus, im Token ist seine Rolle als
Verordnender enthalten. Die Base64-Darstellung des Tokens ist stark
gekürzt.</p>
</div>
<div class="note">
<p>Der Zugreifende, der nicht der betroffene Versicherte ist, muss im
http-Header den <code>AccessCode</code> übergeben. Der
<code>AccessCode</code> ist dem Primärsystem des Verordnenden bekannt,
da von diesem aus das E-Rezept ursprünglich eingestellt wurde.</p>
</div>
<div class="note">
<p>Im http-Header des äußeren http-Requests an die VAU (POST /VAU) sind
die Header <code>X-erp-user: l</code> und
<code>X-erp-resource: Task</code> zu setzen.</p>
</div></td>
</tr>
</tbody>
</table>

**Response**

    HTTP/1.1 204 No Content

Im Ergebnis der $abort-Operation wird der referenzierte Task gelöscht.
Dementsprechend werden keine Daten an den aufrufenden Client
zurückgegeben.

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
<td style="text-align: left;"><p>204</p></td>
<td style="text-align: left;"><pre><code> No Content +
[small]#Die Anfrage wurde erfolgreich bearbeitet. Die Response enthält jedoch keine Daten.#</code></pre></td>
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
berechtigt ist. Beispielsweise ist das Rezept grade in Belieferung durch
eine Apotheke.</span></p></td>
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
<td style="text-align: left;"><p>410</p></td>
<td style="text-align: left;"><p>Gone<br />
<span class="small">Die angeforderte Ressource wird nicht länger
bereitgestellt und wurde dauerhaft entfernt.</span></p></td>
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
