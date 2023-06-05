Auf dieser Seite sind relevante Informationen zum Verhalten des
Fachdienstes während und nach der Übergangszeit aufgeführt. Dieser
Übergangszeitraum wird nach der [Technischen Anlage der
KBV](https://update.kbv.de/ita-update/DigitaleMuster/ERP/III_2023/KBV_ITA_VGEX_Technische_Anlage_ERP.pdf)
(KP36-04) **6 Monate** betragen. Gilt also somit vom 01.07.2023 bis
31.12.2023.

# Zustände des Fachdienstes im Zusammenhang mit dem Übergangszeitraum

Diese Darstellung zeigt die Konfigurationen der Umgebungen des
Fachdienstes zu gegebener Zeit auf. Es ist dargestellt, welche
Profilversionen vom Fachdienst akzeptiert werden. Die Konfigurationen
und Beschreibung sind der Legende zu entnehmen.

![width=100%](../images/puml_fd_zustaende_timeline.png)

# Übersicht Schnittstelle und Antwort

## Methodik

Im Folgenden ist eine Übersicht dargestellt, wie sich der Fachdienst zu
gegebener Zeit verhält und welche Ressourcen als Antwort gegeben werden.
Hierbei gibt es zwei zu betrachtende Zeiträume in der PU: \*
**Übergangszeitraum** (01.07. - 31.12.2023) \* **Nach dem
Übergangszeitraum** (ab 01.01.2024)

Die zu unterscheidenden Profilversionen sind wie folgt bezeichnet: \*
FHIR 2022: bis 30.06.2023 gültige Profilversionen \* FHIR 2023: ab
01.07.2023 gültige Profilversionen

Der Fachdienst wird ab 01.07. so konfiguriert, dass Verordnungen mit dem
Workflowtype 200 oder 209 (PKV Verordnungen), die mit einer KBV
Verordnung der Version 1.0.2 erstellt wurden, abgewiesen werden.

### Übersicht der FHIR-Profile

<table>
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p><strong>Projekt</strong></p></td>
<td style="text-align: left;"><p>FHIR 2022</p></td>
<td style="text-align: left;"><p>FHIR 2023</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>gematik E-Rezept
Workflow</strong></p></td>
<td style="text-align: left;"><p><a
href="https://simplifier.net/packages/de.gematik.erezept-workflow.r4/1.1.0">https://simplifier.net/packages/de.gematik.erezept-workflow.r4/1.1.0</a></p></td>
<td style="text-align: left;"><p><a
href="https://simplifier.net/packages/de.gematik.erezept-workflow.r4/1.2.1">https://simplifier.net/packages/de.gematik.erezept-workflow.r4/1.2.1</a></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>gematik E-Rezept
Abrechnungsinformation</strong></p></td>
<td style="text-align: left;"><p>n/a</p></td>
<td style="text-align: left;"><p><a
href="https://simplifier.net/packages/de.gematik.erezept-patientenrechnung.r4/1.0.1">https://simplifier.net/packages/de.gematik.erezept-patientenrechnung.r4/1.0.1</a></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>KBV eRezept</strong></p></td>
<td style="text-align: left;"><p><a
href="https://simplifier.net/packages/kbv.ita.erp/1.0.2">https://simplifier.net/packages/kbv.ita.erp/1.0.2</a></p></td>
<td style="text-align: left;"><p><a
href="https://simplifier.net/packages/kbv.ita.erp/1.1.1">https://simplifier.net/packages/kbv.ita.erp/1.1.1</a></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>ABDA
eRezeptAbgabedaten</strong></p></td>
<td style="text-align: left;"><p>n/a</p></td>
<td style="text-align: left;"><p><a
href="https://simplifier.net/packages/de.abda.erezeptabgabedatenpkv/1.1.0">https://simplifier.net/packages/de.abda.erezeptabgabedatenpkv/1.1.0</a></p></td>
</tr>
</tbody>
</table>

## Wichtige Bemerkungen

-   Ab Konfiguration "B" antwortet der Fachdienst immer mit den neuen
    Profilversionen von Task, AuditEvent, ChargeItems, Consent, auch
    wenn diese auf alte Profile verweisen

-   Die letzten KBV Bundle und Medication Ressourcen werden den
    Fachdienst rechnerisch nach dem 09.04.2025 verlassen

-   Eine MVO-Verordnung, die am 31.12.2023 eingestellt wird kann, falls
    kein expliziter Gültigkeitszeitraum angegeben wurde, bis zum
    30.12.2024 eingelöst und verarbeitet werden

## Daten

<table>
<colgroup>
<col style="width: 25%" />
<col style="width: 25%" />
<col style="width: 25%" />
<col style="width: 25%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p><strong>Operation</strong></p></td>
<td style="text-align: left;"><p>Schnittstelle zu</p></td>
<td style="text-align: left;"><p>Während Übergangszeit</p></td>
<td style="text-align: left;"><p>Nach Übergangszeit</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>GET /Device</strong></p></td>
<td style="text-align: left;"><p>all</p></td>
<td style="text-align: left;"><p>Request</p>
<ul>
<li><p>n/a</p></li>
</ul>
<p>Response</p>
<ul>
<li><p>FD antwortet immer mit FHIR 2023</p></li>
</ul></td>
<td style="text-align: left;"><p>Request</p>
<ul>
<li><p>n/a</p></li>
</ul>
<p>Response</p>
<ul>
<li><p>FD antwortet immer mit FHIR 2023</p></li>
</ul></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>GET/metadata</strong></p></td>
<td style="text-align: left;"><p>all</p></td>
<td style="text-align: left;"><p>Request</p>
<ul>
<li><p>n/a</p></li>
</ul>
<p>Response</p>
<ul>
<li><p>FD antwortet immer mit FHIR 2023</p></li>
</ul></td>
<td style="text-align: left;"><p>Request</p>
<ul>
<li><p>n/a</p></li>
</ul>
<p>Response</p>
<ul>
<li><p>FD antwortet immer mit FHIR 2023</p></li>
</ul></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>POST
/Task/$create</strong></p></td>
<td style="text-align: left;"><p>verordnende LEI</p></td>
<td style="text-align: left;"><p>Request</p>
<ul>
<li><p>Akzeptiert wird eine &lt;Parameters&gt; FHIR Resource gemäß FHIR
2022 Namespace</p></li>
<li><p>Akzeptiert wird eine &lt;Parameters&gt; FHIR Resource gemäß FHIR
2023 Namespace</p></li>
</ul>
<p>Response</p>
<ul>
<li><p>FD antwortet mit einem Task gemäß FHIR 2023</p></li>
</ul></td>
<td style="text-align: left;"><p>Request</p>
<ul>
<li><p>Akzeptiert wird eine &lt;Parameters&gt; FHIR Resource gemäß FHIR
2023 Namespace</p></li>
</ul>
<p>Response</p>
<ul>
<li><p>FD antwortet mit einem Task gemäß FHIR 2023</p></li>
</ul></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>POST
/Task/&lt;id&gt;/$activate</strong></p></td>
<td style="text-align: left;"><p>verordnende LEI</p></td>
<td style="text-align: left;"><p>Request</p>
<p>Workflow 160/169 (GKV):</p>
<ul>
<li><p>Akzeptiert wird ein 2022 KBV Bundle</p></li>
<li><p>Akzeptiert wird ein 2023 KBV Bundle</p></li>
</ul>
<p>Workflow 200/209 (PKV):</p>
<ul>
<li><p>Akzeptiert wird ein 2023 KBV Bundle</p></li>
</ul>
<p>Response</p>
<ul>
<li><p>FD antwortet mit einem Task gemäß FHIR 2023</p></li>
</ul></td>
<td style="text-align: left;"><p>Request</p>
<ul>
<li><p>Akzeptiert wird ein 2023 KBV Bundle</p></li>
</ul>
<p>Response</p>
<ul>
<li><p>FD antwortet mit einem Task gemäß FHIR 2023</p></li>
</ul></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>POST
/Task/&lt;id&gt;/$abort</strong></p></td>
<td style="text-align: left;"><p>verordnende LEI</p></td>
<td style="text-align: left;"><p>Request</p>
<ul>
<li><p>n/a</p></li>
</ul>
<p>Response</p>
<ul>
<li><p>n/a - no content</p></li>
</ul></td>
<td style="text-align: left;"><p>Request</p>
<ul>
<li><p>n/a</p></li>
</ul>
<p>Response</p>
<ul>
<li><p>n/a - no content</p></li>
</ul></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>GET /Task</strong></p></td>
<td style="text-align: left;"><p>Versicherte</p></td>
<td style="text-align: left;"><p>Request</p>
<ul>
<li><p>n/a</p></li>
</ul>
<p>Response</p>
<ul>
<li><p>Bundle of Tasks gemäß FHIR 2023</p></li>
</ul></td>
<td style="text-align: left;"><p>Request</p>
<ul>
<li><p>n/a</p></li>
</ul>
<p>Response</p>
<ul>
<li><p>Bundle of Tasks gemäß FHIR 2023</p></li>
</ul></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>POST
/Task/&lt;id&gt;/$abort</strong></p></td>
<td style="text-align: left;"><p>Versicherte</p></td>
<td style="text-align: left;"><p>Request</p>
<ul>
<li><p>n/a</p></li>
</ul>
<p>Response</p>
<ul>
<li><p>n/a - no content</p></li>
</ul></td>
<td style="text-align: left;"><p>Request</p>
<ul>
<li><p>n/a</p></li>
</ul>
<p>Response</p>
<ul>
<li><p>n/a - no content</p></li>
</ul></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>POST
/Communication</strong></p></td>
<td style="text-align: left;"><p>Versicherte</p></td>
<td style="text-align: left;"><p>Request</p>
<p><span class=".underline">DispReq</span></p>
<ul>
<li><p>2022 FHIR Communication</p></li>
<li><p>2023 FHIR Communication</p></li>
</ul>
<p><span class=".underline">InfoReq</span></p>
<ul>
<li><p>Implementierung in der App erfolgt Q3/Q4 2023</p></li>
<li><p>2023 FHIR Communication mit 2022 KBV Medication</p></li>
<li><p>2023 FHIR Communication mit 2023 KBV Medication</p></li>
</ul>
<p>Response</p>
<ul>
<li><p>Der FD antwortet mit der Communication mit den Profilversionen,
wie sie eingestellt wurde</p></li>
</ul></td>
<td style="text-align: left;"><p>Der ERP-FD müsste zumindest die "2022
KBV Medication" akzeptieren, bis diese abgelaufen sind. Das kann bei MVO
1 Jahr + &lt;Dauer Übergangszeit&gt; nach Gültigkeit der Fall sein.</p>
<p>Request</p>
<p><span class=".underline">DispReq</span></p>
<ul>
<li><p>2023 FHIR Communication</p></li>
</ul>
<p><span class=".underline">InfoReq</span></p>
<ul>
<li><p>Implementierung erfolgt in der App voraussichtlich Q3/Q4
2023</p></li>
<li><p>2023 FHIR Communication mit 2022 KBV Medication</p>
<ul>
<li><p>bis 30.12.2024</p></li>
<li><p>ergibt sich aus: Ende Übergangszeitraum + 1 Jahr (MVO)</p></li>
</ul></li>
<li><p>2023 FHIR Communication mit 2023 KBV Medication</p></li>
</ul>
<p>Response</p>
<ul>
<li><p>Der FD antwortet mit der Communication mit den Profilversionen,
wie sie eingestellt wurde</p></li>
</ul></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>GET
/Communication</strong></p></td>
<td style="text-align: left;"><p>Versicherte</p></td>
<td style="text-align: left;"><p>Request</p>
<ul>
<li><p>n/a</p></li>
</ul>
<p>Response</p>
<p><span class=".underline">DispReq</span></p>
<ul>
<li><p>2022 FHIR Communication</p></li>
<li><p>2023 FHIR Communication</p></li>
</ul>
<p><span class=".underline">InfoReq</span></p>
<ul>
<li><p>Implementierung in der App erfolgt Q3/Q4 2023</p></li>
<li><p>2023 FHIR Communication mit 2022 KBV_Medication</p></li>
<li><p>2023 FHIR Communication mit 2023 KBV_Medication</p></li>
</ul>
<p><span class=".underline">Communication_Reply</span></p>
<ul>
<li><p>2022 FHIR Communication</p></li>
<li><p>2023 FHIR Communication</p></li>
</ul>
<p>Der FD antwortet mit der Communication mit den Profilversionen, wie
sie eingestellt wurden.</p></td>
<td style="text-align: left;"><p>Request</p>
<ul>
<li><p>n/a</p></li>
</ul>
<p>Response</p>
<p><span class=".underline">DispReq</span></p>
<ul>
<li><p>2023 FHIR Communication</p></li>
</ul>
<p><span class=".underline">InfoReq</span></p>
<ul>
<li><p>Implementierung in der App erfolgt Q3/Q4 2023</p></li>
<li><p>2023 FHIR Communication mit 2022 KBV_Medication</p></li>
<li><p>2023 FHIR Communication mit 2023 KBV_Medication</p></li>
</ul>
<p><span class=".underline">Communication_Reply</span></p>
<ul>
<li><p>2023 FHIR Communication</p></li>
</ul>
<p>Der FD antwortet mit der Communication mit den Profilversionen, wie
sie eingestellt wurden.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>GET
/AuditEvent</strong></p></td>
<td style="text-align: left;"><p>Versicherte</p></td>
<td style="text-align: left;"><p>Request</p>
<ul>
<li><p>n/a</p></li>
</ul>
<p>Response</p>
<ul>
<li><p>Bundle of AuditEvents gemäß FHIR 2023</p></li>
</ul></td>
<td style="text-align: left;"><p>Request</p>
<ul>
<li><p>n/a</p></li>
</ul>
<p>Response</p>
<ul>
<li><p>Bundle of AuditEvents gemäß FHIR 2023</p></li>
</ul></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>GET
/Task/&lt;id&gt;</strong></p></td>
<td style="text-align: left;"><p>Versicherte</p></td>
<td style="text-align: left;"><p>Request</p>
<ul>
<li><p>n/a</p></li>
</ul>
<p>Response</p>
<p>Der FD antwortet mit einem Bundle bestehend aus Task und KBV
Bundle</p>
<ul>
<li><p>Task gemäß FHIR 2023 Profil</p></li>
<li><p>KBV Bundle 2022 FHIR oder KBV Bundle 2023 FHIR</p></li>
</ul></td>
<td style="text-align: left;"><p>Request</p>
<ul>
<li><p>n/a</p></li>
</ul>
<p>Response</p>
<p>Der FD antwortet mit einem Bundle bestehend aus Task und KBV
Bundle</p>
<ul>
<li><p>Task gemäß FHIR 2023 Profil mit</p>
<ul>
<li><p>KBV Bundle 2022 FHIR</p>
<ul>
<li><p>bis 09.04.2025</p></li>
<li><p>ergibt sich aus: Ende Übergangszeitraum + MVO (1 Jahr) +
Löschfrist (100 Tage)</p></li>
</ul></li>
<li><p>oder KBV Bundle 2023 FHIR</p></li>
</ul></li>
</ul></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>GET
/ChargeItem/&lt;id&gt;</strong></p></td>
<td style="text-align: left;"><p>Versicherte</p></td>
<td style="text-align: left;"><p>pkv</p></td>
<td style="text-align: left;"><p>pkv</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>DELETE
/Communication/&lt;id&gt;</strong></p></td>
<td style="text-align: left;"><p>Versicherte</p></td>
<td style="text-align: left;"><p>Request</p>
<ul>
<li><p>n/a</p></li>
</ul>
<p>Response</p>
<ul>
<li><p>n/a</p></li>
</ul></td>
<td style="text-align: left;"><p>Request</p>
<ul>
<li><p>n/a</p></li>
</ul>
<p>Response</p>
<ul>
<li><p>n/a</p></li>
</ul></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>GET
/MedicationDispense</strong></p></td>
<td style="text-align: left;"><p>Versicherte</p></td>
<td style="text-align: left;"><p>Request</p>
<ul>
<li><p>akzeptiert PrescriptionId gemäß</p>
<ul>
<li><p>2022 Namespace</p></li>
<li><p>2023 Namespace</p></li>
</ul></li>
</ul>
<p>Response</p>
<ul>
<li><p>Bundle von MedicationDispenses (wie vom AVS eingestellt)</p>
<ul>
<li><p>MedicationDispense 2022 mit 2022 KBV_Medication</p></li>
<li><p>MedicationDispense 2022 mit 2023 KBV_Medication</p></li>
<li><p>MedicationDispense 2023 mit 2022 KBV_Medication</p></li>
<li><p>MedicationDispense 2023 mit 2023 KBV_Medication</p></li>
</ul></li>
</ul></td>
<td style="text-align: left;"><p>Request</p>
<ul>
<li><p>akzeptiert PrescriptionId gemäß</p>
<ul>
<li><p>2022 Namespace (bis 01.07.2024)</p></li>
<li><p>2023 Namespace</p></li>
</ul></li>
</ul>
<p>Response</p>
<ul>
<li><p>Bundle von MedicationDispenses (wie vom AVS eingestellt)</p>
<ul>
<li><p>MedicationDispense 2023 mit 2022 KBV_Medication</p>
<ul>
<li><p>bis 30.01.2025</p></li>
<li><p>ergibt sich aus: Ende Übergangszeitraum + MVO (1 Jahr) +
Einlösezeit der Apotheken (1 Monat)</p></li>
</ul></li>
<li><p>MedicationDispense 2023 mit 2023 KBV_Medication</p></li>
</ul></li>
</ul></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>GET
/ChargeItem</strong></p></td>
<td style="text-align: left;"><p>Versicherte</p></td>
<td style="text-align: left;"><p>pkv</p></td>
<td style="text-align: left;"><p>pkv</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>DELETE
/ChargeItem/&lt;id&gt;</strong></p></td>
<td style="text-align: left;"><p>Versicherte</p></td>
<td style="text-align: left;"><p>pkv</p></td>
<td style="text-align: left;"><p>pkv</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>PATCH
/ChargeItem/&lt;id&gt;</strong></p></td>
<td style="text-align: left;"><p>Versicherte</p></td>
<td style="text-align: left;"><p>pkv</p></td>
<td style="text-align: left;"><p>pkv</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>GET /Consent</strong></p></td>
<td style="text-align: left;"><p>Versicherte</p></td>
<td style="text-align: left;"><p>pkv</p></td>
<td style="text-align: left;"><p>pkv</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>POST /Consent</strong></p></td>
<td style="text-align: left;"><p>Versicherte</p></td>
<td style="text-align: left;"><p>pkv</p></td>
<td style="text-align: left;"><p>pkv</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>DELETE
/Consent</strong></p></td>
<td style="text-align: left;"><p>Versicherte</p></td>
<td style="text-align: left;"><p>pkv</p></td>
<td style="text-align: left;"><p>pkv</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>POST
/Task/&lt;id&gt;/$accept</strong></p></td>
<td style="text-align: left;"><p>abgebende LEI</p></td>
<td style="text-align: left;"><p>Request</p>
<ul>
<li><p>n/a</p></li>
</ul>
<p>Response</p>
<p>&lt;Bundle&gt; mit Tasks und PKCS7 Datei mit Verordnung</p>
<ul>
<li><p>Task gemäß FHIR 2023</p></li>
<li><p>KBV Bundle FHIR 2022 oder FHIR 2023</p></li>
</ul></td>
<td style="text-align: left;"><p>Request</p>
<ul>
<li><p>n/a</p></li>
</ul>
<p>Response</p>
<p>&lt;Bundle&gt; mit Tasks und PKCS7 Datei mit Verordnung</p>
<ul>
<li><p>Task gemäß FHIR 2023</p></li>
<li><p>Die Verordnung ist wie vom Arzt eingestellt</p>
<ul>
<li><p>KBV Bundle FHIR 2022</p>
<ul>
<li><p>bis 30.12.2024</p></li>
<li><p>ergibt sich aus: Ende Übergangszeitraum + MVO (1 Jahr)</p></li>
</ul></li>
<li><p>KBV Bundle FHIR 2023</p></li>
</ul></li>
</ul></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>POST
/Task/&lt;id&gt;/$reject</strong></p></td>
<td style="text-align: left;"><p>abgebende LEI</p></td>
<td style="text-align: left;"><p>Request</p>
<ul>
<li><p>n/a</p></li>
</ul>
<p>Response</p>
<ul>
<li><p>n/a - no content</p></li>
</ul></td>
<td style="text-align: left;"><p>Request</p>
<ul>
<li><p>n/a</p></li>
</ul>
<p>Response</p>
<ul>
<li><p>n/a - no content</p></li>
</ul></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>POST
/Task/&lt;id&gt;/$abort</strong></p></td>
<td style="text-align: left;"><p>abgebende LEI</p></td>
<td style="text-align: left;"><p>Request</p>
<ul>
<li><p>n/a</p></li>
</ul>
<p>Response</p>
<ul>
<li><p>n/a - no content</p></li>
</ul></td>
<td style="text-align: left;"><p>Request</p>
<ul>
<li><p>n/a</p></li>
</ul>
<p>Response</p>
<ul>
<li><p>n/a - no content</p></li>
</ul></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>POST
/Task/&lt;id&gt;/$close</strong></p></td>
<td style="text-align: left;"><p>abgebende LEI</p></td>
<td style="text-align: left;"><p>Request</p>
<ul>
<li><p>&lt;MedicationDispense&gt; bzw. Bundle von MedicationDispense -
FHIR 2023</p>
<ul>
<li><p>enthält 2022 KBV Medication</p></li>
<li><p>enthält 2023 KBV Medication</p></li>
</ul></li>
</ul>
<p>Response</p>
<ul>
<li><p>&lt;Bundle&gt; mit PKCS7 mit Quittung - FHIR 2023</p></li>
</ul></td>
<td style="text-align: left;"><p>Request</p>
<ul>
<li><p>&lt;MedicationDispense&gt; bzw. Bundle von MedicationDispense -
FHIR 2023</p>
<ul>
<li><p>enthält 2022 KBV Medication</p>
<ul>
<li><p>bis 09.04.2025</p></li>
<li><p>ergibt sich aus: Ende Übergangszeitraum + MVO (1 Jahr) +
Löschfrist (100 Tage)</p></li>
</ul></li>
<li><p>enthält 2023 KBV Medication</p></li>
</ul></li>
</ul>
<p>Response</p>
<ul>
<li><p>&lt;Bundle&gt; mit PKCS7 mit Quittung - FHIR 2023</p></li>
</ul></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>POST
/Communication</strong></p></td>
<td style="text-align: left;"><p>abgebende LEI</p></td>
<td style="text-align: left;"><p>Request</p>
<ul>
<li><p>2022 FHIR Communication</p></li>
<li><p>2023 FHIR Communication</p></li>
</ul>
<p>Response</p>
<ul>
<li><p>Der FD antwortet mit der Communication mit den Profilversionen,
wie sie eingestellt wurde</p></li>
</ul></td>
<td style="text-align: left;"><p>Request</p>
<ul>
<li><p>2023 FHIR Communication</p></li>
</ul>
<p>Response</p>
<ul>
<li><p>Der FD antwortet mit der Communication mit den Profilversionen,
wie sie eingestellt wurde</p></li>
</ul></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>GET
/Task/&lt;id&gt;</strong></p></td>
<td style="text-align: left;"><p>abgebende LEI</p></td>
<td style="text-align: left;"><p>Request</p>
<ul>
<li><p>n/a</p></li>
</ul>
<p>Response</p>
<ul>
<li><p>&lt;Bundle&gt; mit PKCS7 mit Quittung - FHIR 2022 (falls
ursprünglich vor dem 01.07. erzeugt)</p></li>
<li><p>&lt;Bundle&gt; mit PKCS7 mit Quittung - FHIR 2023</p></li>
</ul></td>
<td style="text-align: left;"><p>Request</p>
<ul>
<li><p>n/a</p></li>
</ul>
<p>Response</p>
<ul>
<li><p>&lt;Bundle&gt; mit PKCS7 mit Quittung - FHIR 2023</p></li>
</ul></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>DELETE
/Communication/&lt;id&gt;</strong></p></td>
<td style="text-align: left;"><p>abgebende LEI</p></td>
<td style="text-align: left;"><p>Request</p>
<ul>
<li><p>n/a</p></li>
</ul>
<p>Response</p>
<ul>
<li><p>n/a - no content</p></li>
</ul></td>
<td style="text-align: left;"><p>Request</p>
<ul>
<li><p>n/a</p></li>
</ul>
<p>Response</p>
<ul>
<li><p>n/a - no content</p></li>
</ul></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>GET
/ChargeItem/&lt;id&gt;</strong></p></td>
<td style="text-align: left;"><p>abgebende LEI</p></td>
<td style="text-align: left;"><p>pkv</p></td>
<td style="text-align: left;"><p>pkv</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>POST
/ChargeItem</strong></p></td>
<td style="text-align: left;"><p>abgebende LEI</p></td>
<td style="text-align: left;"><p>pkv</p></td>
<td style="text-align: left;"><p>pkv</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>GET /Task</strong></p></td>
<td style="text-align: left;"><p>abgebende LEI</p></td>
<td style="text-align: left;"><p>Request</p>
<ul>
<li><p>n/a</p></li>
</ul>
<p>Response</p>
<ul>
<li><p>Bundle of Tasks gemäß FHIR 2023</p></li>
</ul></td>
<td style="text-align: left;"><p>Request</p>
<ul>
<li><p>n/a</p></li>
</ul>
<p>Response</p>
<ul>
<li><p>Bundle of Tasks gemäß FHIR 2023</p></li>
</ul></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>PUT
/ChargeItem/&lt;id&gt;</strong></p></td>
<td style="text-align: left;"><p>abgebende LEI</p></td>
<td style="text-align: left;"><p>pkv</p></td>
<td style="text-align: left;"><p>pkv</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>POST
/Subscription</strong></p></td>
<td style="text-align: left;"><p>abgebende LEI</p></td>
<td style="text-align: left;"><p>Request</p>
<ul>
<li><p>2022 FHIR Subscription</p></li>
<li><p>2023 FHIR Subscription</p></li>
</ul>
<p>Response</p>
<ul>
<li><p>2023 FHIR Subscription</p></li>
</ul></td>
<td style="text-align: left;"><p>Request</p>
<ul>
<li><p>2023 FHIR Subscription</p></li>
</ul>
<p>Response</p>
<ul>
<li><p>2023 FHIR Subscription</p></li>
</ul></td>
</tr>
</tbody>
</table>
