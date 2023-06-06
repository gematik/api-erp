Hier dokumentiert die gematik die Nutzung der Schnittstellen rund um das
E-Rezept aus Sicht des abgebenden Leistungserbringers.

# Anwendungsfall E-Rezept beliefern

Mit diesem UseCase beliefert ein Apotheker ein E-Rezept, das auf dem
E-Rezept-Fachdienst bereitliegt. Eine Unterscheidung zwischen einer
Filial- oder Versandapotheke ist dabei zweitrangig, da der Unterschied
im Ablauf lediglich in der Übermittlung der `Task-ID` und des
`AccessCodes` durch den Versicherten besteht. Mit der Bekanntmachung der
`Task-ID` und des `AccessCodes` durch den Versicherten mittels
Präsentation eines 2D-Barcodes oder via Kommunikationsnachricht liegen
im Apothekenverwaltungssystem (AVS) alle notwendigen Parameter für den
Abruf des Rezepts vor.  
Ist der Task inkl. des E-Rezept-Datensatzes heruntergeladen, prüft das
AVS die Signatur des E-Rezept-Datensatzes mit Hilfe des Konnektors. Ist
das E-Rezept gültig signiert und das E-Rezept beliefert, erfolgt der
Abschluss der Transaktion mit dem Bereitstellen der
Dispensierinformationen für den Versicherten. Der E-Rezept-Fachdienst
erzeugt daraufhin eine Signatur als Quittung für den Apotheker und den
Versicherten und beendet den Workflow.

![width=100%](../images/api_rezept_abrufen.png)

Im Ablaufdiagramm sind zusätzliche Arbeitsschritte des
Apothekenpersonals wie Securpharm-Scan und Zuzahlung des Patienten nicht
berücksichtigt.

# Profilierung

Für diesen Anwendungsfall werden die FHIR-Resourcen "Task":
<http://hl7.org/fhir/task.html> und MedicationDispense
<https://www.hl7.org/fhir/medicationdispense.html> profiliert. Die
Profile können als JSON oder XML hier eingesehen werden:
<https://simplifier.net/erezept-workflow/gem_erp_pr_task> bzw.
<https://simplifier.net/erezept-workflow/gem_erp_pr_medicationdispense>

Die für diese Anwendung wichtigen Attribute und Besonderheiten durch die
Profilierung der Ressourcen werden in der folgenden Tabelle kurz
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
<td colspan="2"
style="text-align: left;"><p><strong>Task</strong></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>identifier:PrescriptionID</p></td>
<td style="text-align: left;"><p>Rezept-ID; eindeutig für jedes
Rezept</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>identifier:AccessCode</p></td>
<td style="text-align: left;"><p>vom E-Rezept-Fachdienst generierter
Berechtigungs-Code</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>identifier:Secret</p></td>
<td style="text-align: left;"><p>vom E-Rezept-Fachdienst generierter
Berechtigungs-Code</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>status</p></td>
<td style="text-align: left;"><p>Status des E-Rezepts</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>intent</p></td>
<td style="text-align: left;"><p>Intension des Tasks. Fixer
Wert="order"</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>for</p></td>
<td style="text-align: left;"><p>Krankenversichertennummer</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>authoredOn</p></td>
<td style="text-align: left;"><p>Erstellungszeitpunkt des Tasks</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>lastModified</p></td>
<td style="text-align: left;"><p>letzte Änderung am Task</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>performerType</p></td>
<td style="text-align: left;"><p>Institution, in der das Rezept
eingelöst werden soll</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>input</p></td>
<td style="text-align: left;"><p>Verweis auf die für den Patienten und
den Leistungserbringer gedachten Bundle</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>output</p></td>
<td style="text-align: left;"><p>Verweis auf das
Quittungs-Bundle</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>extension:flowType</p></td>
<td style="text-align: left;"><p>gibt den Typ des Rezeptes an</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>extension:expiryDate</p></td>
<td style="text-align: left;"><p>Verfallsdatum</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>extension:acceptDate</p></td>
<td style="text-align: left;"><p>Datum bis zu welchem die Krankenkasse
spätestens die Kosten übernimmt</p></td>
</tr>
<tr class="odd">
<td colspan="2"
style="text-align: left;"><p><strong>MedicationDispense</strong></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>identifier:PrescriptionID</p></td>
<td style="text-align: left;"><p>Rezept-ID; eindeutig für jedes
Rezept</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>status</p></td>
<td style="text-align: left;"><p>Status des E-Rezepts</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>medication</p></td>
<td style="text-align: left;"><p>das dem Versicherten ausgehändigte
Medikament</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>subject:identifier</p></td>
<td style="text-align: left;"><p>Krankenversichertennummer</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>performer</p></td>
<td style="text-align: left;"><p>Telematik-ID der Apotheke, die das
E-Rezept beliefert hat</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>whenHandedOver</p></td>
<td style="text-align: left;"><p>Datum der Übergabe bzw. Herausgabe an
den Versicherten</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>dosageInstruction</p></td>
<td style="text-align: left;"><p>Dosierungsinformationen des
Medikaments, falls abweichend von der ärztlichen Verordnung</p></td>
</tr>
<tr class="odd">
<td colspan="2" style="text-align: left;"><p><strong>Medication
innerhalb MedicationDispense</strong></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>code</p></td>
<td style="text-align: left;"><p>Enthält je nach Rezepttyp die PZN und
den Handelsnamen, Kennzeichnung als Wirkstoffverordnung oder eine
Rezeptur</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>form</p></td>
<td style="text-align: left;"><p>Darreichungsform (Tabletten, Kapseln,
Salbe, etc.)</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>ingredient</p></td>
<td style="text-align: left;"><p>Wirkstoff bei
Wirkstoffverordnung</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>batch</p></td>
<td style="text-align: left;"><p>Chargeninformation</p></td>
</tr>
</tbody>
</table>

In den folgenden Kapiteln wird erläutert, wann und wie die Befüllung
dieser Attribute erfolgt.

# E-Rezept abrufen

Ein Apotheker hat vom Versicherten mittels Abscannen eines 2D-Codes die
Informationen
`https://erp.zentral.erp.splitdns.ti-dienste.de/Task/160.123.456.789.123.58/$accept?ac=777bea0e13cc9c42ceec14aec3ddee2263325dc2c6c699db115f58fe423607ea`
für den Abruf eines E-Rezepts vom E-Rezept-Fachdienst erhalten.

Der Aufruf erfolgt als http-POST-Operation mit der FHIR-Operation
`$accept`. Im http-Request-Header `Authorization` muss das während der
Authentisierung erhaltene ACCESS\_TOKEN übergeben werden. Als
URL-Parameter `?ac=...` muss der beim Erzeugen des Tasks generierte
`AccessCode` für die Berechtigungsprüfung übergeben werden. Im
http-ResponseBody wird der referenzierte Task sowie das qualifiziert
signierte E-Rezept als E-Rezept-Datensatz zurückgegeben, wobei im Task
das `secret` als zusätzliches Geheimnis in einem Task.identifier
generiert wird, das in allen folgenden Zugriffen durch den Apotheker
mitgeteilt werden muss.

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
href="https://erp.zentral.erp.splitdns.ti-dienste.de/Task/160.123.456.789.123.58/$accept?ac=777bea0e13cc9c42ceec14aec3ddee2263325dc2c6c699db115f58fe423607ea">https://erp.zentral.erp.splitdns.ti-dienste.de/Task/160.123.456.789.123.58/$accept?ac=777bea0e13cc9c42ceec14aec3ddee2263325dc2c6c699db115f58fe423607ea</a></p></td>
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
<p>Im http-Header des äußeren http-Requests an die VAU (POST /VAU) sind
die Header <code>X-erp-user: l</code> und
<code>X-erp-resource: Task</code> zu setzen.</p>
</div></td>
</tr>
</tbody>
</table>

**Response**

    HTTP/1.1 200 OK
    Content-Type: application/fhir+xml;charset=utf-8

    <Bundle xmlns="http://hl7.org/fhir">
        <id value="dffbfd6a-5712-4798-bdc8-07201eb77ab8"/>
        <meta>
            <lastUpdated value="2020-03-13T07:31:34.328+00:00"/>
        </meta>
        <type value="collection"/>
        <entry>
            <fullUrl value="https://erp.zentral.erp.splitdns.ti-dienste.de/Task/160.123.456.789.123.58"/>
            <resource>
                <Task xmlns="http://hl7.org/fhir">
                    <id value="160.123.456.789.123.58"/>
                    <meta>
                        <versionId value="2"/>
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
                        <valueDate value="2020-06-02" />
                    </extension>
                    <extension url="https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_EX_AcceptDate">
                        <valueDate value="2020-04-01" />
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
                    <identifier>
                        <system value="https://gematik.de/fhir/erp/NamingSystem/GEM_ERP_NS_Secret"/>
                        <value value="c36ca26502892b371d252c99b496e31505ff449aca9bc69e231c58148f6233cf"/>
                    </identifier>
                    <status value="in-progress"/>
                    <intent value="order"/>
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
                        <valueDate value="2020-06-02" />
                    </extension>
                    <extension url="https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_EX_AcceptDate">
                        <valueDate value="2020-04-01" />
                    </extension>
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
                                <display value="Health Care Provider Prescription" />
                            </coding>
                        </type>
                        <valueReference>
                            <reference value="281a985c-f25b-4aae-91a6-41ad744080b0"/>
                        </valueReference>
                    </input>
                </Task>
            </resource>
        </entry>
        <entry>
            <resource>
                <Binary>
                    <id value="281a985c-f25b-4aae-91a6-41ad744080b0"/>
                    <meta>
                        <versionId value="1"/>
                        <source value="#AsYRxq34dvONJAiv"/>
                        <profile value="https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_PR_Binary"/>
                    </meta>
                    <contentType value="application/pkcs7-mime" />
                    <data value="MIJTfQYJKoZIhvcNAQcCoIJTbjCCU2oCAQUxDzANBglghkgBZQMEAg..." />
                </Binary>
            </resource>
        </entry>
    </Bundle>

Wenn ein E-Rezept vom Workflow-type 200/209 abgerufen wird, liefert der
E-Rezept-Fachdienst einen Consent zurück, wenn der Versicherte die
Einwilligung über die Bereitstellung der Abrechnungsinformationen im
Frontend des Versicherten erteilt hat.

