Hier dokumentiert die gematik die Nutzung der Schnittstellen rund um das
E-Rezept aus Sicht der verordnenden Leistungserbringer.

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

![width=100%](../images/api_rezept_einstellen.png)

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

# E-Rezept erstellen

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
<span id="cb2-2"><a href="#cb2-2" aria-hidden="true" tabindex="-1"></a>  &lt;<span class="kw">parameter</span>&gt;</span>
<span id="cb2-3"><a href="#cb2-3" aria-hidden="true" tabindex="-1"></a>    &lt;<span class="kw">name</span><span class="ot"> value=</span><span class="st">&quot;workflowType&quot;</span>/&gt;</span>
<span id="cb2-4"><a href="#cb2-4" aria-hidden="true" tabindex="-1"></a>    &lt;<span class="kw">valueCoding</span>&gt;</span>
<span id="cb2-5"><a href="#cb2-5" aria-hidden="true" tabindex="-1"></a>      &lt;<span class="kw">system</span><span class="ot"> value=</span><span class="st">&quot;https://gematik.de/fhir/erp/CodeSystem/GEM_ERP_CS_FlowType&quot;</span>/&gt;</span>
<span id="cb2-6"><a href="#cb2-6" aria-hidden="true" tabindex="-1"></a>      &lt;<span class="kw">code</span><span class="ot"> value=</span><span class="st">&quot;160&quot;</span>/&gt;</span>
<span id="cb2-7"><a href="#cb2-7" aria-hidden="true" tabindex="-1"></a>    &lt;/<span class="kw">valueCoding</span>&gt;</span>
<span id="cb2-8"><a href="#cb2-8" aria-hidden="true" tabindex="-1"></a>  &lt;/<span class="kw">parameter</span>&gt;</span>
<span id="cb2-9"><a href="#cb2-9" aria-hidden="true" tabindex="-1"></a>&lt;/<span class="kw">Parameters</span>&gt;</span></code></pre></div>
<div class="note">
<p>Der Parameter <code>&lt;code value="*"/&gt;</code> steuert den Typ
des dem Task zugrunde liegenden Workflows. In Stufe 1 des E-Rezepts wird
das Muster16 umgesetzt. Daraus ergibt sich, dass der Versicherte diese
Rezepte nur in einer Apotheke einlösen kann.</p>
</div></td>
</tr>
</tbody>
</table>

**Response**

    HTTP/1.1 201 Created
    Content-Type: application/fhir+xml; charset=UTF-8

    <Task xmlns="http://hl7.org/fhir">
        <id value="160.123.456.789.123.58"/>
        <meta>
            <versionId value="1"/>
            <lastUpdated value="2020-03-02T08:26:21.594+00:00"/>
            <profile value="https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_PR_Task|1.2"/>
            <source value="#AsYR9plLkvONJAiv"/>
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
        <status value="draft"/>
        <intent value="order"/>
        <authoredOn value="2020-03-02T08:25:05+00:00"/>
        <lastModified value="2020-03-02T08:25:05+00:00"/>
        <performerType>
            <coding>
                <system value="urn:ietf:rfc:3986"/>
                <code value="urn:oid:1.2.276.0.76.4.54"/>
                <display value="Öffentliche Apotheke"/>
            </coding>
            <text value="Apotheke"/>
        </performerType>
    </Task>

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
</tbody>
</table>

# E-Rezept qualifiziert signieren

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

DEPRECATED KBV-Bundle, zulässig bis 30.06.2023. Da die Signatur nicht
verändert werden kann, wird hier noch ein altes KBV-Bundle beispielhaft
verwendet.

In den Profilen ist unter meta.profile auch die Version mit anzugeben.
(Bsp.:
"https://fhir.kbv.de/StructureDefinition/KBV\_PR\_ERP\_Bundle|**1.0.1**")

    <Bundle xmlns="http://hl7.org/fhir">
        <!-- Beispiel-Bundle Wirkstoffverordnung -->
        <id value="4fe2013d-ae94-441a-a1b1-78236ae65680" />
        <meta>
            <lastUpdated value="2020-05-04T08:30:00Z" />
            <profile value="https://fhir.kbv.de/StructureDefinition/KBV_PR_ERP_Bundle|1.0.1" />
        </meta>
        <identifier>
            <system value="https://gematik.de/fhir/NamingSystem/PrescriptionID" />
            <value value="160.123.456.789.123.58" />
        </identifier>
        <type value="document" />
        <timestamp value="2020-05-04T08:30:00Z" />
        <entry>
            <fullUrl value="http://pvs.praxis-topp-gluecklich.local/fhir/Composition/b0e22b86-e7e9-46c1-80fe-e6e24442d77c" />
            <resource>
                <Composition xmlns="http://hl7.org/fhir">
                    <id value="b0e22b86-e7e9-46c1-80fe-e6e24442d77c" />
                    <meta>
                        <profile value="https://fhir.kbv.de/StructureDefinition/KBV_PR_ERP_Composition|1.0.1" />
                    </meta>
                    <extension url="https://fhir.kbv.de/StructureDefinition/KBV_EX_FOR_Legal_basis">
                        <valueCoding>
                            <system value="https://fhir.kbv.de/CodeSystem/KBV_CS_SFHIR_KBV_STATUSKENNZEICHEN" />
                            <code value="00" />
                        </valueCoding>
                    </extension>
                    <status value="final" />
                    <type>
                        <coding>
                            <system value="https://fhir.kbv.de/CodeSystem/KBV_CS_SFHIR_KBV_FORMULAR_ART" />
                            <code value="e16A" />
                        </coding>
                    </type>
                    <subject>
                        <reference value="Patient/9774f67f-a238-4daf-b4e6-679deeef3811" />
                    </subject>
                    <date value="2020-02-03T11:30:02Z" />
                    <author>
                        <reference value="Practitioner/d8463daf-258e-4cad-a86a-6fd42fac161c" />
                        <type value="Practitioner" />
                    </author>
                    <author>
                        <type value="Device" />
                        <identifier>
                            <system value="https://fhir.kbv.de/NamingSystem/KBV_NS_FOR_Pruefnummer" />
                            <value value="Y/400/1910/36/346" />
                        </identifier>
                    </author>
                    <title value="elektronische Arzneimittelverordnung" />
                    <attester>
                        <mode value="legal" />
                        <party>
                            <reference value="Practitioner/20597e0e-cb2a-45b3-95f0-dc3dbdb617c3" />
                        </party>
                    </attester>
                    <custodian>
                        <reference value="Organization/cf042e44-086a-4d51-9c77-172f9a972e3b" />
                    </custodian>
                    <section>
                        <code>
                            <coding>
                                <system value="https://fhir.kbv.de/CodeSystem/KBV_CS_ERP_Section_Type" />
                                <code value="Prescription" />
                            </coding>
                        </code>
                        <entry>
                            <!-- Referenz auf Verordnung (MedicationRequest) -->
                            <reference value="MedicationRequest/f58f4403-7a3a-4a12-bb15-b2fa25b02561" />
                        </entry>
                    </section>
                    <section>
                        <code>
                            <coding>
                                <system value="https://fhir.kbv.de/CodeSystem/KBV_CS_ERP_Section_Type" />
                                <code value="Coverage" />
                            </coding>
                        </code>
                        <entry>
                            <!-- Referenz auf Krankenkasse/KostentrĂ¤ger  -->
                            <reference value="Coverage/1b1ffb6e-eb05-43d7-87eb-e7818fe9661a" />
                        </entry>
                    </section>
                </Composition>
            </resource>
        </entry>
        <entry>
            <fullUrl value="http://pvs.praxis-topp-gluecklich.local/fhir/MedicationRequest/f58f4403-7a3a-4a12-bb15-b2fa25b02561" />
            <resource>
                <MedicationRequest xmlns="http://hl7.org/fhir">
                    <id value="f58f4403-7a3a-4a12-bb15-b2fa25b02561" />
                    <meta>
                        <profile value="https://fhir.kbv.de/StructureDefinition/KBV_PR_ERP_Prescription|1.0.1" />
                    </meta>
                    <extension url="https://fhir.kbv.de/StructureDefinition/KBV_EX_ERP_StatusCoPayment">
                        <valueCoding>
                            <system value="https://fhir.kbv.de/CodeSystem/KBV_CS_ERP_StatusCoPayment" />
                            <code value="0" />
                        </valueCoding>
                    </extension>
                    <extension url="https://fhir.kbv.de/StructureDefinition/KBV_EX_ERP_EmergencyServicesFee">
                        <valueBoolean value="false" />
                    </extension>
                    <extension url="https://fhir.kbv.de/StructureDefinition/KBV_EX_ERP_BVG">
                        <valueBoolean value="false" />
                    </extension>
                    <extension url="https://fhir.kbv.de/StructureDefinition/KBV_EX_ERP_Accident">
                        <extension url="unfallkennzeichen">
                            <valueCoding>
                                <system value="https://fhir.kbv.de/CodeSystem/KBV_CS_FOR_Ursache_Type" />
                                <code value="1" />
                            </valueCoding>
                        </extension>
                        <extension url="unfalltag">
                            <valueDate value="2020-05-01" />
                        </extension>
                    </extension>
                    <extension url="https://fhir.kbv.de/StructureDefinition/KBV_EX_ERP_Multiple_Prescription">
                        <extension url="Kennzeichen">
                            <valueBoolean value="true" />
                        </extension>
                        <extension url="Nummerierung">
                            <valueRatio>
                                <numerator>
                                    <value value="2" />
                                </numerator>
                                <denominator>
                                    <value value="4" />
                                </denominator>
                            </valueRatio>
                        </extension>
                        <extension url="Zeitraum">
                            <valuePeriod>
                                <start value="2021-01-02" />
                                <end value="2021-03-30" />
                            </valuePeriod>
                        </extension>
                    </extension>
                    <status value="active" />
                    <intent value="order" />
                    <medicationReference>
                        <reference value="Medication/e3a4efa7-84fc-465b-b14c-720195097783" />
                    </medicationReference>
                    <subject>
                        <reference value="Patient/9774f67f-a238-4daf-b4e6-679deeef3811" />
                    </subject>
                    <authoredOn value="2020-05-02" />
                    <requester>
                        <reference value="Practitioner/20597e0e-cb2a-45b3-95f0-dc3dbdb617c3" />
                    </requester>
                    <insurance>
                        <reference value="Coverage/1b1ffb6e-eb05-43d7-87eb-e7818fe9661a" />
                    </insurance>
                    <note>
                        <text value="Dummy-Hinweis für die Apotheke" />
                    </note>
                    <dosageInstruction>
                        <extension url="https://fhir.kbv.de/StructureDefinition/KBV_EX_ERP_DosageFlag">
                            <valueBoolean value="false" />
                        </extension>
                    </dosageInstruction>
                    <dispenseRequest>
                        <quantity>
                            <value value="2" />
                            <system value="http://unitsofmeasure.org" />
                            <code value="{Package}" />
                        </quantity>
                    </dispenseRequest>
                    <substitution>
                        <allowedBoolean value="true" />
                    </substitution>
                </MedicationRequest>
            </resource>
        </entry>
        <entry>
            <fullUrl value="http://pvs.praxis-topp-gluecklich.local/fhir/Medication/e3a4efa7-84fc-465b-b14c-720195097783" />
            <resource>
                <Medication xmlns="http://hl7.org/fhir">
                    <id value="e3a4efa7-84fc-465b-b14c-720195097783" />
                    <meta>
                        <profile value="https://fhir.kbv.de/StructureDefinition/KBV_PR_ERP_Medication_Ingredient|1.0.1" />
                    </meta>
                    <extension url="https://fhir.kbv.de/StructureDefinition/KBV_EX_ERP_Medication_Category">
                        <valueCoding>
                            <system value="https://fhir.kbv.de/CodeSystem/KBV_CS_ERP_Medication_Category" />
                            <code value="00" />
                        </valueCoding>
                    </extension>
                    <extension url="https://fhir.kbv.de/StructureDefinition/KBV_EX_ERP_Medication_Vaccine">
                        <valueBoolean value="false" />
                    </extension>
                    <code>
                        <coding>
                            <system value="https://fhir.kbv.de/CodeSystem/KBV_CS_ERP_Medication_Type" />
                            <code value="wirkstoff" />
                        </coding>
                    </code>
                    <form>
                        <text value="Tabletten" />
                    </form>
                    <amount>
                        <numerator>
                            <value value="20" />
                            <unit value="Stk" />
                        </numerator>
                        <denominator>
                            <value value="1" />
                        </denominator>
                    </amount>
                    <ingredient>
                        <itemCodeableConcept>
                            <coding>
                                <system value="http://fhir.de/CodeSystem/ask" />
                                <code value="Dummy-ASK" />
                            </coding>
                            <text value="Ibuprofen" />
                        </itemCodeableConcept>
                        <strength>
                            <numerator>
                                <value value="800" />
                                <unit value="mg" />
                            </numerator>
                            <denominator>
                                <value value="1" />
                            </denominator>
                        </strength>
                    </ingredient>
                </Medication>
            </resource>
        </entry>
        <entry>
            <fullUrl value="http://pvs.praxis-topp-gluecklich.local/fhir/Patient/9774f67f-a238-4daf-b4e6-679deeef3811" />
            <resource>
                <Patient xmlns="http://hl7.org/fhir">
                    <id value="9774f67f-a238-4daf-b4e6-679deeef3811" />
                    <meta>
                        <profile value="https://fhir.kbv.de/StructureDefinition/KBV_PR_FOR_Patient|1.0.3" />
                    </meta>
                    <identifier>
                        <type>
                            <coding>
                                <system value="http://fhir.de/CodeSystem/identifier-type-de-basis" />
                                <code value="GKV" />
                            </coding>
                        </type>
                        <system value="http://fhir.de/NamingSystem/gkv/kvid-10" />
                        <value value="X234567890" />
                    </identifier>
                    <name>
                        <use value="official" />
                        <family value="Ludger Königsstein">
                            <extension url="http://hl7.org/fhir/StructureDefinition/humanname-own-name">
                                <valueString value="Königsstein" />
                            </extension>
                        </family>
                        <given value="Ludger" />
                    </name>
                    <birthDate value="1935-06-22" />
                    <address>
                        <type value="both" />
                        <line value="Musterstr. 1">
                            <extension url="http://hl7.org/fhir/StructureDefinition/iso21090-ADXP-houseNumber">
                                <valueString value="1" />
                            </extension>
                            <extension url="http://hl7.org/fhir/StructureDefinition/iso21090-ADXP-streetName">
                                <valueString value="Musterstr." />
                            </extension>
                        </line>
                        <city value="Berlin" />
                        <postalCode value="10623" />
                    </address>
                </Patient>
            </resource>
        </entry>
        <entry>
            <fullUrl value="http://pvs.praxis-topp-gluecklich.local/fhir/Practitioner/20597e0e-cb2a-45b3-95f0-dc3dbdb617c3" />
            <resource>
                <Practitioner xmlns="http://hl7.org/fhir">
                    <id value="20597e0e-cb2a-45b3-95f0-dc3dbdb617c3" />
                    <meta>
                        <profile value="https://fhir.kbv.de/StructureDefinition/KBV_PR_FOR_Practitioner|1.0.3" />
                    </meta>
                    <identifier>
                        <type>
                            <coding>
                                <system value="http://terminology.hl7.org/CodeSystem/v2-0203" />
                                <code value="LANR" />
                            </coding>
                        </type>
                        <system value="https://fhir.kbv.de/NamingSystem/KBV_NS_Base_ANR" />
                        <value value="838382202" />
                    </identifier>
                    <name>
                        <use value="official" />
                        <family value="Topp-Glücklich">
                            <extension url="http://hl7.org/fhir/StructureDefinition/humanname-own-name">
                                <valueString value="Topp-Glücklich" />
                            </extension>
                        </family>
                        <given value="Hans" />
                        <prefix value="Dr. med.">
                            <extension url="http://hl7.org/fhir/StructureDefinition/iso21090-EN-qualifier">
                                <valueCode value="AC" />
                            </extension>
                        </prefix>
                    </name>
                    <qualification>
                        <code>
                            <coding>
                                <system value="https://fhir.kbv.de/CodeSystem/KBV_CS_FOR_Qualification_Type" />
                                <code value="00" />
                            </coding>
                        </code>
                    </qualification>
                    <qualification>
                        <code>
                            <text value="Hausarzt" />
                        </code>
                    </qualification>
                </Practitioner>
            </resource>
        </entry>
        <entry>
            <fullUrl value="http://pvs.praxis-topp-gluecklich.local/fhir/Practitioner/d8463daf-258e-4cad-a86a-6fd42fac161c" />
            <resource>
                <Practitioner xmlns="http://hl7.org/fhir">
                    <id value="d8463daf-258e-4cad-a86a-6fd42fac161c" />
                    <meta>
                        <profile value="https://fhir.kbv.de/StructureDefinition/KBV_PR_FOR_Practitioner|1.0.3" />
                    </meta>
                    <identifier>
                        <type>
                            <coding>
                                <system value="http://terminology.hl7.org/CodeSystem/v2-0203" />
                                <code value="LANR" />
                            </coding>
                        </type>
                        <system value="https://fhir.kbv.de/NamingSystem/KBV_NS_Base_ANR" />
                        <value value="838382210" />
                    </identifier>
                    <name>
                        <use value="official" />
                        <family value="Meier">
                            <extension url="http://hl7.org/fhir/StructureDefinition/humanname-own-name">
                                <valueString value="Meier" />
                            </extension>
                        </family>
                        <given value="Jörgen" />
                    </name>
                    <qualification>
                        <code>
                            <coding>
                                <system value="https://fhir.kbv.de/CodeSystem/KBV_CS_FOR_Qualification_Type" />
                                <code value="03" />
                            </coding>
                        </code>
                    </qualification>
                    <qualification>
                        <code>
                            <text value="Arzt in Weiterbildung" />
                        </code>
                    </qualification>
                </Practitioner>
            </resource>
        </entry>
        <entry>
            <fullUrl value="http://pvs.praxis-topp-gluecklich.local/fhir/Organization/cf042e44-086a-4d51-9c77-172f9a972e3b" />
            <resource>
                <Organization xmlns="http://hl7.org/fhir">
                    <id value="cf042e44-086a-4d51-9c77-172f9a972e3b" />
                    <meta>
                        <profile value="https://fhir.kbv.de/StructureDefinition/KBV_PR_FOR_Organization|1.0.3" />
                    </meta>
                    <identifier>
                        <type>
                            <coding>
                                <system value="http://terminology.hl7.org/CodeSystem/v2-0203" />
                                <code value="BSNR" />
                            </coding>
                        </type>
                        <system value="https://fhir.kbv.de/NamingSystem/KBV_NS_Base_BSNR" />
                        <value value="031234567" />
                    </identifier>
                    <name value="Hausarztpraxis Dr. Topp-Glücklich" />
                    <telecom>
                        <system value="phone" />
                        <value value="0301234567" />
                    </telecom>
                    <address>
                        <type value="both" />
                        <line value="Musterstr. 2">
                            <extension url="http://hl7.org/fhir/StructureDefinition/iso21090-ADXP-houseNumber">
                                <valueString value="2" />
                            </extension>
                            <extension url="http://hl7.org/fhir/StructureDefinition/iso21090-ADXP-streetName">
                                <valueString value="Musterstr." />
                            </extension>
                        </line>
                        <city value="Berlin" />
                        <postalCode value="10623" />
                    </address>
                </Organization>
            </resource>
        </entry>
        <entry>
            <fullUrl value="http://pvs.praxis-topp-gluecklich.local/fhir/Coverage/1b1ffb6e-eb05-43d7-87eb-e7818fe9661a" />
            <resource>
                <Coverage xmlns="http://hl7.org/fhir">
                    <id value="1b1ffb6e-eb05-43d7-87eb-e7818fe9661a" />
                    <meta>
                        <profile value="https://fhir.kbv.de/StructureDefinition/KBV_PR_FOR_Coverage|1.0.3" />
                    </meta>
                    <extension url="http://fhir.de/StructureDefinition/gkv/besondere-personengruppe">
                        <valueCoding>
                            <system value="https://fhir.kbv.de/CodeSystem/KBV_CS_SFHIR_KBV_PERSONENGRUPPE" />
                            <code value="00" />
                        </valueCoding>
                    </extension>
                    <extension url="http://fhir.de/StructureDefinition/gkv/dmp-kennzeichen">
                        <valueCoding>
                            <system value="https://fhir.kbv.de/CodeSystem/KBV_CS_SFHIR_KBV_DMP" />
                            <code value="00" />
                        </valueCoding>
                    </extension>
                    <extension url="http://fhir.de/StructureDefinition/gkv/wop">
                        <valueCoding>
                            <system value="https://fhir.kbv.de/CodeSystem/KBV_CS_SFHIR_ITA_WOP" />
                            <code value="03" />
                        </valueCoding>
                    </extension>
                    <extension url="http://fhir.de/StructureDefinition/gkv/versichertenart">
                        <valueCoding>
                            <system value="https://fhir.kbv.de/CodeSystem/KBV_CS_SFHIR_KBV_VERSICHERTENSTATUS" />
                            <code value="1" />
                        </valueCoding>
                    </extension>
                    <status value="active" />
                    <type>
                        <coding>
                            <system value="http://fhir.de/CodeSystem/versicherungsart-de-basis" />
                            <code value="GKV" />
                        </coding>
                    </type>
                    <beneficiary>
                        <reference value="Patient/9774f67f-a238-4daf-b4e6-679deeef3811" />
                    </beneficiary>
                    <payor>
                        <identifier>
                            <system value="http://fhir.de/NamingSystem/arge-ik/iknr" />
                            <value value="104212059" />
                        </identifier>
                        <display value="AOK Rheinland/Hamburg" />
                    </payor>
                </Coverage>
            </resource>
        </entry>
    </Bundle>