HTTP/1.1 200 OK Content-Type: application/fhir+xml;charset=utf-8

    <Bundle xmlns="http://hl7.org/fhir">
        <id value="f6af166c-36f1-4e0d-9cf9-1bc5051270f6"/>
        <type value="collection"/>
        <timestamp value="2023-03-10T07:46:42.385+00:00"/>
        <link>
            <relation value="self"/>
            <url value="https://erp-dev.zentral.erp.splitdns.ti-dienste.de/Task/200.000.001.213.340.73/$accept/"/>
        </link>
        <entry>
            <fullUrl value="https://erp-dev.zentral.erp.splitdns.ti-dienste.de/Task/200.000.001.213.340.73"/>
            <resource>
                <Task xmlns="http://hl7.org/fhir">
                    <id value="200.000.001.213.340.73"/>
                    <meta>
                        <profile value="https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_PR_Task|1.2"/>
                    </meta>
                    <extension url="https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_EX_PrescriptionType">
                        <valueCoding>
                            <system value="https://gematik.de/fhir/erp/CodeSystem/GEM_ERP_CS_FlowType"/>
                            <code value="200"/>
                            <display value="PKV (Apothekenpflichtige Arzneimittel)"/>
                        </valueCoding>
                    </extension>
                    <extension url="https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_EX_ExpiryDate">
                        <valueDate value="2023-06-10"/>
                    </extension>
                    <extension url="https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_EX_AcceptDate">
                        <valueDate value="2023-06-10"/>
                    </extension>
                    <identifier>
                        <use value="official"/>
                        <system value="https://gematik.de/fhir/erp/NamingSystem/GEM_ERP_NS_PrescriptionId"/>
                        <value value="200.000.001.213.340.73"/>
                    </identifier>
                    <identifier>
                        <use value="official"/>
                        <system value="https://gematik.de/fhir/erp/NamingSystem/GEM_ERP_NS_AccessCode"/>
                        <value value="8532d3accd0b23fe7f780161c4cf8d4ddab3ce028c1ad22f61bbea5720f60dec"/>
                    </identifier>
                    <identifier>
                        <use value="official"/>
                        <system value="https://gematik.de/fhir/erp/NamingSystem/GEM_ERP_NS_Secret"/>
                        <value value="e761743e424b3199e7e432b256075a82efb0e8ca9ec2db162b29872d9e54ddc4"/>
                    </identifier>
                    <status value="in-progress"/>
                    <intent value="order"/>
                    <for>
                        <identifier>
                            <system value="http://fhir.de/sid/pkv/kvid-10"/>
                            <value value="X110465770"/>
                        </identifier>
                    </for>
                    <authoredOn value="2023-03-10T07:46:41.430+00:00"/>
                    <lastModified value="2023-03-10T07:46:42.381+00:00"/>
                    <performerType>
                        <coding>
                            <system value="https://gematik.de/fhir/erp/CodeSystem/GEM_ERP_CS_OrganizationType"/>
                            <code value="urn:oid:1.2.276.0.76.4.54"/>
                            <display value="Öffentliche Apotheke"/>
                        </coding>
                        <text value="Öffentliche Apotheke"/>
                    </performerType>
                    <input>
                        <type>
                            <coding>
                                <system value="https://gematik.de/fhir/erp/CodeSystem/GEM_ERP_CS_DocumentType"/>
                                <code value="1"/>
                            </coding>
                        </type>
                        <valueReference>
                            <reference value="c89c8312-0000-0000-0001-000000000000"/>
                        </valueReference>
                    </input>
                </Task>
            </resource>
        </entry>
        <entry>
            <fullUrl value="urn:uuid:c89c8312-0000-0000-0001-000000000000"/>
            <resource>
                <Binary xmlns="http://hl7.org/fhir">
                    <meta>
                        <versionId value="1"/>
                        <profile value="https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_PR_Binary|1.2"/>
                    </meta>
                    <contentType value="application/pkcs7-mime"/>
                    <data value="MII6bAYJKoZIhvcNAQcCoII6XTCCOlkCAQExDTALBglghkgBZQMEAgEwgis9BgkqhkiG9w0BBwGggisuBIIrKjxCdW5kbGUgeG1sbnM9Imh0dHA6Ly9obDcub3JnL2ZoaXIiPjxpZCB2YWx1ZT0iMjYwMGQzNmEtY2JkZi00NWExLThiNmYtYWQ3ZjdiNzY3OGFiIi8+PG1ldGE+PGxhc3RVcGRhdGVkIHZhbHVlPSIyMDIzLTAzLTEwVDA4OjQ2OjQwLjYxOSswMTowMCIvPjxwcm9maWxlIHZhbHVlPSJodHRwczovL2ZoaXIua2J2LmRlL1N0cnVjdHVyZURlZmluaXRpb24vS0JWX1BSX0VSUF9CdW5kbGV8MS4xLjAiLz48L21ldGE+PGlkZW50aWZpZXI+PHN5c3RlbSB2YWx1ZT0iaHR0cHM6Ly9nZW1hdGlrLmRlL2ZoaXIvZXJwL05hbWluZ1N5c3RlbS9HRU1fRVJQX05TX1ByZXNjcmlwdGlvbklkIi8+PHZhbHVlIHZhbHVlPSIyMDAuMDAwLjAwMS4yMTMuMzQwLjczIi8+PC9pZGVudGlmaWVyPjx0eXBlIHZhbHVlPSJkb2N1bWVudCIvPjx0aW1lc3RhbXAgdmFsdWU9IjIwMjMtMDMtMTBUMDg6NDY6NDAuNjE5KzAxOjAwIi8+PGVudHJ5PjxmdWxsVXJsIHZhbHVlPSJodHRwczovL3B2cy5nZW1hdGlrLmRlL2ZoaXIvQ29tcG9zaXRpb24vZWExZGMxYzgtMGU3NS00NzM3LWEwMWQtMWU2OTVjNDM2NjllIi8+PHJlc291cmNlPjxDb21wb3NpdGlvbiB4bWxucz0iaHR0cDovL2hsNy5vcmcvZmhpciI+PGlkIHZhbHVlPSJlYTFkYzFjOC0wZTc1LTQ3MzctYTAxZC0xZTY5NWM0MzY2OWUiLz48bWV0YT48cHJvZmlsZSB2YWx1ZT0iaHR0cHM6Ly9maGlyLmtidi5kZS9TdHJ1Y3R1cmVEZWZpbml0aW9uL0tCVl9QUl9FUlBfQ29tcG9zaXRpb258MS4xLjAiLz48L21ldGE+PGV4dGVuc2lvbiB1cmw9Imh0dHBzOi8vZmhpci5rYnYuZGUvU3RydWN0dXJlRGVmaW5pdGlvbi9LQlZfRVhfRk9SX1BLVl9UYXJpZmYiPjx2YWx1ZUNvZGluZz48c3lzdGVtIHZhbHVlPSJodHRwczovL2ZoaXIua2J2LmRlL0NvZGVTeXN0ZW0vS0JWX0NTX1NGSElSX0tCVl9QS1ZfVEFSSUZGIi8+PGNvZGUgdmFsdWU9IjAzIi8+PC92YWx1ZUNvZGluZz48L2V4dGVuc2lvbj48ZXh0ZW5zaW9uIHVybD0iaHR0cHM6Ly9maGlyLmtidi5kZS9TdHJ1Y3R1cmVEZWZpbml0aW9uL0tCVl9FWF9GT1JfTGVnYWxfYmFzaXMiPjx2YWx1ZUNvZGluZz48c3lzdGVtIHZhbHVlPSJodHRwczovL2ZoaXIua2J2LmRlL0NvZGVTeXN0ZW0vS0JWX0NTX1NGSElSX0tCVl9TVEFUVVNLRU5OWkVJQ0hFTiIvPjxjb2RlIHZhbHVlPSIwMCIvPjwvdmFsdWVDb2Rpbmc+PC9leHRlbnNpb24+PHN0YXR1cyB2YWx1ZT0iZmluYWwiLz48dHlwZT48Y29kaW5nPjxzeXN0ZW0gdmFsdWU9Imh0dHBzOi8vZmhpci5rYnYuZGUvQ29kZVN5c3RlbS9LQlZfQ1NfU0ZISVJfS0JWX0ZPUk1VTEFSX0FSVCIvPjxjb2RlIHZhbHVlPSJlMTZBIi8+PC9jb2Rpbmc+PC90eXBlPjxzdWJqZWN0PjxyZWZlcmVuY2UgdmFsdWU9IlBhdGllbnQvZTYyNzRjMDUtZjYzYy00ZWExLTljM2ItMzgzNDBlY2JjYTZjIi8+PC9zdWJqZWN0PjxkYXRlIHZhbHVlPSIyMDIzLTAzLTEwVDA4OjQ2OjQwKzAxOjAwIi8+PGF1dGhvcj48cmVmZXJlbmNlIHZhbHVlPSJQcmFjdGl0aW9uZXIvODllMzY3MTItOWFiMS00Y2I2LWFhN2ItMjkxMjNjZDQ5OWUzIi8+PHR5cGUgdmFsdWU9IlByYWN0aXRpb25lciIvPjwvYXV0aG9yPjxhdXRob3I+PHR5cGUgdmFsdWU9IkRldmljZSIvPjxpZGVudGlmaWVyPjxzeXN0ZW0gdmFsdWU9Imh0dHBzOi8vZmhpci5rYnYuZGUvTmFtaW5nU3lzdGVtL0tCVl9OU19GT1JfUHJ1ZWZudW1tZXIiLz48dmFsdWUgdmFsdWU9IkdFTUFUSUsvNDEwLzIxMDkvMzYvMTIzIi8+PC9pZGVudGlmaWVyPjwvYXV0aG9yPjx0aXRsZSB2YWx1ZT0iZWxla3Ryb25pc2NoZSBBcnpuZWltaXR0ZWx2ZXJvcmRudW5nIi8+PGN1c3RvZGlhbj48cmVmZXJlbmNlIHZhbHVlPSJPcmdhbml6YXRpb24vOWVkOGY3MDYtNDc0NS00ZmU0LThlOGQtOTBjZjVmODkwOWMxIi8+PC9jdXN0b2RpYW4+PHNlY3Rpb24+PGNvZGU+PGNvZGluZz48c3lzdGVtIHZhbHVlPSJodHRwczovL2ZoaXIua2J2LmRlL0NvZGVTeXN0ZW0vS0JWX0NTX0VSUF9TZWN0aW9uX1R5cGUiLz48Y29kZSB2YWx1ZT0iQ292ZXJhZ2UiLz48L2NvZGluZz48L2NvZGU+PGVudHJ5PjxyZWZlcmVuY2UgdmFsdWU9IkNvdmVyYWdlLzBjYWE2YzVhLWUzYWUtNGIyNi1iNWI2LWU2ZDEyZjUzNWJlNiIvPjwvZW50cnk+PC9zZWN0aW9uPjxzZWN0aW9uPjxjb2RlPjxjb2Rpbmc+PHN5c3RlbSB2YWx1ZT0iaHR0cHM6Ly9maGlyLmtidi5kZS9Db2RlU3lzdGVtL0tCVl9DU19FUlBfU2VjdGlvbl9UeXBlIi8+PGNvZGUgdmFsdWU9IlByZXNjcmlwdGlvbiIvPjwvY29kaW5nPjwvY29kZT48ZW50cnk+PHJlZmVyZW5jZSB2YWx1ZT0iTWVkaWNhdGlvblJlcXVlc3QvNWMzZjNjNTAtZTg4Ny00OGJiLWFlOTItMTMxNDY3MGQ4MjljIi8+PC9lbnRyeT48L3NlY3Rpb24+PC9Db21wb3NpdGlvbj48L3Jlc291cmNlPjwvZW50cnk+PGVudHJ5PjxmdWxsVXJsIHZhbHVlPSJodHRwczovL3B2cy5nZW1hdGlrLmRlL2ZoaXIvTWVkaWNhdGlvblJlcXVlc3QvNWMzZjNjNTAtZTg4Ny00OGJiLWFlOTItMTMxNDY3MGQ4MjljIi8+PHJlc291cmNlPjxNZWRpY2F0aW9uUmVxdWVzdCB4bWxucz0iaHR0cDovL2hsNy5vcmcvZmhpciI+PGlkIHZhbHVlPSI1YzNmM2M1MC1lODg3LTQ4YmItYWU5Mi0xMzE0NjcwZDgyOWMiLz48bWV0YT48cHJvZmlsZSB2YWx1ZT0iaHR0cHM6Ly9maGlyLmtidi5kZS9TdHJ1Y3R1cmVEZWZpbml0aW9uL0tCVl9QUl9FUlBfUHJlc2NyaXB0aW9ufDEuMS4wIi8+PC9tZXRhPjxleHRlbnNpb24gdXJsPSJodHRwczovL2ZoaXIua2J2LmRlL1N0cnVjdHVyZURlZmluaXRpb24vS0JWX0VYX0VSUF9CVkciPjx2YWx1ZUJvb2xlYW4gdmFsdWU9ImZhbHNlIi8+PC9leHRlbnNpb24+PGV4dGVuc2lvbiB1cmw9Imh0dHBzOi8vZmhpci5rYnYuZGUvU3RydWN0dXJlRGVmaW5pdGlvbi9LQlZfRVhfRVJQX0VtZXJnZW5jeVNlcnZpY2VzRmVlIj48dmFsdWVCb29sZWFuIHZhbHVlPSJmYWxzZSIvPjwvZXh0ZW5zaW9uPjxleHRlbnNpb24gdXJsPSJodHRwczovL2ZoaXIua2J2LmRlL1N0cnVjdHVyZURlZmluaXRpb24vS0JWX0VYX0VSUF9NdWx0aXBsZV9QcmVzY3JpcHRpb24iPjxleHRlbnNpb24gdXJsPSJLZW5uemVpY2hlbiI+PHZhbHVlQm9vbGVhbiB2YWx1ZT0iZmFsc2UiLz48L2V4dGVuc2lvbj48L2V4dGVuc2lvbj48ZXh0ZW5zaW9uIHVybD0iaHR0cHM6Ly9maGlyLmtidi5kZS9TdHJ1Y3R1cmVEZWZpbml0aW9uL0tCVl9FWF9GT1JfU3RhdHVzQ29QYXltZW50Ij48dmFsdWVDb2Rpbmc+PHN5c3RlbSB2YWx1ZT0iaHR0cHM6Ly9maGlyLmtidi5kZS9Db2RlU3lzdGVtL0tCVl9DU19GT1JfU3RhdHVzQ29QYXltZW50Ii8+PGNvZGUgdmFsdWU9IjAiLz48L3ZhbHVlQ29kaW5nPjwvZXh0ZW5zaW9uPjxzdGF0dXMgdmFsdWU9ImFjdGl2ZSIvPjxpbnRlbnQgdmFsdWU9Im9yZGVyIi8+PG1lZGljYXRpb25SZWZlcmVuY2U+PHJlZmVyZW5jZSB2YWx1ZT0iTWVkaWNhdGlvbi8wODkzNGVmMS1jZDQzLTRiZGItYTY2YS02YTkzY2QwY2Q4YjQiLz48L21lZGljYXRpb25SZWZlcmVuY2U+PHN1YmplY3Q+PHJlZmVyZW5jZSB2YWx1ZT0iUGF0aWVudC9lNjI3NGMwNS1mNjNjLTRlYTEtOWMzYi0zODM0MGVjYmNhNmMiLz48L3N1YmplY3Q+PGF1dGhvcmVkT24gdmFsdWU9IjIwMjMtMDMtMTAiLz48cmVxdWVzdGVyPjxyZWZlcmVuY2UgdmFsdWU9IlByYWN0aXRpb25lci84OWUzNjcxMi05YWIxLTRjYjYtYWE3Yi0yOTEyM2NkNDk5ZTMiLz48L3JlcXVlc3Rlcj48aW5zdXJhbmNlPjxyZWZlcmVuY2UgdmFsdWU9IkNvdmVyYWdlLzBjYWE2YzVhLWUzYWUtNGIyNi1iNWI2LWU2ZDEyZjUzNWJlNiIvPjwvaW5zdXJhbmNlPjxkb3NhZ2VJbnN0cnVjdGlvbj48ZXh0ZW5zaW9uIHVybD0iaHR0cHM6Ly9maGlyLmtidi5kZS9TdHJ1Y3R1cmVEZWZpbml0aW9uL0tCVl9FWF9FUlBfRG9zYWdlRmxhZyI+PHZhbHVlQm9vbGVhbiB2YWx1ZT0idHJ1ZSIvPjwvZXh0ZW5zaW9uPjx0ZXh0IHZhbHVlPSIxLTAtMC0wIi8+PC9kb3NhZ2VJbnN0cnVjdGlvbj48ZGlzcGVuc2VSZXF1ZXN0PjxxdWFudGl0eT48dmFsdWUgdmFsdWU9IjEiLz48c3lzdGVtIHZhbHVlPSJodHRwOi8vdW5pdHNvZm1lYXN1cmUub3JnIi8+PGNvZGUgdmFsdWU9IntQYWNrYWdlfSIvPjwvcXVhbnRpdHk+PC9kaXNwZW5zZVJlcXVlc3Q+PHN1YnN0aXR1dGlvbj48YWxsb3dlZEJvb2xlYW4gdmFsdWU9InRydWUiLz48L3N1YnN0aXR1dGlvbj48L01lZGljYXRpb25SZXF1ZXN0PjwvcmVzb3VyY2U+PC9lbnRyeT48ZW50cnk+PGZ1bGxVcmwgdmFsdWU9Imh0dHBzOi8vcHZzLmdlbWF0aWsuZGUvZmhpci9NZWRpY2F0aW9uLzA4OTM0ZWYxLWNkNDMtNGJkYi1hNjZhLTZhOTNjZDBjZDhiNCIvPjxyZXNvdXJjZT48TWVkaWNhdGlvbiB4bWxucz0iaHR0cDovL2hsNy5vcmcvZmhpciI+PGlkIHZhbHVlPSIwODkzNGVmMS1jZDQzLTRiZGItYTY2YS02YTkzY2QwY2Q4YjQiLz48bWV0YT48cHJvZmlsZSB2YWx1ZT0iaHR0cHM6Ly9maGlyLmtidi5kZS9TdHJ1Y3R1cmVEZWZpbml0aW9uL0tCVl9QUl9FUlBfTWVkaWNhdGlvbl9QWk58MS4xLjAiLz48L21ldGE+PGV4dGVuc2lvbiB1cmw9Imh0dHBzOi8vZmhpci5rYnYuZGUvU3RydWN0dXJlRGVmaW5pdGlvbi9LQlZfRVhfQmFzZV9NZWRpY2F0aW9uX1R5cGUiPjx2YWx1ZUNvZGVhYmxlQ29uY2VwdD48Y29kaW5nPjxzeXN0ZW0gdmFsdWU9Imh0dHA6Ly9zbm9tZWQuaW5mby9zY3QiLz48dmVyc2lvbiB2YWx1ZT0iaHR0cDovL3Nub21lZC5pbmZvL3NjdC85MDAwMDAwMDAwMDAyMDcwMDgvdmVyc2lvbi8yMDIyMDMzMSIvPjxjb2RlIHZhbHVlPSI3NjMxNTgwMDMiLz48ZGlzcGxheSB2YWx1ZT0iTWVkaWNpbmFsIHByb2R1Y3QgKHByb2R1Y3QpIi8+PC9jb2Rpbmc+PC92YWx1ZUNvZGVhYmxlQ29uY2VwdD48L2V4dGVuc2lvbj48ZXh0ZW5zaW9uIHVybD0iaHR0cHM6Ly9maGlyLmtidi5kZS9TdHJ1Y3R1cmVEZWZpbml0aW9uL0tCVl9FWF9FUlBfTWVkaWNhdGlvbl9DYXRlZ29yeSI+PHZhbHVlQ29kaW5nPjxzeXN0ZW0gdmFsdWU9Imh0dHBzOi8vZmhpci5rYnYuZGUvQ29kZVN5c3RlbS9LQlZfQ1NfRVJQX01lZGljYXRpb25fQ2F0ZWdvcnkiLz48Y29kZSB2YWx1ZT0iMDAiLz48L3ZhbHVlQ29kaW5nPjwvZXh0ZW5zaW9uPjxleHRlbnNpb24gdXJsPSJodHRwczovL2ZoaXIua2J2LmRlL1N0cnVjdHVyZURlZmluaXRpb24vS0JWX0VYX0VSUF9NZWRpY2F0aW9uX1ZhY2NpbmUiPjx2YWx1ZUJvb2xlYW4gdmFsdWU9ImZhbHNlIi8+PC9leHRlbnNpb24+PGV4dGVuc2lvbiB1cmw9Imh0dHA6Ly9maGlyLmRlL1N0cnVjdHVyZURlZmluaXRpb24vbm9ybWdyb2Vzc2UiPjx2YWx1ZUNvZGUgdmFsdWU9Ik5CIi8+PC9leHRlbnNpb24+PGNvZGU+PGNvZGluZz48c3lzdGVtIHZhbHVlPSJodHRwOi8vZmhpci5kZS9Db2RlU3lzdGVtL2lmYS9wem4iLz48Y29kZSB2YWx1ZT0iNTIxNjQ4MDgiLz48L2NvZGluZz48dGV4dCB2YWx1ZT0iU2NobWVyem1pdHRlbCIvPjwvY29kZT48Zm9ybT48Y29kaW5nPjxzeXN0ZW0gdmFsdWU9Imh0dHBzOi8vZmhpci5rYnYuZGUvQ29kZVN5c3RlbS9LQlZfQ1NfU0ZISVJfS0JWX0RBUlJFSUNIVU5HU0ZPUk0iLz48Y29kZSB2YWx1ZT0iVEFCIi8+PC9jb2Rpbmc+PC9mb3JtPjxhbW91bnQ+PG51bWVyYXRvcj48ZXh0ZW5zaW9uIHVybD0iaHR0cHM6Ly9maGlyLmtidi5kZS9TdHJ1Y3R1cmVEZWZpbml0aW9uL0tCVl9FWF9FUlBfTWVkaWNhdGlvbl9QYWNrYWdpbmdTaXplIj48dmFsdWVTdHJpbmcgdmFsdWU9IjEiLz48L2V4dGVuc2lvbj48dW5pdCB2YWx1ZT0iU3RrIi8+PC9udW1lcmF0b3I+PGRlbm9taW5hdG9yPjx2YWx1ZSB2YWx1ZT0iMSIvPjwvZGVub21pbmF0b3I+PC9hbW91bnQ+PC9NZWRpY2F0aW9uPjwvcmVzb3VyY2U+PC9lbnRyeT48ZW50cnk+PGZ1bGxVcmwgdmFsdWU9Imh0dHBzOi8vcHZzLmdlbWF0aWsuZGUvZmhpci9QYXRpZW50L2U2Mjc0YzA1LWY2M2MtNGVhMS05YzNiLTM4MzQwZWNiY2E2YyIvPjxyZXNvdXJjZT48UGF0aWVudCB4bWxucz0iaHR0cDovL2hsNy5vcmcvZmhpciI+PGlkIHZhbHVlPSJlNjI3NGMwNS1mNjNjLTRlYTEtOWMzYi0zODM0MGVjYmNhNmMiLz48bWV0YT48cHJvZmlsZSB2YWx1ZT0iaHR0cHM6Ly9maGlyLmtidi5kZS9TdHJ1Y3R1cmVEZWZpbml0aW9uL0tCVl9QUl9GT1JfUGF0aWVudHwxLjEuMCIvPjwvbWV0YT48aWRlbnRpZmllcj48dHlwZT48Y29kaW5nPjxzeXN0ZW0gdmFsdWU9Imh0dHA6Ly9maGlyLmRlL0NvZGVTeXN0ZW0vaWRlbnRpZmllci10eXBlLWRlLWJhc2lzIi8+PGNvZGUgdmFsdWU9IlBLViIvPjwvY29kaW5nPjwvdHlwZT48c3lzdGVtIHZhbHVlPSJodHRwOi8vZmhpci5kZS9zaWQvcGt2L2t2aWQtMTAiLz48dmFsdWUgdmFsdWU9IlgxMTA0NjU3NzAiLz48L2lkZW50aWZpZXI+PG5hbWU+PHVzZSB2YWx1ZT0ib2ZmaWNpYWwiLz48ZmFtaWx5IHZhbHVlPSJBbmdlcm3DpG5uIj48ZXh0ZW5zaW9uIHVybD0iaHR0cDovL2hsNy5vcmcvZmhpci9TdHJ1Y3R1cmVEZWZpbml0aW9uL2h1bWFubmFtZS1vd24tbmFtZSI+PHZhbHVlU3RyaW5nIHZhbHVlPSJBbmdlcm3DpG5uIi8+PC9leHRlbnNpb24+PC9mYW1pbHk+PGdpdmVuIHZhbHVlPSJHw7xudGhlciIvPjwvbmFtZT48YmlydGhEYXRlIHZhbHVlPSIyMDA0LTAxLTI5Ii8+PGFkZHJlc3M+PHR5cGUgdmFsdWU9ImJvdGgiLz48bGluZSB2YWx1ZT0iTHVyY2hlbndlZyAxNDgiPjxleHRlbnNpb24gdXJsPSJodHRwOi8vaGw3Lm9yZy9maGlyL1N0cnVjdHVyZURlZmluaXRpb24vaXNvMjEwOTAtQURYUC1ob3VzZU51bWJlciI+PHZhbHVlU3RyaW5nIHZhbHVlPSIxNDgiLz48L2V4dGVuc2lvbj48ZXh0ZW5zaW9uIHVybD0iaHR0cDovL2hsNy5vcmcvZmhpci9TdHJ1Y3R1cmVEZWZpbml0aW9uL2lzbzIxMDkwLUFEWFAtc3RyZWV0TmFtZSI+PHZhbHVlU3RyaW5nIHZhbHVlPSJMdXJjaGVud2VnIi8+PC9leHRlbnNpb24+PC9saW5lPjxjaXR5IHZhbHVlPSJOb3JkIFBhdWxhIi8+PHBvc3RhbENvZGUgdmFsdWU9IjMzNDgxIi8+PGNvdW50cnkgdmFsdWU9IkQiLz48L2FkZHJlc3M+PC9QYXRpZW50PjwvcmVzb3VyY2U+PC9lbnRyeT48ZW50cnk+PGZ1bGxVcmwgdmFsdWU9Imh0dHBzOi8vcHZzLmdlbWF0aWsuZGUvZmhpci9Pcmdhbml6YXRpb24vOWVkOGY3MDYtNDc0NS00ZmU0LThlOGQtOTBjZjVmODkwOWMxIi8+PHJlc291cmNlPjxPcmdhbml6YXRpb24geG1sbnM9Imh0dHA6Ly9obDcub3JnL2ZoaXIiPjxpZCB2YWx1ZT0iOWVkOGY3MDYtNDc0NS00ZmU0LThlOGQtOTBjZjVmODkwOWMxIi8+PG1ldGE+PHByb2ZpbGUgdmFsdWU9Imh0dHBzOi8vZmhpci5rYnYuZGUvU3RydWN0dXJlRGVmaW5pdGlvbi9LQlZfUFJfRk9SX09yZ2FuaXphdGlvbnwxLjEuMCIvPjwvbWV0YT48aWRlbnRpZmllcj48dHlwZT48Y29kaW5nPjxzeXN0ZW0gdmFsdWU9Imh0dHA6Ly90ZXJtaW5vbG9neS5obDcub3JnL0NvZGVTeXN0ZW0vdjItMDIwMyIvPjxjb2RlIHZhbHVlPSJCU05SIi8+PC9jb2Rpbmc+PC90eXBlPjxzeXN0ZW0gdmFsdWU9Imh0dHBzOi8vZmhpci5rYnYuZGUvTmFtaW5nU3lzdGVtL0tCVl9OU19CYXNlX0JTTlIiLz48dmFsdWUgdmFsdWU9IjgzMTUzMTE2OSIvPjwvaWRlbnRpZmllcj48bmFtZSB2YWx1ZT0iQXJ6dHByYXhpcyBTY2hyYcOfZXIiLz48dGVsZWNvbT48c3lzdGVtIHZhbHVlPSJwaG9uZSIvPjx2YWx1ZSB2YWx1ZT0iKDA5NTE5KSAwNDI1MTIyIi8+PC90ZWxlY29tPjx0ZWxlY29tPjxzeXN0ZW0gdmFsdWU9ImVtYWlsIi8+PHZhbHVlIHZhbHVlPSJicmlhbi5wZmzDvGduZXJAa3VtbWxlLm5ldCIvPjwvdGVsZWNvbT48YWRkcmVzcz48dHlwZSB2YWx1ZT0iYm90aCIvPjxsaW5lIHZhbHVlPSJIZWlucmljaC1Mw7xia2UtU3RyLiAwIj48ZXh0ZW5zaW9uIHVybD0iaHR0cDovL2hsNy5vcmcvZmhpci9TdHJ1Y3R1cmVEZWZpbml0aW9uL2lzbzIxMDkwLUFEWFAtaG91c2VOdW1iZXIiPjx2YWx1ZVN0cmluZyB2YWx1ZT0iMCIvPjwvZXh0ZW5zaW9uPjxleHRlbnNpb24gdXJsPSJodHRwOi8vaGw3Lm9yZy9maGlyL1N0cnVjdHVyZURlZmluaXRpb24vaXNvMjEwOTAtQURYUC1zdHJlZXROYW1lIj48dmFsdWVTdHJpbmcgdmFsdWU9IkhlaW5yaWNoLUzDvGJrZS1TdHIuIi8+PC9leHRlbnNpb24+PC9saW5lPjxjaXR5IHZhbHVlPSJNaW50emxhZmZzY2hlaWQiLz48cG9zdGFsQ29kZSB2YWx1ZT0iMjYxNzAiLz48Y291bnRyeSB2YWx1ZT0iRCIvPjwvYWRkcmVzcz48L09yZ2FuaXphdGlvbj48L3Jlc291cmNlPjwvZW50cnk+PGVudHJ5PjxmdWxsVXJsIHZhbHVlPSJodHRwczovL3B2cy5nZW1hdGlrLmRlL2ZoaXIvQ292ZXJhZ2UvMGNhYTZjNWEtZTNhZS00YjI2LWI1YjYtZTZkMTJmNTM1YmU2Ii8+PHJlc291cmNlPjxDb3ZlcmFnZSB4bWxucz0iaHR0cDovL2hsNy5vcmcvZmhpciI+PGlkIHZhbHVlPSIwY2FhNmM1YS1lM2FlLTRiMjYtYjViNi1lNmQxMmY1MzViZTYiLz48bWV0YT48cHJvZmlsZSB2YWx1ZT0iaHR0cHM6Ly9maGlyLmtidi5kZS9TdHJ1Y3R1cmVEZWZpbml0aW9uL0tCVl9QUl9GT1JfQ292ZXJhZ2V8MS4xLjAiLz48L21ldGE+PGV4dGVuc2lvbiB1cmw9Imh0dHA6Ly9maGlyLmRlL1N0cnVjdHVyZURlZmluaXRpb24vZ2t2L2Jlc29uZGVyZS1wZXJzb25lbmdydXBwZSI+PHZhbHVlQ29kaW5nPjxzeXN0ZW0gdmFsdWU9Imh0dHBzOi8vZmhpci5rYnYuZGUvQ29kZVN5c3RlbS9LQlZfQ1NfU0ZISVJfS0JWX1BFUlNPTkVOR1JVUFBFIi8+PGNvZGUgdmFsdWU9IjAwIi8+PC92YWx1ZUNvZGluZz48L2V4dGVuc2lvbj48ZXh0ZW5zaW9uIHVybD0iaHR0cDovL2ZoaXIuZGUvU3RydWN0dXJlRGVmaW5pdGlvbi9na3YvZG1wLWtlbm56ZWljaGVuIj48dmFsdWVDb2Rpbmc+PHN5c3RlbSB2YWx1ZT0iaHR0cHM6Ly9maGlyLmtidi5kZS9Db2RlU3lzdGVtL0tCVl9DU19TRkhJUl9LQlZfRE1QIi8+PGNvZGUgdmFsdWU9IjAwIi8+PC92YWx1ZUNvZGluZz48L2V4dGVuc2lvbj48ZXh0ZW5zaW9uIHVybD0iaHR0cDovL2ZoaXIuZGUvU3RydWN0dXJlRGVmaW5pdGlvbi9na3Yvd29wIj48dmFsdWVDb2Rpbmc+PHN5c3RlbSB2YWx1ZT0iaHR0cHM6Ly9maGlyLmtidi5kZS9Db2RlU3lzdGVtL0tCVl9DU19TRkhJUl9JVEFfV09QIi8+PGNvZGUgdmFsdWU9IjczIi8+PC92YWx1ZUNvZGluZz48L2V4dGVuc2lvbj48ZXh0ZW5zaW9uIHVybD0iaHR0cDovL2ZoaXIuZGUvU3RydWN0dXJlRGVmaW5pdGlvbi9na3YvdmVyc2ljaGVydGVuYXJ0Ij48dmFsdWVDb2Rpbmc+PHN5c3RlbSB2YWx1ZT0iaHR0cHM6Ly9maGlyLmtidi5kZS9Db2RlU3lzdGVtL0tCVl9DU19TRkhJUl9LQlZfVkVSU0lDSEVSVEVOU1RBVFVTIi8+PGNvZGUgdmFsdWU9IjEiLz48L3ZhbHVlQ29kaW5nPjwvZXh0ZW5zaW9uPjxzdGF0dXMgdmFsdWU9ImFjdGl2ZSIvPjx0eXBlPjxjb2Rpbmc+PHN5c3RlbSB2YWx1ZT0iaHR0cDovL2ZoaXIuZGUvQ29kZVN5c3RlbS92ZXJzaWNoZXJ1bmdzYXJ0LWRlLWJhc2lzIi8+PGNvZGUgdmFsdWU9IlBLViIvPjwvY29kaW5nPjwvdHlwZT48YmVuZWZpY2lhcnk+PHJlZmVyZW5jZSB2YWx1ZT0iUGF0aWVudC9lMDA3NzRmZC0yZTk4LTRhYTMtOGQ3My0wZWNlYWQzZGQ5NmUiLz48L2JlbmVmaWNpYXJ5PjxwYXlvcj48aWRlbnRpZmllcj48c3lzdGVtIHZhbHVlPSJodHRwOi8vZmhpci5kZS9zaWQvYXJnZS1pay9pa25yIi8+PHZhbHVlIHZhbHVlPSI2NzMzODAyNDciLz48L2lkZW50aWZpZXI+PGRpc3BsYXkgdmFsdWU9IktPQSBCZXJsaW4iLz48L3BheW9yPjwvQ292ZXJhZ2U+PC9yZXNvdXJjZT48L2VudHJ5PjxlbnRyeT48ZnVsbFVybCB2YWx1ZT0iaHR0cHM6Ly9wdnMuZ2VtYXRpay5kZS9maGlyL1ByYWN0aXRpb25lci84OWUzNjcxMi05YWIxLTRjYjYtYWE3Yi0yOTEyM2NkNDk5ZTMiLz48cmVzb3VyY2U+PFByYWN0aXRpb25lciB4bWxucz0iaHR0cDovL2hsNy5vcmcvZmhpciI+PGlkIHZhbHVlPSI4OWUzNjcxMi05YWIxLTRjYjYtYWE3Yi0yOTEyM2NkNDk5ZTMiLz48bWV0YT48cHJvZmlsZSB2YWx1ZT0iaHR0cHM6Ly9maGlyLmtidi5kZS9TdHJ1Y3R1cmVEZWZpbml0aW9uL0tCVl9QUl9GT1JfUHJhY3RpdGlvbmVyfDEuMS4wIi8+PC9tZXRhPjxpZGVudGlmaWVyPjx0eXBlPjxjb2Rpbmc+PHN5c3RlbSB2YWx1ZT0iaHR0cDovL3Rlcm1pbm9sb2d5LmhsNy5vcmcvQ29kZVN5c3RlbS92Mi0wMjAzIi8+PGNvZGUgdmFsdWU9IkxBTlIiLz48L2NvZGluZz48L3R5cGU+PHN5c3RlbSB2YWx1ZT0iaHR0cHM6Ly9maGlyLmtidi5kZS9OYW1pbmdTeXN0ZW0vS0JWX05TX0Jhc2VfQU5SIi8+PHZhbHVlIHZhbHVlPSI3MTY2MDgzMDUiLz48L2lkZW50aWZpZXI+PG5hbWU+PHVzZSB2YWx1ZT0ib2ZmaWNpYWwiLz48ZmFtaWx5IHZhbHVlPSJTY2hyYcOfZXIiPjxleHRlbnNpb24gdXJsPSJodHRwOi8vaGw3Lm9yZy9maGlyL1N0cnVjdHVyZURlZmluaXRpb24vaHVtYW5uYW1lLW93bi1uYW1lIj48dmFsdWVTdHJpbmcgdmFsdWU9IlNjaHJhw59lciIvPjwvZXh0ZW5zaW9uPjwvZmFtaWx5PjxnaXZlbiB2YWx1ZT0iRHIuIi8+PHByZWZpeCB2YWx1ZT0iRHIuIj48ZXh0ZW5zaW9uIHVybD0iaHR0cDovL2hsNy5vcmcvZmhpci9TdHJ1Y3R1cmVEZWZpbml0aW9uL2lzbzIxMDkwLUVOLXF1YWxpZmllciI+PHZhbHVlQ29kZSB2YWx1ZT0iQUMiLz48L2V4dGVuc2lvbj48L3ByZWZpeD48L25hbWU+PHF1YWxpZmljYXRpb24+PGNvZGU+PGNvZGluZz48c3lzdGVtIHZhbHVlPSJodHRwczovL2ZoaXIua2J2LmRlL0NvZGVTeXN0ZW0vS0JWX0NTX0ZPUl9RdWFsaWZpY2F0aW9uX1R5cGUiLz48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"/>
                </Binary>
            </resource>
        </entry>
        <entry>
            <fullUrl value="https://erp-dev.zentral.erp.splitdns.ti-dienste.de/Consent/CHARGCONS-X110465770"/>
            <resource>
                <Consent xmlns="http://hl7.org/fhir">
                    <id value="CHARGCONS-X110465770"/>
                    <meta>
                        <profile value="https://gematik.de/fhir/erpchrg/StructureDefinition/GEM_ERPCHRG_PR_Consent|1.0"/>
                    </meta>
                    <status value="active"/>
                    <scope>
                        <coding>
                            <system value="http://terminology.hl7.org/CodeSystem/consentscope"/>
                            <code value="patient-privacy"/>
                            <display value="Privacy Consent"/>
                        </coding>
                    </scope>
                    <category>
                        <coding>
                            <system value="https://gematik.de/fhir/erpchrg/CodeSystem/GEM_ERPCHRG_CS_ConsentType"/>
                            <code value="CHARGCONS"/>
                            <display value="Consent for saving electronic charge item"/>
                        </coding>
                    </category>
                    <patient>
                        <identifier>
                            <system value="http://fhir.de/sid/pkv/kvid-10"/>
                            <value value="X110465770"/>
                        </identifier>
                    </patient>
                    <dateTime value="2023-03-10T07:46:39.000+00:00"/>
                    <policyRule>
                        <coding>
                            <system value="http://terminology.hl7.org/CodeSystem/v3-ActCode"/>
                            <code value="OPTIN"/>
                        </coding>
                    </policyRule>
                </Consent>
            </resource>
        </entry>
    </Bundle>

Das generierte `Secret` stellt den Zugriffscode der abrufenden Apotheke
dar und muss in allen folgenden Workflowschritten als
`<identifier><value value="*"/></identifier>` angegeben werden, damit
nicht eine fremde Apotheke den Prozess übernehmen kann.

Der Status des Tasks unter `<status value="*"/>` ist in Bearbeitung
(`in-progress`)

Das Element `<Binary> <data value="*"/></Binary>` enthält den
qualifiziert signierten Verordnungsdatensatz als PKCS#7-Datei in
Base64-codierter Form. Innerhalb des Signaturobjekts ist das
E-Rezept-Bundle enthalten (Enveloping-Signatur) und muss vom
Apothekensystem für die Bearbeitung des E-Rezepts verarbeitet werden.
Der codierte Base64-String ist hier aus Gründen der Lesbarkeit nicht
vollständig dargestellt. Das vollständige Beispiel findet sich im
Unterordner der [Beispiele](../samples/qes/signed) in der Datei
`4fe2013d-ae94-441a-a1b1-78236ae65680_S_SECUN_secu_kon_4.8.2_4.1.3.p7`

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
[small]#Die Anfrage wurde erfolgreich bearbeitet. Die Response enthält die angefragten Daten.#</code></pre></td>
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
<td style="text-align: left;"><p>409</p></td>
<td style="text-align: left;"><p>Conflict<br />
<span class="small">Die Anfrage wurde unter falschen Annahmen gestellt.
Das E-Rezept hat nicht den Status, dass es durch die Apotheke abgerufen
werden kann.</span><br />
<span class="small">Im OperationOutcome werden weitere Informationen
gegeben:</span><br />
<span class="small">"Task has invalid status completed"</span><br />
<span class="small">"Task has invalid status in-progress"</span><br />
<span class="small">"Task has invalid status draft"</span></p></td>
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

# Qualifizierte Signatur des E-Rezepts prüfen