Dieses E-Rezept-Bundle in XML-Darstellung muss nun digital
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
class="sourceCode xml"><code class="sourceCode xml"><span id="cb2-1"><a href="#cb2-1" aria-hidden="true" tabindex="-1"></a><span class="fu">&lt;?xml</span><span class="ot"> version=</span><span class="st">&quot;1.0&quot;</span><span class="ot"> encoding=</span><span class="st">&quot;utf-8&quot;</span><span class="fu">?&gt;</span></span>
<span id="cb2-2"><a href="#cb2-2" aria-hidden="true" tabindex="-1"></a>&lt;<span class="kw">SOAP-ENV:Envelope</span><span class="ot"> xmlns:SOAP-ENV=</span><span class="st">&quot;http://schemas.xmlsoap.org/soap/envelope/&quot;</span></span>
<span id="cb2-3"><a href="#cb2-3" aria-hidden="true" tabindex="-1"></a><span class="ot">    xmlns:SOAP-ENC=</span><span class="st">&quot;http://schemas.xmlsoap.org/soap/encoding/&quot;</span></span>
<span id="cb2-4"><a href="#cb2-4" aria-hidden="true" tabindex="-1"></a><span class="ot">    xmlns:xsi=</span><span class="st">&quot;http://www.w3.org/2001/XMLSchema-instance&quot;</span></span>
<span id="cb2-5"><a href="#cb2-5" aria-hidden="true" tabindex="-1"></a><span class="ot">    xmlns:xsd=</span><span class="st">&quot;http://www.w3.org/2001/XMLSchema&quot;</span></span>
<span id="cb2-6"><a href="#cb2-6" aria-hidden="true" tabindex="-1"></a><span class="ot">    xmlns:m0=</span><span class="st">&quot;http://ws.gematik.de/conn/ConnectorCommon/v5.0&quot;</span></span>
<span id="cb2-7"><a href="#cb2-7" aria-hidden="true" tabindex="-1"></a><span class="ot">    xmlns:m1=</span><span class="st">&quot;http://ws.gematik.de/conn/ConnectorContext/v2.0&quot;</span></span>
<span id="cb2-8"><a href="#cb2-8" aria-hidden="true" tabindex="-1"></a><span class="ot">    xmlns:m2=</span><span class="st">&quot;urn:oasis:names:tc:dss:1.0:core:schema&quot;</span></span>
<span id="cb2-9"><a href="#cb2-9" aria-hidden="true" tabindex="-1"></a><span class="ot">    xmlns:m3=</span><span class="st">&quot;http://www.w3.org/2000/09/xmldsig#&quot;</span></span>
<span id="cb2-10"><a href="#cb2-10" aria-hidden="true" tabindex="-1"></a><span class="ot">    xmlns:m4=</span><span class="st">&quot;urn:oasis:names:tc:dss-x:1.0:profiles:SignaturePolicy:schema#&quot;</span>&gt;</span>
<span id="cb2-11"><a href="#cb2-11" aria-hidden="true" tabindex="-1"></a>    &lt;<span class="kw">SOAP-ENV:Body</span>&gt;</span>
<span id="cb2-12"><a href="#cb2-12" aria-hidden="true" tabindex="-1"></a>        &lt;<span class="kw">m:SignDocument</span><span class="ot"> xmlns:m=</span><span class="st">&quot;http://ws.gematik.de/conn/SignatureService/v7.4&quot;</span>&gt;</span>
<span id="cb2-13"><a href="#cb2-13" aria-hidden="true" tabindex="-1"></a>            &lt;<span class="kw">m0:CardHandle</span>&gt;HBA-5&lt;/<span class="kw">m0:CardHandle</span>&gt;</span>
<span id="cb2-14"><a href="#cb2-14" aria-hidden="true" tabindex="-1"></a>            &lt;<span class="kw">m1:Context</span>&gt;</span>
<span id="cb2-15"><a href="#cb2-15" aria-hidden="true" tabindex="-1"></a>                &lt;<span class="kw">m0:MandantId</span>&gt;Mandant1&lt;/<span class="kw">m0:MandantId</span>&gt;</span>
<span id="cb2-16"><a href="#cb2-16" aria-hidden="true" tabindex="-1"></a>                &lt;<span class="kw">m0:ClientSystemId</span>&gt;ClientID1&lt;/<span class="kw">m0:ClientSystemId</span>&gt;</span>
<span id="cb2-17"><a href="#cb2-17" aria-hidden="true" tabindex="-1"></a>                &lt;<span class="kw">m0:WorkplaceId</span>&gt;CATS&lt;/<span class="kw">m0:WorkplaceId</span>&gt;</span>
<span id="cb2-18"><a href="#cb2-18" aria-hidden="true" tabindex="-1"></a>                &lt;<span class="kw">m0:UserId</span>&gt;197610&lt;/<span class="kw">m0:UserId</span>&gt;</span>
<span id="cb2-19"><a href="#cb2-19" aria-hidden="true" tabindex="-1"></a>            &lt;/<span class="kw">m1:Context</span>&gt;</span>
<span id="cb2-20"><a href="#cb2-20" aria-hidden="true" tabindex="-1"></a>            &lt;<span class="kw">m:TvMode</span>&gt;NONE&lt;/<span class="kw">m:TvMode</span>&gt;</span>
<span id="cb2-21"><a href="#cb2-21" aria-hidden="true" tabindex="-1"></a>            &lt;<span class="kw">m:JobNumber</span>&gt;MMD-636&lt;/<span class="kw">m:JobNumber</span>&gt;</span>
<span id="cb2-22"><a href="#cb2-22" aria-hidden="true" tabindex="-1"></a>            &lt;<span class="kw">m:SignRequest</span><span class="ot"> RequestID=</span><span class="st">&quot;Doc1&quot;</span>&gt;</span>
<span id="cb2-23"><a href="#cb2-23" aria-hidden="true" tabindex="-1"></a>                &lt;<span class="kw">m:OptionalInputs</span>&gt;</span>
<span id="cb2-24"><a href="#cb2-24" aria-hidden="true" tabindex="-1"></a>                    &lt;<span class="kw">m2:SignatureType</span>&gt;urn:ietf:rfc:5652&lt;/<span class="kw">m2:SignatureType</span>&gt;</span>
<span id="cb2-25"><a href="#cb2-25" aria-hidden="true" tabindex="-1"></a>                    &lt;<span class="kw">m:IncludeEContent</span>&gt;true&lt;/<span class="kw">m:IncludeEContent</span>&gt;</span>
<span id="cb2-26"><a href="#cb2-26" aria-hidden="true" tabindex="-1"></a>                &lt;/<span class="kw">m:OptionalInputs</span>&gt;</span>
<span id="cb2-27"><a href="#cb2-27" aria-hidden="true" tabindex="-1"></a>                &lt;<span class="kw">m:Document</span><span class="ot"> ID=</span><span class="st">&quot;CMS-Doc1&quot;</span><span class="ot"> ShortText=</span><span class="st">&quot;a CMSDocument2sign&quot;</span>&gt;</span>
<span id="cb2-28"><a href="#cb2-28" aria-hidden="true" tabindex="-1"></a>                    &lt;<span class="kw">m2:Base64Data</span><span class="ot"> MimeType=</span><span class="st">&quot;text/plain; charset=utf-8&quot;</span>&gt;PEJ1bmRsZSB4bWxucz0iaHR0cDovL2hsNy5vcmcvZmhpciI+DQogIDwhLS0gQmVpc3BpZWwtQnVu</span>
<span id="cb2-29"><a href="#cb2-29" aria-hidden="true" tabindex="-1"></a>ZGxlIFdpcmtzdG9mZnZlcm9yZG51bmcgLS0+DQogIDxpZCB2YWx1ZT0iNGZlMjAxM2QtYWU5NC00</span>
<span id="cb2-30"><a href="#cb2-30" aria-hidden="true" tabindex="-1"></a>NDFhLWExYjEtNzgyMzZhZTY1NjgwIiAvPg0KICA8bWV0YT4NCiAgICA8bGFzdFVwZGF0ZWQgdmFs</span>
<span id="cb2-31"><a href="#cb2-31" aria-hidden="true" tabindex="-1"></a>dWU9IjIwMjAtMDUtMDRUMDg6MzA6MDBaIiAvPg0KICAgIDxwcm9maWxlIHZhbHVlPSJodHRwczov</span>
<span id="cb2-32"><a href="#cb2-32" aria-hidden="true" tabindex="-1"></a>L2ZoaXIua2J2LmRlL1N0cnVjdHVyZURlZmluaXRpb24vS0JWX1BSX0VSUF9CdW5kbGV8MS4wLjEi</span>
<span id="cb2-33"><a href="#cb2-33" aria-hidden="true" tabindex="-1"></a>IC8+DQogIDwvbWV0YT4NCiAgPGlkZW50aWZpZXI+DQogICAgPHN5c3RlbSB2YWx1ZT0iaHR0cHM6</span>
<span id="cb2-34"><a href="#cb2-34" aria-hidden="true" tabindex="-1"></a>Ly9nZW1hdGlrLmRlL2ZoaXIvTmFtaW5nU3lzdGVtL1ByZXNjcmlwdGlvbklEIiAvPg0KICAgIDx2</span>
<span id="cb2-35"><a href="#cb2-35" aria-hidden="true" tabindex="-1"></a>YWx1ZSB2YWx1ZT0iMTYwLjEyMy40NTYuNzg5LjEyMy41OCIgLz4NCiAgPC9pZGVudGlmaWVyPg0K</span>
<span id="cb2-36"><a href="#cb2-36" aria-hidden="true" tabindex="-1"></a>ICA8dHlwZSB2YWx1ZT0iZG9jdW1lbnQiIC8+DQogIDx0aW1lc3RhbXAgdmFsdWU9IjIwMjAtMDUt</span>
<span id="cb2-37"><a href="#cb2-37" aria-hidden="true" tabindex="-1"></a>MDRUMDg6MzA6MDBaIiAvPg0KICA8ZW50cnk+DQogICAgPGZ1bGxVcmwgdmFsdWU9Imh0dHA6Ly9w</span>
<span id="cb2-38"><a href="#cb2-38" aria-hidden="true" tabindex="-1"></a>dnMucHJheGlzLXRvcHAtZ2x1ZWNrbGljaC5sb2NhbC9maGlyL0NvbXBvc2l0aW9uL2IwZTIyYjg2</span>
<span id="cb2-39"><a href="#cb2-39" aria-hidden="true" tabindex="-1"></a>LWU3ZTktNDZjMS04MGZlLWU2ZTI0NDQyZDc3YyIgLz4NCiAgICA8cmVzb3VyY2U+DQogICAgICA8</span>
<span id="cb2-40"><a href="#cb2-40" aria-hidden="true" tabindex="-1"></a>Q29tcG9zaXRpb24geG1sbnM9Imh0dHA6Ly9obDcub3JnL2ZoaXIiPg0KICAgICAgICA8aWQgdmFs</span>
<span id="cb2-41"><a href="#cb2-41" aria-hidden="true" tabindex="-1"></a>dWU9ImIwZTIyYjg2LWU3ZTktNDZjMS04MGZlLWU2ZTI0NDQyZDc3YyIgLz4NCiAgICAgICAgPG1l</span>
<span id="cb2-42"><a href="#cb2-42" aria-hidden="true" tabindex="-1"></a>dGE+DQogICAgICAgICAgPHByb2ZpbGUgdmFsdWU9Imh0dHBzOi8vZmhpci5rYnYuZGUvU3RydWN0</span>
<span id="cb2-43"><a href="#cb2-43" aria-hidden="true" tabindex="-1"></a>dXJlRGVmaW5pdGlvbi9LQlZfUFJfRVJQX0NvbXBvc2l0aW9ufDEuMC4xIiAvPg0KICAgICAgICA8</span>
<span id="cb2-44"><a href="#cb2-44" aria-hidden="true" tabindex="-1"></a>L21ldGE+DQogICAgICAgIDxleHRlbnNpb24gdXJsPSJodHRwczovL2ZoaXIua2J2LmRlL1N0cnVj</span>
<span id="cb2-45"><a href="#cb2-45" aria-hidden="true" tabindex="-1"></a>dHVyZURlZmluaXRpb24vS0JWX0VYX0ZPUl9MZWdhbF9iYXNpcyI+DQogICAgICAgICAgPHZhbHVl</span>
<span id="cb2-46"><a href="#cb2-46" aria-hidden="true" tabindex="-1"></a>Q29kaW5nPg0KICAgICAgICAgICAgPHN5c3RlbSB2YWx1ZT0iaHR0cHM6Ly9maGlyLmtidi5kZS9D</span>
<span id="cb2-47"><a href="#cb2-47" aria-hidden="true" tabindex="-1"></a>b2RlU3lzdGVtL0tCVl9DU19TRkhJUl9LQlZfU1RBVFVTS0VOTlpFSUNIRU4iIC8+DQogICAgICAg</span>
<span id="cb2-48"><a href="#cb2-48" aria-hidden="true" tabindex="-1"></a>ICAgICA8Y29kZSB2YWx1ZT0iMDAiIC8+DQogICAgICAgICAgPC92YWx1ZUNvZGluZz4NCiAgICAg</span>
<span id="cb2-49"><a href="#cb2-49" aria-hidden="true" tabindex="-1"></a>ICAgPC9leHRlbnNpb24+DQogICAgICAgIDxzdGF0dXMgdmFsdWU9ImZpbmFsIiAvPg0KICAgICAg</span>
<span id="cb2-50"><a href="#cb2-50" aria-hidden="true" tabindex="-1"></a>ICA8dHlwZT4NCiAgICAgICAgICA8Y29kaW5nPg0KICAgICAgICAgICAgPHN5c3RlbSB2YWx1ZT0i</span>
<span id="cb2-51"><a href="#cb2-51" aria-hidden="true" tabindex="-1"></a>aHR0cHM6Ly9maGlyLmtidi5kZS9Db2RlU3lzdGVtL0tCVl9DU19TRkhJUl9LQlZfRk9STVVMQVJf</span>
<span id="cb2-52"><a href="#cb2-52" aria-hidden="true" tabindex="-1"></a>QVJUIiAvPg0KICAgICAgICAgICAgPGNvZGUgdmFsdWU9ImUxNkEiIC8+DQogICAgICAgICAgPC9j</span>
<span id="cb2-53"><a href="#cb2-53" aria-hidden="true" tabindex="-1"></a>b2Rpbmc+DQogICAgICAgIDwvdHlwZT4NCiAgICAgICAgPHN1YmplY3Q+DQogICAgICAgICAgPHJl</span>
<span id="cb2-54"><a href="#cb2-54" aria-hidden="true" tabindex="-1"></a>ZmVyZW5jZSB2YWx1ZT0iUGF0aWVudC85Nzc0ZjY3Zi1hMjM4LTRkYWYtYjRlNi02NzlkZWVlZjM4</span>
<span id="cb2-55"><a href="#cb2-55" aria-hidden="true" tabindex="-1"></a>MTEiIC8+DQogICAgICAgIDwvc3ViamVjdD4NCiAgICAgICAgPGRhdGUgdmFsdWU9IjIwMjAtMDIt</span>
<span id="cb2-56"><a href="#cb2-56" aria-hidden="true" tabindex="-1"></a>MDNUMTE6MzA6MDJaIiAvPg0KICAgICAgICA8YXV0aG9yPg0KICAgICAgICAgIDxyZWZlcmVuY2Ug</span>
<span id="cb2-57"><a href="#cb2-57" aria-hidden="true" tabindex="-1"></a>dmFsdWU9IlByYWN0aXRpb25lci9kODQ2M2RhZi0yNThlLTRjYWQtYTg2YS02ZmQ0MmZhYzE2MWMi</span>
<span id="cb2-58"><a href="#cb2-58" aria-hidden="true" tabindex="-1"></a>IC8+DQogICAgICAgICAgPHR5cGUgdmFsdWU9IlByYWN0aXRpb25lciIgLz4NCiAgICAgICAgPC9h</span>
<span id="cb2-59"><a href="#cb2-59" aria-hidden="true" tabindex="-1"></a>dXRob3I+DQogICAgICAgIDxhdXRob3I+DQogICAgICAgICAgPHR5cGUgdmFsdWU9IkRldmljZSIg</span>
<span id="cb2-60"><a href="#cb2-60" aria-hidden="true" tabindex="-1"></a>Lz4NCiAgICAgICAgICA8aWRlbnRpZmllcj4NCiAgICAgICAgICAgIDxzeXN0ZW0gdmFsdWU9Imh0</span>
<span id="cb2-61"><a href="#cb2-61" aria-hidden="true" tabindex="-1"></a>dHBzOi8vZmhpci5rYnYuZGUvTmFtaW5nU3lzdGVtL0tCVl9OU19GT1JfUHJ1ZWZudW1tZXIiIC8+</span>
<span id="cb2-62"><a href="#cb2-62" aria-hidden="true" tabindex="-1"></a>DQogICAgICAgICAgICA8dmFsdWUgdmFsdWU9IlkvNDAwLzE5MTAvMzYvMzQ2IiAvPg0KICAgICAg</span>
<span id="cb2-63"><a href="#cb2-63" aria-hidden="true" tabindex="-1"></a>ICAgIDwvaWRlbnRpZmllcj4NCiAgICAgICAgPC9hdXRob3I+DQogICAgICAgIDx0aXRsZSB2YWx1</span>
<span id="cb2-64"><a href="#cb2-64" aria-hidden="true" tabindex="-1"></a>ZT0iZWxla3Ryb25pc2NoZSBBcnpuZWltaXR0ZWx2ZXJvcmRudW5nIiAvPg0KICAgICAgICA8YXR0</span>
<span id="cb2-65"><a href="#cb2-65" aria-hidden="true" tabindex="-1"></a>ZXN0ZXI+DQogICAgICAgICAgPG1vZGUgdmFsdWU9ImxlZ2FsIiAvPg0KICAgICAgICAgIDxwYXJ0</span>
<span id="cb2-66"><a href="#cb2-66" aria-hidden="true" tabindex="-1"></a>eT4NCiAgICAgICAgICAgIDxyZWZlcmVuY2UgdmFsdWU9IlByYWN0aXRpb25lci8yMDU5N2UwZS1j</span>
<span id="cb2-67"><a href="#cb2-67" aria-hidden="true" tabindex="-1"></a>YjJhLTQ1YjMtOTVmMC1kYzNkYmRiNjE3YzMiIC8+DQogICAgICAgICAgPC9wYXJ0eT4NCiAgICAg</span>
<span id="cb2-68"><a href="#cb2-68" aria-hidden="true" tabindex="-1"></a>ICAgPC9hdHRlc3Rlcj4NCiAgICAgICAgPGN1c3RvZGlhbj4NCiAgICAgICAgICA8cmVmZXJlbmNl</span>
<span id="cb2-69"><a href="#cb2-69" aria-hidden="true" tabindex="-1"></a>IHZhbHVlPSJPcmdhbml6YXRpb24vY2YwNDJlNDQtMDg2YS00ZDUxLTljNzctMTcyZjlhOTcyZTNi</span>
<span id="cb2-70"><a href="#cb2-70" aria-hidden="true" tabindex="-1"></a>IiAvPg0KICAgICAgICA8L2N1c3RvZGlhbj4NCiAgICAgICAgPHNlY3Rpb24+DQogICAgICAgICAg</span>
<span id="cb2-71"><a href="#cb2-71" aria-hidden="true" tabindex="-1"></a>PGNvZGU+DQogICAgICAgICAgICA8Y29kaW5nPg0KICAgICAgICAgICAgICA8c3lzdGVtIHZhbHVl</span>
<span id="cb2-72"><a href="#cb2-72" aria-hidden="true" tabindex="-1"></a>PSJodHRwczovL2ZoaXIua2J2LmRlL0NvZGVTeXN0ZW0vS0JWX0NTX0VSUF9TZWN0aW9uX1R5cGUi</span>
<span id="cb2-73"><a href="#cb2-73" aria-hidden="true" tabindex="-1"></a>IC8+DQogICAgICAgICAgICAgIDxjb2RlIHZhbHVlPSJQcmVzY3JpcHRpb24iIC8+DQogICAgICAg</span>
<span id="cb2-74"><a href="#cb2-74" aria-hidden="true" tabindex="-1"></a>ICAgICA8L2NvZGluZz4NCiAgICAgICAgICA8L2NvZGU+DQogICAgICAgICAgPGVudHJ5Pg0KICAg</span>
<span id="cb2-75"><a href="#cb2-75" aria-hidden="true" tabindex="-1"></a>ICAgICAgICAgPCEtLSBSZWZlcmVueiBhdWYgVmVyb3JkbnVuZyAoTWVkaWNhdGlvblJlcXVlc3Qp</span>
<span id="cb2-76"><a href="#cb2-76" aria-hidden="true" tabindex="-1"></a>IC0tPg0KICAgICAgICAgICAgPHJlZmVyZW5jZSB2YWx1ZT0iTWVkaWNhdGlvblJlcXVlc3QvZjU4</span>
<span id="cb2-77"><a href="#cb2-77" aria-hidden="true" tabindex="-1"></a>ZjQ0MDMtN2EzYS00YTEyLWJiMTUtYjJmYTI1YjAyNTYxIiAvPg0KICAgICAgICAgIDwvZW50cnk+</span>
<span id="cb2-78"><a href="#cb2-78" aria-hidden="true" tabindex="-1"></a>DQogICAgICAgIDwvc2VjdGlvbj4NCiAgICAgICAgPHNlY3Rpb24+DQogICAgICAgICAgPGNvZGU+</span>
<span id="cb2-79"><a href="#cb2-79" aria-hidden="true" tabindex="-1"></a>DQogICAgICAgICAgICA8Y29kaW5nPg0KICAgICAgICAgICAgICA8c3lzdGVtIHZhbHVlPSJodHRw</span>
<span id="cb2-80"><a href="#cb2-80" aria-hidden="true" tabindex="-1"></a>czovL2ZoaXIua2J2LmRlL0NvZGVTeXN0ZW0vS0JWX0NTX0VSUF9TZWN0aW9uX1R5cGUiIC8+DQog</span>
<span id="cb2-81"><a href="#cb2-81" aria-hidden="true" tabindex="-1"></a>ICAgICAgICAgICAgIDxjb2RlIHZhbHVlPSJDb3ZlcmFnZSIgLz4NCiAgICAgICAgICAgIDwvY29k</span>
<span id="cb2-82"><a href="#cb2-82" aria-hidden="true" tabindex="-1"></a>aW5nPg0KICAgICAgICAgIDwvY29kZT4NCiAgICAgICAgICA8ZW50cnk+DQogICAgICAgICAgICA8</span>
<span id="cb2-83"><a href="#cb2-83" aria-hidden="true" tabindex="-1"></a>IS0tIFJlZmVyZW56IGF1ZiBLcmFua2Vua2Fzc2UvS29zdGVudHLEgsKkZ2VyICAtLT4NCiAgICAg</span>
<span id="cb2-84"><a href="#cb2-84" aria-hidden="true" tabindex="-1"></a>ICAgICAgIDxyZWZlcmVuY2UgdmFsdWU9IkNvdmVyYWdlLzFiMWZmYjZlLWViMDUtNDNkNy04N2Vi</span>
<span id="cb2-85"><a href="#cb2-85" aria-hidden="true" tabindex="-1"></a>LWU3ODE4ZmU5NjYxYSIgLz4NCiAgICAgICAgICA8L2VudHJ5Pg0KICAgICAgICA8L3NlY3Rpb24+</span>
<span id="cb2-86"><a href="#cb2-86" aria-hidden="true" tabindex="-1"></a>DQogICAgICA8L0NvbXBvc2l0aW9uPg0KICAgIDwvcmVzb3VyY2U+DQogIDwvZW50cnk+DQogIDxl</span>
<span id="cb2-87"><a href="#cb2-87" aria-hidden="true" tabindex="-1"></a>bnRyeT4NCiAgICA8ZnVsbFVybCB2YWx1ZT0iaHR0cDovL3B2cy5wcmF4aXMtdG9wcC1nbHVlY2ts</span>
<span id="cb2-88"><a href="#cb2-88" aria-hidden="true" tabindex="-1"></a>aWNoLmxvY2FsL2ZoaXIvTWVkaWNhdGlvblJlcXVlc3QvZjU4ZjQ0MDMtN2EzYS00YTEyLWJiMTUt</span>
<span id="cb2-89"><a href="#cb2-89" aria-hidden="true" tabindex="-1"></a>YjJmYTI1YjAyNTYxIiAvPg0KICAgIDxyZXNvdXJjZT4NCiAgICAgIDxNZWRpY2F0aW9uUmVxdWVz</span>
<span id="cb2-90"><a href="#cb2-90" aria-hidden="true" tabindex="-1"></a>dCB4bWxucz0iaHR0cDovL2hsNy5vcmcvZmhpciI+DQogICAgICAgIDxpZCB2YWx1ZT0iZjU4ZjQ0</span>
<span id="cb2-91"><a href="#cb2-91" aria-hidden="true" tabindex="-1"></a>MDMtN2EzYS00YTEyLWJiMTUtYjJmYTI1YjAyNTYxIiAvPg0KICAgICAgICA8bWV0YT4NCiAgICAg</span>
<span id="cb2-92"><a href="#cb2-92" aria-hidden="true" tabindex="-1"></a>ICAgICA8cHJvZmlsZSB2YWx1ZT0iaHR0cHM6Ly9maGlyLmtidi5kZS9TdHJ1Y3R1cmVEZWZpbml0</span>
<span id="cb2-93"><a href="#cb2-93" aria-hidden="true" tabindex="-1"></a>aW9uL0tCVl9QUl9FUlBfUHJlc2NyaXB0aW9ufDEuMC4xIiAvPg0KICAgICAgICA8L21ldGE+DQog</span>
<span id="cb2-94"><a href="#cb2-94" aria-hidden="true" tabindex="-1"></a>ICAgICAgIDxleHRlbnNpb24gdXJsPSJodHRwczovL2ZoaXIua2J2LmRlL1N0cnVjdHVyZURlZmlu</span>
<span id="cb2-95"><a href="#cb2-95" aria-hidden="true" tabindex="-1"></a>aXRpb24vS0JWX0VYX0VSUF9TdGF0dXNDb1BheW1lbnQiPg0KICAgICAgICAgIDx2YWx1ZUNvZGlu</span>
<span id="cb2-96"><a href="#cb2-96" aria-hidden="true" tabindex="-1"></a>Zz4NCiAgICAgICAgICAgIDxzeXN0ZW0gdmFsdWU9Imh0dHBzOi8vZmhpci5rYnYuZGUvQ29kZVN5</span>
<span id="cb2-97"><a href="#cb2-97" aria-hidden="true" tabindex="-1"></a>c3RlbS9LQlZfQ1NfRVJQX1N0YXR1c0NvUGF5bWVudCIgLz4NCiAgICAgICAgICAgIDxjb2RlIHZh</span>
<span id="cb2-98"><a href="#cb2-98" aria-hidden="true" tabindex="-1"></a>bHVlPSIwIiAvPg0KICAgICAgICAgIDwvdmFsdWVDb2Rpbmc+DQogICAgICAgIDwvZXh0ZW5zaW9u</span>
<span id="cb2-99"><a href="#cb2-99" aria-hidden="true" tabindex="-1"></a>Pg0KICAgICAgICA8ZXh0ZW5zaW9uIHVybD0iaHR0cHM6Ly9maGlyLmtidi5kZS9TdHJ1Y3R1cmVE</span>
<span id="cb2-100"><a href="#cb2-100" aria-hidden="true" tabindex="-1"></a>ZWZpbml0aW9uL0tCVl9FWF9FUlBfRW1lcmdlbmN5U2VydmljZXNGZWUiPg0KICAgICAgICAgIDx2</span>
<span id="cb2-101"><a href="#cb2-101" aria-hidden="true" tabindex="-1"></a>YWx1ZUJvb2xlYW4gdmFsdWU9ImZhbHNlIiAvPg0KICAgICAgICA8L2V4dGVuc2lvbj4NCiAgICAg</span>
<span id="cb2-102"><a href="#cb2-102" aria-hidden="true" tabindex="-1"></a>ICAgPGV4dGVuc2lvbiB1cmw9Imh0dHBzOi8vZmhpci5rYnYuZGUvU3RydWN0dXJlRGVmaW5pdGlv</span>
<span id="cb2-103"><a href="#cb2-103" aria-hidden="true" tabindex="-1"></a>bi9LQlZfRVhfRVJQX0JWRyI+DQogICAgICAgICAgPHZhbHVlQm9vbGVhbiB2YWx1ZT0iZmFsc2Ui</span>
<span id="cb2-104"><a href="#cb2-104" aria-hidden="true" tabindex="-1"></a>IC8+DQogICAgICAgIDwvZXh0ZW5zaW9uPg0KICAgICAgICA8ZXh0ZW5zaW9uIHVybD0iaHR0cHM6</span>
<span id="cb2-105"><a href="#cb2-105" aria-hidden="true" tabindex="-1"></a>Ly9maGlyLmtidi5kZS9TdHJ1Y3R1cmVEZWZpbml0aW9uL0tCVl9FWF9FUlBfQWNjaWRlbnQiPg0K</span>
<span id="cb2-106"><a href="#cb2-106" aria-hidden="true" tabindex="-1"></a>ICAgICAgICAgIDxleHRlbnNpb24gdXJsPSJ1bmZhbGxrZW5uemVpY2hlbiI+DQogICAgICAgICAg</span>
<span id="cb2-107"><a href="#cb2-107" aria-hidden="true" tabindex="-1"></a>ICA8dmFsdWVDb2Rpbmc+DQogICAgICAgICAgICAgIDxzeXN0ZW0gdmFsdWU9Imh0dHBzOi8vZmhp</span>
<span id="cb2-108"><a href="#cb2-108" aria-hidden="true" tabindex="-1"></a>ci5rYnYuZGUvQ29kZVN5c3RlbS9LQlZfQ1NfRk9SX1Vyc2FjaGVfVHlwZSIgLz4NCiAgICAgICAg</span>
<span id="cb2-109"><a href="#cb2-109" aria-hidden="true" tabindex="-1"></a>ICAgICAgPGNvZGUgdmFsdWU9IjEiIC8+DQogICAgICAgICAgICA8L3ZhbHVlQ29kaW5nPg0KICAg</span>
<span id="cb2-110"><a href="#cb2-110" aria-hidden="true" tabindex="-1"></a>ICAgICAgIDwvZXh0ZW5zaW9uPg0KICAgICAgICAgIDxleHRlbnNpb24gdXJsPSJ1bmZhbGx0YWci</span>
<span id="cb2-111"><a href="#cb2-111" aria-hidden="true" tabindex="-1"></a>Pg0KICAgICAgICAgICAgPHZhbHVlRGF0ZSB2YWx1ZT0iMjAyMC0wNS0wMSIgLz4NCiAgICAgICAg</span>
<span id="cb2-112"><a href="#cb2-112" aria-hidden="true" tabindex="-1"></a>ICA8L2V4dGVuc2lvbj4NCiAgICAgICAgPC9leHRlbnNpb24+DQogICAgICAgIDxleHRlbnNpb24g</span>
<span id="cb2-113"><a href="#cb2-113" aria-hidden="true" tabindex="-1"></a>dXJsPSJodHRwczovL2ZoaXIua2J2LmRlL1N0cnVjdHVyZURlZmluaXRpb24vS0JWX0VYX0VSUF9N</span>
<span id="cb2-114"><a href="#cb2-114" aria-hidden="true" tabindex="-1"></a>dWx0aXBsZV9QcmVzY3JpcHRpb24iPg0KICAgICAgICAgIDxleHRlbnNpb24gdXJsPSJLZW5uemVp</span>
<span id="cb2-115"><a href="#cb2-115" aria-hidden="true" tabindex="-1"></a>Y2hlbiI+DQogICAgICAgICAgICA8dmFsdWVCb29sZWFuIHZhbHVlPSJ0cnVlIiAvPg0KICAgICAg</span>
<span id="cb2-116"><a href="#cb2-116" aria-hidden="true" tabindex="-1"></a>ICAgIDwvZXh0ZW5zaW9uPg0KICAgICAgICAgIDxleHRlbnNpb24gdXJsPSJOdW1tZXJpZXJ1bmci</span>
<span id="cb2-117"><a href="#cb2-117" aria-hidden="true" tabindex="-1"></a>Pg0KICAgICAgICAgICAgPHZhbHVlUmF0aW8+DQogICAgICAgICAgICAgIDxudW1lcmF0b3I+DQog</span>
<span id="cb2-118"><a href="#cb2-118" aria-hidden="true" tabindex="-1"></a>ICAgICAgICAgICAgICAgPHZhbHVlIHZhbHVlPSIyIiAvPg0KICAgICAgICAgICAgICA8L251bWVy</span>
<span id="cb2-119"><a href="#cb2-119" aria-hidden="true" tabindex="-1"></a>YXRvcj4NCiAgICAgICAgICAgICAgPGRlbm9taW5hdG9yPg0KICAgICAgICAgICAgICAgIDx2YWx1</span>
<span id="cb2-120"><a href="#cb2-120" aria-hidden="true" tabindex="-1"></a>ZSB2YWx1ZT0iNCIgLz4NCiAgICAgICAgICAgICAgPC9kZW5vbWluYXRvcj4NCiAgICAgICAgICAg</span>
<span id="cb2-121"><a href="#cb2-121" aria-hidden="true" tabindex="-1"></a>IDwvdmFsdWVSYXRpbz4NCiAgICAgICAgICA8L2V4dGVuc2lvbj4NCiAgICAgICAgICA8ZXh0ZW5z</span>
<span id="cb2-122"><a href="#cb2-122" aria-hidden="true" tabindex="-1"></a>aW9uIHVybD0iWmVpdHJhdW0iPg0KICAgICAgICAgICAgPHZhbHVlUGVyaW9kPg0KICAgICAgICAg</span>
<span id="cb2-123"><a href="#cb2-123" aria-hidden="true" tabindex="-1"></a>ICAgICA8c3RhcnQgdmFsdWU9IjIwMjEtMDEtMDIiIC8+DQogICAgICAgICAgICAgIDxlbmQgdmFs</span>
<span id="cb2-124"><a href="#cb2-124" aria-hidden="true" tabindex="-1"></a>dWU9IjIwMjEtMDMtMzAiIC8+DQogICAgICAgICAgICA8L3ZhbHVlUGVyaW9kPg0KICAgICAgICAg</span>
<span id="cb2-125"><a href="#cb2-125" aria-hidden="true" tabindex="-1"></a>IDwvZXh0ZW5zaW9uPg0KICAgICAgICA8L2V4dGVuc2lvbj4NCiAgICAgICAgPHN0YXR1cyB2YWx1</span>
<span id="cb2-126"><a href="#cb2-126" aria-hidden="true" tabindex="-1"></a>ZT0iYWN0aXZlIiAvPg0KICAgICAgICA8aW50ZW50IHZhbHVlPSJvcmRlciIgLz4NCiAgICAgICAg</span>
<span id="cb2-127"><a href="#cb2-127" aria-hidden="true" tabindex="-1"></a>PG1lZGljYXRpb25SZWZlcmVuY2U+DQogICAgICAgICAgPHJlZmVyZW5jZSB2YWx1ZT0iTWVkaWNh</span>
<span id="cb2-128"><a href="#cb2-128" aria-hidden="true" tabindex="-1"></a>dGlvbi9lM2E0ZWZhNy04NGZjLTQ2NWItYjE0Yy03MjAxOTUwOTc3ODMiIC8+DQogICAgICAgIDwv</span>
<span id="cb2-129"><a href="#cb2-129" aria-hidden="true" tabindex="-1"></a>bWVkaWNhdGlvblJlZmVyZW5jZT4NCiAgICAgICAgPHN1YmplY3Q+DQogICAgICAgICAgPHJlZmVy</span>
<span id="cb2-130"><a href="#cb2-130" aria-hidden="true" tabindex="-1"></a>ZW5jZSB2YWx1ZT0iUGF0aWVudC85Nzc0ZjY3Zi1hMjM4LTRkYWYtYjRlNi02NzlkZWVlZjM4MTEi</span>
<span id="cb2-131"><a href="#cb2-131" aria-hidden="true" tabindex="-1"></a>IC8+DQogICAgICAgIDwvc3ViamVjdD4NCiAgICAgICAgPGF1dGhvcmVkT24gdmFsdWU9IjIwMjAt</span>
<span id="cb2-132"><a href="#cb2-132" aria-hidden="true" tabindex="-1"></a>MDUtMDIiIC8+DQogICAgICAgIDxyZXF1ZXN0ZXI+DQogICAgICAgICAgPHJlZmVyZW5jZSB2YWx1</span>
<span id="cb2-133"><a href="#cb2-133" aria-hidden="true" tabindex="-1"></a>ZT0iUHJhY3RpdGlvbmVyLzIwNTk3ZTBlLWNiMmEtNDViMy05NWYwLWRjM2RiZGI2MTdjMyIgLz4N</span>
<span id="cb2-134"><a href="#cb2-134" aria-hidden="true" tabindex="-1"></a>CiAgICAgICAgPC9yZXF1ZXN0ZXI+DQogICAgICAgIDxpbnN1cmFuY2U+DQogICAgICAgICAgPHJl</span>
<span id="cb2-135"><a href="#cb2-135" aria-hidden="true" tabindex="-1"></a>ZmVyZW5jZSB2YWx1ZT0iQ292ZXJhZ2UvMWIxZmZiNmUtZWIwNS00M2Q3LTg3ZWItZTc4MThmZTk2</span>
<span id="cb2-136"><a href="#cb2-136" aria-hidden="true" tabindex="-1"></a>NjFhIiAvPg0KICAgICAgICA8L2luc3VyYW5jZT4NCiAgICAgICAgPG5vdGU+DQogICAgICAgICAg</span>
<span id="cb2-137"><a href="#cb2-137" aria-hidden="true" tabindex="-1"></a>PHRleHQgdmFsdWU9IkR1bW15LUhpbndlaXMgZsO8ciBkaWUgQXBvdGhla2UiIC8+DQogICAgICAg</span>
<span id="cb2-138"><a href="#cb2-138" aria-hidden="true" tabindex="-1"></a>IDwvbm90ZT4NCiAgICAgICAgPGRvc2FnZUluc3RydWN0aW9uPg0KICAgICAgICAgIDxleHRlbnNp</span>
<span id="cb2-139"><a href="#cb2-139" aria-hidden="true" tabindex="-1"></a>b24gdXJsPSJodHRwczovL2ZoaXIua2J2LmRlL1N0cnVjdHVyZURlZmluaXRpb24vS0JWX0VYX0VS</span>
<span id="cb2-140"><a href="#cb2-140" aria-hidden="true" tabindex="-1"></a>UF9Eb3NhZ2VGbGFnIj4NCiAgICAgICAgICAgIDx2YWx1ZUJvb2xlYW4gdmFsdWU9ImZhbHNlIiAv</span>
<span id="cb2-141"><a href="#cb2-141" aria-hidden="true" tabindex="-1"></a>Pg0KICAgICAgICAgIDwvZXh0ZW5zaW9uPg0KICAgICAgICA8L2Rvc2FnZUluc3RydWN0aW9uPg0K</span>
<span id="cb2-142"><a href="#cb2-142" aria-hidden="true" tabindex="-1"></a>ICAgICAgICA8ZGlzcGVuc2VSZXF1ZXN0Pg0KICAgICAgICAgIDxxdWFudGl0eT4NCiAgICAgICAg</span>
<span id="cb2-143"><a href="#cb2-143" aria-hidden="true" tabindex="-1"></a>ICAgIDx2YWx1ZSB2YWx1ZT0iMiIgLz4NCiAgICAgICAgICAgIDxzeXN0ZW0gdmFsdWU9Imh0dHA6</span>
<span id="cb2-144"><a href="#cb2-144" aria-hidden="true" tabindex="-1"></a>Ly91bml0c29mbWVhc3VyZS5vcmciIC8+DQogICAgICAgICAgICA8Y29kZSB2YWx1ZT0ie1BhY2th</span>
<span id="cb2-145"><a href="#cb2-145" aria-hidden="true" tabindex="-1"></a>Z2V9IiAvPg0KICAgICAgICAgIDwvcXVhbnRpdHk+DQogICAgICAgIDwvZGlzcGVuc2VSZXF1ZXN0</span>
<span id="cb2-146"><a href="#cb2-146" aria-hidden="true" tabindex="-1"></a>Pg0KICAgICAgICA8c3Vic3RpdHV0aW9uPg0KICAgICAgICAgIDxhbGxvd2VkQm9vbGVhbiB2YWx1</span>
<span id="cb2-147"><a href="#cb2-147" aria-hidden="true" tabindex="-1"></a>ZT0idHJ1ZSIgLz4NCiAgICAgICAgPC9zdWJzdGl0dXRpb24+DQogICAgICA8L01lZGljYXRpb25S</span>
<span id="cb2-148"><a href="#cb2-148" aria-hidden="true" tabindex="-1"></a>ZXF1ZXN0Pg0KICAgIDwvcmVzb3VyY2U+DQogIDwvZW50cnk+DQogIDxlbnRyeT4NCiAgICA8ZnVs</span>
<span id="cb2-149"><a href="#cb2-149" aria-hidden="true" tabindex="-1"></a>bFVybCB2YWx1ZT0iaHR0cDovL3B2cy5wcmF4aXMtdG9wcC1nbHVlY2tsaWNoLmxvY2FsL2ZoaXIv</span>
<span id="cb2-150"><a href="#cb2-150" aria-hidden="true" tabindex="-1"></a>TWVkaWNhdGlvbi9lM2E0ZWZhNy04NGZjLTQ2NWItYjE0Yy03MjAxOTUwOTc3ODMiIC8+DQogICAg</span>
<span id="cb2-151"><a href="#cb2-151" aria-hidden="true" tabindex="-1"></a>PHJlc291cmNlPg0KICAgICAgPE1lZGljYXRpb24geG1sbnM9Imh0dHA6Ly9obDcub3JnL2ZoaXIi</span>
<span id="cb2-152"><a href="#cb2-152" aria-hidden="true" tabindex="-1"></a>Pg0KICAgICAgICA8aWQgdmFsdWU9ImUzYTRlZmE3LTg0ZmMtNDY1Yi1iMTRjLTcyMDE5NTA5Nzc4</span>
<span id="cb2-153"><a href="#cb2-153" aria-hidden="true" tabindex="-1"></a>MyIgLz4NCiAgICAgICAgPG1ldGE+DQogICAgICAgICAgPHByb2ZpbGUgdmFsdWU9Imh0dHBzOi8v</span>
<span id="cb2-154"><a href="#cb2-154" aria-hidden="true" tabindex="-1"></a>Zmhpci5rYnYuZGUvU3RydWN0dXJlRGVmaW5pdGlvbi9LQlZfUFJfRVJQX01lZGljYXRpb25fSW5n</span>
<span id="cb2-155"><a href="#cb2-155" aria-hidden="true" tabindex="-1"></a>cmVkaWVudHwxLjAuMSIgLz4NCiAgICAgICAgPC9tZXRhPg0KICAgICAgICA8ZXh0ZW5zaW9uIHVy</span>
<span id="cb2-156"><a href="#cb2-156" aria-hidden="true" tabindex="-1"></a>bD0iaHR0cHM6Ly9maGlyLmtidi5kZS9TdHJ1Y3R1cmVEZWZpbml0aW9uL0tCVl9FWF9FUlBfTWVk</span>
<span id="cb2-157"><a href="#cb2-157" aria-hidden="true" tabindex="-1"></a>aWNhdGlvbl9DYXRlZ29yeSI+DQogICAgICAgICAgPHZhbHVlQ29kaW5nPg0KICAgICAgICAgICAg</span>
<span id="cb2-158"><a href="#cb2-158" aria-hidden="true" tabindex="-1"></a>PHN5c3RlbSB2YWx1ZT0iaHR0cHM6Ly9maGlyLmtidi5kZS9Db2RlU3lzdGVtL0tCVl9DU19FUlBf</span>
<span id="cb2-159"><a href="#cb2-159" aria-hidden="true" tabindex="-1"></a>TWVkaWNhdGlvbl9DYXRlZ29yeSIgLz4NCiAgICAgICAgICAgIDxjb2RlIHZhbHVlPSIwMCIgLz4N</span>
<span id="cb2-160"><a href="#cb2-160" aria-hidden="true" tabindex="-1"></a>CiAgICAgICAgICA8L3ZhbHVlQ29kaW5nPg0KICAgICAgICA8L2V4dGVuc2lvbj4NCiAgICAgICAg</span>
<span id="cb2-161"><a href="#cb2-161" aria-hidden="true" tabindex="-1"></a>PGV4dGVuc2lvbiB1cmw9Imh0dHBzOi8vZmhpci5rYnYuZGUvU3RydWN0dXJlRGVmaW5pdGlvbi9L</span>
<span id="cb2-162"><a href="#cb2-162" aria-hidden="true" tabindex="-1"></a>QlZfRVhfRVJQX01lZGljYXRpb25fVmFjY2luZSI+DQogICAgICAgICAgPHZhbHVlQm9vbGVhbiB2</span>
<span id="cb2-163"><a href="#cb2-163" aria-hidden="true" tabindex="-1"></a>YWx1ZT0iZmFsc2UiIC8+DQogICAgICAgIDwvZXh0ZW5zaW9uPg0KICAgICAgICA8Y29kZT4NCiAg</span>
<span id="cb2-164"><a href="#cb2-164" aria-hidden="true" tabindex="-1"></a>ICAgICAgICA8Y29kaW5nPg0KICAgICAgICAgICAgPHN5c3RlbSB2YWx1ZT0iaHR0cHM6Ly9maGly</span>
<span id="cb2-165"><a href="#cb2-165" aria-hidden="true" tabindex="-1"></a>Lmtidi5kZS9Db2RlU3lzdGVtL0tCVl9DU19FUlBfTWVkaWNhdGlvbl9UeXBlIiAvPg0KICAgICAg</span>
<span id="cb2-166"><a href="#cb2-166" aria-hidden="true" tabindex="-1"></a>ICAgICAgPGNvZGUgdmFsdWU9IndpcmtzdG9mZiIgLz4NCiAgICAgICAgICA8L2NvZGluZz4NCiAg</span>
<span id="cb2-167"><a href="#cb2-167" aria-hidden="true" tabindex="-1"></a>ICAgICAgPC9jb2RlPg0KICAgICAgICA8Zm9ybT4NCiAgICAgICAgICA8dGV4dCB2YWx1ZT0iVGFi</span>
<span id="cb2-168"><a href="#cb2-168" aria-hidden="true" tabindex="-1"></a>bGV0dGVuIiAvPg0KICAgICAgICA8L2Zvcm0+DQogICAgICAgIDxhbW91bnQ+DQogICAgICAgICAg</span>
<span id="cb2-169"><a href="#cb2-169" aria-hidden="true" tabindex="-1"></a>PG51bWVyYXRvcj4NCiAgICAgICAgICAgIDx2YWx1ZSB2YWx1ZT0iMjAiIC8+DQogICAgICAgICAg</span>
<span id="cb2-170"><a href="#cb2-170" aria-hidden="true" tabindex="-1"></a>ICA8dW5pdCB2YWx1ZT0iU3RrIiAvPg0KICAgICAgICAgIDwvbnVtZXJhdG9yPg0KICAgICAgICAg</span>
<span id="cb2-171"><a href="#cb2-171" aria-hidden="true" tabindex="-1"></a>IDxkZW5vbWluYXRvcj4NCiAgICAgICAgICAgIDx2YWx1ZSB2YWx1ZT0iMSIgLz4NCiAgICAgICAg</span>
<span id="cb2-172"><a href="#cb2-172" aria-hidden="true" tabindex="-1"></a>ICA8L2Rlbm9taW5hdG9yPg0KICAgICAgICA8L2Ftb3VudD4NCiAgICAgICAgPGluZ3JlZGllbnQ+</span>
<span id="cb2-173"><a href="#cb2-173" aria-hidden="true" tabindex="-1"></a>DQogICAgICAgICAgPGl0ZW1Db2RlYWJsZUNvbmNlcHQ+DQogICAgICAgICAgICA8Y29kaW5nPg0K</span>
<span id="cb2-174"><a href="#cb2-174" aria-hidden="true" tabindex="-1"></a>ICAgICAgICAgICAgICA8c3lzdGVtIHZhbHVlPSJodHRwOi8vZmhpci5kZS9Db2RlU3lzdGVtL2Fz</span>
<span id="cb2-175"><a href="#cb2-175" aria-hidden="true" tabindex="-1"></a>ayIgLz4NCiAgICAgICAgICAgICAgPGNvZGUgdmFsdWU9IkR1bW15LUFTSyIgLz4NCiAgICAgICAg</span>
<span id="cb2-176"><a href="#cb2-176" aria-hidden="true" tabindex="-1"></a>ICAgIDwvY29kaW5nPg0KICAgICAgICAgICAgPHRleHQgdmFsdWU9IklidXByb2ZlbiIgLz4NCiAg</span>
<span id="cb2-177"><a href="#cb2-177" aria-hidden="true" tabindex="-1"></a>ICAgICAgICA8L2l0ZW1Db2RlYWJsZUNvbmNlcHQ+DQogICAgICAgICAgPHN0cmVuZ3RoPg0KICAg</span>
<span id="cb2-178"><a href="#cb2-178" aria-hidden="true" tabindex="-1"></a>ICAgICAgICAgPG51bWVyYXRvcj4NCiAgICAgICAgICAgICAgPHZhbHVlIHZhbHVlPSI4MDAiIC8+</span>
<span id="cb2-179"><a href="#cb2-179" aria-hidden="true" tabindex="-1"></a>DQogICAgICAgICAgICAgIDx1bml0IHZhbHVlPSJtZyIgLz4NCiAgICAgICAgICAgIDwvbnVtZXJh</span>
<span id="cb2-180"><a href="#cb2-180" aria-hidden="true" tabindex="-1"></a>dG9yPg0KICAgICAgICAgICAgPGRlbm9taW5hdG9yPg0KICAgICAgICAgICAgICA8dmFsdWUgdmFs</span>
<span id="cb2-181"><a href="#cb2-181" aria-hidden="true" tabindex="-1"></a>dWU9IjEiIC8+DQogICAgICAgICAgICA8L2Rlbm9taW5hdG9yPg0KICAgICAgICAgIDwvc3RyZW5n</span>
<span id="cb2-182"><a href="#cb2-182" aria-hidden="true" tabindex="-1"></a>dGg+DQogICAgICAgIDwvaW5ncmVkaWVudD4NCiAgICAgIDwvTWVkaWNhdGlvbj4NCiAgICA8L3Jl</span>
<span id="cb2-183"><a href="#cb2-183" aria-hidden="true" tabindex="-1"></a>c291cmNlPg0KICA8L2VudHJ5Pg0KICA8ZW50cnk+DQogICAgPGZ1bGxVcmwgdmFsdWU9Imh0dHA6</span>
<span id="cb2-184"><a href="#cb2-184" aria-hidden="true" tabindex="-1"></a>Ly9wdnMucHJheGlzLXRvcHAtZ2x1ZWNrbGljaC5sb2NhbC9maGlyL1BhdGllbnQvOTc3NGY2N2Yt</span>
<span id="cb2-185"><a href="#cb2-185" aria-hidden="true" tabindex="-1"></a>YTIzOC00ZGFmLWI0ZTYtNjc5ZGVlZWYzODExIiAvPg0KICAgIDxyZXNvdXJjZT4NCiAgICAgIDxQ</span>
<span id="cb2-186"><a href="#cb2-186" aria-hidden="true" tabindex="-1"></a>YXRpZW50IHhtbG5zPSJodHRwOi8vaGw3Lm9yZy9maGlyIj4NCiAgICAgICAgPGlkIHZhbHVlPSI5</span>
<span id="cb2-187"><a href="#cb2-187" aria-hidden="true" tabindex="-1"></a>Nzc0ZjY3Zi1hMjM4LTRkYWYtYjRlNi02NzlkZWVlZjM4MTEiIC8+DQogICAgICAgIDxtZXRhPg0K</span>
<span id="cb2-188"><a href="#cb2-188" aria-hidden="true" tabindex="-1"></a>ICAgICAgICAgIDxwcm9maWxlIHZhbHVlPSJodHRwczovL2ZoaXIua2J2LmRlL1N0cnVjdHVyZURl</span>
<span id="cb2-189"><a href="#cb2-189" aria-hidden="true" tabindex="-1"></a>ZmluaXRpb24vS0JWX1BSX0ZPUl9QYXRpZW50fDEuMC4zIiAvPg0KICAgICAgICA8L21ldGE+DQog</span>
<span id="cb2-190"><a href="#cb2-190" aria-hidden="true" tabindex="-1"></a>ICAgICAgIDxpZGVudGlmaWVyPg0KICAgICAgICAgIDx0eXBlPg0KICAgICAgICAgICAgPGNvZGlu</span>
<span id="cb2-191"><a href="#cb2-191" aria-hidden="true" tabindex="-1"></a>Zz4NCiAgICAgICAgICAgICAgPHN5c3RlbSB2YWx1ZT0iaHR0cDovL2ZoaXIuZGUvQ29kZVN5c3Rl</span>
<span id="cb2-192"><a href="#cb2-192" aria-hidden="true" tabindex="-1"></a>bS9pZGVudGlmaWVyLXR5cGUtZGUtYmFzaXMiIC8+DQogICAgICAgICAgICAgIDxjb2RlIHZhbHVl</span>
<span id="cb2-193"><a href="#cb2-193" aria-hidden="true" tabindex="-1"></a>PSJHS1YiIC8+DQogICAgICAgICAgICA8L2NvZGluZz4NCiAgICAgICAgICA8L3R5cGU+DQogICAg</span>
<span id="cb2-194"><a href="#cb2-194" aria-hidden="true" tabindex="-1"></a>ICAgICAgPHN5c3RlbSB2YWx1ZT0iaHR0cDovL2ZoaXIuZGUvTmFtaW5nU3lzdGVtL2drdi9rdmlk</span>
<span id="cb2-195"><a href="#cb2-195" aria-hidden="true" tabindex="-1"></a>LTEwIiAvPg0KICAgICAgICAgIDx2YWx1ZSB2YWx1ZT0iWDIzNDU2Nzg5MCIgLz4NCiAgICAgICAg</span>
<span id="cb2-196"><a href="#cb2-196" aria-hidden="true" tabindex="-1"></a>PC9pZGVudGlmaWVyPg0KICAgICAgICA8bmFtZT4NCiAgICAgICAgICA8dXNlIHZhbHVlPSJvZmZp</span>
<span id="cb2-197"><a href="#cb2-197" aria-hidden="true" tabindex="-1"></a>Y2lhbCIgLz4NCiAgICAgICAgICA8ZmFtaWx5IHZhbHVlPSJMdWRnZXIgS8O2bmlnc3N0ZWluIj4N</span>
<span id="cb2-198"><a href="#cb2-198" aria-hidden="true" tabindex="-1"></a>CiAgICAgICAgICAgIDxleHRlbnNpb24gdXJsPSJodHRwOi8vaGw3Lm9yZy9maGlyL1N0cnVjdHVy</span>
<span id="cb2-199"><a href="#cb2-199" aria-hidden="true" tabindex="-1"></a>ZURlZmluaXRpb24vaHVtYW5uYW1lLW93bi1uYW1lIj4NCiAgICAgICAgICAgICAgPHZhbHVlU3Ry</span>
<span id="cb2-200"><a href="#cb2-200" aria-hidden="true" tabindex="-1"></a>aW5nIHZhbHVlPSJLw7ZuaWdzc3RlaW4iIC8+DQogICAgICAgICAgICA8L2V4dGVuc2lvbj4NCiAg</span>
<span id="cb2-201"><a href="#cb2-201" aria-hidden="true" tabindex="-1"></a>ICAgICAgICA8L2ZhbWlseT4NCiAgICAgICAgICA8Z2l2ZW4gdmFsdWU9Ikx1ZGdlciIgLz4NCiAg</span>
<span id="cb2-202"><a href="#cb2-202" aria-hidden="true" tabindex="-1"></a>ICAgICAgPC9uYW1lPg0KICAgICAgICA8YmlydGhEYXRlIHZhbHVlPSIxOTM1LTA2LTIyIiAvPg0K</span>
<span id="cb2-203"><a href="#cb2-203" aria-hidden="true" tabindex="-1"></a>ICAgICAgICA8YWRkcmVzcz4NCiAgICAgICAgICA8dHlwZSB2YWx1ZT0iYm90aCIgLz4NCiAgICAg</span>
<span id="cb2-204"><a href="#cb2-204" aria-hidden="true" tabindex="-1"></a>ICAgICA8bGluZSB2YWx1ZT0iTXVzdGVyc3RyLiAxIj4NCiAgICAgICAgICAgIDxleHRlbnNpb24g</span>
<span id="cb2-205"><a href="#cb2-205" aria-hidden="true" tabindex="-1"></a>dXJsPSJodHRwOi8vaGw3Lm9yZy9maGlyL1N0cnVjdHVyZURlZmluaXRpb24vaXNvMjEwOTAtQURY</span>
<span id="cb2-206"><a href="#cb2-206" aria-hidden="true" tabindex="-1"></a>UC1ob3VzZU51bWJlciI+DQogICAgICAgICAgICAgIDx2YWx1ZVN0cmluZyB2YWx1ZT0iMSIgLz4N</span>
<span id="cb2-207"><a href="#cb2-207" aria-hidden="true" tabindex="-1"></a>CiAgICAgICAgICAgIDwvZXh0ZW5zaW9uPg0KICAgICAgICAgICAgPGV4dGVuc2lvbiB1cmw9Imh0</span>
<span id="cb2-208"><a href="#cb2-208" aria-hidden="true" tabindex="-1"></a>dHA6Ly9obDcub3JnL2ZoaXIvU3RydWN0dXJlRGVmaW5pdGlvbi9pc28yMTA5MC1BRFhQLXN0cmVl</span>
<span id="cb2-209"><a href="#cb2-209" aria-hidden="true" tabindex="-1"></a>dE5hbWUiPg0KICAgICAgICAgICAgICA8dmFsdWVTdHJpbmcgdmFsdWU9Ik11c3RlcnN0ci4iIC8+</span>
<span id="cb2-210"><a href="#cb2-210" aria-hidden="true" tabindex="-1"></a>DQogICAgICAgICAgICA8L2V4dGVuc2lvbj4NCiAgICAgICAgICA8L2xpbmU+DQogICAgICAgICAg</span>
<span id="cb2-211"><a href="#cb2-211" aria-hidden="true" tabindex="-1"></a>PGNpdHkgdmFsdWU9IkJlcmxpbiIgLz4NCiAgICAgICAgICA8cG9zdGFsQ29kZSB2YWx1ZT0iMTA2</span>
<span id="cb2-212"><a href="#cb2-212" aria-hidden="true" tabindex="-1"></a>MjMiIC8+DQogICAgICAgIDwvYWRkcmVzcz4NCiAgICAgIDwvUGF0aWVudD4NCiAgICA8L3Jlc291</span>
<span id="cb2-213"><a href="#cb2-213" aria-hidden="true" tabindex="-1"></a>cmNlPg0KICA8L2VudHJ5Pg0KICA8ZW50cnk+DQogICAgPGZ1bGxVcmwgdmFsdWU9Imh0dHA6Ly9w</span>
<span id="cb2-214"><a href="#cb2-214" aria-hidden="true" tabindex="-1"></a>dnMucHJheGlzLXRvcHAtZ2x1ZWNrbGljaC5sb2NhbC9maGlyL1ByYWN0aXRpb25lci8yMDU5N2Uw</span>
<span id="cb2-215"><a href="#cb2-215" aria-hidden="true" tabindex="-1"></a>ZS1jYjJhLTQ1YjMtOTVmMC1kYzNkYmRiNjE3YzMiIC8+DQogICAgPHJlc291cmNlPg0KICAgICAg</span>
<span id="cb2-216"><a href="#cb2-216" aria-hidden="true" tabindex="-1"></a>PFByYWN0aXRpb25lciB4bWxucz0iaHR0cDovL2hsNy5vcmcvZmhpciI+DQogICAgICAgIDxpZCB2</span>
<span id="cb2-217"><a href="#cb2-217" aria-hidden="true" tabindex="-1"></a>YWx1ZT0iMjA1OTdlMGUtY2IyYS00NWIzLTk1ZjAtZGMzZGJkYjYxN2MzIiAvPg0KICAgICAgICA8</span>
<span id="cb2-218"><a href="#cb2-218" aria-hidden="true" tabindex="-1"></a>bWV0YT4NCiAgICAgICAgICA8cHJvZmlsZSB2YWx1ZT0iaHR0cHM6Ly9maGlyLmtidi5kZS9TdHJ1</span>
<span id="cb2-219"><a href="#cb2-219" aria-hidden="true" tabindex="-1"></a>Y3R1cmVEZWZpbml0aW9uL0tCVl9QUl9GT1JfUHJhY3RpdGlvbmVyfDEuMC4zIiAvPg0KICAgICAg</span>
<span id="cb2-220"><a href="#cb2-220" aria-hidden="true" tabindex="-1"></a>ICA8L21ldGE+DQogICAgICAgIDxpZGVudGlmaWVyPg0KICAgICAgICAgIDx0eXBlPg0KICAgICAg</span>
<span id="cb2-221"><a href="#cb2-221" aria-hidden="true" tabindex="-1"></a>ICAgICAgPGNvZGluZz4NCiAgICAgICAgICAgICAgPHN5c3RlbSB2YWx1ZT0iaHR0cDovL3Rlcm1p</span>
<span id="cb2-222"><a href="#cb2-222" aria-hidden="true" tabindex="-1"></a>bm9sb2d5LmhsNy5vcmcvQ29kZVN5c3RlbS92Mi0wMjAzIiAvPg0KICAgICAgICAgICAgICA8Y29k</span>
<span id="cb2-223"><a href="#cb2-223" aria-hidden="true" tabindex="-1"></a>ZSB2YWx1ZT0iTEFOUiIgLz4NCiAgICAgICAgICAgIDwvY29kaW5nPg0KICAgICAgICAgIDwvdHlw</span>
<span id="cb2-224"><a href="#cb2-224" aria-hidden="true" tabindex="-1"></a>ZT4NCiAgICAgICAgICA8c3lzdGVtIHZhbHVlPSJodHRwczovL2ZoaXIua2J2LmRlL05hbWluZ1N5</span>
<span id="cb2-225"><a href="#cb2-225" aria-hidden="true" tabindex="-1"></a>c3RlbS9LQlZfTlNfQmFzZV9BTlIiIC8+DQogICAgICAgICAgPHZhbHVlIHZhbHVlPSI4MzgzODIy</span>
<span id="cb2-226"><a href="#cb2-226" aria-hidden="true" tabindex="-1"></a>MDIiIC8+DQogICAgICAgIDwvaWRlbnRpZmllcj4NCiAgICAgICAgPG5hbWU+DQogICAgICAgICAg</span>
<span id="cb2-227"><a href="#cb2-227" aria-hidden="true" tabindex="-1"></a>PHVzZSB2YWx1ZT0ib2ZmaWNpYWwiIC8+DQogICAgICAgICAgPGZhbWlseSB2YWx1ZT0iVG9wcC1H</span>
<span id="cb2-228"><a href="#cb2-228" aria-hidden="true" tabindex="-1"></a>bMO8Y2tsaWNoIj4NCiAgICAgICAgICAgIDxleHRlbnNpb24gdXJsPSJodHRwOi8vaGw3Lm9yZy9m</span>
<span id="cb2-229"><a href="#cb2-229" aria-hidden="true" tabindex="-1"></a>aGlyL1N0cnVjdHVyZURlZmluaXRpb24vaHVtYW5uYW1lLW93bi1uYW1lIj4NCiAgICAgICAgICAg</span>
<span id="cb2-230"><a href="#cb2-230" aria-hidden="true" tabindex="-1"></a>ICAgPHZhbHVlU3RyaW5nIHZhbHVlPSJUb3BwLUdsw7xja2xpY2giIC8+DQogICAgICAgICAgICA8</span>
<span id="cb2-231"><a href="#cb2-231" aria-hidden="true" tabindex="-1"></a>L2V4dGVuc2lvbj4NCiAgICAgICAgICA8L2ZhbWlseT4NCiAgICAgICAgICA8Z2l2ZW4gdmFsdWU9</span>
<span id="cb2-232"><a href="#cb2-232" aria-hidden="true" tabindex="-1"></a>IkhhbnMiIC8+DQogICAgICAgICAgPHByZWZpeCB2YWx1ZT0iRHIuIG1lZC4iPg0KICAgICAgICAg</span>
<span id="cb2-233"><a href="#cb2-233" aria-hidden="true" tabindex="-1"></a>ICAgPGV4dGVuc2lvbiB1cmw9Imh0dHA6Ly9obDcub3JnL2ZoaXIvU3RydWN0dXJlRGVmaW5pdGlv</span>
<span id="cb2-234"><a href="#cb2-234" aria-hidden="true" tabindex="-1"></a>bi9pc28yMTA5MC1FTi1xdWFsaWZpZXIiPg0KICAgICAgICAgICAgICA8dmFsdWVDb2RlIHZhbHVl</span>
<span id="cb2-235"><a href="#cb2-235" aria-hidden="true" tabindex="-1"></a>PSJBQyIgLz4NCiAgICAgICAgICAgIDwvZXh0ZW5zaW9uPg0KICAgICAgICAgIDwvcHJlZml4Pg0K</span>
<span id="cb2-236"><a href="#cb2-236" aria-hidden="true" tabindex="-1"></a>ICAgICAgICA8L25hbWU+DQogICAgICAgIDxxdWFsaWZpY2F0aW9uPg0KICAgICAgICAgIDxjb2Rl</span>
<span id="cb2-237"><a href="#cb2-237" aria-hidden="true" tabindex="-1"></a>Pg0KICAgICAgICAgICAgPGNvZGluZz4NCiAgICAgICAgICAgICAgPHN5c3RlbSB2YWx1ZT0iaHR0</span>
<span id="cb2-238"><a href="#cb2-238" aria-hidden="true" tabindex="-1"></a>cHM6Ly9maGlyLmtidi5kZS9Db2RlU3lzdGVtL0tCVl9DU19GT1JfUXVhbGlmaWNhdGlvbl9UeXBl</span>
<span id="cb2-239"><a href="#cb2-239" aria-hidden="true" tabindex="-1"></a>IiAvPg0KICAgICAgICAgICAgICA8Y29kZSB2YWx1ZT0iMDAiIC8+DQogICAgICAgICAgICA8L2Nv</span>
<span id="cb2-240"><a href="#cb2-240" aria-hidden="true" tabindex="-1"></a>ZGluZz4NCiAgICAgICAgICA8L2NvZGU+DQogICAgICAgIDwvcXVhbGlmaWNhdGlvbj4NCiAgICAg</span>
<span id="cb2-241"><a href="#cb2-241" aria-hidden="true" tabindex="-1"></a>ICAgPHF1YWxpZmljYXRpb24+DQogICAgICAgICAgPGNvZGU+DQogICAgICAgICAgICA8dGV4dCB2</span>
<span id="cb2-242"><a href="#cb2-242" aria-hidden="true" tabindex="-1"></a>YWx1ZT0iSGF1c2FyenQiIC8+DQogICAgICAgICAgPC9jb2RlPg0KICAgICAgICA8L3F1YWxpZmlj</span>
<span id="cb2-243"><a href="#cb2-243" aria-hidden="true" tabindex="-1"></a>YXRpb24+DQogICAgICA8L1ByYWN0aXRpb25lcj4NCiAgICA8L3Jlc291cmNlPg0KICA8L2VudHJ5</span>
<span id="cb2-244"><a href="#cb2-244" aria-hidden="true" tabindex="-1"></a>Pg0KICA8ZW50cnk+DQogICAgPGZ1bGxVcmwgdmFsdWU9Imh0dHA6Ly9wdnMucHJheGlzLXRvcHAt</span>
<span id="cb2-245"><a href="#cb2-245" aria-hidden="true" tabindex="-1"></a>Z2x1ZWNrbGljaC5sb2NhbC9maGlyL1ByYWN0aXRpb25lci9kODQ2M2RhZi0yNThlLTRjYWQtYTg2</span>
<span id="cb2-246"><a href="#cb2-246" aria-hidden="true" tabindex="-1"></a>YS02ZmQ0MmZhYzE2MWMiIC8+DQogICAgPHJlc291cmNlPg0KICAgICAgPFByYWN0aXRpb25lciB4</span>
<span id="cb2-247"><a href="#cb2-247" aria-hidden="true" tabindex="-1"></a>bWxucz0iaHR0cDovL2hsNy5vcmcvZmhpciI+DQogICAgICAgIDxpZCB2YWx1ZT0iZDg0NjNkYWYt</span>
<span id="cb2-248"><a href="#cb2-248" aria-hidden="true" tabindex="-1"></a>MjU4ZS00Y2FkLWE4NmEtNmZkNDJmYWMxNjFjIiAvPg0KICAgICAgICA8bWV0YT4NCiAgICAgICAg</span>
<span id="cb2-249"><a href="#cb2-249" aria-hidden="true" tabindex="-1"></a>ICA8cHJvZmlsZSB2YWx1ZT0iaHR0cHM6Ly9maGlyLmtidi5kZS9TdHJ1Y3R1cmVEZWZpbml0aW9u</span>
<span id="cb2-250"><a href="#cb2-250" aria-hidden="true" tabindex="-1"></a>L0tCVl9QUl9GT1JfUHJhY3RpdGlvbmVyfDEuMC4zIiAvPg0KICAgICAgICA8L21ldGE+DQogICAg</span>
<span id="cb2-251"><a href="#cb2-251" aria-hidden="true" tabindex="-1"></a>ICAgIDxpZGVudGlmaWVyPg0KICAgICAgICAgIDx0eXBlPg0KICAgICAgICAgICAgPGNvZGluZz4N</span>
<span id="cb2-252"><a href="#cb2-252" aria-hidden="true" tabindex="-1"></a>CiAgICAgICAgICAgICAgPHN5c3RlbSB2YWx1ZT0iaHR0cDovL3Rlcm1pbm9sb2d5LmhsNy5vcmcv</span>
<span id="cb2-253"><a href="#cb2-253" aria-hidden="true" tabindex="-1"></a>Q29kZVN5c3RlbS92Mi0wMjAzIiAvPg0KICAgICAgICAgICAgICA8Y29kZSB2YWx1ZT0iTEFOUiIg</span>
<span id="cb2-254"><a href="#cb2-254" aria-hidden="true" tabindex="-1"></a>Lz4NCiAgICAgICAgICAgIDwvY29kaW5nPg0KICAgICAgICAgIDwvdHlwZT4NCiAgICAgICAgICA8</span>
<span id="cb2-255"><a href="#cb2-255" aria-hidden="true" tabindex="-1"></a>c3lzdGVtIHZhbHVlPSJodHRwczovL2ZoaXIua2J2LmRlL05hbWluZ1N5c3RlbS9LQlZfTlNfQmFz</span>
<span id="cb2-256"><a href="#cb2-256" aria-hidden="true" tabindex="-1"></a>ZV9BTlIiIC8+DQogICAgICAgICAgPHZhbHVlIHZhbHVlPSI4MzgzODIyMTAiIC8+DQogICAgICAg</span>
<span id="cb2-257"><a href="#cb2-257" aria-hidden="true" tabindex="-1"></a>IDwvaWRlbnRpZmllcj4NCiAgICAgICAgPG5hbWU+DQogICAgICAgICAgPHVzZSB2YWx1ZT0ib2Zm</span>
<span id="cb2-258"><a href="#cb2-258" aria-hidden="true" tabindex="-1"></a>aWNpYWwiIC8+DQogICAgICAgICAgPGZhbWlseSB2YWx1ZT0iTWVpZXIiPg0KICAgICAgICAgICAg</span>
<span id="cb2-259"><a href="#cb2-259" aria-hidden="true" tabindex="-1"></a>PGV4dGVuc2lvbiB1cmw9Imh0dHA6Ly9obDcub3JnL2ZoaXIvU3RydWN0dXJlRGVmaW5pdGlvbi9o</span>
<span id="cb2-260"><a href="#cb2-260" aria-hidden="true" tabindex="-1"></a>dW1hbm5hbWUtb3duLW5hbWUiPg0KICAgICAgICAgICAgICA8dmFsdWVTdHJpbmcgdmFsdWU9Ik1l</span>
<span id="cb2-261"><a href="#cb2-261" aria-hidden="true" tabindex="-1"></a>aWVyIiAvPg0KICAgICAgICAgICAgPC9leHRlbnNpb24+DQogICAgICAgICAgPC9mYW1pbHk+DQog</span>
<span id="cb2-262"><a href="#cb2-262" aria-hidden="true" tabindex="-1"></a>ICAgICAgICAgPGdpdmVuIHZhbHVlPSJKw7ZyZ2VuIiAvPg0KICAgICAgICA8L25hbWU+DQogICAg</span>
<span id="cb2-263"><a href="#cb2-263" aria-hidden="true" tabindex="-1"></a>ICAgIDxxdWFsaWZpY2F0aW9uPg0KICAgICAgICAgIDxjb2RlPg0KICAgICAgICAgICAgPGNvZGlu</span>
<span id="cb2-264"><a href="#cb2-264" aria-hidden="true" tabindex="-1"></a>Zz4NCiAgICAgICAgICAgICAgPHN5c3RlbSB2YWx1ZT0iaHR0cHM6Ly9maGlyLmtidi5kZS9Db2Rl</span>
<span id="cb2-265"><a href="#cb2-265" aria-hidden="true" tabindex="-1"></a>U3lzdGVtL0tCVl9DU19GT1JfUXVhbGlmaWNhdGlvbl9UeXBlIiAvPg0KICAgICAgICAgICAgICA8</span>
<span id="cb2-266"><a href="#cb2-266" aria-hidden="true" tabindex="-1"></a>Y29kZSB2YWx1ZT0iMDMiIC8+DQogICAgICAgICAgICA8L2NvZGluZz4NCiAgICAgICAgICA8L2Nv</span>
<span id="cb2-267"><a href="#cb2-267" aria-hidden="true" tabindex="-1"></a>ZGU+DQogICAgICAgIDwvcXVhbGlmaWNhdGlvbj4NCiAgICAgICAgPHF1YWxpZmljYXRpb24+DQog</span>
<span id="cb2-268"><a href="#cb2-268" aria-hidden="true" tabindex="-1"></a>ICAgICAgICAgPGNvZGU+DQogICAgICAgICAgICA8dGV4dCB2YWx1ZT0iQXJ6dCBpbiBXZWl0ZXJi</span>
<span id="cb2-269"><a href="#cb2-269" aria-hidden="true" tabindex="-1"></a>aWxkdW5nIiAvPg0KICAgICAgICAgIDwvY29kZT4NCiAgICAgICAgPC9xdWFsaWZpY2F0aW9uPg0K</span>
<span id="cb2-270"><a href="#cb2-270" aria-hidden="true" tabindex="-1"></a>ICAgICAgPC9QcmFjdGl0aW9uZXI+DQogICAgPC9yZXNvdXJjZT4NCiAgPC9lbnRyeT4NCiAgPGVu</span>
<span id="cb2-271"><a href="#cb2-271" aria-hidden="true" tabindex="-1"></a>dHJ5Pg0KICAgIDxmdWxsVXJsIHZhbHVlPSJodHRwOi8vcHZzLnByYXhpcy10b3BwLWdsdWVja2xp</span>
<span id="cb2-272"><a href="#cb2-272" aria-hidden="true" tabindex="-1"></a>Y2gubG9jYWwvZmhpci9Pcmdhbml6YXRpb24vY2YwNDJlNDQtMDg2YS00ZDUxLTljNzctMTcyZjlh</span>
<span id="cb2-273"><a href="#cb2-273" aria-hidden="true" tabindex="-1"></a>OTcyZTNiIiAvPg0KICAgIDxyZXNvdXJjZT4NCiAgICAgIDxPcmdhbml6YXRpb24geG1sbnM9Imh0</span>
<span id="cb2-274"><a href="#cb2-274" aria-hidden="true" tabindex="-1"></a>dHA6Ly9obDcub3JnL2ZoaXIiPg0KICAgICAgICA8aWQgdmFsdWU9ImNmMDQyZTQ0LTA4NmEtNGQ1</span>
<span id="cb2-275"><a href="#cb2-275" aria-hidden="true" tabindex="-1"></a>MS05Yzc3LTE3MmY5YTk3MmUzYiIgLz4NCiAgICAgICAgPG1ldGE+DQogICAgICAgICAgPHByb2Zp</span>
<span id="cb2-276"><a href="#cb2-276" aria-hidden="true" tabindex="-1"></a>bGUgdmFsdWU9Imh0dHBzOi8vZmhpci5rYnYuZGUvU3RydWN0dXJlRGVmaW5pdGlvbi9LQlZfUFJf</span>
<span id="cb2-277"><a href="#cb2-277" aria-hidden="true" tabindex="-1"></a>Rk9SX09yZ2FuaXphdGlvbnwxLjAuMyIgLz4NCiAgICAgICAgPC9tZXRhPg0KICAgICAgICA8aWRl</span>
<span id="cb2-278"><a href="#cb2-278" aria-hidden="true" tabindex="-1"></a>bnRpZmllcj4NCiAgICAgICAgICA8dHlwZT4NCiAgICAgICAgICAgIDxjb2Rpbmc+DQogICAgICAg</span>
<span id="cb2-279"><a href="#cb2-279" aria-hidden="true" tabindex="-1"></a>ICAgICAgIDxzeXN0ZW0gdmFsdWU9Imh0dHA6Ly90ZXJtaW5vbG9neS5obDcub3JnL0NvZGVTeXN0</span>
<span id="cb2-280"><a href="#cb2-280" aria-hidden="true" tabindex="-1"></a>ZW0vdjItMDIwMyIgLz4NCiAgICAgICAgICAgICAgPGNvZGUgdmFsdWU9IkJTTlIiIC8+DQogICAg</span>
<span id="cb2-281"><a href="#cb2-281" aria-hidden="true" tabindex="-1"></a>ICAgICAgICA8L2NvZGluZz4NCiAgICAgICAgICA8L3R5cGU+DQogICAgICAgICAgPHN5c3RlbSB2</span>
<span id="cb2-282"><a href="#cb2-282" aria-hidden="true" tabindex="-1"></a>YWx1ZT0iaHR0cHM6Ly9maGlyLmtidi5kZS9OYW1pbmdTeXN0ZW0vS0JWX05TX0Jhc2VfQlNOUiIg</span>
<span id="cb2-283"><a href="#cb2-283" aria-hidden="true" tabindex="-1"></a>Lz4NCiAgICAgICAgICA8dmFsdWUgdmFsdWU9IjAzMTIzNDU2NyIgLz4NCiAgICAgICAgPC9pZGVu</span>
<span id="cb2-284"><a href="#cb2-284" aria-hidden="true" tabindex="-1"></a>dGlmaWVyPg0KICAgICAgICA8bmFtZSB2YWx1ZT0iSGF1c2FyenRwcmF4aXMgRHIuIFRvcHAtR2zD</span>
<span id="cb2-285"><a href="#cb2-285" aria-hidden="true" tabindex="-1"></a>vGNrbGljaCIgLz4NCiAgICAgICAgPHRlbGVjb20+DQogICAgICAgICAgPHN5c3RlbSB2YWx1ZT0i</span>
<span id="cb2-286"><a href="#cb2-286" aria-hidden="true" tabindex="-1"></a>cGhvbmUiIC8+DQogICAgICAgICAgPHZhbHVlIHZhbHVlPSIwMzAxMjM0NTY3IiAvPg0KICAgICAg</span>
<span id="cb2-287"><a href="#cb2-287" aria-hidden="true" tabindex="-1"></a>ICA8L3RlbGVjb20+DQogICAgICAgIDxhZGRyZXNzPg0KICAgICAgICAgIDx0eXBlIHZhbHVlPSJi</span>
<span id="cb2-288"><a href="#cb2-288" aria-hidden="true" tabindex="-1"></a>b3RoIiAvPg0KICAgICAgICAgIDxsaW5lIHZhbHVlPSJNdXN0ZXJzdHIuIDIiPg0KICAgICAgICAg</span>
<span id="cb2-289"><a href="#cb2-289" aria-hidden="true" tabindex="-1"></a>ICAgPGV4dGVuc2lvbiB1cmw9Imh0dHA6Ly9obDcub3JnL2ZoaXIvU3RydWN0dXJlRGVmaW5pdGlv</span>
<span id="cb2-290"><a href="#cb2-290" aria-hidden="true" tabindex="-1"></a>bi9pc28yMTA5MC1BRFhQLWhvdXNlTnVtYmVyIj4NCiAgICAgICAgICAgICAgPHZhbHVlU3RyaW5n</span>
<span id="cb2-291"><a href="#cb2-291" aria-hidden="true" tabindex="-1"></a>IHZhbHVlPSIyIiAvPg0KICAgICAgICAgICAgPC9leHRlbnNpb24+DQogICAgICAgICAgICA8ZXh0</span>
<span id="cb2-292"><a href="#cb2-292" aria-hidden="true" tabindex="-1"></a>ZW5zaW9uIHVybD0iaHR0cDovL2hsNy5vcmcvZmhpci9TdHJ1Y3R1cmVEZWZpbml0aW9uL2lzbzIx</span>
<span id="cb2-293"><a href="#cb2-293" aria-hidden="true" tabindex="-1"></a>MDkwLUFEWFAtc3RyZWV0TmFtZSI+DQogICAgICAgICAgICAgIDx2YWx1ZVN0cmluZyB2YWx1ZT0i</span>
<span id="cb2-294"><a href="#cb2-294" aria-hidden="true" tabindex="-1"></a>TXVzdGVyc3RyLiIgLz4NCiAgICAgICAgICAgIDwvZXh0ZW5zaW9uPg0KICAgICAgICAgIDwvbGlu</span>
<span id="cb2-295"><a href="#cb2-295" aria-hidden="true" tabindex="-1"></a>ZT4NCiAgICAgICAgICA8Y2l0eSB2YWx1ZT0iQmVybGluIiAvPg0KICAgICAgICAgIDxwb3N0YWxD</span>
<span id="cb2-296"><a href="#cb2-296" aria-hidden="true" tabindex="-1"></a>b2RlIHZhbHVlPSIxMDYyMyIgLz4NCiAgICAgICAgPC9hZGRyZXNzPg0KICAgICAgPC9Pcmdhbml6</span>
<span id="cb2-297"><a href="#cb2-297" aria-hidden="true" tabindex="-1"></a>YXRpb24+DQogICAgPC9yZXNvdXJjZT4NCiAgPC9lbnRyeT4NCiAgPGVudHJ5Pg0KICAgIDxmdWxs</span>
<span id="cb2-298"><a href="#cb2-298" aria-hidden="true" tabindex="-1"></a>VXJsIHZhbHVlPSJodHRwOi8vcHZzLnByYXhpcy10b3BwLWdsdWVja2xpY2gubG9jYWwvZmhpci9D</span>
<span id="cb2-299"><a href="#cb2-299" aria-hidden="true" tabindex="-1"></a>b3ZlcmFnZS8xYjFmZmI2ZS1lYjA1LTQzZDctODdlYi1lNzgxOGZlOTY2MWEiIC8+DQogICAgPHJl</span>
<span id="cb2-300"><a href="#cb2-300" aria-hidden="true" tabindex="-1"></a>c291cmNlPg0KICAgICAgPENvdmVyYWdlIHhtbG5zPSJodHRwOi8vaGw3Lm9yZy9maGlyIj4NCiAg</span>
<span id="cb2-301"><a href="#cb2-301" aria-hidden="true" tabindex="-1"></a>ICAgICAgPGlkIHZhbHVlPSIxYjFmZmI2ZS1lYjA1LTQzZDctODdlYi1lNzgxOGZlOTY2MWEiIC8+</span>
<span id="cb2-302"><a href="#cb2-302" aria-hidden="true" tabindex="-1"></a>DQogICAgICAgIDxtZXRhPg0KICAgICAgICAgIDxwcm9maWxlIHZhbHVlPSJodHRwczovL2ZoaXIu</span>
<span id="cb2-303"><a href="#cb2-303" aria-hidden="true" tabindex="-1"></a>a2J2LmRlL1N0cnVjdHVyZURlZmluaXRpb24vS0JWX1BSX0ZPUl9Db3ZlcmFnZXwxLjAuMyIgLz4N</span>
<span id="cb2-304"><a href="#cb2-304" aria-hidden="true" tabindex="-1"></a>CiAgICAgICAgPC9tZXRhPg0KICAgICAgICA8ZXh0ZW5zaW9uIHVybD0iaHR0cDovL2ZoaXIuZGUv</span>
<span id="cb2-305"><a href="#cb2-305" aria-hidden="true" tabindex="-1"></a>U3RydWN0dXJlRGVmaW5pdGlvbi9na3YvYmVzb25kZXJlLXBlcnNvbmVuZ3J1cHBlIj4NCiAgICAg</span>
<span id="cb2-306"><a href="#cb2-306" aria-hidden="true" tabindex="-1"></a>ICAgICA8dmFsdWVDb2Rpbmc+DQogICAgICAgICAgICA8c3lzdGVtIHZhbHVlPSJodHRwczovL2Zo</span>
<span id="cb2-307"><a href="#cb2-307" aria-hidden="true" tabindex="-1"></a>aXIua2J2LmRlL0NvZGVTeXN0ZW0vS0JWX0NTX1NGSElSX0tCVl9QRVJTT05FTkdSVVBQRSIgLz4N</span>
<span id="cb2-308"><a href="#cb2-308" aria-hidden="true" tabindex="-1"></a>CiAgICAgICAgICAgIDxjb2RlIHZhbHVlPSIwMCIgLz4NCiAgICAgICAgICA8L3ZhbHVlQ29kaW5n</span>
<span id="cb2-309"><a href="#cb2-309" aria-hidden="true" tabindex="-1"></a>Pg0KICAgICAgICA8L2V4dGVuc2lvbj4NCiAgICAgICAgPGV4dGVuc2lvbiB1cmw9Imh0dHA6Ly9m</span>
<span id="cb2-310"><a href="#cb2-310" aria-hidden="true" tabindex="-1"></a>aGlyLmRlL1N0cnVjdHVyZURlZmluaXRpb24vZ2t2L2RtcC1rZW5uemVpY2hlbiI+DQogICAgICAg</span>
<span id="cb2-311"><a href="#cb2-311" aria-hidden="true" tabindex="-1"></a>ICAgPHZhbHVlQ29kaW5nPg0KICAgICAgICAgICAgPHN5c3RlbSB2YWx1ZT0iaHR0cHM6Ly9maGly</span>
<span id="cb2-312"><a href="#cb2-312" aria-hidden="true" tabindex="-1"></a>Lmtidi5kZS9Db2RlU3lzdGVtL0tCVl9DU19TRkhJUl9LQlZfRE1QIiAvPg0KICAgICAgICAgICAg</span>
<span id="cb2-313"><a href="#cb2-313" aria-hidden="true" tabindex="-1"></a>PGNvZGUgdmFsdWU9IjAwIiAvPg0KICAgICAgICAgIDwvdmFsdWVDb2Rpbmc+DQogICAgICAgIDwv</span>
<span id="cb2-314"><a href="#cb2-314" aria-hidden="true" tabindex="-1"></a>ZXh0ZW5zaW9uPg0KICAgICAgICA8ZXh0ZW5zaW9uIHVybD0iaHR0cDovL2ZoaXIuZGUvU3RydWN0</span>
<span id="cb2-315"><a href="#cb2-315" aria-hidden="true" tabindex="-1"></a>dXJlRGVmaW5pdGlvbi9na3Yvd29wIj4NCiAgICAgICAgICA8dmFsdWVDb2Rpbmc+DQogICAgICAg</span>
<span id="cb2-316"><a href="#cb2-316" aria-hidden="true" tabindex="-1"></a>ICAgICA8c3lzdGVtIHZhbHVlPSJodHRwczovL2ZoaXIua2J2LmRlL0NvZGVTeXN0ZW0vS0JWX0NT</span>
<span id="cb2-317"><a href="#cb2-317" aria-hidden="true" tabindex="-1"></a>X1NGSElSX0lUQV9XT1AiIC8+DQogICAgICAgICAgICA8Y29kZSB2YWx1ZT0iMDMiIC8+DQogICAg</span>
<span id="cb2-318"><a href="#cb2-318" aria-hidden="true" tabindex="-1"></a>ICAgICAgPC92YWx1ZUNvZGluZz4NCiAgICAgICAgPC9leHRlbnNpb24+DQogICAgICAgIDxleHRl</span>
<span id="cb2-319"><a href="#cb2-319" aria-hidden="true" tabindex="-1"></a>bnNpb24gdXJsPSJodHRwOi8vZmhpci5kZS9TdHJ1Y3R1cmVEZWZpbml0aW9uL2drdi92ZXJzaWNo</span>
<span id="cb2-320"><a href="#cb2-320" aria-hidden="true" tabindex="-1"></a>ZXJ0ZW5hcnQiPg0KICAgICAgICAgIDx2YWx1ZUNvZGluZz4NCiAgICAgICAgICAgIDxzeXN0ZW0g</span>
<span id="cb2-321"><a href="#cb2-321" aria-hidden="true" tabindex="-1"></a>dmFsdWU9Imh0dHBzOi8vZmhpci5rYnYuZGUvQ29kZVN5c3RlbS9LQlZfQ1NfU0ZISVJfS0JWX1ZF</span>
<span id="cb2-322"><a href="#cb2-322" aria-hidden="true" tabindex="-1"></a>UlNJQ0hFUlRFTlNUQVRVUyIgLz4NCiAgICAgICAgICAgIDxjb2RlIHZhbHVlPSIxIiAvPg0KICAg</span>
<span id="cb2-323"><a href="#cb2-323" aria-hidden="true" tabindex="-1"></a>ICAgICAgIDwvdmFsdWVDb2Rpbmc+DQogICAgICAgIDwvZXh0ZW5zaW9uPg0KICAgICAgICA8c3Rh</span>
<span id="cb2-324"><a href="#cb2-324" aria-hidden="true" tabindex="-1"></a>dHVzIHZhbHVlPSJhY3RpdmUiIC8+DQogICAgICAgIDx0eXBlPg0KICAgICAgICAgIDxjb2Rpbmc+</span>
<span id="cb2-325"><a href="#cb2-325" aria-hidden="true" tabindex="-1"></a>DQogICAgICAgICAgICA8c3lzdGVtIHZhbHVlPSJodHRwOi8vZmhpci5kZS9Db2RlU3lzdGVtL3Zl</span>
<span id="cb2-326"><a href="#cb2-326" aria-hidden="true" tabindex="-1"></a>cnNpY2hlcnVuZ3NhcnQtZGUtYmFzaXMiIC8+DQogICAgICAgICAgICA8Y29kZSB2YWx1ZT0iR0tW</span>
<span id="cb2-327"><a href="#cb2-327" aria-hidden="true" tabindex="-1"></a>IiAvPg0KICAgICAgICAgIDwvY29kaW5nPg0KICAgICAgICA8L3R5cGU+DQogICAgICAgIDxiZW5l</span>
<span id="cb2-328"><a href="#cb2-328" aria-hidden="true" tabindex="-1"></a>ZmljaWFyeT4NCiAgICAgICAgICA8cmVmZXJlbmNlIHZhbHVlPSJQYXRpZW50Lzk3NzRmNjdmLWEy</span>
<span id="cb2-329"><a href="#cb2-329" aria-hidden="true" tabindex="-1"></a>MzgtNGRhZi1iNGU2LTY3OWRlZWVmMzgxMSIgLz4NCiAgICAgICAgPC9iZW5lZmljaWFyeT4NCiAg</span>
<span id="cb2-330"><a href="#cb2-330" aria-hidden="true" tabindex="-1"></a>ICAgICAgPHBheW9yPg0KICAgICAgICAgIDxpZGVudGlmaWVyPg0KICAgICAgICAgICAgPHN5c3Rl</span>
<span id="cb2-331"><a href="#cb2-331" aria-hidden="true" tabindex="-1"></a>bSB2YWx1ZT0iaHR0cDovL2ZoaXIuZGUvTmFtaW5nU3lzdGVtL2FyZ2UtaWsvaWtuciIgLz4NCiAg</span>
<span id="cb2-332"><a href="#cb2-332" aria-hidden="true" tabindex="-1"></a>ICAgICAgICAgIDx2YWx1ZSB2YWx1ZT0iMTA0MjEyMDU5IiAvPg0KICAgICAgICAgIDwvaWRlbnRp</span>
<span id="cb2-333"><a href="#cb2-333" aria-hidden="true" tabindex="-1"></a>Zmllcj4NCiAgICAgICAgICA8ZGlzcGxheSB2YWx1ZT0iQU9LIFJoZWlubGFuZC9IYW1idXJnIiAv</span>
<span id="cb2-334"><a href="#cb2-334" aria-hidden="true" tabindex="-1"></a>Pg0KICAgICAgICA8L3BheW9yPg0KICAgICAgPC9Db3ZlcmFnZT4NCiAgICA8L3Jlc291cmNlPg0K</span>
<span id="cb2-335"><a href="#cb2-335" aria-hidden="true" tabindex="-1"></a>ICA8L2VudHJ5Pg0KPC9CdW5kbGU+</span>
<span id="cb2-336"><a href="#cb2-336" aria-hidden="true" tabindex="-1"></a>                    &lt;/<span class="kw">m2:Base64Data</span>&gt;</span>
<span id="cb2-337"><a href="#cb2-337" aria-hidden="true" tabindex="-1"></a>                &lt;/<span class="kw">m:Document</span>&gt;</span>
<span id="cb2-338"><a href="#cb2-338" aria-hidden="true" tabindex="-1"></a>                &lt;<span class="kw">m:IncludeRevocationInfo</span>&gt;true&lt;/<span class="kw">m:IncludeRevocationInfo</span>&gt;</span>
<span id="cb2-339"><a href="#cb2-339" aria-hidden="true" tabindex="-1"></a>            &lt;/<span class="kw">m:SignRequest</span>&gt;</span>
<span id="cb2-340"><a href="#cb2-340" aria-hidden="true" tabindex="-1"></a>        &lt;/<span class="kw">m:SignDocument</span>&gt;</span>
<span id="cb2-341"><a href="#cb2-341" aria-hidden="true" tabindex="-1"></a>    &lt;/<span class="kw">SOAP-ENV:Body</span>&gt;</span>
<span id="cb2-342"><a href="#cb2-342" aria-hidden="true" tabindex="-1"></a>&lt;/<span class="kw">SOAP-ENV:Envelope</span>&gt;</span></code></pre></div>
<div class="note">
<p>Mit der Referenz
<code>&lt;m2:SignatureType&gt;urn:ietf:rfc:5652&lt;/m2:SignatureType&gt;</code>
auf den RFC-5652 erfolgt die Erzeugung der QES als CMS-Signatur
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
<code>&lt;m:Document ID="CMS-Doc1" ShortText="a CMSDocument2sign"&gt;</code>
erfolgt die Übergabe des mittels QES zu signierenden FHIR-Bundles in
Base64-codierter Form.<br />
<strong><em>ShortText nicht länger als 30 Zeichen!</em></strong></p>
</div>
<div class="note">
<p>Das Flag
<code>&lt;m:IncludeRevocationInfo&gt;true&lt;/m:IncludeRevocationInfo&gt;</code>
weist den Konnektor an, die OCSP-Statusprüfung des Signaturzertifikats
in den Signaturcontainer mit einzubetten. Dadurch kann die spätere
Signaturprüfung ohne erneute Statusabfrage erfolgen.</p>
</div></td>
</tr>
</tbody>
</table>