Im Apothekenverwaltungssystem liegen nach dem Abruf aus dem
E-Rezept-Fachdienst der Task des Workflows und der qualifiziert
signierte Verordnungsdatensatz vor. Die Rechtmäßigkeit der
elektronischen Verordnung wird mittels Prüfung der QES durch den
Konnektor verifiziert. Nur bei gültiger qualifizierter elektronischer
Signatur des E-Rezepts darf der Apotheker mit der Bearbeitung der
Verordnung fortfahren. Für die Prüfung wird die soeben heruntergeladene
PKCS#7-Datei in Base64-codierter Form an die SOAP-Schnittstelle der
Signaturprüfung des Konnektors als http-POST-Operation geschickt.

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
Content-Length: 1234</code></pre></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>Payload</strong></p></td>
<td style="text-align: left;"><div class="sourceCode" id="cb2"><pre
class="sourceCode xml"><code class="sourceCode xml"><span id="cb2-1"><a href="#cb2-1" aria-hidden="true" tabindex="-1"></a><span class="fu">&lt;?xml</span><span class="ot"> version=</span><span class="st">&quot;1.0&quot;</span><span class="ot"> encoding=</span><span class="st">&quot;utf-8&quot;</span><span class="fu">?&gt;</span></span>
<span id="cb2-2"><a href="#cb2-2" aria-hidden="true" tabindex="-1"></a>&lt;<span class="kw">SOAP-ENV:Envelope</span><span class="ot"> xmlns:SOAP-ENV=</span><span class="st">&quot;http://schemas.xmlsoap.org/soap/envelope/&quot;</span></span>
<span id="cb2-3"><a href="#cb2-3" aria-hidden="true" tabindex="-1"></a><span class="ot">    xmlns:SOAP-ENC=</span><span class="st">&quot;http://schemas.xmlsoap.org/soap/encoding/&quot;</span></span>
<span id="cb2-4"><a href="#cb2-4" aria-hidden="true" tabindex="-1"></a><span class="ot">    xmlns:xsi=</span><span class="st">&quot;http://www.w3.org/2001/XMLSchema-instance&quot;</span></span>
<span id="cb2-5"><a href="#cb2-5" aria-hidden="true" tabindex="-1"></a><span class="ot">    xmlns:xsd=</span><span class="st">&quot;http://www.w3.org/2001/XMLSchema&quot;</span></span>
<span id="cb2-6"><a href="#cb2-6" aria-hidden="true" tabindex="-1"></a><span class="ot">    xmlns:m0=</span><span class="st">&quot;http://ws.gematik.de/conn/ConnectorContext/v2.0&quot;</span></span>
<span id="cb2-7"><a href="#cb2-7" aria-hidden="true" tabindex="-1"></a><span class="ot">    xmlns:m1=</span><span class="st">&quot;http://ws.gematik.de/conn/ConnectorCommon/v5.0&quot;</span></span>
<span id="cb2-8"><a href="#cb2-8" aria-hidden="true" tabindex="-1"></a><span class="ot">    xmlns:m2=</span><span class="st">&quot;urn:oasis:names:tc:dss:1.0:core:schema&quot;</span></span>
<span id="cb2-9"><a href="#cb2-9" aria-hidden="true" tabindex="-1"></a><span class="ot">    xmlns:m3=</span><span class="st">&quot;http://www.w3.org/2000/09/xmldsig#&quot;</span></span>
<span id="cb2-10"><a href="#cb2-10" aria-hidden="true" tabindex="-1"></a><span class="ot">    xmlns:m4=</span><span class="st">&quot;urn:oasis:names:tc:dss-x:1.0:profiles:verificationreport:schema#&quot;</span>&gt;</span>
<span id="cb2-11"><a href="#cb2-11" aria-hidden="true" tabindex="-1"></a>    &lt;<span class="kw">SOAP-ENV:Body</span>&gt;</span>
<span id="cb2-12"><a href="#cb2-12" aria-hidden="true" tabindex="-1"></a>        &lt;<span class="kw">m:VerifyDocument</span><span class="ot"> xmlns:m=</span><span class="st">&quot;http://ws.gematik.de/conn/SignatureService/v7.4&quot;</span>&gt;</span>
<span id="cb2-13"><a href="#cb2-13" aria-hidden="true" tabindex="-1"></a>            &lt;<span class="kw">m0:Context</span>&gt;</span>
<span id="cb2-14"><a href="#cb2-14" aria-hidden="true" tabindex="-1"></a>                &lt;<span class="kw">m1:MandantId</span>&gt;Mandant1&lt;/<span class="kw">m1:MandantId</span>&gt;</span>
<span id="cb2-15"><a href="#cb2-15" aria-hidden="true" tabindex="-1"></a>                &lt;<span class="kw">m1:ClientSystemId</span>&gt;ClientID1&lt;/<span class="kw">m1:ClientSystemId</span>&gt;</span>
<span id="cb2-16"><a href="#cb2-16" aria-hidden="true" tabindex="-1"></a>                &lt;<span class="kw">m1:WorkplaceId</span>&gt;CATS&lt;/<span class="kw">m1:WorkplaceId</span>&gt;</span>
<span id="cb2-17"><a href="#cb2-17" aria-hidden="true" tabindex="-1"></a>            &lt;/<span class="kw">m0:Context</span>&gt;</span>
<span id="cb2-18"><a href="#cb2-18" aria-hidden="true" tabindex="-1"></a>            &lt;<span class="kw">m:TvMode</span>&gt;NONE&lt;/<span class="kw">m:TvMode</span>&gt;</span>
<span id="cb2-19"><a href="#cb2-19" aria-hidden="true" tabindex="-1"></a>            &lt;<span class="kw">m:OptionalInputs</span>&gt;</span>
<span id="cb2-20"><a href="#cb2-20" aria-hidden="true" tabindex="-1"></a>                &lt;<span class="kw">m:UseVerificationTime</span>&gt;</span>
<span id="cb2-21"><a href="#cb2-21" aria-hidden="true" tabindex="-1"></a>                    &lt;<span class="kw">m2:CurrentTime</span>/&gt;</span>
<span id="cb2-22"><a href="#cb2-22" aria-hidden="true" tabindex="-1"></a>                &lt;/<span class="kw">m:UseVerificationTime</span>&gt;</span>
<span id="cb2-23"><a href="#cb2-23" aria-hidden="true" tabindex="-1"></a>                &lt;<span class="kw">m4:ReturnVerificationReport</span>&gt;</span>
<span id="cb2-24"><a href="#cb2-24" aria-hidden="true" tabindex="-1"></a>                    &lt;<span class="kw">m4:IncludeVerifier</span>&gt;true&lt;/<span class="kw">m4:IncludeVerifier</span>&gt;</span>
<span id="cb2-25"><a href="#cb2-25" aria-hidden="true" tabindex="-1"></a>                    &lt;<span class="kw">m4:IncludeCertificateValues</span>&gt;true&lt;/<span class="kw">m4:IncludeCertificateValues</span>&gt;</span>
<span id="cb2-26"><a href="#cb2-26" aria-hidden="true" tabindex="-1"></a>                    &lt;<span class="kw">m4:IncludeRevocationValues</span>&gt;true&lt;/<span class="kw">m4:IncludeRevocationValues</span>&gt;</span>
<span id="cb2-27"><a href="#cb2-27" aria-hidden="true" tabindex="-1"></a>                    &lt;<span class="kw">m4:ExpandBinaryValues</span>&gt;false&lt;/<span class="kw">m4:ExpandBinaryValues</span>&gt;</span>
<span id="cb2-28"><a href="#cb2-28" aria-hidden="true" tabindex="-1"></a>                &lt;/<span class="kw">m4:ReturnVerificationReport</span>&gt;</span>
<span id="cb2-29"><a href="#cb2-29" aria-hidden="true" tabindex="-1"></a>            &lt;/<span class="kw">m:OptionalInputs</span>&gt;</span>
<span id="cb2-30"><a href="#cb2-30" aria-hidden="true" tabindex="-1"></a>            &lt;<span class="kw">m2:SignatureObject</span>&gt;</span>
<span id="cb2-31"><a href="#cb2-31" aria-hidden="true" tabindex="-1"></a>                &lt;<span class="kw">m2:Base64Signature</span><span class="ot"> Type=</span><span class="st">&quot;urn:ietf:rfc:5652&quot;</span>&gt; MIJTfQYJKoZIhvcNAQcCoIJTbjCCU2oCAQUxDzANBglghkgBZQMEAgEFADCCRIMGCSqGSIb3DQEH AaCCRHQEgkRwPEJ1bmRsZSB4bWxucz0iaHR0cDovL2hsNy5vcmcvZmhpciI+DQogIDwhLS0gQmVp c3BpZWwtQnVuZGxlIFdpcmtzdG9mZnZlcm9yZG51bmcgLS0+DQogIDxpZCB2YWx1ZT0iNGZlMjAx M2QtYWU5NC00NDFhLWExYjEtNzgyMzZhZTY1NjgwIiAvPg0KICA8bWV0YT4NCiAgICA8bGFzdFVw ZGF0ZWQgdmFsdWU9IjIwMjAtMDUtMDRUMDg6MzA6MDBaIiAvPg0KICAgIDxwcm9maWxlIHZhbHVl PSJodHRwczovL2ZoaXIua2J2LmRlL1N0cnVjdHVyZURlZmluaXRpb24vS0JWX1BSX0VSUF9CdW5k bGV8MS4wLjEiIC8+DQogIDwvbWV0YT4NCiAgPGlkZW50aWZpZXI+DQogICAgPHN5c3RlbSB2YWx1 ZT0iaHR0cHM6Ly9nZW1hdGlrLmRlL2ZoaXIvTmFtaW5nU3lzdGVtL1ByZXNjcmlwdGlvbklEIiAv Pg0KICAgIDx2YWx1ZSB2YWx1ZT0iMTYwLjEyMy40NTYuNzg5LjEyMy41OCIgLz4NCiAgPC9pZGVu dGlmaWVyPg0KICA8dHlwZSB2YWx1ZT0iZG9jdW1lbnQiIC8+DQogIDx0aW1lc3RhbXAgdmFsdWU9 IjIwMjAtMDUtMDRUMDg6MzA6MDBaIiAvPg0KICA8ZW50cnk+DQogICAgPGZ1bGxVcmwgdmFsdWU9 Imh0dHA6Ly9wdnMucHJheGlzLXRvcHAtZ2x1ZWNrbGljaC5sb2NhbC9maGlyL0NvbXBvc2l0aW9u L2IwZTIyYjg2LWU3ZTktNDZjMS04MGZlLWU2ZTI0NDQyZDc3YyIgLz4NCiAgICA8cmVzb3VyY2U+ DQogICAgICA8Q29tcG9zaXRpb24geG1sbnM9Imh0dHA6Ly9obDcub3JnL2ZoaXIiPg0KICAgICAg ICA8aWQgdmFsdWU9ImIwZTIyYjg2LWU3ZTktNDZjMS04MGZlLWU2ZTI0NDQyZDc3YyIgLz4NCiAg ICAgICAgPG1ldGE+DQogICAgICAgICAgPHByb2ZpbGUgdmFsdWU9Imh0dHBzOi8vZmhpci5rYnYu ZGUvU3RydWN0dXJlRGVmaW5pdGlvbi9LQlZfUFJfRVJQX0NvbXBvc2l0aW9ufDEuMC4xIiAvPg0K ICAgICAgICA8L21ldGE+DQogICAgICAgIDxleHRlbnNpb24gdXJsPSJodHRwczovL2ZoaXIua2J2 LmRlL1N0cnVjdHVyZURlZmluaXRpb24vS0JWX0VYX0ZPUl9MZWdhbF9iYXNpcyI+DQogICAgICAg ICAgPHZhbHVlQ29kaW5nPg0KICAgICAgICAgICAgPHN5c3RlbSB2YWx1ZT0iaHR0cHM6Ly9maGly Lmtidi5kZS9Db2RlU3lzdGVtL0tCVl9DU19TRkhJUl9LQlZfU1RBVFVTS0VOTlpFSUNIRU4iIC8+ DQogICAgICAgICAgICA8Y29kZSB2YWx1ZT0iMDAiIC8+DQogICAgICAgICAgPC92YWx1ZUNvZGlu Zz4NCiAgICAgICAgPC9leHRlbnNpb24+DQogICAgICAgIDxzdGF0dXMgdmFsdWU9ImZpbmFsIiAv Pg0KICAgICAgICA8dHlwZT4NCiAgICAgICAgICA8Y29kaW5nPg0KICAgICAgICAgICAgPHN5c3Rl bSB2YWx1ZT0iaHR0cHM6Ly9maGlyLmtidi5kZS9Db2RlU3lzdGVtL0tCVl9DU19TRkhJUl9LQlZf Rk9STVVMQVJfQVJUIiAvPg0KICAgICAgICAgICAgPGNvZGUgdmFsdWU9ImUxNkEiIC8+DQogICAg ICAgICAgPC9jb2Rpbmc+DQogICAgICAgIDwvdHlwZT4NCiAgICAgICAgPHN1YmplY3Q+DQogICAg ICAgICAgPHJlZmVyZW5jZSB2YWx1ZT0iUGF0aWVudC85Nzc0ZjY3Zi1hMjM4LTRkYWYtYjRlNi02 NzlkZWVlZjM4MTEiIC8+DQogICAgICAgIDwvc3ViamVjdD4NCiAgICAgICAgPGRhdGUgdmFsdWU9 IjIwMjAtMDItMDNUMTE6MzA6MDJaIiAvPg0KICAgICAgICA8YXV0aG9yPg0KICAgICAgICAgIDxy ZWZlcmVuY2UgdmFsdWU9IlByYWN0aXRpb25lci9kODQ2M2RhZi0yNThlLTRjYWQtYTg2YS02ZmQ0 MmZhYzE2MWMiIC8+DQogICAgICAgICAgPHR5cGUgdmFsdWU9IlByYWN0aXRpb25lciIgLz4NCiAg ICAgICAgPC9hdXRob3I+DQogICAgICAgIDxhdXRob3I+DQogICAgICAgICAgPHR5cGUgdmFsdWU9 IkRldmljZSIgLz4NCiAgICAgICAgICA8aWRlbnRpZmllcj4NCiAgICAgICAgICAgIDxzeXN0ZW0g dmFsdWU9Imh0dHBzOi8vZmhpci5rYnYuZGUvTmFtaW5nU3lzdGVtL0tCVl9OU19GT1JfUHJ1ZWZu dW1tZXIiIC8+DQogICAgICAgICAgICA8dmFsdWUgdmFsdWU9IlkvNDAwLzE5MTAvMzYvMzQ2IiAv Pg0KICAgICAgICAgIDwvaWRlbnRpZmllcj4NCiAgICAgICAgPC9hdXRob3I+DQogICAgICAgIDx0 aXRsZSB2YWx1ZT0iZWxla3Ryb25pc2NoZSBBcnpuZWltaXR0ZWx2ZXJvcmRudW5nIiAvPg0KICAg ICAgICA8YXR0ZXN0ZXI+DQogICAgICAgICAgPG1vZGUgdmFsdWU9ImxlZ2FsIiAvPg0KICAgICAg ICAgIDxwYXJ0eT4NCiAgICAgICAgICAgIDxyZWZlcmVuY2UgdmFsdWU9IlByYWN0aXRpb25lci8y MDU5N2UwZS1jYjJhLTQ1YjMtOTVmMC1kYzNkYmRiNjE3YzMiIC8+DQogICAgICAgICAgPC9wYXJ0 eT4NCiAgICAgICAgPC9hdHRlc3Rlcj4NCiAgICAgICAgPGN1c3RvZGlhbj4NCiAgICAgICAgICA8 cmVmZXJlbmNlIHZhbHVlPSJPcmdhbml6YXRpb24vY2YwNDJlNDQtMDg2YS00ZDUxLTljNzctMTcy ZjlhOTcyZTNiIiAvPg0KICAgICAgICA8L2N1c3RvZGlhbj4NCiAgICAgICAgPHNlY3Rpb24+DQog ICAgICAgICAgPGNvZGU+DQogICAgICAgICAgICA8Y29kaW5nPg0KICAgICAgICAgICAgICA8c3lz dGVtIHZhbHVlPSJodHRwczovL2ZoaXIua2J2LmRlL0NvZGVTeXN0ZW0vS0JWX0NTX0VSUF9TZWN0 aW9uX1R5cGUiIC8+DQogICAgICAgICAgICAgIDxjb2RlIHZhbHVlPSJQcmVzY3JpcHRpb24iIC8+ DQogICAgICAgICAgICA8L2NvZGluZz4NCiAgICAgICAgICA8L2NvZGU+DQogICAgICAgICAgPGVu dHJ5Pg0KICAgICAgICAgICAgPCEtLSBSZWZlcmVueiBhdWYgVmVyb3JkbnVuZyAoTWVkaWNhdGlv blJlcXVlc3QpIC0tPg0KICAgICAgICAgICAgPHJlZmVyZW5jZSB2YWx1ZT0iTWVkaWNhdGlvblJl cXVlc3QvZjU4ZjQ0MDMtN2EzYS00YTEyLWJiMTUtYjJmYTI1YjAyNTYxIiAvPg0KICAgICAgICAg IDwvZW50cnk+DQogICAgICAgIDwvc2VjdGlvbj4NCiAgICAgICAgPHNlY3Rpb24+DQogICAgICAg ICAgPGNvZGU+DQogICAgICAgICAgICA8Y29kaW5nPg0KICAgICAgICAgICAgICA8c3lzdGVtIHZh bHVlPSJodHRwczovL2ZoaXIua2J2LmRlL0NvZGVTeXN0ZW0vS0JWX0NTX0VSUF9TZWN0aW9uX1R5 cGUiIC8+DQogICAgICAgICAgICAgIDxjb2RlIHZhbHVlPSJDb3ZlcmFnZSIgLz4NCiAgICAgICAg ICAgIDwvY29kaW5nPg0KICAgICAgICAgIDwvY29kZT4NCiAgICAgICAgICA8ZW50cnk+DQogICAg ICAgICAgICA8IS0tIFJlZmVyZW56IGF1ZiBLcmFua2Vua2Fzc2UvS29zdGVudHLEgsKkZ2VyICAt LT4NCiAgICAgICAgICAgIDxyZWZlcmVuY2UgdmFsdWU9IkNvdmVyYWdlLzFiMWZmYjZlLWViMDUt NDNkNy04N2ViLWU3ODE4ZmU5NjYxYSIgLz4NCiAgICAgICAgICA8L2VudHJ5Pg0KICAgICAgICA8 L3NlY3Rpb24+DQogICAgICA8L0NvbXBvc2l0aW9uPg0KICAgIDwvcmVzb3VyY2U+DQogIDwvZW50 cnk+DQogIDxlbnRyeT4NCiAgICA8ZnVsbFVybCB2YWx1ZT0iaHR0cDovL3B2cy5wcmF4aXMtdG9w cC1nbHVlY2tsaWNoLmxvY2FsL2ZoaXIvTWVkaWNhdGlvblJlcXVlc3QvZjU4ZjQ0MDMtN2EzYS00 YTEyLWJiMTUtYjJmYTI1YjAyNTYxIiAvPg0KICAgIDxyZXNvdXJjZT4NCiAgICAgIDxNZWRpY2F0 aW9uUmVxdWVzdCB4bWxucz0iaHR0cDovL2hsNy5vcmcvZmhpciI+DQogICAgICAgIDxpZCB2YWx1 ZT0iZjU4ZjQ0MDMtN2EzYS00YTEyLWJiMTUtYjJmYTI1YjAyNTYxIiAvPg0KICAgICAgICA8bWV0 YT4NCiAgICAgICAgICA8cHJvZmlsZSB2YWx1ZT0iaHR0cHM6Ly9maGlyLmtidi5kZS9TdHJ1Y3R1 cmVEZWZpbml0aW9uL0tCVl9QUl9FUlBfUHJlc2NyaXB0aW9ufDEuMC4xIiAvPg0KICAgICAgICA8 L21ldGE+DQogICAgICAgIDxleHRlbnNpb24gdXJsPSJodHRwczovL2ZoaXIua2J2LmRlL1N0cnVj dHVyZURlZmluaXRpb24vS0JWX0VYX0VSUF9TdGF0dXNDb1BheW1lbnQiPg0KICAgICAgICAgIDx2 YWx1ZUNvZGluZz4NCiAgICAgICAgICAgIDxzeXN0ZW0gdmFsdWU9Imh0dHBzOi8vZmhpci5rYnYu ZGUvQ29kZVN5c3RlbS9LQlZfQ1NfRVJQX1N0YXR1c0NvUGF5bWVudCIgLz4NCiAgICAgICAgICAg IDxjb2RlIHZhbHVlPSIwIiAvPg0KICAgICAgICAgIDwvdmFsdWVDb2Rpbmc+DQogICAgICAgIDwv ZXh0ZW5zaW9uPg0KICAgICAgICA8ZXh0ZW5zaW9uIHVybD0iaHR0cHM6Ly9maGlyLmtidi5kZS9T dHJ1Y3R1cmVEZWZpbml0aW9uL0tCVl9FWF9FUlBfRW1lcmdlbmN5U2VydmljZXNGZWUiPg0KICAg ICAgICAgIDx2YWx1ZUJvb2xlYW4gdmFsdWU9ImZhbHNlIiAvPg0KICAgICAgICA8L2V4dGVuc2lv bj4NCiAgICAgICAgPGV4dGVuc2lvbiB1cmw9Imh0dHBzOi8vZmhpci5rYnYuZGUvU3RydWN0dXJl RGVmaW5pdGlvbi9LQlZfRVhfRVJQX0JWRyI+DQogICAgICAgICAgPHZhbHVlQm9vbGVhbiB2YWx1 ZT0iZmFsc2UiIC8+DQogICAgICAgIDwvZXh0ZW5zaW9uPg0KICAgICAgICA8ZXh0ZW5zaW9uIHVy bD0iaHR0cHM6Ly9maGlyLmtidi5kZS9TdHJ1Y3R1cmVEZWZpbml0aW9uL0tCVl9FWF9FUlBfQWNj aWRlbnQiPg0KICAgICAgICAgIDxleHRlbnNpb24gdXJsPSJ1bmZhbGxrZW5uemVpY2hlbiI+DQog ICAgICAgICAgICA8dmFsdWVDb2Rpbmc+DQogICAgICAgICAgICAgIDxzeXN0ZW0gdmFsdWU9Imh0 dHBzOi8vZmhpci5rYnYuZGUvQ29kZVN5c3RlbS9LQlZfQ1NfRk9SX1Vyc2FjaGVfVHlwZSIgLz4N CiAgICAgICAgICAgICAgPGNvZGUgdmFsdWU9IjEiIC8+DQogICAgICAgICAgICA8L3ZhbHVlQ29k aW5nPg0KICAgICAgICAgIDwvZXh0ZW5zaW9uPg0KICAgICAgICAgIDxleHRlbnNpb24gdXJsPSJ1 bmZhbGx0YWciPg0KICAgICAgICAgICAgPHZhbHVlRGF0ZSB2YWx1ZT0iMjAyMC0wNS0wMSIgLz4N CiAgICAgICAgICA8L2V4dGVuc2lvbj4NCiAgICAgICAgPC9leHRlbnNpb24+DQogICAgICAgIDxl eHRlbnNpb24gdXJsPSJodHRwczovL2ZoaXIua2J2LmRlL1N0cnVjdHVyZURlZmluaXRpb24vS0JW X0VYX0VSUF9NdWx0aXBsZV9QcmVzY3JpcHRpb24iPg0KICAgICAgICAgIDxleHRlbnNpb24gdXJs PSJLZW5uemVpY2hlbiI+DQogICAgICAgICAgICA8dmFsdWVCb29sZWFuIHZhbHVlPSJ0cnVlIiAv Pg0KICAgICAgICAgIDwvZXh0ZW5zaW9uPg0KICAgICAgICAgIDxleHRlbnNpb24gdXJsPSJOdW1t ZXJpZXJ1bmciPg0KICAgICAgICAgICAgPHZhbHVlUmF0aW8+DQogICAgICAgICAgICAgIDxudW1l cmF0b3I+DQogICAgICAgICAgICAgICAgPHZhbHVlIHZhbHVlPSIyIiAvPg0KICAgICAgICAgICAg ICA8L251bWVyYXRvcj4NCiAgICAgICAgICAgICAgPGRlbm9taW5hdG9yPg0KICAgICAgICAgICAg ICAgIDx2YWx1ZSB2YWx1ZT0iNCIgLz4NCiAgICAgICAgICAgICAgPC9kZW5vbWluYXRvcj4NCiAg ICAgICAgICAgIDwvdmFsdWVSYXRpbz4NCiAgICAgICAgICA8L2V4dGVuc2lvbj4NCiAgICAgICAg ICA8ZXh0ZW5zaW9uIHVybD0iWmVpdHJhdW0iPg0KICAgICAgICAgICAgPHZhbHVlUGVyaW9kPg0K ICAgICAgICAgICAgICA8c3RhcnQgdmFsdWU9IjIwMjEtMDEtMDIiIC8+DQogICAgICAgICAgICAg IDxlbmQgdmFsdWU9IjIwMjEtMDMtMzAiIC8+DQogICAgICAgICAgICA8L3ZhbHVlUGVyaW9kPg0K ICAgICAgICAgIDwvZXh0ZW5zaW9uPg0KICAgICAgICA8L2V4dGVuc2lvbj4NCiAgICAgICAgPHN0 YXR1cyB2YWx1ZT0iYWN0aXZlIiAvPg0KICAgICAgICA8aW50ZW50IHZhbHVlPSJvcmRlciIgLz4N CiAgICAgICAgPG1lZGljYXRpb25SZWZlcmVuY2U+DQogICAgICAgICAgPHJlZmVyZW5jZSB2YWx1 ZT0iTWVkaWNhdGlvbi9lM2E0ZWZhNy04NGZjLTQ2NWItYjE0Yy03MjAxOTUwOTc3ODMiIC8+DQog ICAgICAgIDwvbWVkaWNhdGlvblJlZmVyZW5jZT4NCiAgICAgICAgPHN1YmplY3Q+DQogICAgICAg ICAgPHJlZmVyZW5jZSB2YWx1ZT0iUGF0aWVudC85Nzc0ZjY3Zi1hMjM4LTRkYWYtYjRlNi02Nzlk ZWVlZjM4MTEiIC8+DQogICAgICAgIDwvc3ViamVjdD4NCiAgICAgICAgPGF1dGhvcmVkT24gdmFs dWU9IjIwMjAtMDUtMDIiIC8+DQogICAgICAgIDxyZXF1ZXN0ZXI+DQogICAgICAgICAgPHJlZmVy ZW5jZSB2YWx1ZT0iUHJhY3RpdGlvbmVyLzIwNTk3ZTBlLWNiMmEtNDViMy05NWYwLWRjM2RiZGI2 MTdjMyIgLz4NCiAgICAgICAgPC9yZXF1ZXN0ZXI+DQogICAgICAgIDxpbnN1cmFuY2U+DQogICAg ICAgICAgPHJlZmVyZW5jZSB2YWx1ZT0iQ292ZXJhZ2UvMWIxZmZiNmUtZWIwNS00M2Q3LTg3ZWIt ZTc4MThmZTk2NjFhIiAvPg0KICAgICAgICA8L2luc3VyYW5jZT4NCiAgICAgICAgPG5vdGU+DQog ICAgICAgICAgPHRleHQgdmFsdWU9IkR1bW15LUhpbndlaXMgZsO8ciBkaWUgQXBvdGhla2UiIC8+ DQogICAgICAgIDwvbm90ZT4NCiAgICAgICAgPGRvc2FnZUluc3RydWN0aW9uPg0KICAgICAgICAg IDxleHRlbnNpb24gdXJsPSJodHRwczovL2ZoaXIua2J2LmRlL1N0cnVjdHVyZURlZmluaXRpb24v S0JWX0VYX0VSUF9Eb3NhZ2VGbGFnIj4NCiAgICAgICAgICAgIDx2YWx1ZUJvb2xlYW4gdmFsdWU9 ImZhbHNlIiAvPg0KICAgICAgICAgIDwvZXh0ZW5zaW9uPg0KICAgICAgICA8L2Rvc2FnZUluc3Ry dWN0aW9uPg0KICAgICAgICA8ZGlzcGVuc2VSZXF1ZXN0Pg0KICAgICAgICAgIDxxdWFudGl0eT4N CiAgICAgICAgICAgIDx2YWx1ZSB2YWx1ZT0iMiIgLz4NCiAgICAgICAgICAgIDxzeXN0ZW0gdmFs dWU9Imh0dHA6Ly91bml0c29mbWVhc3VyZS5vcmciIC8+DQogICAgICAgICAgICA8Y29kZSB2YWx1 ZT0ie1BhY2thZ2V9IiAvPg0KICAgICAgICAgIDwvcXVhbnRpdHk+DQogICAgICAgIDwvZGlzcGVu c2VSZXF1ZXN0Pg0KICAgICAgICA8c3Vic3RpdHV0aW9uPg0KICAgICAgICAgIDxhbGxvd2VkQm9v bGVhbiB2YWx1ZT0idHJ1ZSIgLz4NCiAgICAgICAgPC9zdWJzdGl0dXRpb24+DQogICAgICA8L01l ZGljYXRpb25SZXF1ZXN0Pg0KICAgIDwvcmVzb3VyY2U+DQogIDwvZW50cnk+DQogIDxlbnRyeT4N CiAgICA8ZnVsbFVybCB2YWx1ZT0iaHR0cDovL3B2cy5wcmF4aXMtdG9wcC1nbHVlY2tsaWNoLmxv Y2FsL2ZoaXIvTWVkaWNhdGlvbi9lM2E0ZWZhNy04NGZjLTQ2NWItYjE0Yy03MjAxOTUwOTc3ODMi IC8+DQogICAgPHJlc291cmNlPg0KICAgICAgPE1lZGljYXRpb24geG1sbnM9Imh0dHA6Ly9obDcu b3JnL2ZoaXIiPg0KICAgICAgICA8aWQgdmFsdWU9ImUzYTRlZmE3LTg0ZmMtNDY1Yi1iMTRjLTcy MDE5NTA5Nzc4MyIgLz4NCiAgICAgICAgPG1ldGE+DQogICAgICAgICAgPHByb2ZpbGUgdmFsdWU9 Imh0dHBzOi8vZmhpci5rYnYuZGUvU3RydWN0dXJlRGVmaW5pdGlvbi9LQlZfUFJfRVJQX01lZGlj YXRpb25fSW5ncmVkaWVudHwxLjAuMSIgLz4NCiAgICAgICAgPC9tZXRhPg0KICAgICAgICA8ZXh0 ZW5zaW9uIHVybD0iaHR0cHM6Ly9maGlyLmtidi5kZS9TdHJ1Y3R1cmVEZWZpbml0aW9uL0tCVl9F WF9FUlBfTWVkaWNhdGlvbl9DYXRlZ29yeSI+DQogICAgICAgICAgPHZhbHVlQ29kaW5nPg0KICAg ICAgICAgICAgPHN5c3RlbSB2YWx1ZT0iaHR0cHM6Ly9maGlyLmtidi5kZS9Db2RlU3lzdGVtL0tC Vl9DU19FUlBfTWVkaWNhdGlvbl9DYXRlZ29yeSIgLz4NCiAgICAgICAgICAgIDxjb2RlIHZhbHVl PSIwMCIgLz4NCiAgICAgICAgICA8L3ZhbHVlQ29kaW5nPg0KICAgICAgICA8L2V4dGVuc2lvbj4N CiAgICAgICAgPGV4dGVuc2lvbiB1cmw9Imh0dHBzOi8vZmhpci5rYnYuZGUvU3RydWN0dXJlRGVm aW5pdGlvbi9LQlZfRVhfRVJQX01lZGljYXRpb25fVmFjY2luZSI+DQogICAgICAgICAgPHZhbHVl Qm9vbGVhbiB2YWx1ZT0iZmFsc2UiIC8+DQogICAgICAgIDwvZXh0ZW5zaW9uPg0KICAgICAgICA8 Y29kZT4NCiAgICAgICAgICA8Y29kaW5nPg0KICAgICAgICAgICAgPHN5c3RlbSB2YWx1ZT0iaHR0 cHM6Ly9maGlyLmtidi5kZS9Db2RlU3lzdGVtL0tCVl9DU19FUlBfTWVkaWNhdGlvbl9UeXBlIiAv Pg0KICAgICAgICAgICAgPGNvZGUgdmFsdWU9IndpcmtzdG9mZiIgLz4NCiAgICAgICAgICA8L2Nv ZGluZz4NCiAgICAgICAgPC9jb2RlPg0KICAgICAgICA8Zm9ybT4NCiAgICAgICAgICA8dGV4dCB2 YWx1ZT0iVGFibGV0dGVuIiAvPg0KICAgICAgICA8L2Zvcm0+DQogICAgICAgIDxhbW91bnQ+DQog ICAgICAgICAgPG51bWVyYXRvcj4NCiAgICAgICAgICAgIDx2YWx1ZSB2YWx1ZT0iMjAiIC8+DQog ICAgICAgICAgICA8dW5pdCB2YWx1ZT0iU3RrIiAvPg0KICAgICAgICAgIDwvbnVtZXJhdG9yPg0K ICAgICAgICAgIDxkZW5vbWluYXRvcj4NCiAgICAgICAgICAgIDx2YWx1ZSB2YWx1ZT0iMSIgLz4N CiAgICAgICAgICA8L2Rlbm9taW5hdG9yPg0KICAgICAgICA8L2Ftb3VudD4NCiAgICAgICAgPGlu Z3JlZGllbnQ+DQogICAgICAgICAgPGl0ZW1Db2RlYWJsZUNvbmNlcHQ+DQogICAgICAgICAgICA8 Y29kaW5nPg0KICAgICAgICAgICAgICA8c3lzdGVtIHZhbHVlPSJodHRwOi8vZmhpci5kZS9Db2Rl U3lzdGVtL2FzayIgLz4NCiAgICAgICAgICAgICAgPGNvZGUgdmFsdWU9IkR1bW15LUFTSyIgLz4N CiAgICAgICAgICAgIDwvY29kaW5nPg0KICAgICAgICAgICAgPHRleHQgdmFsdWU9IklidXByb2Zl biIgLz4NCiAgICAgICAgICA8L2l0ZW1Db2RlYWJsZUNvbmNlcHQ+DQogICAgICAgICAgPHN0cmVu Z3RoPg0KICAgICAgICAgICAgPG51bWVyYXRvcj4NCiAgICAgICAgICAgICAgPHZhbHVlIHZhbHVl PSI4MDAiIC8+DQogICAgICAgICAgICAgIDx1bml0IHZhbHVlPSJtZyIgLz4NCiAgICAgICAgICAg IDwvbnVtZXJhdG9yPg0KICAgICAgICAgICAgPGRlbm9taW5hdG9yPg0KICAgICAgICAgICAgICA8 dmFsdWUgdmFsdWU9IjEiIC8+DQogICAgICAgICAgICA8L2Rlbm9taW5hdG9yPg0KICAgICAgICAg IDwvc3RyZW5ndGg+DQogICAgICAgIDwvaW5ncmVkaWVudD4NCiAgICAgIDwvTWVkaWNhdGlvbj4N CiAgICA8L3Jlc291cmNlPg0KICA8L2VudHJ5Pg0KICA8ZW50cnk+DQogICAgPGZ1bGxVcmwgdmFs dWU9Imh0dHA6Ly9wdnMucHJheGlzLXRvcHAtZ2x1ZWNrbGljaC5sb2NhbC9maGlyL1BhdGllbnQv OTc3NGY2N2YtYTIzOC00ZGFmLWI0ZTYtNjc5ZGVlZWYzODExIiAvPg0KICAgIDxyZXNvdXJjZT4N CiAgICAgIDxQYXRpZW50IHhtbG5zPSJodHRwOi8vaGw3Lm9yZy9maGlyIj4NCiAgICAgICAgPGlk IHZhbHVlPSI5Nzc0ZjY3Zi1hMjM4LTRkYWYtYjRlNi02NzlkZWVlZjM4MTEiIC8+DQogICAgICAg IDxtZXRhPg0KICAgICAgICAgIDxwcm9maWxlIHZhbHVlPSJodHRwczovL2ZoaXIua2J2LmRlL1N0 cnVjdHVyZURlZmluaXRpb24vS0JWX1BSX0ZPUl9QYXRpZW50fDEuMC4zIiAvPg0KICAgICAgICA8 L21ldGE+DQogICAgICAgIDxpZGVudGlmaWVyPg0KICAgICAgICAgIDx0eXBlPg0KICAgICAgICAg ICAgPGNvZGluZz4NCiAgICAgICAgICAgICAgPHN5c3RlbSB2YWx1ZT0iaHR0cDovL2ZoaXIuZGUv Q29kZVN5c3RlbS9pZGVudGlmaWVyLXR5cGUtZGUtYmFzaXMiIC8+DQogICAgICAgICAgICAgIDxj b2RlIHZhbHVlPSJHS1YiIC8+DQogICAgICAgICAgICA8L2NvZGluZz4NCiAgICAgICAgICA8L3R5 cGU+DQogICAgICAgICAgPHN5c3RlbSB2YWx1ZT0iaHR0cDovL2ZoaXIuZGUvTmFtaW5nU3lzdGVt L2drdi9rdmlkLTEwIiAvPg0KICAgICAgICAgIDx2YWx1ZSB2YWx1ZT0iWDIzNDU2Nzg5MCIgLz4N CiAgICAgICAgPC9pZGVudGlmaWVyPg0KICAgICAgICA8bmFtZT4NCiAgICAgICAgICA8dXNlIHZh bHVlPSJvZmZpY2lhbCIgLz4NCiAgICAgICAgICA8ZmFtaWx5IHZhbHVlPSJMdWRnZXIgS8O2bmln c3N0ZWluIj4NCiAgICAgICAgICAgIDxleHRlbnNpb24gdXJsPSJodHRwOi8vaGw3Lm9yZy9maGly L1N0cnVjdHVyZURlZmluaXRpb24vaHVtYW5uYW1lLW93bi1uYW1lIj4NCiAgICAgICAgICAgICAg PHZhbHVlU3RyaW5nIHZhbHVlPSJLw7ZuaWdzc3RlaW4iIC8+DQogICAgICAgICAgICA8L2V4dGVu c2lvbj4NCiAgICAgICAgICA8L2ZhbWlseT4NCiAgICAgICAgICA8Z2l2ZW4gdmFsdWU9Ikx1ZGdl ciIgLz4NCiAgICAgICAgPC9uYW1lPg0KICAgICAgICA8YmlydGhEYXRlIHZhbHVlPSIxOTM1LTA2 LTIyIiAvPg0KICAgICAgICA8YWRkcmVzcz4NCiAgICAgICAgICA8dHlwZSB2YWx1ZT0iYm90aCIg Lz4NCiAgICAgICAgICA8bGluZSB2YWx1ZT0iTXVzdGVyc3RyLiAxIj4NCiAgICAgICAgICAgIDxl eHRlbnNpb24gdXJsPSJodHRwOi8vaGw3Lm9yZy9maGlyL1N0cnVjdHVyZURlZmluaXRpb24vaXNv MjEwOTAtQURYUC1ob3VzZU51bWJlciI+DQogICAgICAgICAgICAgIDx2YWx1ZVN0cmluZyB2YWx1 ZT0iMSIgLz4NCiAgICAgICAgICAgIDwvZXh0ZW5zaW9uPg0KICAgICAgICAgICAgPGV4dGVuc2lv biB1cmw9Imh0dHA6Ly9obDcub3JnL2ZoaXIvU3RydWN0dXJlRGVmaW5pdGlvbi9pc28yMTA5MC1B RFhQLXN0cmVldE5hbWUiPg0KICAgICAgICAgICAgICA8dmFsdWVTdHJpbmcgdmFsdWU9Ik11c3Rl cnN0ci4iIC8+DQogICAgICAgICAgICA8L2V4dGVuc2lvbj4NCiAgICAgICAgICA8L2xpbmU+DQog ICAgICAgICAgPGNpdHkgdmFsdWU9IkJlcmxpbiIgLz4NCiAgICAgICAgICA8cG9zdGFsQ29kZSB2 YWx1ZT0iMTA2MjMiIC8+DQogICAgICAgIDwvYWRkcmVzcz4NCiAgICAgIDwvUGF0aWVudD4NCiAg ICA8L3Jlc291cmNlPg0KICA8L2VudHJ5Pg0KICA8ZW50cnk+DQogICAgPGZ1bGxVcmwgdmFsdWU9 Imh0dHA6Ly9wdnMucHJheGlzLXRvcHAtZ2x1ZWNrbGljaC5sb2NhbC9maGlyL1ByYWN0aXRpb25l ci8yMDU5N2UwZS1jYjJhLTQ1YjMtOTVmMC1kYzNkYmRiNjE3YzMiIC8+DQogICAgPHJlc291cmNl Pg0KICAgICAgPFByYWN0aXRpb25lciB4bWxucz0iaHR0cDovL2hsNy5vcmcvZmhpciI+DQogICAg ICAgIDxpZCB2YWx1ZT0iMjA1OTdlMGUtY2IyYS00NWIzLTk1ZjAtZGMzZGJkYjYxN2MzIiAvPg0K ICAgICAgICA8bWV0YT4NCiAgICAgICAgICA8cHJvZmlsZSB2YWx1ZT0iaHR0cHM6Ly9maGlyLmti di5kZS9TdHJ1Y3R1cmVEZWZpbml0aW9uL0tCVl9QUl9GT1JfUHJhY3RpdGlvbmVyfDEuMC4zIiAv Pg0KICAgICAgICA8L21ldGE+DQogICAgICAgIDxpZGVudGlmaWVyPg0KICAgICAgICAgIDx0eXBl Pg0KICAgICAgICAgICAgPGNvZGluZz4NCiAgICAgICAgICAgICAgPHN5c3RlbSB2YWx1ZT0iaHR0 cDovL3Rlcm1pbm9sb2d5LmhsNy5vcmcvQ29kZVN5c3RlbS92Mi0wMjAzIiAvPg0KICAgICAgICAg ICAgICA8Y29kZSB2YWx1ZT0iTEFOUiIgLz4NCiAgICAgICAgICAgIDwvY29kaW5nPg0KICAgICAg ICAgIDwvdHlwZT4NCiAgICAgICAgICA8c3lzdGVtIHZhbHVlPSJodHRwczovL2ZoaXIua2J2LmRl L05hbWluZ1N5c3RlbS9LQlZfTlNfQmFzZV9BTlIiIC8+DQogICAgICAgICAgPHZhbHVlIHZhbHVl PSI4MzgzODIyMDIiIC8+DQogICAgICAgIDwvaWRlbnRpZmllcj4NCiAgICAgICAgPG5hbWU+DQog ICAgICAgICAgPHVzZSB2YWx1ZT0ib2ZmaWNpYWwiIC8+DQogICAgICAgICAgPGZhbWlseSB2YWx1 ZT0iVG9wcC1HbMO8Y2tsaWNoIj4NCiAgICAgICAgICAgIDxleHRlbnNpb24gdXJsPSJodHRwOi8v aGw3Lm9yZy9maGlyL1N0cnVjdHVyZURlZmluaXRpb24vaHVtYW5uYW1lLW93bi1uYW1lIj4NCiAg ICAgICAgICAgICAgPHZhbHVlU3RyaW5nIHZhbHVlPSJUb3BwLUdsw7xja2xpY2giIC8+DQogICAg ICAgICAgICA8L2V4dGVuc2lvbj4NCiAgICAgICAgICA8L2ZhbWlseT4NCiAgICAgICAgICA8Z2l2 ZW4gdmFsdWU9IkhhbnMiIC8+DQogICAgICAgICAgPHByZWZpeCB2YWx1ZT0iRHIuIG1lZC4iPg0K ICAgICAgICAgICAgPGV4dGVuc2lvbiB1cmw9Imh0dHA6Ly9obDcub3JnL2ZoaXIvU3RydWN0dXJl RGVmaW5pdGlvbi9pc28yMTA5MC1FTi1xdWFsaWZpZXIiPg0KICAgICAgICAgICAgICA8dmFsdWVD b2RlIHZhbHVlPSJBQyIgLz4NCiAgICAgICAgICAgIDwvZXh0ZW5zaW9uPg0KICAgICAgICAgIDwv cHJlZml4Pg0KICAgICAgICA8L25hbWU+DQogICAgICAgIDxxdWFsaWZpY2F0aW9uPg0KICAgICAg ICAgIDxjb2RlPg0KICAgICAgICAgICAgPGNvZGluZz4NCiAgICAgICAgICAgICAgPHN5c3RlbSB2 YWx1ZT0iaHR0cHM6Ly9maGlyLmtidi5kZS9Db2RlU3lzdGVtL0tCVl9DU19GT1JfUXVhbGlmaWNh dGlvbl9UeXBlIiAvPg0KICAgICAgICAgICAgICA8Y29kZSB2YWx1ZT0iMDAiIC8+DQogICAgICAg ICAgICA8L2NvZGluZz4NCiAgICAgICAgICA8L2NvZGU+DQogICAgICAgIDwvcXVhbGlmaWNhdGlv bj4NCiAgICAgICAgPHF1YWxpZmljYXRpb24+DQogICAgICAgICAgPGNvZGU+DQogICAgICAgICAg ICA8dGV4dCB2YWx1ZT0iSGF1c2FyenQiIC8+DQogICAgICAgICAgPC9jb2RlPg0KICAgICAgICA8 L3F1YWxpZmljYXRpb24+DQogICAgICA8L1ByYWN0aXRpb25lcj4NCiAgICA8L3Jlc291cmNlPg0K ICA8L2VudHJ5Pg0KICA8ZW50cnk+DQogICAgPGZ1bGxVcmwgdmFsdWU9Imh0dHA6Ly9wdnMucHJh eGlzLXRvcHAtZ2x1ZWNrbGljaC5sb2NhbC9maGlyL1ByYWN0aXRpb25lci9kODQ2M2RhZi0yNThl LTRjYWQtYTg2YS02ZmQ0MmZhYzE2MWMiIC8+DQogICAgPHJlc291cmNlPg0KICAgICAgPFByYWN0 aXRpb25lciB4bWxucz0iaHR0cDovL2hsNy5vcmcvZmhpciI+DQogICAgICAgIDxpZCB2YWx1ZT0i ZDg0NjNkYWYtMjU4ZS00Y2FkLWE4NmEtNmZkNDJmYWMxNjFjIiAvPg0KICAgICAgICA8bWV0YT4N CiAgICAgICAgICA8cHJvZmlsZSB2YWx1ZT0iaHR0cHM6Ly9maGlyLmtidi5kZS9TdHJ1Y3R1cmVE ZWZpbml0aW9uL0tCVl9QUl9GT1JfUHJhY3RpdGlvbmVyfDEuMC4zIiAvPg0KICAgICAgICA8L21l dGE+DQogICAgICAgIDxpZGVudGlmaWVyPg0KICAgICAgICAgIDx0eXBlPg0KICAgICAgICAgICAg PGNvZGluZz4NCiAgICAgICAgICAgICAgPHN5c3RlbSB2YWx1ZT0iaHR0cDovL3Rlcm1pbm9sb2d5 LmhsNy5vcmcvQ29kZVN5c3RlbS92Mi0wMjAzIiAvPg0KICAgICAgICAgICAgICA8Y29kZSB2YWx1 ZT0iTEFOUiIgLz4NCiAgICAgICAgICAgIDwvY29kaW5nPg0KICAgICAgICAgIDwvdHlwZT4NCiAg ICAgICAgICA8c3lzdGVtIHZhbHVlPSJodHRwczovL2ZoaXIua2J2LmRlL05hbWluZ1N5c3RlbS9L QlZfTlNfQmFzZV9BTlIiIC8+DQogICAgICAgICAgPHZhbHVlIHZhbHVlPSI4MzgzODIyMTAiIC8+ DQogICAgICAgIDwvaWRlbnRpZmllcj4NCiAgICAgICAgPG5hbWU+DQogICAgICAgICAgPHVzZSB2 YWx1ZT0ib2ZmaWNpYWwiIC8+DQogICAgICAgICAgPGZhbWlseSB2YWx1ZT0iTWVpZXIiPg0KICAg ICAgICAgICAgPGV4dGVuc2lvbiB1cmw9Imh0dHA6Ly9obDcub3JnL2ZoaXIvU3RydWN0dXJlRGVm aW5pdGlvbi9odW1hbm5hbWUtb3duLW5hbWUiPg0KICAgICAgICAgICAgICA8dmFsdWVTdHJpbmcg dmFsdWU9Ik1laWVyIiAvPg0KICAgICAgICAgICAgPC9leHRlbnNpb24+DQogICAgICAgICAgPC9m YW1pbHk+DQogICAgICAgICAgPGdpdmVuIHZhbHVlPSJKw7ZyZ2VuIiAvPg0KICAgICAgICA8L25h bWU+DQogICAgICAgIDxxdWFsaWZpY2F0aW9uPg0KICAgICAgICAgIDxjb2RlPg0KICAgICAgICAg ICAgPGNvZGluZz4NCiAgICAgICAgICAgICAgPHN5c3RlbSB2YWx1ZT0iaHR0cHM6Ly9maGlyLmti di5kZS9Db2RlU3lzdGVtL0tCVl9DU19GT1JfUXVhbGlmaWNhdGlvbl9UeXBlIiAvPg0KICAgICAg ICAgICAgICA8Y29kZSB2YWx1ZT0iMDMiIC8+DQogICAgICAgICAgICA8L2NvZGluZz4NCiAgICAg ICAgICA8L2NvZGU+DQogICAgICAgIDwvcXVhbGlmaWNhdGlvbj4NCiAgICAgICAgPHF1YWxpZmlj YXRpb24+DQogICAgICAgICAgPGNvZGU+DQogICAgICAgICAgICA8dGV4dCB2YWx1ZT0iQXJ6dCBp biBXZWl0ZXJiaWxkdW5nIiAvPg0KICAgICAgICAgIDwvY29kZT4NCiAgICAgICAgPC9xdWFsaWZp Y2F0aW9uPg0KICAgICAgPC9QcmFjdGl0aW9uZXI+DQogICAgPC9yZXNvdXJjZT4NCiAgPC9lbnRy eT4NCiAgPGVudHJ5Pg0KICAgIDxmdWxsVXJsIHZhbHVlPSJodHRwOi8vcHZzLnByYXhpcy10b3Bw LWdsdWVja2xpY2gubG9jYWwvZmhpci9Pcmdhbml6YXRpb24vY2YwNDJlNDQtMDg2YS00ZDUxLTlj NzctMTcyZjlhOTcyZTNiIiAvPg0KICAgIDxyZXNvdXJjZT4NCiAgICAgIDxPcmdhbml6YXRpb24g eG1sbnM9Imh0dHA6Ly9obDcub3JnL2ZoaXIiPg0KICAgICAgICA8aWQgdmFsdWU9ImNmMDQyZTQ0 LTA4NmEtNGQ1MS05Yzc3LTE3MmY5YTk3MmUzYiIgLz4NCiAgICAgICAgPG1ldGE+DQogICAgICAg ICAgPHByb2ZpbGUgdmFsdWU9Imh0dHBzOi8vZmhpci5rYnYuZGUvU3RydWN0dXJlRGVmaW5pdGlv bi9LQlZfUFJfRk9SX09yZ2FuaXphdGlvbnwxLjAuMyIgLz4NCiAgICAgICAgPC9tZXRhPg0KICAg ICAgICA8aWRlbnRpZmllcj4NCiAgICAgICAgICA8dHlwZT4NCiAgICAgICAgICAgIDxjb2Rpbmc+ DQogICAgICAgICAgICAgIDxzeXN0ZW0gdmFsdWU9Imh0dHA6Ly90ZXJtaW5vbG9neS5obDcub3Jn L0NvZGVTeXN0ZW0vdjItMDIwMyIgLz4NCiAgICAgICAgICAgICAgPGNvZGUgdmFsdWU9IkJTTlIi IC8+DQogICAgICAgICAgICA8L2NvZGluZz4NCiAgICAgICAgICA8L3R5cGU+DQogICAgICAgICAg PHN5c3RlbSB2YWx1ZT0iaHR0cHM6Ly9maGlyLmtidi5kZS9OYW1pbmdTeXN0ZW0vS0JWX05TX0Jh c2VfQlNOUiIgLz4NCiAgICAgICAgICA8dmFsdWUgdmFsdWU9IjAzMTIzNDU2NyIgLz4NCiAgICAg ICAgPC9pZGVudGlmaWVyPg0KICAgICAgICA8bmFtZSB2YWx1ZT0iSGF1c2FyenRwcmF4aXMgRHIu IFRvcHAtR2zDvGNrbGljaCIgLz4NCiAgICAgICAgPHRlbGVjb20+DQogICAgICAgICAgPHN5c3Rl bSB2YWx1ZT0icGhvbmUiIC8+DQogICAgICAgICAgPHZhbHVlIHZhbHVlPSIwMzAxMjM0NTY3IiAv Pg0KICAgICAgICA8L3RlbGVjb20+DQogICAgICAgIDxhZGRyZXNzPg0KICAgICAgICAgIDx0eXBl IHZhbHVlPSJib3RoIiAvPg0KICAgICAgICAgIDxsaW5lIHZhbHVlPSJNdXN0ZXJzdHIuIDIiPg0K ICAgICAgICAgICAgPGV4dGVuc2lvbiB1cmw9Imh0dHA6Ly9obDcub3JnL2ZoaXIvU3RydWN0dXJl RGVmaW5pdGlvbi9pc28yMTA5MC1BRFhQLWhvdXNlTnVtYmVyIj4NCiAgICAgICAgICAgICAgPHZh bHVlU3RyaW5nIHZhbHVlPSIyIiAvPg0KICAgICAgICAgICAgPC9leHRlbnNpb24+DQogICAgICAg ICAgICA8ZXh0ZW5zaW9uIHVybD0iaHR0cDovL2hsNy5vcmcvZmhpci9TdHJ1Y3R1cmVEZWZpbml0 aW9uL2lzbzIxMDkwLUFEWFAtc3RyZWV0TmFtZSI+DQogICAgICAgICAgICAgIDx2YWx1ZVN0cmlu ZyB2YWx1ZT0iTXVzdGVyc3RyLiIgLz4NCiAgICAgICAgICAgIDwvZXh0ZW5zaW9uPg0KICAgICAg ICAgIDwvbGluZT4NCiAgICAgICAgICA8Y2l0eSB2YWx1ZT0iQmVybGluIiAvPg0KICAgICAgICAg IDxwb3N0YWxDb2RlIHZhbHVlPSIxMDYyMyIgLz4NCiAgICAgICAgPC9hZGRyZXNzPg0KICAgICAg PC9Pcmdhbml6YXRpb24+DQogICAgPC9yZXNvdXJjZT4NCiAgPC9lbnRyeT4NCiAgPGVudHJ5Pg0K ICAgIDxmdWxsVXJsIHZhbHVlPSJodHRwOi8vcHZzLnByYXhpcy10b3BwLWdsdWVja2xpY2gubG9j YWwvZmhpci9Db3ZlcmFnZS8xYjFmZmI2ZS1lYjA1LTQzZDctODdlYi1lNzgxOGZlOTY2MWEiIC8+ DQogICAgPHJlc291cmNlPg0KICAgICAgPENvdmVyYWdlIHhtbG5zPSJodHRwOi8vaGw3Lm9yZy9m aGlyIj4NCiAgICAgICAgPGlkIHZhbHVlPSIxYjFmZmI2ZS1lYjA1LTQzZDctODdlYi1lNzgxOGZl OTY2MWEiIC8+DQogICAgICAgIDxtZXRhPg0KICAgICAgICAgIDxwcm9maWxlIHZhbHVlPSJodHRw czovL2ZoaXIua2J2LmRlL1N0cnVjdHVyZURlZmluaXRpb24vS0JWX1BSX0ZPUl9Db3ZlcmFnZXwx LjAuMyIgLz4NCiAgICAgICAgPC9tZXRhPg0KICAgICAgICA8ZXh0ZW5zaW9uIHVybD0iaHR0cDov L2ZoaXIuZGUvU3RydWN0dXJlRGVmaW5pdGlvbi9na3YvYmVzb25kZXJlLXBlcnNvbmVuZ3J1cHBl Ij4NCiAgICAgICAgICA8dmFsdWVDb2Rpbmc+DQogICAgICAgICAgICA8c3lzdGVtIHZhbHVlPSJo dHRwczovL2ZoaXIua2J2LmRlL0NvZGVTeXN0ZW0vS0JWX0NTX1NGSElSX0tCVl9QRVJTT05FTkdS VVBQRSIgLz4NCiAgICAgICAgICAgIDxjb2RlIHZhbHVlPSIwMCIgLz4NCiAgICAgICAgICA8L3Zh bHVlQ29kaW5nPg0KICAgICAgICA8L2V4dGVuc2lvbj4NCiAgICAgICAgPGV4dGVuc2lvbiB1cmw9 Imh0dHA6Ly9maGlyLmRlL1N0cnVjdHVyZURlZmluaXRpb24vZ2t2L2RtcC1rZW5uemVpY2hlbiI+ DQogICAgICAgICAgPHZhbHVlQ29kaW5nPg0KICAgICAgICAgICAgPHN5c3RlbSB2YWx1ZT0iaHR0 cHM6Ly9maGlyLmtidi5kZS9Db2RlU3lzdGVtL0tCVl9DU19TRkhJUl9LQlZfRE1QIiAvPg0KICAg ICAgICAgICAgPGNvZGUgdmFsdWU9IjAwIiAvPg0KICAgICAgICAgIDwvdmFsdWVDb2Rpbmc+DQog ICAgICAgIDwvZXh0ZW5zaW9uPg0KICAgICAgICA8ZXh0ZW5zaW9uIHVybD0iaHR0cDovL2ZoaXIu ZGUvU3RydWN0dXJlRGVmaW5pdGlvbi9na3Yvd29wIj4NCiAgICAgICAgICA8dmFsdWVDb2Rpbmc+ DQogICAgICAgICAgICA8c3lzdGVtIHZhbHVlPSJodHRwczovL2ZoaXIua2J2LmRlL0NvZGVTeXN0 ZW0vS0JWX0NTX1NGSElSX0lUQV9XT1AiIC8+DQogICAgICAgICAgICA8Y29kZSB2YWx1ZT0iMDMi IC8+DQogICAgICAgICAgPC92YWx1ZUNvZGluZz4NCiAgICAgICAgPC9leHRlbnNpb24+DQogICAg ICAgIDxleHRlbnNpb24gdXJsPSJodHRwOi8vZmhpci5kZS9TdHJ1Y3R1cmVEZWZpbml0aW9uL2dr di92ZXJzaWNoZXJ0ZW5hcnQiPg0KICAgICAgICAgIDx2YWx1ZUNvZGluZz4NCiAgICAgICAgICAg IDxzeXN0ZW0gdmFsdWU9Imh0dHBzOi8vZmhpci5rYnYuZGUvQ29kZVN5c3RlbS9LQlZfQ1NfU0ZI SVJfS0JWX1ZFUlNJQ0hFUlRFTlNUQVRVUyIgLz4NCiAgICAgICAgICAgIDxjb2RlIHZhbHVlPSIx IiAvPg0KICAgICAgICAgIDwvdmFsdWVDb2Rpbmc+DQogICAgICAgIDwvZXh0ZW5zaW9uPg0KICAg ICAgICA8c3RhdHVzIHZhbHVlPSJhY3RpdmUiIC8+DQogICAgICAgIDx0eXBlPg0KICAgICAgICAg IDxjb2Rpbmc+DQogICAgICAgICAgICA8c3lzdGVtIHZhbHVlPSJodHRwOi8vZmhpci5kZS9Db2Rl U3lzdGVtL3ZlcnNpY2hlcnVuZ3NhcnQtZGUtYmFzaXMiIC8+DQogICAgICAgICAgICA8Y29kZSB2 YWx1ZT0iR0tWIiAvPg0KICAgICAgICAgIDwvY29kaW5nPg0KICAgICAgICA8L3R5cGU+DQogICAg ICAgIDxiZW5lZmljaWFyeT4NCiAgICAgICAgICA8cmVmZXJlbmNlIHZhbHVlPSJQYXRpZW50Lzk3 NzRmNjdmLWEyMzgtNGRhZi1iNGU2LTY3OWRlZWVmMzgxMSIgLz4NCiAgICAgICAgPC9iZW5lZmlj aWFyeT4NCiAgICAgICAgPHBheW9yPg0KICAgICAgICAgIDxpZGVudGlmaWVyPg0KICAgICAgICAg ICAgPHN5c3RlbSB2YWx1ZT0iaHR0cDovL2ZoaXIuZGUvTmFtaW5nU3lzdGVtL2FyZ2UtaWsvaWtu ciIgLz4NCiAgICAgICAgICAgIDx2YWx1ZSB2YWx1ZT0iMTA0MjEyMDU5IiAvPg0KICAgICAgICAg IDwvaWRlbnRpZmllcj4NCiAgICAgICAgICA8ZGlzcGxheSB2YWx1ZT0iQU9LIFJoZWlubGFuZC9I YW1idXJnIiAvPg0KICAgICAgICA8L3BheW9yPg0KICAgICAgPC9Db3ZlcmFnZT4NCiAgICA8L3Jl c291cmNlPg0KICA8L2VudHJ5Pg0KPC9CdW5kbGU+oIIEwTCCBL0wggOloAMCAQICBwJBwffTq9gw DQYJKoZIhvcNAQELBQAwUDELMAkGA1UEBhMCREUxHzAdBgNVBAoMFmdlbWF0aWsgR21iSCBOT1Qt VkFMSUQxIDAeBgNVBAMMF0dFTS5IQkEtcUNBMjQgVEVTVC1PTkxZMB4XDTE4MTEwNTAwMDAwMFoX DTIzMTEwNDIzNTk1OVoweDEfMB0GA1UEAwwWU2FtIFNjaHJhw59lclRFU1QtT05MWTEVMBMGA1UE KgwMU2FtIEZyZWloZXJyMRIwEAYDVQQEDAlTY2hyYcOfZXIxHTAbBgNVBAUTFDgwMjc2ODgzMTEw MDAwMDk1NzY3MQswCQYDVQQGEwJERTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAIjH tUOCYpiywQU20DMmvw9K4HmynW5l9ZkBJtFqPAJ0q8MqAcp4blNoRSng2wc7YZGWVsGMRaGqz9y7 hDf1OojNl+R57MNfzanWoyjCyyk3KdugWoIUFxFQ0stSDbD0JTSzip7mMEkQH7GeUg3deIkPksih vOpJMizQnYdDds8coLZ7mbcGueUBS7udVGde+vwyK5o2d/q5TljUINSareFr0OHq9ySgKQavZHy7 VpTxPe7MAhvq+xpapZDvJODJ9YQiSj6xMqEPTWD7pa1SA4iH+TYZJxX9H4YuwLhGut8mVqCyUo06 DsfAi+GFh4l49SunT2whBWxVZtJW625il+MCAwEAAaOCAXIwggFuMB0GA1UdDgQWBBS+1xJ1Qaz1 Rp96GAR2QEa3mH4TWjAMBgNVHRMBAf8EAjAAMBsGCSsGAQQBwG0DBQQOMAwGCisGAQQBwG0DBQEw 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 Qfo=</span>
<span id="cb2-32"><a href="#cb2-32" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb2-33"><a href="#cb2-33" aria-hidden="true" tabindex="-1"></a>                &lt;/<span class="kw">m2:Base64Signature</span>&gt;</span>
<span id="cb2-34"><a href="#cb2-34" aria-hidden="true" tabindex="-1"></a>            &lt;/<span class="kw">m2:SignatureObject</span>&gt;</span>
<span id="cb2-35"><a href="#cb2-35" aria-hidden="true" tabindex="-1"></a>            &lt;<span class="kw">m:IncludeRevocationInfo</span>&gt;false&lt;/<span class="kw">m:IncludeRevocationInfo</span>&gt;</span>
<span id="cb2-36"><a href="#cb2-36" aria-hidden="true" tabindex="-1"></a>        &lt;/<span class="kw">m:VerifyDocument</span>&gt;</span>
<span id="cb2-37"><a href="#cb2-37" aria-hidden="true" tabindex="-1"></a>    &lt;/<span class="kw">SOAP-ENV:Body</span>&gt;</span>
<span id="cb2-38"><a href="#cb2-38" aria-hidden="true" tabindex="-1"></a>&lt;/<span class="kw">SOAP-ENV:Envelope</span>&gt;</span></code></pre></div>
<div class="note">
<p>Das Element
`&lt;m2:Base64Signature&gt;&lt;/m2:Base64Signature&gt;`enthält das
Signaturelement inkl. des signierten E-Rezept-Datensatzes
(CAdES-enveloping) als PKCS#7-Datei in Base64-Codierung</p>
</div>
<div class="note">
<p>Mit dem Attribut
<code>&lt;m:IncludeRevocationInfo&gt;true&lt;/m:IncludeRevocationInfo&gt;</code>
wird der Konnektor angewiesen, die in der Signaturprüfung verwendete
(eingebettete und zum Referenzzeitpunkt gültige ODER neu eingeholte,
weil entweder nicht eingebettet oder zum Referenz-Zeitpunkt ungültige)
OCSP-Response im Prüfergebnis <em>verifyDocumentResponse</em> an das
aufrufende System ebenfalls zurückzugeben. Ist
<code>IncludeRevocationInfo</code> auf <code>false</code> gesetzt, wird
der OCSP-Response nicht zurückgegeben.</p>
</div></td>
</tr>
</tbody>
</table>

Der Inhalt der Base64-codierten Signatur findet sich im Unterordner der
[Beispiele](../samples/qes/signed) in der Datei
`4fe2013d-ae94-441a-a1b1-78236ae65680_S_SECUN_secu_kon_4.8.2_4.1.3.p7`
und kann mit einem ASN.1-Viewer eingesehen werden.

Im Verzeichnis der [Beispiele](../samples/qes/signed) sind alle
Kreuzkombinationen der verschiedenen Konnektorhersteller für
Signaturerstellung und -Prüfung enthalten. Hier dargestellt ist die
Prüfung durch eine Koco-Box einer durch einen Secunet-Konnektor
erstellten QES in
`4fe2013d-ae94-441a-a1b1-78236ae65680_S_SECUN_secu_kon_4.8.2_4.1.3_V_KOCOC_kocobox_3.6.0_2.3.24_req.xml`.

Im Verzeichnis
[HBA-gueltig-bis-24.4.2021](../samples/qes-cases/HBA-gueltig-bis-24.4.2021)
gibt es weitere Beispiele, wie die Signatur und Signaturprüfung
aussieht, wenn ein HBA kurz vor dem Ablauf seiner kryptografischen
Gültigkeit verwendet wurde.

**Response**

    HTTP/1.1 200 OK
    Content-Type: text/xml;charset=utf-8

    <?xml version="1.0"?>
    <S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/">
        <S:Body>
            <ns7:VerifyDocumentResponse xmlns:ns2="http://ws.gematik.de/conn/CertificateServiceCommon/v2.0"
                xmlns:ns3="http://www.w3.org/2001/04/xmlenc#"
                xmlns:ns4="http://www.w3.org/2000/09/xmldsig#"
                xmlns:ns5="http://ws.gematik.de/conn/ConnectorCommon/v5.0"
                xmlns:ns6="http://uri.etsi.org/01903/v1.3.2#"
                xmlns:ns7="http://ws.gematik.de/conn/SignatureService/v7.4"
                xmlns:ns8="http://ws.gematik.de/conn/ConnectorContext/v2.0"
                xmlns:ns9="urn:oasis:names:tc:dss:1.0:core:schema"
                xmlns:ns10="urn:oasis:names:tc:dss-x:1.0:profiles:SignaturePolicy:schema#"
                xmlns:ns11="http://ws.gematik.de/tel/error/v2.0"
                xmlns:ns12="urn:oasis:names:tc:dss-x:1.0:profiles:verificationreport:schema#"
                xmlns:ns13="http://uri.etsi.org/02231/v2#"
                xmlns:ns14="urn:oasis:names:tc:SAML:2.0:assertion"
                xmlns:ns15="urn:oasis:names:tc:SAML:1.0:assertion">
                <ns5:Status>
                    <ns5:Result>Warning</ns5:Result>
                    <ns11:Error>
                        <ns11:MessageID>5615aa5c-e52e-4eab-ad12-69d175d22d1a</ns11:MessageID>
                        <ns11:Timestamp>2021-04-15T11:12:26.228Z</ns11:Timestamp>
                        <ns11:Trace>
                            <ns11:EventID>31b833a2-621e-4e98-88cf-cae7ab3225fa</ns11:EventID>
                            <ns11:Instance>Konnektor-Lokal</ns11:Instance>
                            <ns11:LogReference>31b833a2-621e-4e98-88cf-cae7ab3225fa</ns11:LogReference>
                            <ns11:CompType>Konnektor:PKI</ns11:CompType>
                            <ns11:Code>1050</ns11:Code>
                            <ns11:Severity>Warning</ns11:Severity>
                            <ns11:ErrorType>Technical</ns11:ErrorType>
                            <ns11:ErrorText>Die einem TUC zur Zertifikatsprüfung beigefügte OCSP-Response zu dem zu prüfenden Zertifikat kann nicht erfolgreich gegen das Zertifikat validiert werden.</ns11:ErrorText>
                            <ns11:Detail Encoding="UTF-8">Mitgelieferte Response konnte nicht verwendet werden. Die OCSP-Response enthält eine Exception-Meldung.</ns11:Detail>
                        </ns11:Trace>
                    </ns11:Error>
                </ns5:Status>
                <ns7:VerificationResult>
                    <ns7:HighLevelResult>INCONCLUSIVE</ns7:HighLevelResult>
                    <ns7:TimestampType>USER_DEFINED_TIMESTAMP</ns7:TimestampType>
                    <ns7:Timestamp>2021-04-15T11:12:26.101Z</ns7:Timestamp>
                </ns7:VerificationResult>
                <ns7:OptionalOutputs>
                    <ns12:VerificationReport>
                        <ns9:VerificationTimeInfo>
                            <ns9:VerificationTime>2021-04-15T11:12:26.101Z</ns9:VerificationTime>
                        </ns9:VerificationTimeInfo>
                        <ns12:IndividualReport>
                            <ns12:SignedObjectIdentifier>
                                <ns12:SignedProperties>
                                    <ns12:SignedSignatureProperties>
                                        <ns6:SigningTime>2021-04-14T17:14:02.000Z</ns6:SigningTime>
                                    </ns12:SignedSignatureProperties>
                                    <ns12:Other>
                                        <ns7:ReferenceToSignerCertificate>true</ns7:ReferenceToSignerCertificate>
                                        <ns7:ShortText>a CMSDocument2sign</ns7:ShortText>
                                    </ns12:Other>
                                </ns12:SignedProperties>
                                <ns4:SignatureValue Id="SigRef-000046-001">gMVBhMueikIDcBVvWzg5orgR4hIFa83gsSxr+0n1SXOi8kF9PSGCE9K22o5nR4QA9s9vQ6I2itk1MVmdlRSaQ4pzghbh+fS0R8thpe+Sb/1Se12xIdNfYwvaj/7rVjXJdCOdjMZ4ewNoGVx/sStUvSHNBQNjKPOLoAgi5mKBhxfSfgYBmj4VBiz+Bsp9VVQGaYJm/RKNDDhyfmPnsyAaA2go4tgvE+Pbo34FitE9L4MP9NzMCK1aXKoInXFeRuWXU01oF9tomRMSgebKBiQas2hI453qNrGuqFctFT0UDYEVFy6XUIJK/KdMd990yW565i1w5M7HNWdkMpJystdB+g==</ns4:SignatureValue>
                            </ns12:SignedObjectIdentifier>
                            <ns9:Result>
                                <ns9:ResultMajor>urn:oasis:names:tc:dss:1.0:resultmajor:Success</ns9:ResultMajor>
                                <ns9:ResultMinor>urn:oasis:names:tc:dss:1.0:resultminor:valid:signature:OnAllDocuments</ns9:ResultMinor>
                            </ns9:Result>
                            <ns12:Details>
                                <ns12:DetailedSignatureReport>
                                    <ns12:FormatOK>
                                        <ns12:ResultMajor>urn:oasis:names:tc:dss:1.0:detail:valid</ns12:ResultMajor>
                                    </ns12:FormatOK>
                                    <ns12:SignatureOK>
                                        <ns12:SigMathOK>
                                            <ns12:ResultMajor>urn:oasis:names:tc:dss:1.0:detail:valid</ns12:ResultMajor>
                                        </ns12:SigMathOK>
                                        <ns12:SignatureAlgorithm>
                                            <ns12:Algorithm>http://www.w3.org/2007/05/xmldsig-more#rsa-pss</ns12:Algorithm>
                                            <ns12:Suitability>
                                                <ns12:ResultMajor>urn:oasis:names:tc:dss:1.0:detail:valid</ns12:ResultMajor>
                                            </ns12:Suitability>
                                        </ns12:SignatureAlgorithm>
                                    </ns12:SignatureOK>
                                    <ns12:CertificatePathValidity>
                                        <ns12:PathValiditySummary>
                                            <ns12:ResultMajor>urn:oasis:names:tc:dss:1.0:detail:indetermined</ns12:ResultMajor>
                                        </ns12:PathValiditySummary>
                                        <ns12:CertificateIdentifier>
                                            <ns4:X509IssuerName>GEM.HBA-qCA24 TEST-ONLY</ns4:X509IssuerName>
                                            <ns4:X509SerialNumber>-137122856</ns4:X509SerialNumber>
                                        </ns12:CertificateIdentifier>
                                        <ns12:PathValidityDetail>
                                            <ns12:CertificateValidity>
                                                <ns12:CertificateIdentifier>
                                                    <ns4:X509IssuerName>GEM.HBA-qCA24 TEST-ONLY</ns4:X509IssuerName>
                                                    <ns4:X509SerialNumber>-137122856</ns4:X509SerialNumber>
                                                </ns12:CertificateIdentifier>
                                                <ns12:Subject>Sam SchraßerTEST-ONLY</ns12:Subject>
                                                <ns12:ChainingOK>
                                                    <ns12:ResultMajor>urn:oasis:names:tc:dss:1.0:detail:valid</ns12:ResultMajor>
                                                </ns12:ChainingOK>
                                                <ns12:ValidityPeriodOK>
                                                    <ns12:ResultMajor>urn:oasis:names:tc:dss:1.0:detail:valid</ns12:ResultMajor>
                                                </ns12:ValidityPeriodOK>
                                                <ns12:ExtensionsOK>
                                                    <ns12:ResultMajor>urn:oasis:names:tc:dss:1.0:detail:valid</ns12:ResultMajor>
                                                </ns12:ExtensionsOK>
                                                <ns12:CertificateValue>MIIEvTCCA6WgAwIBAgIHAkHB99Or2DANBgkqhkiG9w0BAQsFADBQMQswCQYDVQQGEwJERTEfMB0GA1UECgwWZ2VtYXRpayBHbWJIIE5PVC1WQUxJRDEgMB4GA1UEAwwXR0VNLkhCQS1xQ0EyNCBURVNULU9OTFkwHhcNMTgxMTA1MDAwMDAwWhcNMjMxMTA0MjM1OTU5WjB4MR8wHQYDVQQDDBZTYW0gU2NocmHDn2VyVEVTVC1PTkxZMRUwEwYDVQQqDAxTYW0gRnJlaWhlcnIxEjAQBgNVBAQMCVNjaHJhw59lcjEdMBsGA1UEBRMUODAyNzY4ODMxMTAwMDAwOTU3NjcxCzAJBgNVBAYTAkRFMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAiMe1Q4JimLLBBTbQMya/D0rgebKdbmX1mQEm0Wo8AnSrwyoBynhuU2hFKeDbBzthkZZWwYxFoarP3LuEN/U6iM2X5Hnsw1/NqdajKMLLKTcp26BaghQXEVDSy1INsPQlNLOKnuYwSRAfsZ5SDd14iQ+SyKG86kkyLNCdh0N2zxygtnuZtwa55QFLu51UZ176/DIrmjZ3+rlOWNQg1Jqt4WvQ4er3JKApBq9kfLtWlPE97swCG+r7GlqlkO8k4Mn1hCJKPrEyoQ9NYPulrVIDiIf5NhknFf0fhi7AuEa63yZWoLJSjToOx8CL4YWHiXj1K6dPbCEFbFVm0lbrbmKX4wIDAQABo4IBcjCCAW4wHQYDVR0OBBYEFL7XEnVBrPVGn3oYBHZARreYfhNaMAwGA1UdEwEB/wQCMAAwGwYJKwYBBAHAbQMFBA4wDAYKKwYBBAHAbQMFATAiBggrBgEFBQcBAwQWMBQwCAYGBACORgEBMAgGBgQAjkYBBDAfBgNVHSMEGDAWgBRnnDG26cA36h0bgeek9TvMHhcBOTA5BgNVHSAEMjAwMAkGByqCFABMBEgwCQYHBACL7EABAjAKBggqghQATASBETAMBgorBgEEAYLNMwEBMA4GA1UdDwEB/wQEAwIGQDA4BggrBgEFBQcBAQQsMCowKAYIKwYBBQUHMAGGHGh0dHA6Ly9laGNhLmdlbWF0aWsuZGUvb2NzcC8wWAYFKyQIAwMETzBNpCgwJjELMAkGA1UEBhMCREUxFzAVBgNVBAoMDmdlbWF0aWsgQmVybGluMCEwHzAdMBswDgwMw4RyenRpbi9Bcnp0MAkGByqCFABMBB4wDQYJKoZIhvcNAQELBQADggEBAIsKzOqakT9O1zoI58GKwmgX0Tii4juUqN6rns1jjHQGOzWGgDQWGatIidCsPvZvUKLz3QuzRGjiSVI4671ohhD9YvdqxU5We51ZuYf0muWE5WAPuB80Mc5rcVywt3C28+par9VVvOAwFMqVHy8PfmyXytDdF3HSXzNZtbpKmZpbYREM28b3gIb0xkNrUzaz2w57TfvtH+fchzj8rPw8012guPORLUp2hUl8MM4YDR/33rSogECGNsSRZgTYi0m9cLKWEob4pLEASF/R+PUTlLOpfEwGpYyLnASS11wcNHeGEGbUgsiWl3FGts933MLS+sC0HKVnSaUy2qAHVR+vK+g=</ns12:CertificateValue>
                                                <ns12:SignatureOK>
                                                    <ns12:SigMathOK>
                                                        <ns12:ResultMajor>urn:oasis:names:tc:dss:1.0:detail:indetermined</ns12:ResultMajor>
                                                    </ns12:SigMathOK>
                                                    <ns12:SignatureAlgorithm>
                                                        <ns12:Algorithm>http://www.w3.org/2001/04/xmldsig-more#rsa-sha256</ns12:Algorithm>
                                                        <ns12:Suitability>
                                                            <ns12:ResultMajor>urn:oasis:names:tc:dss:1.0:detail:valid</ns12:ResultMajor>
                                                        </ns12:Suitability>
                                                    </ns12:SignatureAlgorithm>
                                                </ns12:SignatureOK>
                                                <ns12:CertificateStatus>
                                                    <ns12:CertStatusOK>
                                                        <ns12:ResultMajor>urn:oasis:names:tc:dss:1.0:detail:indetermined</ns12:ResultMajor>
                                                    </ns12:CertStatusOK>
                                                    <ns12:RevocationEvidence>
                                                        <ns12:OCSPValidity>
                                                            <ns12:OCSPIdentifier>
                                                                <ns6:ResponderID>
                                                                    <ns6:ByName>ehca QES OCSP Signer 2 TEST-ONLY</ns6:ByName>
                                                                </ns6:ResponderID>
                                                                <ns6:ProducedAt>2021-04-15T11:12:26.548Z</ns6:ProducedAt>
                                                            </ns12:OCSPIdentifier>
                                                            <ns12:OCSPValue>MIIGdAoBAKCCBm0wggZpBgkrBgEFBQcwAQEEggZaMIIGVjCCAUahVjBUMQswCQYDVQQGEwJERTEaMBgGA1UECgwRZ2VtYXRpayBOT1QtVkFMSUQxKTAnBgNVBAMMIGVoY2EgUUVTIE9DU1AgU2lnbmVyIDIgVEVTVC1PTkxZGA8yMDIxMDQxNTExMTIyNlowgbYwgbMwQDAJBgUrDgMCGgUABBRNFks3lLP4Wm+YY1OyKvXiyNCMcwQUZ5wxtunAN+odG4HnpPU7zB4XATkCBwJBwffTq9iAABgPMjAyMTA0MTUxMTEyMjZaoVwwWjAaBgUrJAgDDAQRGA8yMDE4MTEwNTE1MzQzOVowPAYFKyQIAw0EMzAxMA0GCWCGSAFlAwQCAQUABCDkeQLIwLc5SjI5vgJ9kfKCmV/gALbvRKmia1upSi+2UqEiMCAwHgYJKwYBBQUHMAEGBBEYDzE4NzAwMTA3MDAwMDAwWjANBgkqhkiG9w0BAQsFAAOCAQEAOvB+RJSk8+0N7Bvhtz5+sl4AiiI67VUB1Ro85qiqGmSSOU18xGQbT/Gk5SvpoQegFfnu7SvaPxgzvAjGY+5mHCYBwVEOC8nPUSN/oqipzo7bepS0PGdcNlzt5zh23+AcTT0mJiLjTzsCiTXByJ9I6wuZQ+CkvG8YXEIuMHLLwqVvjQyNH1VNZEC6+AsyWypD39gYMFfdEn+Rk45HpcGtZrgphCbAoGwnsZH/3ztS+TDuSsmEbeBSQdmQr7Z2sUPecP/YyRx3ysoGyBUuRgZZsBxSqG5q06MuNLyFHZN8lvPSE0MHV0tcxLH5KUb6aAD9RQrDbm9eFNpQ/wiXmBOhu6CCA/QwggPwMIID7DCCAtSgAwIBAgIGAdMX4hoWMA0GCSqGSIb3DQEBCwUAMFAxCzAJBgNVBAYTAkRFMR8wHQYDVQQKDBZnZW1hdGlrIEdtYkggTk9ULVZBTElEMSAwHgYDVQQDDBdHRU0uSEJBLXFDQTI0IFRFU1QtT05MWTAeFw0xOTA0MDEwMDAwMDBaFw0yNDA0MDEyMzU5NTlaMFQxCzAJBgNVBAYTAkRFMRowGAYDVQQKDBFnZW1hdGlrIE5PVC1WQUxJRDEpMCcGA1UEAwwgZWhjYSBRRVMgT0NTUCBTaWduZXIgMiBURVNULU9OTFkwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCf1I879/ieGtBfisHaaHyjPaHpgJzXDiLUdasX30xY2JKpr27y0ebriSwSQTPTOwJzXiVefcIZMzvT6/8//OyoDhMn4yBFAIsxMTyxHqMWFEqvvcAcRjB5CQsEcb/nZbjKrYQiCRL8VzsKOhHHzyYK0g84bG44QQ314eOvlbZihKjubDCYCMZ/T6Ta+V8EHMm58F3sR9CXNKKwwr5oOkwZsB047xx0LIg+Gir/golSvpfuq3bmLL0bKRlr8diFUzdkxkD+NIx5pB3o2dKFx/vkI3ArmnUQIZHgjTQn7+vPqMjVJhOFKmJyxb9z2Oqo7E5mUfg5st5G4l8LuwDwoaw7AgMBAAGjgccwgcQwOAYIKwYBBQUHAQEELDAqMCgGCCsGAQUFBzABhhxodHRwOi8vZWhjYS5nZW1hdGlrLmRlL29jc3AvMB0GA1UdDgQWBBT2g0uaT5zD2tBJQHdvfUJYAxRUNjAMBgNVHRMBAf8EAjAAMB8GA1UdIwQYMBaAFGecMbbpwDfqHRuB56T1O8weFwE5MBUGA1UdIAQOMAwwCgYIKoIUAEwEgSMwDgYDVR0PAQH/BAQDAgZAMBMGA1UdJQQMMAoGCCsGAQUFBwMJMA0GCSqGSIb3DQEBCwUAA4IBAQAdTJ/2ljlYtZyRhlHJhj0BrH6Misav0dHHSeBXknV61KJeFbzyDMFNFMidNmnIAVHMKyI8SVZ3RPgZXBa//RvSp0VN5hyl9cpIvfZlLANQ41U460G+n06vJIxX6hpPdQIJkkrZbXpQN13l/hC17X9+c8hg7GKz8oYOsCN8l/Za3vsJpuBFPdwSxySAUiBBH1ei0V4/GNjaAKqBv7XEmZX4Q7sGaDKTEsWykhUlaeINh8PLn3iwGjAqBD22pRSWVPyjooSPwVXPKfIvXZiUSJvNlZkNPaBjXGMpe3ysBw+LxhjnwBHfnokot9dtmKEeorm8eGDjigKPmJXKBmsS/GXw</ns12:OCSPValue>
                                                            <ns12:SignatureOK>
                                                                <ns12:SigMathOK>
                                                                    <ns12:ResultMajor>urn:oasis:names:tc:dss:1.0:detail:valid</ns12:ResultMajor>
                                                                </ns12:SigMathOK>
                                                            </ns12:SignatureOK>
                                                            <ns12:CertificatePathValidity>
                                                                <ns12:PathValiditySummary>
                                                                    <ns12:ResultMajor>urn:oasis:names:tc:dss:1.0:detail:valid</ns12:ResultMajor>
                                                                </ns12:PathValiditySummary>
                                                                <ns12:CertificateIdentifier>
                                                                    <ns4:X509IssuerName>GEM.HBA-qCA24 TEST-ONLY</ns4:X509IssuerName>
                                                                    <ns4:X509SerialNumber>400693782</ns4:X509SerialNumber>
                                                                </ns12:CertificateIdentifier>
                                                            </ns12:CertificatePathValidity>
                                                        </ns12:OCSPValidity>
                                                    </ns12:RevocationEvidence>
                                                </ns12:CertificateStatus>
                                            </ns12:CertificateValidity>
                                            <ns12:CertificateValidity>
                                                <ns12:CertificateIdentifier>
                                                    <ns4:X509IssuerName>GEM.qRCA2 TEST-ONLY</ns4:X509IssuerName>
                                                    <ns4:X509SerialNumber>1230379532</ns4:X509SerialNumber>
                                                </ns12:CertificateIdentifier>
                                                <ns12:Subject>GEM.HBA-qCA24 TEST-ONLY</ns12:Subject>
                                                <ns12:ChainingOK>
                                                    <ns12:ResultMajor>urn:oasis:names:tc:dss:1.0:detail:valid</ns12:ResultMajor>
                                                </ns12:ChainingOK>
                                                <ns12:ValidityPeriodOK>
                                                    <ns12:ResultMajor>urn:oasis:names:tc:dss:1.0:detail:valid</ns12:ResultMajor>
                                                </ns12:ValidityPeriodOK>
                                                <ns12:ExtensionsOK>
                                                    <ns12:ResultMajor>urn:oasis:names:tc:dss:1.0:detail:valid</ns12:ResultMajor>
                                                </ns12:ExtensionsOK>
                                                <ns12:CertificateValue>MIIENjCCAx6gAwIBAgIHA+a9SVYaDDANBgkqhkiG9w0BAQsFADBMMQswCQYDVQQGEwJERTEfMB0GA1UECgwWZ2VtYXRpayBHbWJIIE5PVC1WQUxJRDEcMBoGA1UEAwwTR0VNLnFSQ0EyIFRFU1QtT05MWTAeFw0xNzAxMDMxMDAwMDBaFw0yNTAxMDIxMDAwMDBaMFAxCzAJBgNVBAYTAkRFMR8wHQYDVQQKDBZnZW1hdGlrIEdtYkggTk9ULVZBTElEMSAwHgYDVQQDDBdHRU0uSEJBLXFDQTI0IFRFU1QtT05MWTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAKuT/QUC3KebYuQu54YxKQlWYy2JAwN4IY1CYoQVS5NXhWdGGQwJERwRX55J+CFQyhF1TlpN07A+yRYFp8E2WsGnLTXHQWKfCCDKmwZODjm71uVF4Gv0tP2vZNm8NNMfV76DMjMLZ3wcgE1bmvCgdPviwBewMnqE2ix8RZwDHxmV08kAc12SNJI/K/vx6cjbnknTeGyu0P5cfsJbxejf8+EfW6y4Tz/p11H0y9A7VrMZrpW8oDjvNJVAFwK/Fif722VagwsmSgmwBidtJjTuTLb6aJ3gNI6FOL/rIkfVpPR9kdHy5mGGKSKbHafwwni6DWcYnP12q8AEssRY6Y2mCwsCAwEAAaOCARcwggETMA4GA1UdDwEB/wQEAwICBDAdBgNVHQ4EFgQUZ5wxtunAN+odG4HnpPU7zB4XATkwEgYDVR0TAQH/BAgwBgEB/wIBADApBgNVHSAEIjAgMAcGBSskCAEBMAoGCCqCFABMBIERMAkGBwQAi+xAAQIwGAYIKwYBBQUHAQMEDDAKMAgGBgQAjkYBATAbBgkrBgEEAcBtAwUEDjAMBgorBgEEAcBtAwUBMB8GA1UdIwQYMBaAFJkLY04eermkUYbZw0Xx+VALynIdMEsGCCsGAQUFBwEBBD8wPTA7BggrBgEFBQcwAYYvaHR0cDovL29jc3AucGtpLnRlbGVtYXRpay10ZXN0OjgwODAvQ01PQ1NQL09DU1AwDQYJKoZIhvcNAQELBQADggEBADOUITNN+hyUFNdE2aejRjlgU6ngPTibX5KXJQlqsfaYj+cv4q/MDQXxIvj56w0thEZW6UhQNXxo/8yHJBSAgFWdXAmGVAComMbM3WM2px+7ZzktQ6FSQFrW/tEo8tMj6yEFwZP5oHjYF2tcvO92owTWYCiWyMfDHr5QqTjjHPcBd2bYL1yg4CIOKh1UAMzFX7lS0CjBK0lxOpzQyxuZRKfXeEm1SFvXKLNGFSE6dvLpH9krQKvD0kTTbothEWNl7aaJoHXc2OYa6idpvkTxjQeELY5PSq0XZTgSWMDIT+8iMlcRVKWAwIMCP1rym6RHooI+uIV9sFEWiYVL8OZ16NA=</ns12:CertificateValue>
                                                <ns12:SignatureOK>
                                                    <ns12:SigMathOK>
                                                        <ns12:ResultMajor>urn:oasis:names:tc:dss:1.0:detail:valid</ns12:ResultMajor>
                                                    </ns12:SigMathOK>
                                                </ns12:SignatureOK>
                                                <ns12:CertificateStatus>
                                                    <ns12:CertStatusOK>
                                                        <ns12:ResultMajor>urn:oasis:names:tc:dss:1.0:detail:valid</ns12:ResultMajor>
                                                    </ns12:CertStatusOK>
                                                </ns12:CertificateStatus>
                                            </ns12:CertificateValidity>
                                            <ns12:TrustAnchor>
                                                <ns12:ResultMajor>urn:oasis:names:tc:dss:1.0:detail:valid</ns12:ResultMajor>
                                                <ns12:ResultMinor>urn:oasis:names:tc:dss-x:1.0:profiles:verificationreport:trustanchor:certDataBase</ns12:ResultMinor>
                                            </ns12:TrustAnchor>
                                        </ns12:PathValidityDetail>
                                    </ns12:CertificatePathValidity>
                                </ns12:DetailedSignatureReport>
                                <ns9:VerificationTimeInfo>
                                    <ns9:VerificationTime>2021-04-15T11:12:26.101Z</ns9:VerificationTime>
                                </ns9:VerificationTimeInfo>
                            </ns12:Details>
                        </ns12:IndividualReport>
                    </ns12:VerificationReport>
                </ns7:OptionalOutputs>
            </ns7:VerifyDocumentResponse>
        </S:Body>
    </S:Envelope>