Der Parameter `IncludeRevocationInfo = true` ist von herausragender
Bedeutung. Die in der Signatur eingebettete OCSP-Response vereinfacht
die Signaturprüfung im weiteren Prozess und in der späteren Abrechnung.

**Response**

    HTTP/1.1 200 OK
    Content-Type: text/xml;charset=utf-8

    <SOAP-ENV:Envelope
        xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
        <SOAP-ENV:Header/>
        <SOAP-ENV:Body>
            <ns8:SignDocumentResponse
                xmlns:ns10="urn:oasis:names:tc:dss-x:1.0:profiles:verificationreport:schema#"
                xmlns:ns11="http://uri.etsi.org/01903/v1.3.2#"
                xmlns:ns12="http://uri.etsi.org/02231/v2#"
                xmlns:ns2="http://ws.gematik.de/conn/EncryptionService/v6.1"
                xmlns:ns3="http://ws.gematik.de/conn/ConnectorCommon/v5.0"
                xmlns:ns4="http://ws.gematik.de/conn/ConnectorContext/v2.0"
                xmlns:ns5="urn:oasis:names:tc:dss:1.0:core:schema"
                xmlns:ns6="http://www.w3.org/2000/09/xmldsig#"
                xmlns:ns7="http://ws.gematik.de/tel/error/v2.0"
                xmlns:ns8="http://ws.gematik.de/conn/SignatureService/v7.4"
                xmlns:ns9="urn:oasis:names:tc:dss-x:1.0:profiles:SignaturePolicy:schema#">
                <ns8:SignResponse RequestID="Doc1">
                    <ns3:Status>
                        <ns3:Result>OK</ns3:Result>
                    </ns3:Status>
                    <ns8:OptionalOutputs>
                        <ns8:DocumentWithSignature ID="CMS-Doc1" ShortText="a CMSDocument2sign">
                            <ns5:Base64Data MimeType="text/plain; charset=utf-8"/>
                        </ns8:DocumentWithSignature>
                    </ns8:OptionalOutputs>
                    <ns5:SignatureObject>
                        <ns5:Base64Signature Type="urn:ietf:rfc:5652">MIJTfQYJKoZIhvcNAQcCoIJTbjCCU2oCAQUxDzANBglghkgBZQMEAgEFADCCRIMGCSqGSIb3DQEHAaCCRHQEgkRwPEJ1bmRsZSB4bWxucz0iaHR0cDovL2hsNy5vcmcvZmhpciI+DQogIDwhLS0gQmVpc3BpZWwtQnVuZGxlIFdpcmtzdG9mZnZlcm9yZG51bmcgLS0+DQogIDxpZCB2YWx1ZT0iNGZlMjAxM2QtYWU5NC00NDFhLWExYjEtNzgyMzZhZTY1NjgwIiAvPg0KICA8bWV0YT4NCiAgICA8bGFzdFVwZGF0ZWQgdmFsdWU9IjIwMjAtMDUtMDRUMDg6MzA6MDBaIiAvPg0KICAgIDxwcm9maWxlIHZhbHVlPSJodHRwczovL2ZoaXIua2J2LmRlL1N0cnVjdHVyZURlZmluaXRpb24vS0JWX1BSX0VSUF9CdW5kbGV8MS4wLjEiIC8+DQogIDwvbWV0YT4NCiAgPGlkZW50aWZpZXI+DQogICAgPHN5c3RlbSB2YWx1ZT0iaHR0cHM6Ly9nZW1hdGlrLmRlL2ZoaXIvTmFtaW5nU3lzdGVtL1ByZXNjcmlwdGlvbklEIiAvPg0KICAgIDx2YWx1ZSB2YWx1ZT0iMTYwLjEyMy40NTYuNzg5LjEyMy41OCIgLz4NCiAgPC9pZGVudGlmaWVyPg0KICA8dHlwZSB2YWx1ZT0iZG9jdW1lbnQiIC8+DQogIDx0aW1lc3RhbXAgdmFsdWU9IjIwMjAtMDUtMDRUMDg6MzA6MDBaIiAvPg0KICA8ZW50cnk+DQogICAgPGZ1bGxVcmwgdmFsdWU9Imh0dHA6Ly9wdnMucHJheGlzLXRvcHAtZ2x1ZWNrbGljaC5sb2NhbC9maGlyL0NvbXBvc2l0aW9uL2IwZTIyYjg2LWU3ZTktNDZjMS04MGZlLWU2ZTI0NDQyZDc3YyIgLz4NCiAgICA8cmVzb3VyY2U+DQogICAgICA8Q29tcG9zaXRpb24geG1sbnM9Imh0dHA6Ly9obDcub3JnL2ZoaXIiPg0KICAgICAgICA8aWQgdmFsdWU9ImIwZTIyYjg2LWU3ZTktNDZjMS04MGZlLWU2ZTI0NDQyZDc3YyIgLz4NCiAgICAgICAgPG1ldGE+DQogICAgICAgICAgPHByb2ZpbGUgdmFsdWU9Imh0dHBzOi8vZmhpci5rYnYuZGUvU3RydWN0dXJlRGVmaW5pdGlvbi9LQlZfUFJfRVJQX0NvbXBvc2l0aW9ufDEuMC4xIiAvPg0KICAgICAgICA8L21ldGE+DQogICAgICAgIDxleHRlbnNpb24gdXJsPSJodHRwczovL2ZoaXIua2J2LmRlL1N0cnVjdHVyZURlZmluaXRpb24vS0JWX0VYX0ZPUl9MZWdhbF9iYXNpcyI+DQogICAgICAgICAgPHZhbHVlQ29kaW5nPg0KICAgICAgICAgICAgPHN5c3RlbSB2YWx1ZT0iaHR0cHM6Ly9maGlyLmtidi5kZS9Db2RlU3lzdGVtL0tCVl9DU19TRkhJUl9LQlZfU1RBVFVTS0VOTlpFSUNIRU4iIC8+DQogICAgICAgICAgICA8Y29kZSB2YWx1ZT0iMDAiIC8+DQogICAgICAgICAgPC92YWx1ZUNvZGluZz4NCiAgICAgICAgPC9leHRlbnNpb24+DQogICAgICAgIDxzdGF0dXMgdmFsdWU9ImZpbmFsIiAvPg0KICAgICAgICA8dHlwZT4NCiAgICAgICAgICA8Y29kaW5nPg0KICAgICAgICAgICAgPHN5c3RlbSB2YWx1ZT0iaHR0cHM6Ly9maGlyLmtidi5kZS9Db2RlU3lzdGVtL0tCVl9DU19TRkhJUl9LQlZfRk9STVVMQVJfQVJUIiAvPg0KICAgICAgICAgICAgPGNvZGUgdmFsdWU9ImUxNkEiIC8+DQogICAgICAgICAgPC9jb2Rpbmc+DQogICAgICAgIDwvdHlwZT4NCiAgICAgICAgPHN1YmplY3Q+DQogICAgICAgICAgPHJlZmVyZW5jZSB2YWx1ZT0iUGF0aWVudC85Nzc0ZjY3Zi1hMjM4LTRkYWYtYjRlNi02NzlkZWVlZjM4MTEiIC8+DQogICAgICAgIDwvc3ViamVjdD4NCiAgICAgICAgPGRhdGUgdmFsdWU9IjIwMjAtMDItMDNUMTE6MzA6MDJaIiAvPg0KICAgICAgICA8YXV0aG9yPg0KICAgICAgICAgIDxyZWZlcmVuY2UgdmFsdWU9IlByYWN0aXRpb25lci9kODQ2M2RhZi0yNThlLTRjYWQtYTg2YS02ZmQ0MmZhYzE2MWMiIC8+DQogICAgICAgICAgPHR5cGUgdmFsdWU9IlByYWN0aXRpb25lciIgLz4NCiAgICAgICAgPC9hdXRob3I+DQogICAgICAgIDxhdXRob3I+DQogICAgICAgICAgPHR5cGUgdmFsdWU9IkRldmljZSIgLz4NCiAgICAgICAgICA8aWRlbnRpZmllcj4NCiAgICAgICAgICAgIDxzeXN0ZW0gdmFsdWU9Imh0dHBzOi8vZmhpci5rYnYuZGUvTmFtaW5nU3lzdGVtL0tCVl9OU19GT1JfUHJ1ZWZudW1tZXIiIC8+DQogICAgICAgICAgICA8dmFsdWUgdmFsdWU9IlkvNDAwLzE5MTAvMzYvMzQ2IiAvPg0KICAgICAgICAgIDwvaWRlbnRpZmllcj4NCiAgICAgICAgPC9hdXRob3I+DQogICAgICAgIDx0aXRsZSB2YWx1ZT0iZWxla3Ryb25pc2NoZSBBcnpuZWltaXR0ZWx2ZXJvcmRudW5nIiAvPg0KICAgICAgICA8YXR0ZXN0ZXI+DQogICAgICAgICAgPG1vZGUgdmFsdWU9ImxlZ2FsIiAvPg0KICAgICAgICAgIDxwYXJ0eT4NCiAgICAgICAgICAgIDxyZWZlcmVuY2UgdmFsdWU9IlByYWN0aXRpb25lci8yMDU5N2UwZS1jYjJhLTQ1YjMtOTVmMC1kYzNkYmRiNjE3YzMiIC8+DQogICAgICAgICAgPC9wYXJ0eT4NCiAgICAgICAgPC9hdHRlc3Rlcj4NCiAgICAgICAgPGN1c3RvZGlhbj4NCiAgICAgICAgICA8cmVmZXJlbmNlIHZhbHVlPSJPcmdhbml6YXRpb24vY2YwNDJlNDQtMDg2YS00ZDUxLTljNzctMTcyZjlhOTcyZTNiIiAvPg0KICAgICAgICA8L2N1c3RvZGlhbj4NCiAgICAgICAgPHNlY3Rpb24+DQogICAgICAgICAgPGNvZGU+DQogICAgICAgICAgICA8Y29kaW5nPg0KICAgICAgICAgICAgICA8c3lzdGVtIHZhbHVlPSJodHRwczovL2ZoaXIua2J2LmRlL0NvZGVTeXN0ZW0vS0JWX0NTX0VSUF9TZWN0aW9uX1R5cGUiIC8+DQogICAgICAgICAgICAgIDxjb2RlIHZhbHVlPSJQcmVzY3JpcHRpb24iIC8+DQogICAgICAgICAgICA8L2NvZGluZz4NCiAgICAgICAgICA8L2NvZGU+DQogICAgICAgICAgPGVudHJ5Pg0KICAgICAgICAgICAgPCEtLSBSZWZlcmVueiBhdWYgVmVyb3JkbnVuZyAoTWVkaWNhdGlvblJlcXVlc3QpIC0tPg0KICAgICAgICAgICAgPHJlZmVyZW5jZSB2YWx1ZT0iTWVkaWNhdGlvblJlcXVlc3QvZjU4ZjQ0MDMtN2EzYS00YTEyLWJiMTUtYjJmYTI1YjAyNTYxIiAvPg0KICAgICAgICAgIDwvZW50cnk+DQogICAgICAgIDwvc2VjdGlvbj4NCiAgICAgICAgPHNlY3Rpb24+DQogICAgICAgICAgPGNvZGU+DQogICAgICAgICAgICA8Y29kaW5nPg0KICAgICAgICAgICAgICA8c3lzdGVtIHZhbHVlPSJodHRwczovL2ZoaXIua2J2LmRlL0NvZGVTeXN0ZW0vS0JWX0NTX0VSUF9TZWN0aW9uX1R5cGUiIC8+DQogICAgICAgICAgICAgIDxjb2RlIHZhbHVlPSJDb3ZlcmFnZSIgLz4NCiAgICAgICAgICAgIDwvY29kaW5nPg0KICAgICAgICAgIDwvY29kZT4NCiAgICAgICAgICA8ZW50cnk+DQogICAgICAgICAgICA8IS0tIFJlZmVyZW56IGF1ZiBLcmFua2Vua2Fzc2UvS29zdGVudHLEgsKkZ2VyICAtLT4NCiAgICAgICAgICAgIDxyZWZlcmVuY2UgdmFsdWU9IkNvdmVyYWdlLzFiMWZmYjZlLWViMDUtNDNkNy04N2ViLWU3ODE4ZmU5NjYxYSIgLz4NCiAgICAgICAgICA8L2VudHJ5Pg0KICAgICAgICA8L3NlY3Rpb24+DQogICAgICA8L0NvbXBvc2l0aW9uPg0KICAgIDwvcmVzb3VyY2U+DQogIDwvZW50cnk+DQogIDxlbnRyeT4NCiAgICA8ZnVsbFVybCB2YWx1ZT0iaHR0cDovL3B2cy5wcmF4aXMtdG9wcC1nbHVlY2tsaWNoLmxvY2FsL2ZoaXIvTWVkaWNhdGlvblJlcXVlc3QvZjU4ZjQ0MDMtN2EzYS00YTEyLWJiMTUtYjJmYTI1YjAyNTYxIiAvPg0KICAgIDxyZXNvdXJjZT4NCiAgICAgIDxNZWRpY2F0aW9uUmVxdWVzdCB4bWxucz0iaHR0cDovL2hsNy5vcmcvZmhpciI+DQogICAgICAgIDxpZCB2YWx1ZT0iZjU4ZjQ0MDMtN2EzYS00YTEyLWJiMTUtYjJmYTI1YjAyNTYxIiAvPg0KICAgICAgICA8bWV0YT4NCiAgICAgICAgICA8cHJvZmlsZSB2YWx1ZT0iaHR0cHM6Ly9maGlyLmtidi5kZS9TdHJ1Y3R1cmVEZWZpbml0aW9uL0tCVl9QUl9FUlBfUHJlc2NyaXB0aW9ufDEuMC4xIiAvPg0KICAgICAgICA8L21ldGE+DQogICAgICAgIDxleHRlbnNpb24gdXJsPSJodHRwczovL2ZoaXIua2J2LmRlL1N0cnVjdHVyZURlZmluaXRpb24vS0JWX0VYX0VSUF9TdGF0dXNDb1BheW1lbnQiPg0KICAgICAgICAgIDx2YWx1ZUNvZGluZz4NCiAgICAgICAgICAgIDxzeXN0ZW0gdmFsdWU9Imh0dHBzOi8vZmhpci5rYnYuZGUvQ29kZVN5c3RlbS9LQlZfQ1NfRVJQX1N0YXR1c0NvUGF5bWVudCIgLz4NCiAgICAgICAgICAgIDxjb2RlIHZhbHVlPSIwIiAvPg0KICAgICAgICAgIDwvdmFsdWVDb2Rpbmc+DQogICAgICAgIDwvZXh0ZW5zaW9uPg0KICAgICAgICA8ZXh0ZW5zaW9uIHVybD0iaHR0cHM6Ly9maGlyLmtidi5kZS9TdHJ1Y3R1cmVEZWZpbml0aW9uL0tCVl9FWF9FUlBfRW1lcmdlbmN5U2VydmljZXNGZWUiPg0KICAgICAgICAgIDx2YWx1ZUJvb2xlYW4gdmFsdWU9ImZhbHNlIiAvPg0KICAgICAgICA8L2V4dGVuc2lvbj4NCiAgICAgICAgPGV4dGVuc2lvbiB1cmw9Imh0dHBzOi8vZmhpci5rYnYuZGUvU3RydWN0dXJlRGVmaW5pdGlvbi9LQlZfRVhfRVJQX0JWRyI+DQogICAgICAgICAgPHZhbHVlQm9vbGVhbiB2YWx1ZT0iZmFsc2UiIC8+DQogICAgICAgIDwvZXh0ZW5zaW9uPg0KICAgICAgICA8ZXh0ZW5zaW9uIHVybD0iaHR0cHM6Ly9maGlyLmtidi5kZS9TdHJ1Y3R1cmVEZWZpbml0aW9uL0tCVl9FWF9FUlBfQWNjaWRlbnQiPg0KICAgICAgICAgIDxleHRlbnNpb24gdXJsPSJ1bmZhbGxrZW5uemVpY2hlbiI+DQogICAgICAgICAgICA8dmFsdWVDb2Rpbmc+DQogICAgICAgICAgICAgIDxzeXN0ZW0gdmFsdWU9Imh0dHBzOi8vZmhpci5rYnYuZGUvQ29kZVN5c3RlbS9LQlZfQ1NfRk9SX1Vyc2FjaGVfVHlwZSIgLz4NCiAgICAgICAgICAgICAgPGNvZGUgdmFsdWU9IjEiIC8+DQogICAgICAgICAgICA8L3ZhbHVlQ29kaW5nPg0KICAgICAgICAgIDwvZXh0ZW5zaW9uPg0KICAgICAgICAgIDxleHRlbnNpb24gdXJsPSJ1bmZhbGx0YWciPg0KICAgICAgICAgICAgPHZhbHVlRGF0ZSB2YWx1ZT0iMjAyMC0wNS0wMSIgLz4NCiAgICAgICAgICA8L2V4dGVuc2lvbj4NCiAgICAgICAgPC9leHRlbnNpb24+DQogICAgICAgIDxleHRlbnNpb24gdXJsPSJodHRwczovL2ZoaXIua2J2LmRlL1N0cnVjdHVyZURlZmluaXRpb24vS0JWX0VYX0VSUF9NdWx0aXBsZV9QcmVzY3JpcHRpb24iPg0KICAgICAgICAgIDxleHRlbnNpb24gdXJsPSJLZW5uemVpY2hlbiI+DQogICAgICAgICAgICA8dmFsdWVCb29sZWFuIHZhbHVlPSJ0cnVlIiAvPg0KICAgICAgICAgIDwvZXh0ZW5zaW9uPg0KICAgICAgICAgIDxleHRlbnNpb24gdXJsPSJOdW1tZXJpZXJ1bmciPg0KICAgICAgICAgICAgPHZhbHVlUmF0aW8+DQogICAgICAgICAgICAgIDxudW1lcmF0b3I+DQogICAgICAgICAgICAgICAgPHZhbHVlIHZhbHVlPSIyIiAvPg0KICAgICAgICAgICAgICA8L251bWVyYXRvcj4NCiAgICAgICAgICAgICAgPGRlbm9taW5hdG9yPg0KICAgICAgICAgICAgICAgIDx2YWx1ZSB2YWx1ZT0iNCIgLz4NCiAgICAgICAgICAgICAgPC9kZW5vbWluYXRvcj4NCiAgICAgICAgICAgIDwvdmFsdWVSYXRpbz4NCiAgICAgICAgICA8L2V4dGVuc2lvbj4NCiAgICAgICAgICA8ZXh0ZW5zaW9uIHVybD0iWmVpdHJhdW0iPg0KICAgICAgICAgICAgPHZhbHVlUGVyaW9kPg0KICAgICAgICAgICAgICA8c3RhcnQgdmFsdWU9IjIwMjEtMDEtMDIiIC8+DQogICAgICAgICAgICAgIDxlbmQgdmFsdWU9IjIwMjEtMDMtMzAiIC8+DQogICAgICAgICAgICA8L3ZhbHVlUGVyaW9kPg0KICAgICAgICAgIDwvZXh0ZW5zaW9uPg0KICAgICAgICA8L2V4dGVuc2lvbj4NCiAgICAgICAgPHN0YXR1cyB2YWx1ZT0iYWN0aXZlIiAvPg0KICAgICAgICA8aW50ZW50IHZhbHVlPSJvcmRlciIgLz4NCiAgICAgICAgPG1lZGljYXRpb25SZWZlcmVuY2U+DQogICAgICAgICAgPHJlZmVyZW5jZSB2YWx1ZT0iTWVkaWNhdGlvbi9lM2E0ZWZhNy04NGZjLTQ2NWItYjE0Yy03MjAxOTUwOTc3ODMiIC8+DQogICAgICAgIDwvbWVkaWNhdGlvblJlZmVyZW5jZT4NCiAgICAgICAgPHN1YmplY3Q+DQogICAgICAgICAgPHJlZmVyZW5jZSB2YWx1ZT0iUGF0aWVudC85Nzc0ZjY3Zi1hMjM4LTRkYWYtYjRlNi02NzlkZWVlZjM4MTEiIC8+DQogICAgICAgIDwvc3ViamVjdD4NCiAgICAgICAgPGF1dGhvcmVkT24gdmFsdWU9IjIwMjAtMDUtMDIiIC8+DQogICAgICAgIDxyZXF1ZXN0ZXI+DQogICAgICAgICAgPHJlZmVyZW5jZSB2YWx1ZT0iUHJhY3RpdGlvbmVyLzIwNTk3ZTBlLWNiMmEtNDViMy05NWYwLWRjM2RiZGI2MTdjMyIgLz4NCiAgICAgICAgPC9yZXF1ZXN0ZXI+DQogICAgICAgIDxpbnN1cmFuY2U+DQogICAgICAgICAgPHJlZmVyZW5jZSB2YWx1ZT0iQ292ZXJhZ2UvMWIxZmZiNmUtZWIwNS00M2Q3LTg3ZWItZTc4MThmZTk2NjFhIiAvPg0KICAgICAgICA8L2luc3VyYW5jZT4NCiAgICAgICAgPG5vdGU+DQogICAgICAgICAgPHRleHQgdmFsdWU9IkR1bW15LUhpbndlaXMgZsO8ciBkaWUgQXBvdGhla2UiIC8+DQogICAgICAgIDwvbm90ZT4NCiAgICAgICAgPGRvc2FnZUluc3RydWN0aW9uPg0KICAgICAgICAgIDxleHRlbnNpb24gdXJsPSJodHRwczovL2ZoaXIua2J2LmRlL1N0cnVjdHVyZURlZmluaXRpb24vS0JWX0VYX0VSUF9Eb3NhZ2VGbGFnIj4NCiAgICAgICAgICAgIDx2YWx1ZUJvb2xlYW4gdmFsdWU9ImZhbHNlIiAvPg0KICAgICAgICAgIDwvZXh0ZW5zaW9uPg0KICAgICAgICA8L2Rvc2FnZUluc3RydWN0aW9uPg0KICAgICAgICA8ZGlzcGVuc2VSZXF1ZXN0Pg0KICAgICAgICAgIDxxdWFudGl0eT4NCiAgICAgICAgICAgIDx2YWx1ZSB2YWx1ZT0iMiIgLz4NCiAgICAgICAgICAgIDxzeXN0ZW0gdmFsdWU9Imh0dHA6Ly91bml0c29mbWVhc3VyZS5vcmciIC8+DQogICAgICAgICAgICA8Y29kZSB2YWx1ZT0ie1BhY2thZ2V9IiAvPg0KICAgICAgICAgIDwvcXVhbnRpdHk+DQogICAgICAgIDwvZGlzcGVuc2VSZXF1ZXN0Pg0KICAgICAgICA8c3Vic3RpdHV0aW9uPg0KICAgICAgICAgIDxhbGxvd2VkQm9vbGVhbiB2YWx1ZT0idHJ1ZSIgLz4NCiAgICAgICAgPC9zdWJzdGl0dXRpb24+DQogICAgICA8L01lZGljYXRpb25SZXF1ZXN0Pg0KICAgIDwvcmVzb3VyY2U+DQogIDwvZW50cnk+DQogIDxlbnRyeT4NCiAgICA8ZnVsbFVybCB2YWx1ZT0iaHR0cDovL3B2cy5wcmF4aXMtdG9wcC1nbHVlY2tsaWNoLmxvY2FsL2ZoaXIvTWVkaWNhdGlvbi9lM2E0ZWZhNy04NGZjLTQ2NWItYjE0Yy03MjAxOTUwOTc3ODMiIC8+DQogICAgPHJlc291cmNlPg0KICAgICAgPE1lZGljYXRpb24geG1sbnM9Imh0dHA6Ly9obDcub3JnL2ZoaXIiPg0KICAgICAgICA8aWQgdmFsdWU9ImUzYTRlZmE3LTg0ZmMtNDY1Yi1iMTRjLTcyMDE5NTA5Nzc4MyIgLz4NCiAgICAgICAgPG1ldGE+DQogICAgICAgICAgPHByb2ZpbGUgdmFsdWU9Imh0dHBzOi8vZmhpci5rYnYuZGUvU3RydWN0dXJlRGVmaW5pdGlvbi9LQlZfUFJfRVJQX01lZGljYXRpb25fSW5ncmVkaWVudHwxLjAuMSIgLz4NCiAgICAgICAgPC9tZXRhPg0KICAgICAgICA8ZXh0ZW5zaW9uIHVybD0iaHR0cHM6Ly9maGlyLmtidi5kZS9TdHJ1Y3R1cmVEZWZpbml0aW9uL0tCVl9FWF9FUlBfTWVkaWNhdGlvbl9DYXRlZ29yeSI+DQogICAgICAgICAgPHZhbHVlQ29kaW5nPg0KICAgICAgICAgICAgPHN5c3RlbSB2YWx1ZT0iaHR0cHM6Ly9maGlyLmtidi5kZS9Db2RlU3lzdGVtL0tCVl9DU19FUlBfTWVkaWNhdGlvbl9DYXRlZ29yeSIgLz4NCiAgICAgICAgICAgIDxjb2RlIHZhbHVlPSIwMCIgLz4NCiAgICAgICAgICA8L3ZhbHVlQ29kaW5nPg0KICAgICAgICA8L2V4dGVuc2lvbj4NCiAgICAgICAgPGV4dGVuc2lvbiB1cmw9Imh0dHBzOi8vZmhpci5rYnYuZGUvU3RydWN0dXJlRGVmaW5pdGlvbi9LQlZfRVhfRVJQX01lZGljYXRpb25fVmFjY2luZSI+DQogICAgICAgICAgPHZhbHVlQm9vbGVhbiB2YWx1ZT0iZmFsc2UiIC8+DQogICAgICAgIDwvZXh0ZW5zaW9uPg0KICAgICAgICA8Y29kZT4NCiAgICAgICAgICA8Y29kaW5nPg0KICAgICAgICAgICAgPHN5c3RlbSB2YWx1ZT0iaHR0cHM6Ly9maGlyLmtidi5kZS9Db2RlU3lzdGVtL0tCVl9DU19FUlBfTWVkaWNhdGlvbl9UeXBlIiAvPg0KICAgICAgICAgICAgPGNvZGUgdmFsdWU9IndpcmtzdG9mZiIgLz4NCiAgICAgICAgICA8L2NvZGluZz4NCiAgICAgICAgPC9jb2RlPg0KICAgICAgICA8Zm9ybT4NCiAgICAgICAgICA8dGV4dCB2YWx1ZT0iVGFibGV0dGVuIiAvPg0KICAgICAgICA8L2Zvcm0+DQogICAgICAgIDxhbW91bnQ+DQogICAgICAgICAgPG51bWVyYXRvcj4NCiAgICAgICAgICAgIDx2YWx1ZSB2YWx1ZT0iMjAiIC8+DQogICAgICAgICAgICA8dW5pdCB2YWx1ZT0iU3RrIiAvPg0KICAgICAgICAgIDwvbnVtZXJhdG9yPg0KICAgICAgICAgIDxkZW5vbWluYXRvcj4NCiAgICAgICAgICAgIDx2YWx1ZSB2YWx1ZT0iMSIgLz4NCiAgICAgICAgICA8L2Rlbm9taW5hdG9yPg0KICAgICAgICA8L2Ftb3VudD4NCiAgICAgICAgPGluZ3JlZGllbnQ+DQogICAgICAgICAgPGl0ZW1Db2RlYWJsZUNvbmNlcHQ+DQogICAgICAgICAgICA8Y29kaW5nPg0KICAgICAgICAgICAgICA8c3lzdGVtIHZhbHVlPSJodHRwOi8vZmhpci5kZS9Db2RlU3lzdGVtL2FzayIgLz4NCiAgICAgICAgICAgICAgPGNvZGUgdmFsdWU9IkR1bW15LUFTSyIgLz4NCiAgICAgICAgICAgIDwvY29kaW5nPg0KICAgICAgICAgICAgPHRleHQgdmFsdWU9IklidXByb2ZlbiIgLz4NCiAgICAgICAgICA8L2l0ZW1Db2RlYWJsZUNvbmNlcHQ+DQogICAgICAgICAgPHN0cmVuZ3RoPg0KICAgICAgICAgICAgPG51bWVyYXRvcj4NCiAgICAgICAgICAgICAgPHZhbHVlIHZhbHVlPSI4MDAiIC8+DQogICAgICAgICAgICAgIDx1bml0IHZhbHVlPSJtZyIgLz4NCiAgICAgICAgICAgIDwvbnVtZXJhdG9yPg0KICAgICAgICAgICAgPGRlbm9taW5hdG9yPg0KICAgICAgICAgICAgICA8dmFsdWUgdmFsdWU9IjEiIC8+DQogICAgICAgICAgICA8L2Rlbm9taW5hdG9yPg0KICAgICAgICAgIDwvc3RyZW5ndGg+DQogICAgICAgIDwvaW5ncmVkaWVudD4NCiAgICAgIDwvTWVkaWNhdGlvbj4NCiAgICA8L3Jlc291cmNlPg0KICA8L2VudHJ5Pg0KICA8ZW50cnk+DQogICAgPGZ1bGxVcmwgdmFsdWU9Imh0dHA6Ly9wdnMucHJheGlzLXRvcHAtZ2x1ZWNrbGljaC5sb2NhbC9maGlyL1BhdGllbnQvOTc3NGY2N2YtYTIzOC00ZGFmLWI0ZTYtNjc5ZGVlZWYzODExIiAvPg0KICAgIDxyZXNvdXJjZT4NCiAgICAgIDxQYXRpZW50IHhtbG5zPSJodHRwOi8vaGw3Lm9yZy9maGlyIj4NCiAgICAgICAgPGlkIHZhbHVlPSI5Nzc0ZjY3Zi1hMjM4LTRkYWYtYjRlNi02NzlkZWVlZjM4MTEiIC8+DQogICAgICAgIDxtZXRhPg0KICAgICAgICAgIDxwcm9maWxlIHZhbHVlPSJodHRwczovL2ZoaXIua2J2LmRlL1N0cnVjdHVyZURlZmluaXRpb24vS0JWX1BSX0ZPUl9QYXRpZW50fDEuMC4zIiAvPg0KICAgICAgICA8L21ldGE+DQogICAgICAgIDxpZGVudGlmaWVyPg0KICAgICAgICAgIDx0eXBlPg0KICAgICAgICAgICAgPGNvZGluZz4NCiAgICAgICAgICAgICAgPHN5c3RlbSB2YWx1ZT0iaHR0cDovL2ZoaXIuZGUvQ29kZVN5c3RlbS9pZGVudGlmaWVyLXR5cGUtZGUtYmFzaXMiIC8+DQogICAgICAgICAgICAgIDxjb2RlIHZhbHVlPSJHS1YiIC8+DQogICAgICAgICAgICA8L2NvZGluZz4NCiAgICAgICAgICA8L3R5cGU+DQogICAgICAgICAgPHN5c3RlbSB2YWx1ZT0iaHR0cDovL2ZoaXIuZGUvTmFtaW5nU3lzdGVtL2drdi9rdmlkLTEwIiAvPg0KICAgICAgICAgIDx2YWx1ZSB2YWx1ZT0iWDIzNDU2Nzg5MCIgLz4NCiAgICAgICAgPC9pZGVudGlmaWVyPg0KICAgICAgICA8bmFtZT4NCiAgICAgICAgICA8dXNlIHZhbHVlPSJvZmZpY2lhbCIgLz4NCiAgICAgICAgICA8ZmFtaWx5IHZhbHVlPSJMdWRnZXIgS8O2bmlnc3N0ZWluIj4NCiAgICAgICAgICAgIDxleHRlbnNpb24gdXJsPSJodHRwOi8vaGw3Lm9yZy9maGlyL1N0cnVjdHVyZURlZmluaXRpb24vaHVtYW5uYW1lLW93bi1uYW1lIj4NCiAgICAgICAgICAgICAgPHZhbHVlU3RyaW5nIHZhbHVlPSJLw7ZuaWdzc3RlaW4iIC8+DQogICAgICAgICAgICA8L2V4dGVuc2lvbj4NCiAgICAgICAgICA8L2ZhbWlseT4NCiAgICAgICAgICA8Z2l2ZW4gdmFsdWU9Ikx1ZGdlciIgLz4NCiAgICAgICAgPC9uYW1lPg0KICAgICAgICA8YmlydGhEYXRlIHZhbHVlPSIxOTM1LTA2LTIyIiAvPg0KICAgICAgICA8YWRkcmVzcz4NCiAgICAgICAgICA8dHlwZSB2YWx1ZT0iYm90aCIgLz4NCiAgICAgICAgICA8bGluZSB2YWx1ZT0iTXVzdGVyc3RyLiAxIj4NCiAgICAgICAgICAgIDxleHRlbnNpb24gdXJsPSJodHRwOi8vaGw3Lm9yZy9maGlyL1N0cnVjdHVyZURlZmluaXRpb24vaXNvMjEwOTAtQURYUC1ob3VzZU51bWJlciI+DQogICAgICAgICAgICAgIDx2YWx1ZVN0cmluZyB2YWx1ZT0iMSIgLz4NCiAgICAgICAgICAgIDwvZXh0ZW5zaW9uPg0KICAgICAgICAgICAgPGV4dGVuc2lvbiB1cmw9Imh0dHA6Ly9obDcub3JnL2ZoaXIvU3RydWN0dXJlRGVmaW5pdGlvbi9pc28yMTA5MC1BRFhQLXN0cmVldE5hbWUiPg0KICAgICAgICAgICAgICA8dmFsdWVTdHJpbmcgdmFsdWU9Ik11c3RlcnN0ci4iIC8+DQogICAgICAgICAgICA8L2V4dGVuc2lvbj4NCiAgICAgICAgICA8L2xpbmU+DQogICAgICAgICAgPGNpdHkgdmFsdWU9IkJlcmxpbiIgLz4NCiAgICAgICAgICA8cG9zdGFsQ29kZSB2YWx1ZT0iMTA2MjMiIC8+DQogICAgICAgIDwvYWRkcmVzcz4NCiAgICAgIDwvUGF0aWVudD4NCiAgICA8L3Jlc291cmNlPg0KICA8L2VudHJ5Pg0KICA8ZW50cnk+DQogICAgPGZ1bGxVcmwgdmFsdWU9Imh0dHA6Ly9wdnMucHJheGlzLXRvcHAtZ2x1ZWNrbGljaC5sb2NhbC9maGlyL1ByYWN0aXRpb25lci8yMDU5N2UwZS1jYjJhLTQ1YjMtOTVmMC1kYzNkYmRiNjE3YzMiIC8+DQogICAgPHJlc291cmNlPg0KICAgICAgPFByYWN0aXRpb25lciB4bWxucz0iaHR0cDovL2hsNy5vcmcvZmhpciI+DQogICAgICAgIDxpZCB2YWx1ZT0iMjA1OTdlMGUtY2IyYS00NWIzLTk1ZjAtZGMzZGJkYjYxN2MzIiAvPg0KICAgICAgICA8bWV0YT4NCiAgICAgICAgICA8cHJvZmlsZSB2YWx1ZT0iaHR0cHM6Ly9maGlyLmtidi5kZS9TdHJ1Y3R1cmVEZWZpbml0aW9uL0tCVl9QUl9GT1JfUHJhY3RpdGlvbmVyfDEuMC4zIiAvPg0KICAgICAgICA8L21ldGE+DQogICAgICAgIDxpZGVudGlmaWVyPg0KICAgICAgICAgIDx0eXBlPg0KICAgICAgICAgICAgPGNvZGluZz4NCiAgICAgICAgICAgICAgPHN5c3RlbSB2YWx1ZT0iaHR0cDovL3Rlcm1pbm9sb2d5LmhsNy5vcmcvQ29kZVN5c3RlbS92Mi0wMjAzIiAvPg0KICAgICAgICAgICAgICA8Y29kZSB2YWx1ZT0iTEFOUiIgLz4NCiAgICAgICAgICAgIDwvY29kaW5nPg0KICAgICAgICAgIDwvdHlwZT4NCiAgICAgICAgICA8c3lzdGVtIHZhbHVlPSJodHRwczovL2ZoaXIua2J2LmRlL05hbWluZ1N5c3RlbS9LQlZfTlNfQmFzZV9BTlIiIC8+DQogICAgICAgICAgPHZhbHVlIHZhbHVlPSI4MzgzODIyMDIiIC8+DQogICAgICAgIDwvaWRlbnRpZmllcj4NCiAgICAgICAgPG5hbWU+DQogICAgICAgICAgPHVzZSB2YWx1ZT0ib2ZmaWNpYWwiIC8+DQogICAgICAgICAgPGZhbWlseSB2YWx1ZT0iVG9wcC1HbMO8Y2tsaWNoIj4NCiAgICAgICAgICAgIDxleHRlbnNpb24gdXJsPSJodHRwOi8vaGw3Lm9yZy9maGlyL1N0cnVjdHVyZURlZmluaXRpb24vaHVtYW5uYW1lLW93bi1uYW1lIj4NCiAgICAgICAgICAgICAgPHZhbHVlU3RyaW5nIHZhbHVlPSJUb3BwLUdsw7xja2xpY2giIC8+DQogICAgICAgICAgICA8L2V4dGVuc2lvbj4NCiAgICAgICAgICA8L2ZhbWlseT4NCiAgICAgICAgICA8Z2l2ZW4gdmFsdWU9IkhhbnMiIC8+DQogICAgICAgICAgPHByZWZpeCB2YWx1ZT0iRHIuIG1lZC4iPg0KICAgICAgICAgICAgPGV4dGVuc2lvbiB1cmw9Imh0dHA6Ly9obDcub3JnL2ZoaXIvU3RydWN0dXJlRGVmaW5pdGlvbi9pc28yMTA5MC1FTi1xdWFsaWZpZXIiPg0KICAgICAgICAgICAgICA8dmFsdWVDb2RlIHZhbHVlPSJBQyIgLz4NCiAgICAgICAgICAgIDwvZXh0ZW5zaW9uPg0KICAgICAgICAgIDwvcHJlZml4Pg0KICAgICAgICA8L25hbWU+DQogICAgICAgIDxxdWFsaWZpY2F0aW9uPg0KICAgICAgICAgIDxjb2RlPg0KICAgICAgICAgICAgPGNvZGluZz4NCiAgICAgICAgICAgICAgPHN5c3RlbSB2YWx1ZT0iaHR0cHM6Ly9maGlyLmtidi5kZS9Db2RlU3lzdGVtL0tCVl9DU19GT1JfUXVhbGlmaWNhdGlvbl9UeXBlIiAvPg0KICAgICAgICAgICAgICA8Y29kZSB2YWx1ZT0iMDAiIC8+DQogICAgICAgICAgICA8L2NvZGluZz4NCiAgICAgICAgICA8L2NvZGU+DQogICAgICAgIDwvcXVhbGlmaWNhdGlvbj4NCiAgICAgICAgPHF1YWxpZmljYXRpb24+DQogICAgICAgICAgPGNvZGU+DQogICAgICAgICAgICA8dGV4dCB2YWx1ZT0iSGF1c2FyenQiIC8+DQogICAgICAgICAgPC9jb2RlPg0KICAgICAgICA8L3F1YWxpZmljYXRpb24+DQogICAgICA8L1ByYWN0aXRpb25lcj4NCiAgICA8L3Jlc291cmNlPg0KICA8L2VudHJ5Pg0KICA8ZW50cnk+DQogICAgPGZ1bGxVcmwgdmFsdWU9Imh0dHA6Ly9wdnMucHJheGlzLXRvcHAtZ2x1ZWNrbGljaC5sb2NhbC9maGlyL1ByYWN0aXRpb25lci9kODQ2M2RhZi0yNThlLTRjYWQtYTg2YS02ZmQ0MmZhYzE2MWMiIC8+DQogICAgPHJlc291cmNlPg0KICAgICAgPFByYWN0aXRpb25lciB4bWxucz0iaHR0cDovL2hsNy5vcmcvZmhpciI+DQogICAgICAgIDxpZCB2YWx1ZT0iZDg0NjNkYWYtMjU4ZS00Y2FkLWE4NmEtNmZkNDJmYWMxNjFjIiAvPg0KICAgICAgICA8bWV0YT4NCiAgICAgICAgICA8cHJvZmlsZSB2YWx1ZT0iaHR0cHM6Ly9maGlyLmtidi5kZS9TdHJ1Y3R1cmVEZWZpbml0aW9uL0tCVl9QUl9GT1JfUHJhY3RpdGlvbmVyfDEuMC4zIiAvPg0KICAgICAgICA8L21ldGE+DQogICAgICAgIDxpZGVudGlmaWVyPg0KICAgICAgICAgIDx0eXBlPg0KICAgICAgICAgICAgPGNvZGluZz4NCiAgICAgICAgICAgICAgPHN5c3RlbSB2YWx1ZT0iaHR0cDovL3Rlcm1pbm9sb2d5LmhsNy5vcmcvQ29kZVN5c3RlbS92Mi0wMjAzIiAvPg0KICAgICAgICAgICAgICA8Y29kZSB2YWx1ZT0iTEFOUiIgLz4NCiAgICAgICAgICAgIDwvY29kaW5nPg0KICAgICAgICAgIDwvdHlwZT4NCiAgICAgICAgICA8c3lzdGVtIHZhbHVlPSJodHRwczovL2ZoaXIua2J2LmRlL05hbWluZ1N5c3RlbS9LQlZfTlNfQmFzZV9BTlIiIC8+DQogICAgICAgICAgPHZhbHVlIHZhbHVlPSI4MzgzODIyMTAiIC8+DQogICAgICAgIDwvaWRlbnRpZmllcj4NCiAgICAgICAgPG5hbWU+DQogICAgICAgICAgPHVzZSB2YWx1ZT0ib2ZmaWNpYWwiIC8+DQogICAgICAgICAgPGZhbWlseSB2YWx1ZT0iTWVpZXIiPg0KICAgICAgICAgICAgPGV4dGVuc2lvbiB1cmw9Imh0dHA6Ly9obDcub3JnL2ZoaXIvU3RydWN0dXJlRGVmaW5pdGlvbi9odW1hbm5hbWUtb3duLW5hbWUiPg0KICAgICAgICAgICAgICA8dmFsdWVTdHJpbmcgdmFsdWU9Ik1laWVyIiAvPg0KICAgICAgICAgICAgPC9leHRlbnNpb24+DQogICAgICAgICAgPC9mYW1pbHk+DQogICAgICAgICAgPGdpdmVuIHZhbHVlPSJKw7ZyZ2VuIiAvPg0KICAgICAgICA8L25hbWU+DQogICAgICAgIDxxdWFsaWZpY2F0aW9uPg0KICAgICAgICAgIDxjb2RlPg0KICAgICAgICAgICAgPGNvZGluZz4NCiAgICAgICAgICAgICAgPHN5c3RlbSB2YWx1ZT0iaHR0cHM6Ly9maGlyLmtidi5kZS9Db2RlU3lzdGVtL0tCVl9DU19GT1JfUXVhbGlmaWNhdGlvbl9UeXBlIiAvPg0KICAgICAgICAgICAgICA8Y29kZSB2YWx1ZT0iMDMiIC8+DQogICAgICAgICAgICA8L2NvZGluZz4NCiAgICAgICAgICA8L2NvZGU+DQogICAgICAgIDwvcXVhbGlmaWNhdGlvbj4NCiAgICAgICAgPHF1YWxpZmljYXRpb24+DQogICAgICAgICAgPGNvZGU+DQogICAgICAgICAgICA8dGV4dCB2YWx1ZT0iQXJ6dCBpbiBXZWl0ZXJiaWxkdW5nIiAvPg0KICAgICAgICAgIDwvY29kZT4NCiAgICAgICAgPC9xdWFsaWZpY2F0aW9uPg0KICAgICAgPC9QcmFjdGl0aW9uZXI+DQogICAgPC9yZXNvdXJjZT4NCiAgPC9lbnRyeT4NCiAgPGVudHJ5Pg0KICAgIDxmdWxsVXJsIHZhbHVlPSJodHRwOi8vcHZzLnByYXhpcy10b3BwLWdsdWVja2xpY2gubG9jYWwvZmhpci9Pcmdhbml6YXRpb24vY2YwNDJlNDQtMDg2YS00ZDUxLTljNzctMTcyZjlhOTcyZTNiIiAvPg0KICAgIDxyZXNvdXJjZT4NCiAgICAgIDxPcmdhbml6YXRpb24geG1sbnM9Imh0dHA6Ly9obDcub3JnL2ZoaXIiPg0KICAgICAgICA8aWQgdmFsdWU9ImNmMDQyZTQ0LTA4NmEtNGQ1MS05Yzc3LTE3MmY5YTk3MmUzYiIgLz4NCiAgICAgICAgPG1ldGE+DQogICAgICAgICAgPHByb2ZpbGUgdmFsdWU9Imh0dHBzOi8vZmhpci5rYnYuZGUvU3RydWN0dXJlRGVmaW5pdGlvbi9LQlZfUFJfRk9SX09yZ2FuaXphdGlvbnwxLjAuMyIgLz4NCiAgICAgICAgPC9tZXRhPg0KICAgICAgICA8aWRlbnRpZmllcj4NCiAgICAgICAgICA8dHlwZT4NCiAgICAgICAgICAgIDxjb2Rpbmc+DQogICAgICAgICAgICAgIDxzeXN0ZW0gdmFsdWU9Imh0dHA6Ly90ZXJtaW5vbG9neS5obDcub3JnL0NvZGVTeXN0ZW0vdjItMDIwMyIgLz4NCiAgICAgICAgICAgICAgPGNvZGUgdmFsdWU9IkJTTlIiIC8+DQogICAgICAgICAgICA8L2NvZGluZz4NCiAgICAgICAgICA8L3R5cGU+DQogICAgICAgICAgPHN5c3RlbSB2YWx1ZT0iaHR0cHM6Ly9maGlyLmtidi5kZS9OYW1pbmdTeXN0ZW0vS0JWX05TX0Jhc2VfQlNOUiIgLz4NCiAgICAgICAgICA8dmFsdWUgdmFsdWU9IjAzMTIzNDU2NyIgLz4NCiAgICAgICAgPC9pZGVudGlmaWVyPg0KICAgICAgICA8bmFtZSB2YWx1ZT0iSGF1c2FyenRwcmF4aXMgRHIuIFRvcHAtR2zDvGNrbGljaCIgLz4NCiAgICAgICAgPHRlbGVjb20+DQogICAgICAgICAgPHN5c3RlbSB2YWx1ZT0icGhvbmUiIC8+DQogICAgICAgICAgPHZhbHVlIHZhbHVlPSIwMzAxMjM0NTY3IiAvPg0KICAgICAgICA8L3RlbGVjb20+DQogICAgICAgIDxhZGRyZXNzPg0KICAgICAgICAgIDx0eXBlIHZhbHVlPSJib3RoIiAvPg0KICAgICAgICAgIDxsaW5lIHZhbHVlPSJNdXN0ZXJzdHIuIDIiPg0KICAgICAgICAgICAgPGV4dGVuc2lvbiB1cmw9Imh0dHA6Ly9obDcub3JnL2ZoaXIvU3RydWN0dXJlRGVmaW5pdGlvbi9pc28yMTA5MC1BRFhQLWhvdXNlTnVtYmVyIj4NCiAgICAgICAgICAgICAgPHZhbHVlU3RyaW5nIHZhbHVlPSIyIiAvPg0KICAgICAgICAgICAgPC9leHRlbnNpb24+DQogICAgICAgICAgICA8ZXh0ZW5zaW9uIHVybD0iaHR0cDovL2hsNy5vcmcvZmhpci9TdHJ1Y3R1cmVEZWZpbml0aW9uL2lzbzIxMDkwLUFEWFAtc3RyZWV0TmFtZSI+DQogICAgICAgICAgICAgIDx2YWx1ZVN0cmluZyB2YWx1ZT0iTXVzdGVyc3RyLiIgLz4NCiAgICAgICAgICAgIDwvZXh0ZW5zaW9uPg0KICAgICAgICAgIDwvbGluZT4NCiAgICAgICAgICA8Y2l0eSB2YWx1ZT0iQmVybGluIiAvPg0KICAgICAgICAgIDxwb3N0YWxDb2RlIHZhbHVlPSIxMDYyMyIgLz4NCiAgICAgICAgPC9hZGRyZXNzPg0KICAgICAgPC9Pcmdhbml6YXRpb24+DQogICAgPC9yZXNvdXJjZT4NCiAgPC9lbnRyeT4NCiAgPGVudHJ5Pg0KICAgIDxmdWxsVXJsIHZhbHVlPSJodHRwOi8vcHZzLnByYXhpcy10b3BwLWdsdWVja2xpY2gubG9jYWwvZmhpci9Db3ZlcmFnZS8xYjFmZmI2ZS1lYjA1LTQzZDctODdlYi1lNzgxOGZlOTY2MWEiIC8+DQogICAgPHJlc291cmNlPg0KICAgICAgPENvdmVyYWdlIHhtbG5zPSJodHRwOi8vaGw3Lm9yZy9maGlyIj4NCiAgICAgICAgPGlkIHZhbHVlPSIxYjFmZmI2ZS1lYjA1LTQzZDctODdlYi1lNzgxOGZlOTY2MWEiIC8+DQogICAgICAgIDxtZXRhPg0KICAgICAgICAgIDxwcm9maWxlIHZhbHVlPSJodHRwczovL2ZoaXIua2J2LmRlL1N0cnVjdHVyZURlZmluaXRpb24vS0JWX1BSX0ZPUl9Db3ZlcmFnZXwxLjAuMyIgLz4NCiAgICAgICAgPC9tZXRhPg0KICAgICAgICA8ZXh0ZW5zaW9uIHVybD0iaHR0cDovL2ZoaXIuZGUvU3RydWN0dXJlRGVmaW5pdGlvbi9na3YvYmVzb25kZXJlLXBlcnNvbmVuZ3J1cHBlIj4NCiAgICAgICAgICA8dmFsdWVDb2Rpbmc+DQogICAgICAgICAgICA8c3lzdGVtIHZhbHVlPSJodHRwczovL2ZoaXIua2J2LmRlL0NvZGVTeXN0ZW0vS0JWX0NTX1NGSElSX0tCVl9QRVJTT05FTkdSVVBQRSIgLz4NCiAgICAgICAgICAgIDxjb2RlIHZhbHVlPSIwMCIgLz4NCiAgICAgICAgICA8L3ZhbHVlQ29kaW5nPg0KICAgICAgICA8L2V4dGVuc2lvbj4NCiAgICAgICAgPGV4dGVuc2lvbiB1cmw9Imh0dHA6Ly9maGlyLmRlL1N0cnVjdHVyZURlZmluaXRpb24vZ2t2L2RtcC1rZW5uemVpY2hlbiI+DQogICAgICAgICAgPHZhbHVlQ29kaW5nPg0KICAgICAgICAgICAgPHN5c3RlbSB2YWx1ZT0iaHR0cHM6Ly9maGlyLmtidi5kZS9Db2RlU3lzdGVtL0tCVl9DU19TRkhJUl9LQlZfRE1QIiAvPg0KICAgICAgICAgICAgPGNvZGUgdmFsdWU9IjAwIiAvPg0KICAgICAgICAgIDwvdmFsdWVDb2Rpbmc+DQogICAgICAgIDwvZXh0ZW5zaW9uPg0KICAgICAgICA8ZXh0ZW5zaW9uIHVybD0iaHR0cDovL2ZoaXIuZGUvU3RydWN0dXJlRGVmaW5pdGlvbi9na3Yvd29wIj4NCiAgICAgICAgICA8dmFsdWVDb2Rpbmc+DQogICAgICAgICAgICA8c3lzdGVtIHZhbHVlPSJodHRwczovL2ZoaXIua2J2LmRlL0NvZGVTeXN0ZW0vS0JWX0NTX1NGSElSX0lUQV9XT1AiIC8+DQogICAgICAgICAgICA8Y29kZSB2YWx1ZT0iMDMiIC8+DQogICAgICAgICAgPC92YWx1ZUNvZGluZz4NCiAgICAgICAgPC9leHRlbnNpb24+DQogICAgICAgIDxleHRlbnNpb24gdXJsPSJodHRwOi8vZmhpci5kZS9TdHJ1Y3R1cmVEZWZpbml0aW9uL2drdi92ZXJzaWNoZXJ0ZW5hcnQiPg0KICAgICAgICAgIDx2YWx1ZUNvZGluZz4NCiAgICAgICAgICAgIDxzeXN0ZW0gdmFsdWU9Imh0dHBzOi8vZmhpci5rYnYuZGUvQ29kZVN5c3RlbS9LQlZfQ1NfU0ZISVJfS0JWX1ZFUlNJQ0hFUlRFTlNUQVRVUyIgLz4NCiAgICAgICAgICAgIDxjb2RlIHZhbHVlPSIxIiAvPg0KICAgICAgICAgIDwvdmFsdWVDb2Rpbmc+DQogICAgICAgIDwvZXh0ZW5zaW9uPg0KICAgICAgICA8c3RhdHVzIHZhbHVlPSJhY3RpdmUiIC8+DQogICAgICAgIDx0eXBlPg0KICAgICAgICAgIDxjb2Rpbmc+DQogICAgICAgICAgICA8c3lzdGVtIHZhbHVlPSJodHRwOi8vZmhpci5kZS9Db2RlU3lzdGVtL3ZlcnNpY2hlcnVuZ3NhcnQtZGUtYmFzaXMiIC8+DQogICAgICAgICAgICA8Y29kZSB2YWx1ZT0iR0tWIiAvPg0KICAgICAgICAgIDwvY29kaW5nPg0KICAgICAgICA8L3R5cGU+DQogICAgICAgIDxiZW5lZmljaWFyeT4NCiAgICAgICAgICA8cmVmZXJlbmNlIHZhbHVlPSJQYXRpZW50Lzk3NzRmNjdmLWEyMzgtNGRhZi1iNGU2LTY3OWRlZWVmMzgxMSIgLz4NCiAgICAgICAgPC9iZW5lZmljaWFyeT4NCiAgICAgICAgPHBheW9yPg0KICAgICAgICAgIDxpZGVudGlmaWVyPg0KICAgICAgICAgICAgPHN5c3RlbSB2YWx1ZT0iaHR0cDovL2ZoaXIuZGUvTmFtaW5nU3lzdGVtL2FyZ2UtaWsvaWtuciIgLz4NCiAgICAgICAgICAgIDx2YWx1ZSB2YWx1ZT0iMTA0MjEyMDU5IiAvPg0KICAgICAgICAgIDwvaWRlbnRpZmllcj4NCiAgICAgICAgICA8ZGlzcGxheSB2YWx1ZT0iQU9LIFJoZWlubGFuZC9IYW1idXJnIiAvPg0KICAgICAgICA8L3BheW9yPg0KICAgICAgPC9Db3ZlcmFnZT4NCiAgICA8L3Jlc291cmNlPg0KICA8L2VudHJ5Pg0KPC9CdW5kbGU+oIIEwTCCBL0wggOloAMCAQICBwJBwffTq9gwDQYJKoZIhvcNAQELBQAwUDELMAkGA1UEBhMCREUxHzAdBgNVBAoMFmdlbWF0aWsgR21iSCBOT1QtVkFMSUQxIDAeBgNVBAMMF0dFTS5IQkEtcUNBMjQgVEVTVC1PTkxZMB4XDTE4MTEwNTAwMDAwMFoXDTIzMTEwNDIzNTk1OVoweDEfMB0GA1UEAwwWU2FtIFNjaHJhw59lclRFU1QtT05MWTEVMBMGA1UEKgwMU2FtIEZyZWloZXJyMRIwEAYDVQQEDAlTY2hyYcOfZXIxHTAbBgNVBAUTFDgwMjc2ODgzMTEwMDAwMDk1NzY3MQswCQYDVQQGEwJERTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAIjHtUOCYpiywQU20DMmvw9K4HmynW5l9ZkBJtFqPAJ0q8MqAcp4blNoRSng2wc7YZGWVsGMRaGqz9y7hDf1OojNl+R57MNfzanWoyjCyyk3KdugWoIUFxFQ0stSDbD0JTSzip7mMEkQH7GeUg3deIkPksihvOpJMizQnYdDds8coLZ7mbcGueUBS7udVGde+vwyK5o2d/q5TljUINSareFr0OHq9ySgKQavZHy7VpTxPe7MAhvq+xpapZDvJODJ9YQiSj6xMqEPTWD7pa1SA4iH+TYZJxX9H4YuwLhGut8mVqCyUo06DsfAi+GFh4l49SunT2whBWxVZtJW625il+MCAwEAAaOCAXIwggFuMB0GA1UdDgQWBBS+1xJ1Qaz1Rp96GAR2QEa3mH4TWjAMBgNVHRMBAf8EAjAAMBsGCSsGAQQBwG0DBQQOMAwGCisGAQQBwG0DBQEwIgYIKwYBBQUHAQMEFjAUMAgGBgQAjkYBATAIBgYEAI5GAQQwHwYDVR0jBBgwFoAUZ5wxtunAN+odG4HnpPU7zB4XATkwOQYDVR0gBDIwMDAJBgcqghQATARIMAkGBwQAi+xAAQIwCgYIKoIUAEwEgREwDAYKKwYBBAGCzTMBATAOBgNVHQ8BAf8EBAMCBkAwOAYIKwYBBQUHAQEELDAqMCgGCCsGAQUFBzABhhxodHRwOi8vZWhjYS5nZW1hdGlrLmRlL29jc3AvMFgGBSskCAMDBE8wTaQoMCYxCzAJBgNVBAYTAkRFMRcwFQYDVQQKDA5nZW1hdGlrIEJlcmxpbjAhMB8wHTAbMA4MDMOEcnp0aW4vQXJ6dDAJBgcqghQATAQeMA0GCSqGSIb3DQEBCwUAA4IBAQCLCszqmpE/Ttc6COfBisJoF9E4ouI7lKjeq57NY4x0Bjs1hoA0FhmrSInQrD72b1Ci890Ls0Ro4klSOOu9aIYQ/WL3asVOVnudWbmH9JrlhOVgD7gfNDHOa3FcsLdwtvPqWq/VVbzgMBTKlR8vD35sl8rQ3Rdx0l8zWbW6SpmaW2ERDNvG94CG9MZDa1M2s9sOe0377R/n3Ic4/Kz8PNNdoLjzkS1KdoVJfDDOGA0f9960qIBAhjbEkWYE2ItJvXCylhKG+KSxAEhf0fj1E5SzqXxMBqWMi5wEktdcHDR3hhBm1ILIlpdxRrbPd9zC0vrAtBylZ0mlMtqgB1UfryvooYIGp6GCBqMGCCsGAQUFBxACMIIGlQoBAKCCBo4wggaKBgkrBgEFBQcwAQEEggZ7MIIGdzCCAWehVjBUMQswCQYDVQQGEwJERTEaMBgGA1UECgwRZ2VtYXRpayBOT1QtVkFMSUQxKTAnBgNVBAMMIGVoY2EgUUVTIE9DU1AgU2lnbmVyIDIgVEVTVC1PTkxZGA8yMDIxMDQxNDE3MTQwMlowgbYwgbMwQDAJBgUrDgMCGgUABBRNFks3lLP4Wm+YY1OyKvXiyNCMcwQUZ5wxtunAN+odG4HnpPU7zB4XATkCBwJBwffTq9iAABgPMjAyMTA0MTQxNzE0MDJaoVwwWjAaBgUrJAgDDAQRGA8yMDE4MTEwNTE1MzQzOVowPAYFKyQIAw0EMzAxMA0GCWCGSAFlAwQCAQUABCDkeQLIwLc5SjI5vgJ9kfKCmV/gALbvRKmia1upSi+2UqFDMEEwHgYJKwYBBQUHMAEGBBEYDzE4NzAwMTA3MDAwMDAwWjAfBgkrBgEFBQcwAQIEEgQQ2XVqYP2hI96vt8NjBfGc8jANBgkqhkiG9w0BAQsFAAOCAQEAlxNOGxRtOJls+3xR1JiGdE6yWzjbYEQjfgZ0hOnNcXp6xcvH9JAuZMs6WxBLm4hheIUrmjWMTGe5WZYk4tS/aL1lwlQYOUx/Ltya2XR3Rwjl+2hQ1+N2jHuiEQQ/2uFIsrsNHCt4tm27X/8b9bKaUObSu05aVtYolrjdU6iyZ7FoKPNKpgS2/h6rn0d/Y7uootbhh39AwogD47pDmmMUEaiNv5ArbyvsJFmkuXqDwTJSno5hV2L0owqk1wcLdIridw1LERL6GlS4SWR8GNhRqvRyaVbSM3wpVyon09eHSWG5ZDiM5Wxg+cvY3bUV5+hHcmokebkpD8+RkUiULUyeQaCCA/QwggPwMIID7DCCAtSgAwIBAgIGAdMX4hoWMA0GCSqGSIb3DQEBCwUAMFAxCzAJBgNVBAYTAkRFMR8wHQYDVQQKDBZnZW1hdGlrIEdtYkggTk9ULVZBTElEMSAwHgYDVQQDDBdHRU0uSEJBLXFDQTI0IFRFU1QtT05MWTAeFw0xOTA0MDEwMDAwMDBaFw0yNDA0MDEyMzU5NTlaMFQxCzAJBgNVBAYTAkRFMRowGAYDVQQKDBFnZW1hdGlrIE5PVC1WQUxJRDEpMCcGA1UEAwwgZWhjYSBRRVMgT0NTUCBTaWduZXIgMiBURVNULU9OTFkwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCf1I879/ieGtBfisHaaHyjPaHpgJzXDiLUdasX30xY2JKpr27y0ebriSwSQTPTOwJzXiVefcIZMzvT6/8//OyoDhMn4yBFAIsxMTyxHqMWFEqvvcAcRjB5CQsEcb/nZbjKrYQiCRL8VzsKOhHHzyYK0g84bG44QQ314eOvlbZihKjubDCYCMZ/T6Ta+V8EHMm58F3sR9CXNKKwwr5oOkwZsB047xx0LIg+Gir/golSvpfuq3bmLL0bKRlr8diFUzdkxkD+NIx5pB3o2dKFx/vkI3ArmnUQIZHgjTQn7+vPqMjVJhOFKmJyxb9z2Oqo7E5mUfg5st5G4l8LuwDwoaw7AgMBAAGjgccwgcQwOAYIKwYBBQUHAQEELDAqMCgGCCsGAQUFBzABhhxodHRwOi8vZWhjYS5nZW1hdGlrLmRlL29jc3AvMB0GA1UdDgQWBBT2g0uaT5zD2tBJQHdvfUJYAxRUNjAMBgNVHRMBAf8EAjAAMB8GA1UdIwQYMBaAFGecMbbpwDfqHRuB56T1O8weFwE5MBUGA1UdIAQOMAwwCgYIKoIUAEwEgSMwDgYDVR0PAQH/BAQDAgZAMBMGA1UdJQQMMAoGCCsGAQUFBwMJMA0GCSqGSIb3DQEBCwUAA4IBAQAdTJ/2ljlYtZyRhlHJhj0BrH6Misav0dHHSeBXknV61KJeFbzyDMFNFMidNmnIAVHMKyI8SVZ3RPgZXBa//RvSp0VN5hyl9cpIvfZlLANQ41U460G+n06vJIxX6hpPdQIJkkrZbXpQN13l/hC17X9+c8hg7GKz8oYOsCN8l/Za3vsJpuBFPdwSxySAUiBBH1ei0V4/GNjaAKqBv7XEmZX4Q7sGaDKTEsWykhUlaeINh8PLn3iwGjAqBD22pRSWVPyjooSPwVXPKfIvXZiUSJvNlZkNPaBjXGMpe3ysBw+LxhjnwBHfnokot9dtmKEeorm8eGDjigKPmJXKBmsS/GXwMYIDWzCCA1cCAQEwWzBQMQswCQYDVQQGEwJERTEfMB0GA1UECgwWZ2VtYXRpayBHbWJIIE5PVC1WQUxJRDEgMB4GA1UEAwwXR0VNLkhCQS1xQ0EyNCBURVNULU9OTFkCBwJBwffTq9gwDQYJYIZIAWUDBAIBBQCgggGdMBgGCSqGSIb3DQEJAzELBgkqhkiG9w0BBwEwHAYJKoZIhvcNAQkFMQ8XDTIxMDQxNDE3MTQwMlowLwYJKoZIhvcNAQkEMSIEIJCoxqWWQ1bTJz37ceR9fk30HprTOO9eOn4oF/dz4O/gMDAGCyqGSIb3DQEJEAIEMSEwHwwSYSBDTVNEb2N1bWVudDJzaWduBgkqhkiG9w0BBwEwYQYJKoZIhvcNAQk0MVQwUjANBglghkgBZQMEAgEFAKFBBgkqhkiG9w0BAQowNKAPMA0GCWCGSAFlAwQCAQUAoRwwGgYJKoZIhvcNAQEIMA0GCWCGSAFlAwQCAQUAogMCASAwgZwGCyqGSIb3DQEJEAIvMYGMMIGJMIGGMIGDBCDkeQLIwLc5SjI5vgJ9kfKCmV/gALbvRKmia1upSi+2UjBfMFSkUjBQMQswCQYDVQQGEwJERTEfMB0GA1UECgwWZ2VtYXRpayBHbWJIIE5PVC1WQUxJRDEgMB4GA1UEAwwXR0VNLkhCQS1xQ0EyNCBURVNULU9OTFkCBwJBwffTq9gwQQYJKoZIhvcNAQEKMDSgDzANBglghkgBZQMEAgEFAKEcMBoGCSqGSIb3DQEBCDANBglghkgBZQMEAgEFAKIDAgEgBIIBAIDFQYTLnopCA3AVb1s4OaK4EeISBWvN4LEsa/tJ9UlzovJBfT0hghPSttqOZ0eEAPbPb0OiNorZNTFZnZUUmkOKc4IW4fn0tEfLYaXvkm/9UntdsSHTX2ML2o/+61Y1yXQjnYzGeHsDaBlcf7ErVL0hzQUDYyjzi6AIIuZigYcX0n4GAZo+FQYs/gbKfVVUBmmCZv0SjQw4cn5j57MgGgNoKOLYLxPj26N+BYrRPS+DD/TczAitWlyqCJ1xXkbll1NNaBfbaJkTEoHmygYkGrNoSOOd6jaxrqhXLRU9FA2BFRcul1CCSvynTHffdMlueuYtcOTOxzVnZDKScrLXQfo=</ns5:Base64Signature>
                    </ns5:SignatureObject>
                </ns8:SignResponse>
            </ns8:SignDocumentResponse>
        </SOAP-ENV:Body>
    </SOAP-ENV:Envelope>

Das Ergebnis der erfolgreichen qualifizierten Signatur wird
Base64-codiert in `<ns5:SignatureObject>` zurückgegeben. Darin enthalten
ist eine PKCS#7-Datei in HEX-Codierung, die mit einem ASN1-Decoder
angesehen werden kann.

Der Inhalt der base64-codierten Signatur findet sich im Unterordner der
[Beispiele](../samples/qes/signed) in der Datei
`4fe2013d-ae94-441a-a1b1-78236ae65680_S_SECUN_secu_kon_4.8.2_4.1.3.p7`
und kann mit einem ASN.1-Viewer eingesehen werden.

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

# E-Rezept vervollständigen und Task aktivieren

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