Hier dargestellt ist die QES-Signaturvalidierung einer Koco-Box der
durch einen Secunet-Konnektor erzeugten Signatur aus
`4fe2013d-ae94-441a-a1b1-78236ae65680_S_SECUN_secu_kon_4.8.2_4.1.3_V_KOCOC_kocobox_3.6.0_2.3.24_resp.xml`.
Weitere Beispiele finden sich im Unterordner der
[Beispiele](../samples/qes/signed).

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
<td style="text-align: left;"><p>OK<br />
<span class="small">Die Anfrage wurde erfolgreich bearbeitet und das
Ergebnis der Anfrage wird in der Antwort übertragen. Das gilt ebenso für
Fehler in der Verarbeitung des SOAP-Requests, die als SOAP-Fault
zurückgemeldet werden.</span></p></td>
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
</tbody>
</table>

# E-Rezept-Abgabe vollziehen

Ein Apotheker hat ein E-Rezept abgerufen und beliefert den Patienten mit
dem Medikament. Beim Abschließen des Workflows muss der Rezept-Typ
beachtet werden. Dieser wird durch das Element Task.extension.flowType
bestimmt. Zum Abschluss des Worflows stellt der Apotheker dem
Versicherten Informationen über das abgegebene Medikament bereit und
erhält als Ergebnis eine signierte Quittung, die er in seinen
Abrechnungsprozessen gegenüber dem Apothekenrechenzentrum bzw. der
Krankenkasse als Nachweis des ordnungsgemäßen Abschlusses der
Transaktion verwenden kann. Ist für das Element
Task.extension.flowType.code "value=200" gesetzt, so handelt es sich
hierbei um ein Rezept für eine privat versicherte Person. Hierbei muss
der Apotheker dem Versicherten eine ausgedruckte Quittung übergeben,
damit der Versicherte das Medikament gegenüber seiner Kostenstelle
eigenständig abrechenen kann.

Der Aufruf erfolgt als http-POST-Operation mit der FHIR-Operation
`$close`. Im http-Request-Header `Authorization` muss das während der
Authentisierung erhaltene ACCESS\_TOKEN übergeben werden. Als
URL-Parameter `?secret=...` muss das beim Abrufen des E-Rezepts im Task
generierte `Secret` für die Berechtigungsprüfung übergeben werden.
Zusätzlich werden Informationen über das ausgegebene Medikament an den
Fachdienst übergeben. Im http-ResponseBody wird die serverseitig über
den Task und das E-Rezept-Bundle erzeugte Signatur als
`Quittungs-Bundle`-Ressource zurückgegeben, die dem Apotheker gegenüber
der Krankenkasse als Quittung dient. NOTE: Zurzeit kann die Signatur mit
den Konnektor-Versionen PTV4, PTV4+ und PTV5 nicht geprüft werden.

**Request**

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>¦URI
¦https://erp.zentral.erp.splitdns.ti-dienste.de/Task/160.123.456.789.123.58/$close?secret=c36ca26502892b371d252c99b496e31505ff449aca9bc69e231c58148f6233cf<br />
Zum Nachweis als berechtigte Apotheke, die das E-Rezept gerade in
Bearbeitung hält, muss im URL-Parameter <code>secret</code> das beim
Abrufen generierte Secret übergeben werden. ¦Method ¦POST ¦HTTP Header ¦
---- Content-Type: application/fhir+xml; charset=UTF-8 Authorization:
Bearer eyJraWQ.ewogImL2pA10Qql22ddtutrvx4FsDlz.rHQjEmB1lLmpqn9J ----
NOTE: Mit dem ACCESS_TOKEN im <code>Authorization</code>-Header weist
sich der Zugreifende als Apotheker aus, im Token ist seine Rolle
enthalten. Die Base64-Darstellung des Tokens ist stark gekürzt.</p>
<p>NOTE: Im http-Header des äußeren http-Requests an die VAU (POST /VAU)
sind die Header <code>X-erp-user: l</code> und
<code>X-erp-resource: Task</code> zu setzen.</p>
<p>NOTE: In den Profilen ist unter meta.profile auch die Version mit
anzugeben. (Bsp.:
"https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_PR_MedicationDispense</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>1.2</strong>")</p>
<p>¦Payload ¦ [source,xml] ---- &lt;MedicationDispense
xmlns="http://hl7.org/fhir"&gt; &lt;meta&gt; &lt;profile
value="https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_PR_MedicationDispense</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>1.2" /&gt; &lt;/meta&gt;
&lt;contained&gt; &lt;Medication&gt; &lt;id value="med0314"/&gt;
&lt;meta&gt; &lt;profile
value="https://fhir.kbv.de/StructureDefinition/KBV_PR_ERP_Medication_PZN</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>1.1.0" /&gt; &lt;/meta&gt;
&lt;extension
url="https://fhir.kbv.de/StructureDefinition/KBV_EX_Base_Medication_Type"&gt;
&lt;valueCodeableConcept&gt; &lt;coding&gt; &lt;system
value="http://snomed.info/sct" /&gt; &lt;version
value="http://snomed.info/sct/900000000000207008/version/20220331" /&gt;
&lt;code value="763158003" /&gt; &lt;display value="Medicinal product
(product)" /&gt; &lt;/coding&gt; &lt;/valueCodeableConcept&gt;
&lt;/extension&gt; &lt;extension
url="https://fhir.kbv.de/StructureDefinition/KBV_EX_ERP_Medication_Category"&gt;
&lt;valueCoding&gt; &lt;system
value="https://fhir.kbv.de/CodeSystem/KBV_CS_ERP_Medication_Category"
/&gt; &lt;code value="00" /&gt; &lt;/valueCoding&gt; &lt;/extension&gt;
&lt;extension
url="https://fhir.kbv.de/StructureDefinition/KBV_EX_ERP_Medication_Vaccine"&gt;
&lt;valueBoolean value="false" /&gt; &lt;/extension&gt; &lt;code&gt;
&lt;coding&gt; &lt;system value="http://fhir.de/CodeSystem/ifa/pzn"
/&gt; &lt;code value="06313728" /&gt; &lt;/coding&gt; &lt;text
value="Sumatriptan-1a Pharma 100 mg Tabletten" /&gt; &lt;/code&gt;
&lt;form&gt; &lt;coding&gt; &lt;system
value="https://fhir.kbv.de/CodeSystem/KBV_CS_SFHIR_KBV_DARREICHUNGSFORM"
/&gt; &lt;code value="TAB" /&gt; &lt;/coding&gt; &lt;/form&gt;
&lt;amount&gt; &lt;numerator&gt; &lt;extension
url="https://fhir.kbv.de/StructureDefinition/KBV_EX_ERP_Medication_PackagingSize"&gt;
&lt;valueString value="10" /&gt; &lt;/extension&gt; &lt;unit
value="Tabletten" /&gt; &lt;system value="http://unitsofmeasure.org"
/&gt; &lt;/numerator&gt; &lt;denominator&gt; &lt;value value="1" /&gt;
&lt;/denominator&gt; &lt;/amount&gt; &lt;/Medication&gt;
&lt;/contained&gt; &lt;identifier&gt; &lt;system
value="https://gematik.de/fhir/erp/NamingSystem/GEM_ERP_NS_PrescriptionId"
/&gt; &lt;value value="160.123.456.789.123.58" /&gt; &lt;/identifier&gt;
&lt;status value="completed"/&gt; &lt;medicationReference&gt;
&lt;reference value="#med0314"/&gt; &lt;display value="Sumatriptan-1a
Pharma 100 mg Tabletten"/&gt; &lt;/medicationReference&gt;
&lt;subject&gt; &lt;identifier&gt; &lt;system
value="http://fhir.de/sid/gkv/kvid-10" /&gt; &lt;value
value="X123456789" /&gt; &lt;/identifier&gt; &lt;/subject&gt;
&lt;performer&gt; &lt;actor&gt; &lt;identifier&gt; &lt;system
value="https://gematik.de/fhir/sid/telematik-id" /&gt; &lt;value
value="3-SMC-B-Testkarte-883110000129070" /&gt; &lt;/identifier&gt;
&lt;/actor&gt; &lt;/performer&gt; &lt;quantity&gt; &lt;value value="1"
/&gt; &lt;system value="http://unitsofmeasure.org" /&gt;
&lt;/quantity&gt; &lt;whenHandedOver value="2020-03-20"/&gt;
&lt;dosageInstruction&gt; &lt;text value="1-0-1-0" /&gt;
&lt;/dosageInstruction&gt; &lt;/MedicationDispense&gt; ----</p>
<p>NOTE: Ab dem 01.07.2023 werden Profile in denen die Version in
meta.profile nicht vorhanden ist abgewiesen. Daher ist diese
entsprechend immer anzugeben. Bsp: <a
href="https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_PR_MedicationDispense">https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_PR_MedicationDispense</a>**</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>1.2**</p>
<p>NOTE: Mit der Übergabe der MedicationDispense signalisiert der
Apotheker den Abschluss des E-Rezept-Workflows. Der Versicherte erhält
Informationen über das abgegebene Medikament.</p>
<p>NOTE: Sofern kein Austausch des verordneten Medikaments erfolgte,
können die Medikations-Informationen aus dem E-Rezept übernommen werden,
beim Austausch gegen ein anderes Medikament müssen hier die
entsprechenden Informationen angepasst werden, ebenso etwaig abweichende
Dosierinformationen.</p>
<p>NOTE: Die Zeitangabe in <code>&lt;whenHandedOver value</code> bezieht
sich auf die Übergabe des Medikaments, wann wurde es dem Überbringer des
E-Rezepts ausgehändigt.</p>
<p>NOTE: Die Codierung der Einnahmehinweise in
<code>&lt;dosageInstruction&gt;</code> erfolgt z.B. in Textform
[morgens-mittags-abends-nachts] in boolescher Notation 1=ja,
0=nein</p></td>
</tr>
</tbody>
</table>

Es können auch mehrere MedicationDispenses für eine $close-Operation
übergeben werden. Die MedicationDispenses werden in einem
"collection"-Bundle verschickt.

    <?xml version="1.0" encoding="UTF-8"?>
    <Bundle xmlns="http://hl7.org/fhir">
        <type value="collection"/>
        <entry>
            <fullUrl value="MedicationDispense/a3ddc2b1-826d-4b81-87b2-558834e00f50" />
            <resource>
                <MedicationDispense>
                    <id value="a3ddc2b1-826d-4b81-87b2-558834e00f50" />
                    <meta>
                        <profile value="https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_PR_MedicationDispense|1.2" />
                    </meta>
                    <contained>
                        <Medication>
                            <id value="c2b10a5e-3d71-434c-86e0-824af208a2bf" />
                            <meta>
                                <profile value="https://fhir.kbv.de/StructureDefinition/KBV_PR_ERP_Medication_PZN|1.1.0" />
                            </meta>
                            <extension url="http://fhir.de/StructureDefinition/normgroesse">
                                <valueCode value="N1" />
                            </extension>
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
                                    <system value="http://fhir.de/CodeSystem/ifa/pzn" />
                                    <code value="14186244" />
                                </coding>
                                <text value="FLUSARION EH50/250UG/60 PC" />
                            </code>
                            <form>
                                <coding>
                                    <system value="https://fhir.kbv.de/CodeSystem/KBV_CS_SFHIR_KBV_DARREICHUNGSFORM" />
                                    <code value="IHP" />
                                </coding>
                            </form>
                            <amount>
                                <numerator>
                                    <value value="1" />
                                    <unit value="St" />
                                </numerator>
                                <denominator>
                                    <value value="1" />
                                </denominator>
                            </amount>
                        </Medication>
                    </contained>
                    <identifier>
                        <system value="https://gematik.de/fhir/erp/NamingSystem/GEM_ERP_NS_PrescriptionId" />
                        <value value="160.000.088.357.031.88" />
                    </identifier>
                    <status value="completed" />
                    <medicationReference>
                        <reference value="Medication/c2b10a5e-3d71-434c-86e0-824af208a2bf" />
                    </medicationReference>
                    <subject>
                        <identifier>
                            <system value="http://fhir.de/sid/gkv/kvid-10" />
                            <value value="K220635158" />
                        </identifier>
                    </subject>
                    <performer>
                        <actor>
                            <identifier>
                                <system value="https://gematik.de/fhir/sid/telematik-id" />
                                <value value="3-15.2.1456789123.191" />
                            </identifier>
                        </actor>
                    </performer>
                    <whenHandedOver value="2021-11-30" />
                </MedicationDispense>
            </resource>
        </entry>
        <entry>
            <fullUrl value="MedicationDispense/854b6c62-8c8a-4ad6-b145-d5bac5f9f010" />
            <resource>
                <MedicationDispense>
                    <id value="854b6c62-8c8a-4ad6-b145-d5bac5f9f010" />
                    <meta>
                        <profile value="https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_PR_MedicationDispense|1.2" />
                    </meta>
                    <contained>
                        <Medication>
                            <id value="756b422f-4df0-4afe-9d54-da534a44109e" />
                            <meta>
                                <profile value="https://fhir.kbv.de/StructureDefinition/KBV_PR_ERP_Medication_PZN|1.1.0" />
                            </meta>
                            <extension url="http://fhir.de/StructureDefinition/normgroesse">
                                <valueCode value="N1" />
                            </extension>
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
                                    <system value="http://fhir.de/CodeSystem/ifa/pzn" />
                                    <code value="14186244" />
                                </coding>
                                <text value="FLUSARION EH50/250UG/60 PC" />
                            </code>
                            <form>
                                <coding>
                                    <system value="https://fhir.kbv.de/CodeSystem/KBV_CS_SFHIR_KBV_DARREICHUNGSFORM" />
                                    <code value="IHP" />
                                </coding>
                            </form>
                            <amount>
                                <numerator>
                                    <value value="1" />
                                    <unit value="St" />
                                </numerator>
                                <denominator>
                                    <value value="1" />
                                </denominator>
                            </amount>
                        </Medication>
                    </contained>
                    <identifier>
                        <system value="https://gematik.de/fhir/erp/NamingSystem/GEM_ERP_NS_PrescriptionId" />
                        <value value="160.000.088.357.031.88" />
                    </identifier>
                    <status value="completed" />
                    <medicationReference>
                        <reference value="Medication/756b422f-4df0-4afe-9d54-da534a44109e" />
                    </medicationReference>
                    <subject>
                        <identifier>
                            <system value="http://fhir.de/sid/gkv/kvid-10" />
                            <value value="K220635158" />
                        </identifier>
                    </subject>
                    <performer>
                        <actor>
                            <identifier>
                                <system value="https://gematik.de/fhir/sid/telematik-id" />
                                <value value="3-15.2.1456789123.191" />
                            </identifier>
                        </actor>
                    </performer>
                    <whenHandedOver value="2021-11-30" />
                </MedicationDispense>
            </resource>
        </entry>
    </Bundle>

**Response**

    HTTP/1.1 200 OK
    Content-Length: 3906
    Content-Type: application/fhir+xml;charset=utf-8

    <Bundle xmlns="http://hl7.org/fhir">
        <id value="dffbfd6a-5712-4798-bdc8-07201eb77ab8"/>
        <meta>
            <profile value="https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_PR_Bundle|1.2" />
        </meta>
        <identifier>
            <system value="https://gematik.de/fhir/erp/NamingSystem/GEM_ERP_NS_PrescriptionId" />
            <value value="160.123.456.789.123.58" />
        </identifier>
        <type value="document" />
        <timestamp value="2021-11-26T09:51:36.483+00:00" />
        <link>
            <relation value="self"/>
            <url value="https://erp-ref.zentral.erp.splitdns.ti-dienste.de/Task/160.123.456.789.123.58/$close/"/>
        </link>
        <entry>
            <fullUrl value="urn:uuid:c624cf47-e235-4624-af71-0a09dc9254dc" />
            <resource>
                <Composition>
                    <id value="c624cf47-e235-4624-af71-0a09dc9254dc"/>
                    <meta>
                        <profile value="https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_PR_Composition|1.2" />
                    </meta>
                    <extension url="https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_EX_Beneficiary">
                        <valueIdentifier>
                            <system value="https://gematik.de/fhir/sid/telematik-id" />
                            <value value="3-SMC-B-Testkarte-883110000129070" />
                        </valueIdentifier>
                    </extension>
                    <status value="final" />
                    <type>
                        <coding>
                            <system value="https://gematik.de/fhir/erp/CodeSystem/GEM_ERP_CS_DocumentType" />
                            <code value="3" />
                            <display value= "Receipt"/>
                        </coding>
                    </type>
                    <date value="2021-11-26T09:51:36.483+00:00" />
                    <author>
                        <reference value="https://erp.zentral.erp.splitdns.ti-dienste.de/Device/1" />
                    </author>
                    <title value="Quittung" />
                    <event>
                        <period>
                            <start value="2021-11-26T09:48:36.483+00:00" />
                            <end value="2021-11-26T09:51:36.483+00:00" />
                        </period>
                    </event>
                    <section>
                        <entry>
                            <reference value="Binary/PrescriptionDigest-160.123.456.789.123.58"/>
                        </entry>
                    </section>
                </Composition>
            </resource>
        </entry>
        <entry>
            <fullUrl value="https://erp.zentral.erp.splitdns.ti-dienste.de/Device/1" />
            <resource>
                <Device>
                    <id value="1" />
                    <meta>
                        <profile value="https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_PR_Device|1.2" />
                    </meta>
                    <status value="active" />
                    <serialNumber value="1.4.0" />
                    <deviceName>
                        <name value="E-Rezept-Fachdienst" />
                        <type value="user-friendly-name" />
                    </deviceName>
                    <version>
                        <value value="1.4.0" />
                    </version>
                    <contact>
                        <system value="email"/>
                        <value value="betrieb@gematik.de"/>
                    </contact>
                </Device>
            </resource>
        </entry>
        <entry>
            <fullUrl value="https://erp-ref.zentral.erp.splitdns.ti-dienste.de/Task/160.123.456.789.123.58/PrescriptionDigest" />
            <resource>
                <Binary>
                    <id value="PrescriptionDigest-160.123.456.789.123.58"/>
                    <meta>
                        <versionId value="1"/>
                        <profile value="http://hl7.org/fhir/StructureDefinition/Binary|4.0.1"/>
                    </meta>
                    <contentType value="application/octet-stream"/>
                    <data value="tJg8c5ZtdhzEEhJ0ZpAsUVFx5dKuYgQFs5oKgthi17M="/>
                </Binary>
            </resource>
        </entry>
        <signature>
            <type>
                <system value="urn:iso-astm:E1762-95:2013" />
                <code value="1.2.840.10065.1.12.1.1" />
            </type>
            <when value="2021-11-26T09:51:36.484+00:00" />
            <who>
                <reference value="https://erp.zentral.erp.splitdns.ti-dienste.de/Device/1" />
            </who>
            <sigFormat value="application/pkcs7-mime" />
            <data value="QXVmZ3J1bmQgZGVyIENvcm9uYS1TaXR1YXRpb24ga29ubnRlIGhpZXIga3VyemZyaXN0aWcga2VpbiBCZWlzcGllbCBpbiBkZXIgTGFib3J1bWdlYnVuZyBkZXIgZ2VtYXRpayBlcnN0ZWxsdCB3ZWRlbi4gRGllc2VzIHdpcmQgbmFjaGdlcmVpY2h0LgoKSW5oYWx0bGljaCB1bmQgc3RydWt0dXJlbGwgaXN0IGRpZSBTZXJ2ZXJzaWduYXR1ciBkZXIgUXVpdHR1bmcgZWluZSBFbnZlbG9waW5nIENBZEVTLVNpZ25hdHVyLCBkaWUgZGVuIHNpZ25pZXJ0ZW4gRGF0ZW5zYXR6IGFuYWxvZyB6dXIgS29ubmVrdG9yLVNpZ25hdHVyIGlubmVyaGFsYiBkZXMgQVNOMS5Db250YWluZXJzIHRyYW5zcG9ydGllcnQu" />
        </signature>
    </Bundle>

Im Ergebnis der Operation wird ein signiertes Bundle als Nachweis des
ordnungsgemäßen Durchlaufs des E-Rezept-Workflows zurückgegeben.

Das signierte Quittungs-Bundle enthält unter
`<identifier><value/>`&lt;/identifier&gt;\` die Rezept-ID für eine
eindeutige Zuordnung aller Artefakte des durchlaufenen Workflows

An der Stelle `<Composition><valueIdentifier/></Composition>` ist die
Telematik-ID als Quittungsempfänger bzw. begünstigte Institution
eingetragen, welche die Dispensierung des E-Rezepts vollzogen hat.

Das Startdatum in `<period><start value="*"/></period>` entspricht dem
Abrufdatum des E-Rezepts durch die Apotheke (Statuswechsel des Task:
ready → in-progress)

Signaturzeitpunkt der Quittung in &lt;period&gt;&lt;end
value="\*"/&gt;&lt;/period&gt;, entspricht dem Statuswechsel des Task
in-progress → completed

Das unter
`<fullUrl value="https://erp.zentral.erp.splitdns.ti-dienste.de/Device/*`/&gt;\`
eingebettete Device identifiziert den E-Rezept-Fachdienst als Aussteller
der Quittung.

Unter `<Binary><data value="*"/></Binary>` wird der base64-codierte
Hashwert, über den die QES des Verordnungsdatensatzes erstellt wurde
eingebettet.

Das Element `<signature>*</signature>` enthält die Signatur des
Quittungs-Bundles über alle enthaltenen Objekte als Enveloping
CAdES-Signatur in Base64-Codierung.

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
[small]#Die Anfrage wurde erfolgreich bearbeitet. Die angeforderte Ressource wurde vor dem Senden der Antwort erstellt. Das &quot;Location&quot;-Header-Feld enthält die Adresse der erstellten Ressource.#</code></pre></td>
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
<td style="text-align: left;"><p>409</p></td>
<td style="text-align: left;"><p>Conflict<br />
<span class="small">Die Anfrage wurde unter falschen Annahmen gestellt.
Das E-Rezept befindet sich bereits in Belieferung</span></p></td>
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

# E-Rezept zurückweisen

Ein Apotheker hat im vorherigen Schritt ein E-Rezept abgerufen und
fachlich geprüft. Er kommt zu dem Schluss, das E-Rezept nicht zu
beliefern und möchte nun das E-Rezept zurückweisen, damit der
Versicherte das E-Rezept ggfs. in einer anderen Apotheke einlösen kann.

Der Aufruf erfolgt als http-POST-Operation mit der FHIR-Operation
`$reject`. Im http-Request-Header `Authorization` muss das während der
Authentisierung erhaltene ACCESS\_TOKEN übergeben werden. Als
URL-Parameter `?secret=...` muss das beim Abrufen des E-Rezepts im Task
generierte `Secret` für die Berechtigungsprüfung übergeben werden.

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
href="https://erp.zentral.erp.splitdns.ti-dienste.de/Task/160.123.456.789.123.58/$reject?secret=c36ca26502892b371d252c99b496e31505ff449aca9bc69e231c58148f6233cf">https://erp.zentral.erp.splitdns.ti-dienste.de/Task/160.123.456.789.123.58/$reject?secret=c36ca26502892b371d252c99b496e31505ff449aca9bc69e231c58148f6233cf</a><br />
Zum Nachweis als berechtigte Apotheke, die das E-Rezept gerade in
Bearbeitung hält, muss im URL-Parameter <code>secret</code> das beim
Abrufen generierte Secret übergeben werden</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>Method</strong></p></td>
<td style="text-align: left;"><p>POST</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>HTTP Header</strong></p></td>
<td style="text-align: left;"><pre><code>Content-Type: application/fhir+xml; charset=UTF-8;
Authorization: Bearer eyJraWQ.ewogImL2pA10Qql22ddtutrvx4FsDlz.rHQjEmB1lLmpqn9J</code></pre>
<div class="note">
<p>Mit dem ACCESS_TOKEN im <code>Authorization</code>-Header weist sich
der Zugreifende als Apotheker aus, im Token ist seine Rolle enthalten.
Die Base64-Darstellung des Tokens ist stark gekürzt.</p>
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

Im Ergebnis der $reject-Operation wird der referenzierte Task auf den
aktiven Status `ready` zurückgesetzt und das Secret gelöscht.
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
<td style="text-align: left;"><p>410</p></td>
<td style="text-align: left;"><p>Gone<br />
<span class="small">Die angeforderte Ressource wird nicht länger
bereitgestellt und wurde dauerhaft entfernt.</span></p></td>
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

# E-Rezept löschen

Ein Apotheker hat im vorherigen Schritt ein E-Rezept abgerufen und
fachlich geprüft. Der Versicherte bittet ihn jedoch, das Rezept nicht zu
beliefern sondern zu löschen, da er nicht über ein eigenes Gerät mit
E-Rezept-App verfügt aber sein Recht auf informationelle
Selbstbestimmung wahrnehmen möchte. Der Apotheker kommt diesem Wunsch
nach und löscht das E-Rezept auf dem Fachdienst.

Der Aufruf erfolgt als http-POST-Operation mit der FHIR-Operation
`$abort`. Im http-Request-Header `Authorization` muss das während der
Authentisierung erhaltene ACCESS\_TOKEN übergeben werden. Als
URL-Parameter `?secret=...` muss das beim Abrufen des E-Rezepts im Task
generierte `Secret` für die Berechtigungsprüfung übergeben werden.

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
href="https://erp.zentral.erp.splitdns.ti-dienste.de/Task/160.123.456.789.123.58/$abort?secret=c36ca26502892b371d252c99b496e31505ff449aca9bc69e231c58148f6233cf">https://erp.zentral.erp.splitdns.ti-dienste.de/Task/160.123.456.789.123.58/$abort?secret=c36ca26502892b371d252c99b496e31505ff449aca9bc69e231c58148f6233cf</a><br />
Zum Nachweis als berechtigte Apotheke, die das E-Rezept gerade in
Bearbeitung hält, muss im URL-Parameter <code>secret</code> das beim
Abrufen generierte Secret übergeben werden</p></td>
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
berechtigt ist. Beispielsweise befindet sich das Rezept nicht in der
Belieferung durch diese Apotheke.</span></p></td>
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
<td style="text-align: left;"><p>409</p></td>
<td style="text-align: left;"><p>Conflict<br />
<span class="small">Die Anfrage wurde unter falschen Annahmen gestellt.
Das E-Rezept befindet sich bereits in Belieferung</span></p></td>
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

# Quittung erneut abrufen

Als Apotheker kann es erforderlich sein, die Quittung für ein
beliefertes E-Rezept erneut abzurufen (z.B. am Monatsende für
Abrechnungszwecke, falls das Apothekenverwaltungssystem die Quittung
nicht während der Belieferung gespeichert hat). Der Abruf ist möglich,
solange das E-Rezept nicht automatisch und auch nicht durch den
Versicherten gelöscht wurde.

**Request**

<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p><strong>URI</strong></p></td>
<td style="text-align: left;"><pre><code>https://erp.zentral.erp.splitdns.ti-dienste.de/Task/160.123.456.789.123.58?secret=c36ca26502892b371d252c99b496e31505ff449aca9bc69e231c58148f6233cf</code></pre>
<p>Zum Nachweis als berechtigte Apotheke, die das E-Rezept verarbeitet
hat(te), muss im URL-Parameter <code>secret</code> das beim Abrufen
generierte Secret übergeben werden</p></td>
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
der Zugreifende als Leistungserbringer aus, im Token ist seine Rolle
enthalten. Die Base64-Darstellung des Tokens ist stark gekürzt.</p>
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

    HTTP/1.1 200 OK

    <Bundle xmlns="http://hl7.org/fhir">
        <id value="dffbfd6a-5712-4798-bdc8-07201eb77ab8"/>
        <meta>
            <lastUpdated value="2020-03-13T07:31:34.328+00:00"/>
        </meta>
        <type value="collection"/>
        <entry>
            <fullUrl value="https://erp.zentral.erp.splitdns.ti-dienste.de/Task/160.123.456.789.123.58"/>
            <resource>
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
                    <identifier>
                        <system value="https://gematik.de/fhir/erp/NamingSystem/GEM_ERP_NS_Secret"/>
                        <value value="c36ca26502892b371d252c99b496e31505ff449aca9bc69e231c58148f6233cf"/>
                    </identifier>
                    <status value="completed"/>
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
                            </coding>
                        </type>
                        <valueString value="281a985c-f25b-4aae-91a6-41ad744080b0"/>
                    </input>
                    <output>
                        <type>
                            <coding>
                                <system value="https://gematik.de/fhir/erp/CodeSystem/GEM_ERP_CS_DocumentType"/>
                                <code value="3"/>
                            </coding>
                        </type>
                        <valueString value="dffbfd6a-5712-4798-bdc8-07201eb77ab8"/>
                    </output>
                </Task>
            </resource>
        </entry>
        <entry>
            <resource>
                <Bundle xmlns="http://hl7.org/fhir">
                    <id value="dffbfd6a-5712-4798-bdc8-07201eb77ab8"/>
                    <meta>
                        <profile value="https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_PR_Bundle|1.2" />
                        <tag>
                            <display value="ePrescription receipt" />
                        </tag>
                    </meta>
                    <identifier>
                        <system value="https://gematik.de/fhir/erp/NamingSystem/GEM_ERP_NS_PrescriptionId" />
                        <value value="160.123.456.789.123.58" />
                    </identifier>
                    <type value="document" />
                    <timestamp value="2020-03-20T07:31:34.328+00:00" />
                    <entry>
                        <fullUrl value="https://erp.zentral.erp.splitdns.ti-dienste.de/Composition/example" />
                        <resource>
                            <Composition>
                                <meta>
                                    <profile value="https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_PR_Composition|1.2" />
                                </meta>
                                <extension url="https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_EX_Beneficiary">
                                    <valueIdentifier>
                                        <system value="https://gematik.de/fhir/sid/telematik-id" />
                                        <value value="3-SMC-B-Testkarte-883110000129070" />
                                    </valueIdentifier>
                                </extension>
                                <status value="final" />
                                <type>
                                    <coding>
                                        <system value="https://gematik.de/fhir/erp/CodeSystem/GEM_ERP_CS_DocumentType" />
                                        <code value="3" />
                                    </coding>
                                </type>
                                <date value="2020-03-20T07:31:34.328+00:00" />
                                <author>
                                    <reference value="https://erp.zentral.erp.splitdns.ti-dienste.de/Device/ErxService" />
                                </author>
                                <title value="Quittung" />
                                <event>
                                    <period>
                                        <start value="2020-03-20T07:23:34.328+00:00" />
                                        <end value="2020-03-20T07:31:34.328+00:00" />
                                    </period>
                                </event>
                            </Composition>
                        </resource>
                    </entry>
                    <entry>
                        <fullUrl value="https://erp.zentral.erp.splitdns.ti-dienste.de/Device/1" />
                        <resource>
                            <Device>
                                <id value="1" />
                                <meta>
                                    <profile value="https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_PR_Device|1.2" />
                                </meta>
                                <status value="active" />
                                <serialNumber value="R4.0.0.287342834" />
                                <deviceName>
                                    <name value="E-Rezept-Fachdienst" />
                                    <type value="user-friendly-name" />
                                </deviceName>
                                <version>
                                    <value value="1.0.0" />
                                </version>
                            </Device>
                        </resource>
                    </entry>
                    <signature>
                        <type>
                            <system value="urn:iso-astm:E1762-95:2013" />
                            <code value="1.2.840.10065.1.12.1.1" />
                        </type>
                        <when value="2020-03-20T07:31:34.328+00:00" />
                        <who>
                            <reference value="https://erp.zentral.erp.splitdns.ti-dienste.de/Device/1" />
                        </who>
                        <sigFormat value="application/pkcs7-mime" />
                        <data value="QXVmZ3J1bmQgZGVyIENvcm9uYS1TaXR1YXRpb24ga29ubnRlIGhpZXIga3VyemZyaXN0aWcga2VpbiBCZWlzcGllbCBpbiBkZXIgTGFib3J1bWdlYnVuZyBkZXIgZ2VtYXRpayBlcnN0ZWxsdCB3ZWRlbi4gRGllc2VzIHdpcmQgbmFjaGdlcmVpY2h0LgoKSW5oYWx0bGljaCB1bmQgc3RydWt0dXJlbGwgaXN0IGRpZSBTZXJ2ZXJzaWduYXR1ciBkZXIgUXVpdHR1bmcgZWluZSBFbnZlbG9waW5nIENBZEVTLVNpZ25hdHVyLCBkaWUgZGVuIHNpZ25pZXJ0ZW4gRGF0ZW5zYXR6IGFuYWxvZyB6dXIgS29ubmVrdG9yLVNpZ25hdHVyIGlubmVyaGFsYiBkZXMgQVNOMS5Db250YWluZXJzIHRyYW5zcG9ydGllcnQu" />
                    </signature>
                </Bundle>
            </resource>
        </entry>
    </Bundle>

In `<resource><Bundle/></resource>` wird die Quittung wird als Objekt
zusammen mit dem Task zurückgegeben

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
<td style="text-align: left;"><pre><code> No Content +
[small]#Die Anfrage wurde erfolgreich bearbeitet. Die Response enthält die angefragten Daten.#</code></pre></td>
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
<td style="text-align: left;"><p>410</p></td>
<td style="text-align: left;"><p>Gone<br />
<span class="small">Die angeforderte Ressource wird nicht länger
bereitgestellt und wurde dauerhaft entfernt.</span></p></td>
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

# Beispiele für DataMatrix-Codes (inkl. Schadcodes)

AVS-Systeme müssen im Feld mit einer Vielzahl von Varianten in den von
Patienten vorgelegten DataMatrix-Codes rechnen. Die meisten werden von
geprüften, zertifizierten Primärsystemen generiert, da der Markt aber
offen ist und ebenso mit "Angriffen" zu rechnen ist, zeigt die folgende
Liste einige reale Beispiele.

Always sanitize user inputs.

![width=230px](../images/datamatrix_sample_3.png)

![width=230px](../images/dm_evil_input.png)

![width=230px](../images/dm_gruesse.png)

![width=230px](../images/dm_padding_ascii.png)

![width=230px](../images/dm_padding_whitespace.png)

![width=230px](../images/datamatrix_sample.png)

![width=230px](../images/dm_pwned.png)

![width=230px](../images/dm_script.png)