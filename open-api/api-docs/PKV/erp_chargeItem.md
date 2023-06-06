Hier dokumentiert die gematik die Nutzung der Schnittstellen rund um das
E-Rezept für die elektronische Verarbeitung und Speicherung von
Abrechnungsinformationen für PKV-Versicherte.

# Profilierung

Für diesen Anwendungsfall wird die FHIR-Ressource "ChargeItem":
<http://hl7.org/fhir/chargeitem.html> profiliert. Die Profile können als
JSON- oder XML-Datei hier eingesehen werden:
<https://simplifier.net/erezept-patientenrechnung/gem-erpchrg-pr-chargeitem>

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
style="text-align: left;"><p><strong>ChargeItem</strong></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>extension.markingFlag</p></td>
<td style="text-align: left;"><p>Boolsche Werte für den Versicherten zum
Markieren, ob das ChargeItem bei Institutionen eingereicht
wurde</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>identifier.PrescriptionId</p></td>
<td style="text-align: left;"><p>ID des ChargeItems, zugleich
Rezept-ID</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>identifier.AccessCode</p></td>
<td style="text-align: left;"><p>Geheimnis zum Ändern des
ChargeItems</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>status</p></td>
<td style="text-align: left;"><p>Status des ChargeItems. Fester Wert auf
"billable"</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>code</p></td>
<td style="text-align: left;"><p>Pflichtfeld, welches nicht verwendet
wird. Verwenden Sie das Codesystem <a
href="http://terminology.hl7.org/CodeSystem/data-absent-reason#not-applicable">http://terminology.hl7.org/CodeSystem/data-absent-reason#not-applicable</a>.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>subject</p></td>
<td style="text-align: left;"><p>Versicherten-ID des
PKV-Patienten</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>enterer</p></td>
<td style="text-align: left;"><p>Telematik-ID der abgebenden
LEI</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>enteredDate</p></td>
<td style="text-align: left;"><p>Zeitstempel der Erstellung eines
ChargeItem</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>supportingInformation</p></td>
<td style="text-align: left;"><p>Referenz auf die drei Bestandteile der
Abrechnungsinformationen (Verordnungs-, Abgabedatensatz und die
Quittung)</p></td>
</tr>
</tbody>
</table>

In den folgenden Kapiteln wird erläutert, wann und wie die Befüllung
dieser Attribute erfolgt.

# Anwendungsfall PKV-Abrechnungsinformationen durch den abgebenden Leistungserbringer bereitstellen

Als Apotheker möchte ich dem Versicherten seine Abrechnungsinformationen
bereitstellen. Die Abrechnungsinformationen werden über die
FHIR-Ressource "ChargeItem" abgebildet. Das ChargeItem enthält
Referenzen auf die dazugehörenden Datensätze (als Bundle abgebildet),
Verordnungsdatensatz, Abgabedatensatz und die Quittung. Der
Abgabedatensatz wird als Contained-Objekt in dem ChargeItem mitgegeben.
Der E-Rezept-Fachdienst extrahiert dieses Binary, speichert es gesondert
ab und erstellt eine Referenz in der ChargeItem-Resource. Das Attribut
"ChargeItem.Code" ist nach dem FHIR-Standard ein Pflichtfeld, wird aber
in diesem Kontext fachlich nicht benötigt. Deshalb wird hier ein
Platzhalter-Codesystem angewendet.

Der Aufruf erfolgt als http-`POST`-Operation auf die Ressource
`/ChargeItem`. Im http-Request-Header Authorization muss das während der
Authentisierung erhaltene ACCESS\_TOKEN übergeben werden. Als
URL-Parameter ?secret=…​ muss das beim Abrufen des E-Rezepts (`$accept`)
im Task generierte Secret für die Berechtigungsprüfung übergeben werden.

**Request**

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>¦URI
¦https://prescriptionserver.telematik/ChargeItem?task=200.086.824.605.539.20&amp;secret=c36ca26502892b371d252c99b496e31505ff449aca9bc69e231c58148f6233cf<br />
Mit dem Parameter <code>task=...</code> wird die Zuordnung zum Task des
eingelösten Rezepts hergestellt.<br />
Zum Nachweis als berechtigte Apotheke, die das E-Rezept gerade in
Bearbeitung hält, muss im URL-Parameter <code>secret</code> das beim
Abrufen generierte Secret übergeben werden. ¦Method ¦POST ¦HTTP Header ¦
---- Content-Type: application/fhir+xml; charset=UTF-8 Authorization:
Bearer eyJraWQ.ewogImL2pA10Qql22ddtutrvx4FsDlz.rHQjEmB1lLmpqn9J ----
NOTE: Mit dem ACCESS_TOKEN im <code>Authorization</code>-Header weist
sich der Zugreifende als Apotheke aus, im Token ist die
<code>TelematikID</code> und <code>professionOID</code> für die
Rollenprüfung enthalten. Die Base64-Darstellung des Tokens ist stark
gekürzt.</p>
<p>NOTE: Im http-Header des äußeren http-Requests an die VAU (POST /VAU)
sind die Header <code>X-erp-user: l</code> (kleines L) und
<code>X-erp-resource: ChargeItem</code> zu setzen.</p>
<p>NOTE: In den Profilen ist unter meta.profile auch die Version mit
anzugeben. (Bsp.:
"https://gematik.de/fhir/erpchrg/StructureDefinition/GEM_ERPCHRG_PR_ChargeItem</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>1.0</strong>")</p>
<p>¦Payload ¦ [source,xml] ---- &lt;ChargeItem
xmlns="http://hl7.org/fhir"&gt; &lt;meta&gt; &lt;profile
value="https://gematik.de/fhir/erpchrg/StructureDefinition/GEM_ERPCHRG_PR_ChargeItem</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>1.0" /&gt; &lt;/meta&gt;
&lt;contained&gt; &lt;Binary&gt; &lt;id value="Abg123"/&gt;
&lt;contentType value="application/pkcs7-mime" /&gt; &lt;data value=
"bWVycnkgY2hyaXN0bWFz"/&gt; &lt;/Binary&gt; &lt;/contained&gt;
&lt;identifier&gt; &lt;system
value="https://gematik.de/fhir/erp/NamingSystem/GEM_ERP_NS_PrescriptionId"
/&gt; &lt;value value="200.086.824.605.539.20" /&gt; &lt;/identifier&gt;
&lt;status value="billable" /&gt; &lt;code&gt; &lt;coding&gt; &lt;system
value="http://terminology.hl7.org/CodeSystem/data-absent-reason" /&gt;
&lt;code value="not-applicable" /&gt; &lt;/coding&gt; &lt;/code&gt;
&lt;subject&gt; &lt;identifier&gt; &lt;system
value="http://fhir.de/sid/pkv/kvid-10"/&gt; &lt;value value="X234567890"
/&gt; &lt;assigner&gt; &lt;display value="Name einer privaten
Krankenversicherung" /&gt; &lt;/assigner&gt; &lt;/identifier&gt;
&lt;/subject&gt; &lt;enterer&gt; &lt;identifier&gt; &lt;system
value="https://gematik.de/fhir/sid/telematik-id" /&gt; &lt;value
value="3-15.2.1456789123.191" /&gt; &lt;/identifier&gt; &lt;/enterer&gt;
&lt;enteredDate value="2022-06-01T07:13:00+05:00"/&gt;
&lt;supportingInformation&gt; &lt;reference value="Abg123" /&gt;
&lt;display value="Binary" /&gt; &lt;/supportingInformation&gt;
&lt;/ChargeItem&gt; ---- NOTE: Der PKV-Abgabesatz in Binary.data ist aus
Platzgründen stark gekürzt.</p>
<p>NOTE: In <code>&lt;id value="Abg123"/&gt;</code> befindet sich der
Abgabgedatensatz als Contained-Bundle. Das Contained-Bundle wird später
durch den Fachdienst als eigenständiges Bundle in
"supportingInformation" referenziert.</p>
<p>NOTE: In <code>&lt;value value="X234567890"/&gt;</code> findet sich
die Angabe eines PKV-Identifier.</p>
<p>NOTE: <code>&lt;reference value="#Abg123"/&gt;</code> enthält die
Referenz auf das Contained-Objekt. Das Symbol <em></em> sagt dabei aus,
dass es sich auf eine lokale Referenz innerhalb des Objektes
bezieht.</p></td>
</tr>
</tbody>
</table>

**Response**

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>¦HTTP Status Code¦201 Created ¦HTTP
Header ¦Content-Type: application/fhir+xml;charset=utf-8 ¦Payload¦
[source,xml] ---- &lt;ChargeItem xmlns="http://hl7.org/fhir"&gt; &lt;id
value="abc825bc-bc30-45f8-b109-1b343fff5c45" /&gt; &lt;meta&gt;
&lt;profile
value="https://gematik.de/fhir/erpchrg/StructureDefinition/GEM_ERPCHRG_PR_ChargeItem</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>1.0" /&gt; &lt;tag&gt; &lt;display
value="Example of an ChargeItem." /&gt; &lt;/tag&gt; &lt;/meta&gt;
&lt;identifier&gt; &lt;system
value="https://gematik.de/fhir/erp/NamingSystem/GEM_ERP_NS_PrescriptionId"
/&gt; &lt;value value="200.086.824.605.539.20" /&gt; &lt;/identifier&gt;
&lt;status value="billable" /&gt; &lt;code&gt; &lt;coding&gt; &lt;system
value="http://terminology.hl7.org/CodeSystem/data-absent-reason" /&gt;
&lt;code value="not-applicable" /&gt; &lt;/coding&gt; &lt;/code&gt;
&lt;subject&gt; &lt;identifier&gt; &lt;system
value="http://fhir.de/sid/pkv/kvid-10"/&gt; &lt;value value="X234567890"
/&gt; &lt;assigner&gt; &lt;display value="Name einer privaten
Krankenversicherung" /&gt; &lt;/assigner&gt; &lt;/identifier&gt;
&lt;/subject&gt; &lt;enterer&gt; &lt;identifier&gt; &lt;system
value="https://gematik.de/fhir/sid/telematik-id" /&gt; &lt;value
value="3-15.2.1456789123.191" /&gt; &lt;/identifier&gt; &lt;/enterer&gt;
&lt;enteredDate value="2022-06-01T07:13:00+05:00"/&gt;
&lt;supportingInformation&gt; &lt;reference
value="Bundle/a5142020-7b59-4674-9b02-08f68c583610"/&gt; &lt;display
value="http://fhir.abda.de/eRezeptAbgabedaten/StructureDefinition/DAV-PKV-PR-ERP-AbgabedatenBundle"/&gt;
&lt;/supportingInformation&gt; &lt;/ChargeItem&gt; ----</p></td>
</tr>
</tbody>
</table>

Status Codes

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
<td style="text-align: left;"><p>Created<br />
<span class="small">Die Anfrage wurde erfolgreich
bearbeitet.</span></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>Code</p></td>
<td style="text-align: left;"><p>Type Error</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>400</p></td>
<td style="text-align: left;"><p>Bad Request<br />
<span class="small">Die Anfrage-Nachricht war fehlerhaft aufgebaut.
Mögliche Gründe: Fehlender URL-Parameter task; Die übermittelte
ChargeItem-Ressource ist nicht schema-konform.; Der übermittelte
PKV-Abgabedatensatz ist nicht schema-konform.; Die Signatur des
PKV-Abgabedatensatzes konnte nicht erfolgreich validiert werden.; Der
referenzierte Task entspricht nicht den zulässigen
FlowTypes.</span></p></td>
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
nicht durchgeführt. Mögliche Gründe: Der authentifizierte Benutzer ist
nicht berechtigt; Es liegt keine Einwilligung zum Speichern der
Abrechnungsinformationen durch den Versicherten vor.; Fehlender
URL-Parameter secret; Der in secret übermittelte Wert stimmt nicht mit
dem Geheimnis in Task.secret überein.</span></p></td>
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
<td style="text-align: left;"><p>409</p></td>
<td style="text-align: left;"><p>Conflict<br />
<span class="small">Die Anfrage wurde unter falschen Annahmen gestellt.
Es wurde kein entsprechendes Task-Objekt mit dem Status Task.status =
completed gefunden.</span></p></td>
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

# Anwendungsfall Abrechnungsinformation zum Ändern abrufen

Falls die Abrechnung eine Korrektur benötigt, kann der Versicherte die
Apotheke um eine Änderung des PKV-Abgabedatensatzes bitten. Hierzu
übermittelt der Versicherte der Apotheke den AccessCode zum Ändern
mittels einer Nachricht über das E-Rezept-FdV oder durch Anzeige zum
Abscannen im E-Rezept-FdV. Mit diesem AccessCode ruft die Apotheke die
Daten des zu ändernden PKV-Abgabedatensatz vom E-Rezept-Fachdienst ab.

Rückgabewert ist ein Bundle, welches folgende Einträge enthält:

-   das ChargeItem

-   den Verordnungsdatensatz mit der QES des Verordnenden in .signature

-   den Abgabedatensatz mit seiner ursprünglich eingestellten Signatur
    in .signature

Der Aufruf erfolgt als http-`GET`-Operation auf die Ressource
`/ChargeItem/'PrescriptionID'`. Im Aufruf muss das während der
Authentisierung erhaltene ACCESS\_TOKEN im http-Request-Header
`Authorization` übergeben werden, der Fachdienst filtert die
ChargeItem-Einträge nach der im ACCESS\_TOKEN enthaltenen KVNR des
Versicherten.

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
href="https://prescriptionserver.telematik/ChargeItem/200.000.000.022.127.38?ac=777bea0e13cc9c42ceec14aec3ddee2263325dc2c6c699db115f58fe423607ea">https://prescriptionserver.telematik/ChargeItem/200.000.000.022.127.38?ac=777bea0e13cc9c42ceec14aec3ddee2263325dc2c6c699db115f58fe423607ea</a></p></td>
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
</div></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>Payload</strong></p></td>
<td style="text-align: left;"><pre><code>-</code></pre></td>
</tr>
</tbody>
</table>

**Response**

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>¦HTTP Status Code¦200 OK ¦HTTP Header
¦Content-Type: application/fhir+xml;charset=utf-8 ¦Payload ¦
[source,xml] ---- &lt;?xml version="1.0" encoding="utf-8"?&gt;
&lt;Bundle xmlns="http://hl7.org/fhir"&gt; &lt;id
value="60f3d654-0a8c-457a-baf1-c3021f55cea5" /&gt; &lt;type
value="collection" /&gt; &lt;timestamp
value="2023-03-07T15:41:28.916+00:00" /&gt; &lt;entry&gt; &lt;fullUrl
value="https://erp.zentral.erp.splitdns.ti-dienste.de/ChargeItem/200.000.000.022.127.38"
/&gt; &lt;resource&gt; &lt;ChargeItem&gt; &lt;id
value="200.000.000.022.127.38" /&gt; &lt;meta&gt; &lt;profile
value="https://gematik.de/fhir/erpchrg/StructureDefinition/GEM_ERPCHRG_PR_ChargeItem</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>1.0" /&gt; &lt;/meta&gt;
&lt;identifier&gt; &lt;system
value="https://gematik.de/fhir/erp/NamingSystem/GEM_ERP_NS_PrescriptionId"
/&gt; &lt;value value="200.000.000.022.127.38" /&gt; &lt;/identifier&gt;
&lt;status value="billable" /&gt; &lt;code&gt; &lt;coding&gt; &lt;system
value="http://terminology.hl7.org/CodeSystem/data-absent-reason" /&gt;
&lt;code value="not-applicable" /&gt; &lt;/coding&gt; &lt;/code&gt;
&lt;subject&gt; &lt;identifier&gt; &lt;system
value="http://fhir.de/sid/pkv/kvid-10" /&gt; &lt;value
value="X276456719" /&gt; &lt;/identifier&gt; &lt;/subject&gt;
&lt;enterer&gt; &lt;identifier&gt; &lt;system
value="https://gematik.de/fhir/sid/telematik-id" /&gt; &lt;value
value="23456799" /&gt; &lt;/identifier&gt; &lt;/enterer&gt;
&lt;enteredDate value="2023-03-07T15:41:28.158+00:00" /&gt;
&lt;supportingInformation&gt; &lt;reference
value="urn:uuid:c86f5600-0000-0000-0001-000000000000" /&gt; &lt;display
value="https://fhir.kbv.de/StructureDefinition/KBV_PR_ERP_Bundle" /&gt;
&lt;/supportingInformation&gt; &lt;supportingInformation&gt;
&lt;reference value="urn:uuid:c86f5600-0000-0000-0004-000000000000"
/&gt; &lt;display
value="http://fhir.abda.de/eRezeptAbgabedaten/StructureDefinition/DAV-PKV-PR-ERP-AbgabedatenBundle"
/&gt; &lt;/supportingInformation&gt; &lt;/ChargeItem&gt;
&lt;/resource&gt; &lt;/entry&gt; &lt;entry&gt; &lt;fullUrl
value="urn:uuid:c86f5600-0000-0000-0004-000000000000" /&gt;
&lt;resource&gt; &lt;Bundle&gt; &lt;id
value="abc825bc-bc30-45f8-b109-1b343fff5c45" /&gt; &lt;meta&gt;
&lt;profile
value="http://fhir.abda.de/eRezeptAbgabedaten/StructureDefinition/DAV-PKV-PR-ERP-AbgabedatenBundle</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>1.2"/&gt; &lt;tag&gt; &lt;display
value="ACHTUNG! Der fachlich korrekte Inhalt der Beispielinstanz kann
nicht gewährleistet werden. Wir sind jederzeit dankbar für Hinweise auf
Fehler oder für Verbesserungsvorschläge."/&gt; &lt;/tag&gt;
&lt;/meta&gt; &lt;identifier&gt; &lt;system
value="https://gematik.de/fhir/erp/NamingSystem/GEM_ERP_NS_PrescriptionId"/&gt;
&lt;value value="200.000.000.022.127.38"/&gt; &lt;/identifier&gt;
&lt;type value="document"/&gt; &lt;timestamp
value="2023-07-03T11:30:00Z"/&gt; &lt;entry&gt; &lt;fullUrl
value="urn:uuid:a6deb8d4-a41e-484f-b1aa-47c8a96d88fd"/&gt;
&lt;resource&gt; &lt;Composition&gt; &lt;id
value="a6deb8d4-a41e-484f-b1aa-47c8a96d88fd"/&gt; &lt;meta&gt;
&lt;profile
value="http://fhir.abda.de/eRezeptAbgabedaten/StructureDefinition/DAV-PKV-PR-ERP-AbgabedatenComposition</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>1.2"/&gt; &lt;/meta&gt; &lt;status
value="final"/&gt; &lt;type&gt; &lt;coding&gt; &lt;system
value="http://fhir.abda.de/eRezeptAbgabedaten/CodeSystem/DAV-CS-ERP-CompositionTypes"/&gt;
&lt;code value="ERezeptAbgabedaten"/&gt; &lt;/coding&gt; &lt;/type&gt;
&lt;date value="2023-07-03T11:30:00Z"/&gt; &lt;author&gt; &lt;reference
value="urn:uuid:016a3696-bb88-4e94-8f91-05146a04d028"/&gt;
&lt;/author&gt; &lt;title value="ERezeptAbgabedaten"/&gt;
&lt;section&gt; &lt;title value="Abgabeinformationen"/&gt; &lt;entry&gt;
&lt;reference value="urn:uuid:1c79f862-2ca0-498b-be44-05b6bd6dc0f9"/&gt;
&lt;/entry&gt; &lt;/section&gt; &lt;section&gt; &lt;title
value="Apotheke"/&gt; &lt;entry&gt; &lt;reference
value="urn:uuid:016a3696-bb88-4e94-8f91-05146a04d028"/&gt;
&lt;/entry&gt; &lt;/section&gt; &lt;/Composition&gt; &lt;/resource&gt;
&lt;/entry&gt; &lt;entry&gt; &lt;fullUrl
value="urn:uuid:016a3696-bb88-4e94-8f91-05146a04d028"/&gt;
&lt;resource&gt; &lt;Organization&gt; &lt;id
value="016a3696-bb88-4e94-8f91-05146a04d028"/&gt; &lt;meta&gt;
&lt;profile
value="http://fhir.abda.de/eRezeptAbgabedaten/StructureDefinition/DAV-PKV-PR-ERP-Apotheke</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>1.2"/&gt; &lt;/meta&gt;
&lt;identifier&gt; &lt;system
value="http://fhir.de/sid/arge-ik/iknr"/&gt; &lt;value
value="308412345"/&gt; &lt;/identifier&gt; &lt;name
value="Adler-Apotheke"/&gt; &lt;address&gt; &lt;type
value="physical"/&gt; &lt;line value="Taunusstraße 89"&gt; &lt;extension
url="http://hl7.org/fhir/StructureDefinition/iso21090-ADXP-streetName"&gt;
&lt;valueString value="Taunusstraße"/&gt; &lt;/extension&gt;
&lt;extension
url="http://hl7.org/fhir/StructureDefinition/iso21090-ADXP-houseNumber"&gt;
&lt;valueString value="89"/&gt; &lt;/extension&gt; &lt;/line&gt;
&lt;city value="Langen"/&gt; &lt;postalCode value="63225"/&gt;
&lt;country value="D"/&gt; &lt;/address&gt; &lt;/Organization&gt;
&lt;/resource&gt; &lt;/entry&gt; &lt;entry&gt; &lt;fullUrl
value="urn:uuid:1c79f862-2ca0-498b-be44-05b6bd6dc0f9"/&gt;
&lt;resource&gt; &lt;MedicationDispense&gt; &lt;id
value="1c79f862-2ca0-498b-be44-05b6bd6dc0f9"/&gt; &lt;meta&gt;
&lt;profile
value="http://fhir.abda.de/eRezeptAbgabedaten/StructureDefinition/DAV-PKV-PR-ERP-Abgabeinformationen</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>1.2"/&gt; &lt;/meta&gt; &lt;extension
url="http://fhir.abda.de/eRezeptAbgabedaten/StructureDefinition/DAV-EX-ERP-Abrechnungszeilen"&gt;
&lt;valueReference&gt; &lt;reference
value="urn:uuid:7ac4e17b-b87f-43ab-a9dc-f3c191c1c15d"/&gt;
&lt;/valueReference&gt; &lt;/extension&gt; &lt;extension
url="http://fhir.abda.de/eRezeptAbgabedaten/StructureDefinition/DAV-PKV-EX-ERP-AbrechnungsTyp"&gt;
&lt;valueCodeableConcept&gt; &lt;coding&gt; &lt;system
value="http://fhir.abda.de/eRezeptAbgabedaten/CodeSystem/DAV-PKV-CS-ERP-AbrechnungsTyp"/&gt;
&lt;code value="1"/&gt; &lt;/coding&gt; &lt;/valueCodeableConcept&gt;
&lt;/extension&gt; &lt;status value="completed"/&gt;
&lt;medicationCodeableConcept&gt; &lt;coding&gt; &lt;system
value="http://terminology.hl7.org/CodeSystem/data-absent-reason"/&gt;
&lt;code value="not-applicable"/&gt; &lt;/coding&gt;
&lt;/medicationCodeableConcept&gt; &lt;performer&gt; &lt;actor&gt;
&lt;reference value="urn:uuid:016a3696-bb88-4e94-8f91-05146a04d028"/&gt;
&lt;/actor&gt; &lt;/performer&gt; &lt;authorizingPrescription&gt;
&lt;identifier&gt; &lt;system
value="https://gematik.de/fhir/erp/NamingSystem/GEM_ERP_NS_PrescriptionId"/&gt;
&lt;value value="200.000.000.022.127.38"/&gt; &lt;/identifier&gt;
&lt;/authorizingPrescription&gt; &lt;type&gt; &lt;coding&gt; &lt;system
value="http://fhir.abda.de/eRezeptAbgabedaten/CodeSystem/DAV-CS-ERP-MedicationDispenseTyp"/&gt;
&lt;code value="Abgabeinformationen"/&gt; &lt;/coding&gt; &lt;/type&gt;
&lt;whenHandedOver value="2023-07-03"/&gt; &lt;/MedicationDispense&gt;
&lt;/resource&gt; &lt;/entry&gt; &lt;entry&gt; &lt;fullUrl
value="urn:uuid:7ac4e17b-b87f-43ab-a9dc-f3c191c1c15d"/&gt;
&lt;resource&gt; &lt;Invoice&gt; &lt;id
value="7ac4e17b-b87f-43ab-a9dc-f3c191c1c15d"/&gt; &lt;meta&gt;
&lt;profile
value="http://fhir.abda.de/eRezeptAbgabedaten/StructureDefinition/DAV-PKV-PR-ERP-Abrechnungszeilen</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>1.2"/&gt; &lt;/meta&gt; &lt;status
value="issued"/&gt; &lt;type&gt; &lt;coding&gt; &lt;system
value="http://fhir.abda.de/eRezeptAbgabedaten/CodeSystem/DAV-CS-ERP-InvoiceTyp"/&gt;
&lt;code value="Abrechnungszeilen"/&gt; &lt;/coding&gt; &lt;/type&gt;
&lt;lineItem&gt; &lt;sequence value="1"/&gt;
&lt;chargeItemCodeableConcept&gt; &lt;coding&gt; &lt;system
value="http://fhir.de/CodeSystem/ifa/pzn"/&gt; &lt;code
value="09494280"/&gt; &lt;/coding&gt; &lt;text value="VENLAFAXIN Heumann
75 mg Tabletten 100 St"/&gt; &lt;/chargeItemCodeableConcept&gt;
&lt;priceComponent&gt; &lt;extension
url="http://fhir.abda.de/eRezeptAbgabedaten/StructureDefinition/DAV-EX-ERP-MwStSatz"&gt;
&lt;valueDecimal value="19.00"/&gt; &lt;/extension&gt; &lt;extension
url="http://fhir.abda.de/eRezeptAbgabedaten/StructureDefinition/DAV-EX-ERP-KostenVersicherter"&gt;
&lt;extension url="Kategorie"&gt; &lt;valueCodeableConcept&gt;
&lt;coding&gt; &lt;system
value="http://fhir.abda.de/eRezeptAbgabedaten/CodeSystem/DAV-PKV-CS-ERP-KostenVersicherterKategorie"/&gt;
&lt;code value="0"/&gt; &lt;/coding&gt; &lt;/valueCodeableConcept&gt;
&lt;/extension&gt; &lt;extension url="Kostenbetrag"&gt;
&lt;valueMoney&gt; &lt;value value="0.00"/&gt; &lt;currency
value="EUR"/&gt; &lt;/valueMoney&gt; &lt;/extension&gt;
&lt;/extension&gt; &lt;type value="informational"/&gt; &lt;factor
value="1"/&gt; &lt;amount&gt; &lt;value value="31.40"/&gt; &lt;currency
value="EUR"/&gt; &lt;/amount&gt; &lt;/priceComponent&gt;
&lt;/lineItem&gt; &lt;totalGross&gt; &lt;extension
url="http://fhir.abda.de/eRezeptAbgabedaten/StructureDefinition/DAV-EX-ERP-Gesamtzuzahlung"&gt;
&lt;valueMoney&gt; &lt;value value="0.00"/&gt; &lt;currency
value="EUR"/&gt; &lt;/valueMoney&gt; &lt;/extension&gt; &lt;value
value="31.40"/&gt; &lt;currency value="EUR"/&gt; &lt;/totalGross&gt;
&lt;/Invoice&gt; &lt;/resource&gt; &lt;/entry&gt; &lt;signature&gt;
&lt;type&gt; &lt;system value="urn:iso-astm:E1762-95:2013" /&gt;
&lt;code value="1.2.840.10065.1.12.1.1" /&gt; &lt;/type&gt; &lt;when
value="2023-03-07T15:41:28.937+00:00" /&gt; &lt;who&gt; &lt;reference
value="https://erp.dev2.erezepttest.net//Device/1" /&gt; &lt;/who&gt;
&lt;sigFormat value="application/pkcs7-mime" /&gt; &lt;data
value="MII0vQ…" /&gt; &lt;/signature&gt; &lt;/Bundle&gt;
&lt;/resource&gt; &lt;/entry&gt; &lt;entry&gt; &lt;fullUrl
value="urn:uuid:c86f5600-0000-0000-0001-000000000000" /&gt;
&lt;resource&gt; &lt;Bundle&gt; &lt;id
value="a7008bf4-662f-46e8-89ab-ac339fc83c3d" /&gt; &lt;meta&gt;
&lt;lastUpdated value="2022-05-31T14:57:35.688+02:00" /&gt; &lt;profile
value="https://fhir.kbv.de/StructureDefinition/KBV_PR_ERP_Bundle</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>1.0.2" /&gt; &lt;/meta&gt;
&lt;identifier&gt; &lt;system
value="https://gematik.de/fhir/NamingSystem/PrescriptionID" /&gt;
&lt;value value="200.000.000.022.127.38" /&gt; &lt;/identifier&gt;
&lt;type value="document" /&gt; &lt;timestamp
value="2022-05-31T14:57:35.689+02:00" /&gt; &lt;entry&gt; &lt;fullUrl
value="https://pvs.gematik.de/fhir/Composition/7ebdcb09-edec-4017-a7df-e790b5bc8138"
/&gt; &lt;resource&gt; &lt;Composition&gt; &lt;id
value="7ebdcb09-edec-4017-a7df-e790b5bc8138" /&gt; &lt;meta&gt;
&lt;profile
value="https://fhir.kbv.de/StructureDefinition/KBV_PR_ERP_Composition</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>1.0.2" /&gt; &lt;/meta&gt;
&lt;extension
url="https://fhir.kbv.de/StructureDefinition/KBV_EX_FOR_Legal_basis"&gt;
&lt;valueCoding&gt; &lt;system
value="https://fhir.kbv.de/CodeSystem/KBV_CS_SFHIR_KBV_STATUSKENNZEICHEN"
/&gt; &lt;code value="00" /&gt; &lt;/valueCoding&gt; &lt;/extension&gt;
&lt;extension
url="https://fhir.kbv.de/StructureDefinition/KBV_EX_FOR_PKV_Tariff"&gt;
&lt;valueCoding&gt; &lt;system
value="https://fhir.kbv.de/CodeSystem/KBV_CS_SFHIR_KBV_PKV_TARIFF" /&gt;
&lt;code value="01" /&gt; &lt;/valueCoding&gt; &lt;/extension&gt;
&lt;status value="final" /&gt; &lt;type&gt; &lt;coding&gt; &lt;system
value="https://fhir.kbv.de/CodeSystem/KBV_CS_SFHIR_KBV_FORMULAR_ART"
/&gt; &lt;code value="e16A" /&gt; &lt;/coding&gt; &lt;/type&gt;
&lt;subject&gt; &lt;reference
value="Patient/5691bb6d-36fe-48b0-97b7-f48bf7b0a395" /&gt;
&lt;/subject&gt; &lt;date value="2022-05-31T14:57:35+02:00" /&gt;
&lt;author&gt; &lt;reference
value="Practitioner/8aed3aa3-3d50-49d7-ba69-e707984c7c1c" /&gt; &lt;type
value="Practitioner" /&gt; &lt;/author&gt; &lt;author&gt; &lt;type
value="Device" /&gt; &lt;identifier&gt; &lt;system
value="https://fhir.kbv.de/NamingSystem/KBV_NS_FOR_Pruefnummer" /&gt;
&lt;value value="GEMATIK/410/2109/36/123" /&gt; &lt;/identifier&gt;
&lt;/author&gt; &lt;title value="elektronische Arzneimittelverordnung"
/&gt; &lt;custodian&gt; &lt;reference
value="Organization/7b02666d-b519-462d-b47b-8ec85203c25a" /&gt;
&lt;/custodian&gt; &lt;section&gt; &lt;code&gt; &lt;coding&gt;
&lt;system
value="https://fhir.kbv.de/CodeSystem/KBV_CS_ERP_Section_Type" /&gt;
&lt;code value="Coverage" /&gt; &lt;/coding&gt; &lt;/code&gt;
&lt;entry&gt; &lt;reference
value="Coverage/65c00ca9-2998-42d2-8a2b-cfe548168b4d" /&gt;
&lt;/entry&gt; &lt;/section&gt; &lt;section&gt; &lt;code&gt;
&lt;coding&gt; &lt;system
value="https://fhir.kbv.de/CodeSystem/KBV_CS_ERP_Section_Type" /&gt;
&lt;code value="Prescription" /&gt; &lt;/coding&gt; &lt;/code&gt;
&lt;entry&gt; &lt;reference
value="MedicationRequest/d89a83dd-7168-4e68-8ea6-3d093763f591" /&gt;
&lt;/entry&gt; &lt;/section&gt; &lt;/Composition&gt; &lt;/resource&gt;
&lt;/entry&gt; &lt;entry&gt; &lt;fullUrl
value="https://pvs.gematik.de/fhir/MedicationRequest/d89a83dd-7168-4e68-8ea6-3d093763f591"
/&gt; &lt;resource&gt; &lt;MedicationRequest&gt; &lt;id
value="d89a83dd-7168-4e68-8ea6-3d093763f591" /&gt; &lt;meta&gt;
&lt;profile
value="https://fhir.kbv.de/StructureDefinition/KBV_PR_ERP_Prescription</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>1.0.2" /&gt; &lt;/meta&gt;
&lt;extension
url="https://fhir.kbv.de/StructureDefinition/KBV_EX_ERP_BVG"&gt;
&lt;valueBoolean value="false" /&gt; &lt;/extension&gt; &lt;extension
url="https://fhir.kbv.de/StructureDefinition/KBV_EX_ERP_EmergencyServicesFee"&gt;
&lt;valueBoolean value="false" /&gt; &lt;/extension&gt; &lt;extension
url="https://fhir.kbv.de/StructureDefinition/KBV_EX_ERP_Multiple_Prescription"&gt;
&lt;extension url="Kennzeichen"&gt; &lt;valueBoolean value="false" /&gt;
&lt;/extension&gt; &lt;/extension&gt; &lt;extension
url="https://fhir.kbv.de/StructureDefinition/KBV_EX_ERP_StatusCoPayment"&gt;
&lt;valueCoding&gt; &lt;system
value="https://fhir.kbv.de/CodeSystem/KBV_CS_ERP_StatusCoPayment" /&gt;
&lt;code value="0" /&gt; &lt;/valueCoding&gt; &lt;/extension&gt;
&lt;status value="active" /&gt; &lt;intent value="order" /&gt;
&lt;medicationReference&gt; &lt;reference
value="Medication/4521ce6e-27c3-4762-86db-e22bd4889918" /&gt;
&lt;/medicationReference&gt; &lt;subject&gt; &lt;reference
value="Patient/5691bb6d-36fe-48b0-97b7-f48bf7b0a395" /&gt;
&lt;/subject&gt; &lt;authoredOn value="2023-03-07" /&gt;
&lt;requester&gt; &lt;reference
value="Practitioner/8aed3aa3-3d50-49d7-ba69-e707984c7c1c" /&gt;
&lt;/requester&gt; &lt;insurance&gt; &lt;reference
value="Coverage/65c00ca9-2998-42d2-8a2b-cfe548168b4d" /&gt;
&lt;/insurance&gt; &lt;dosageInstruction&gt; &lt;extension
url="https://fhir.kbv.de/StructureDefinition/KBV_EX_ERP_DosageFlag"&gt;
&lt;valueBoolean value="true" /&gt; &lt;/extension&gt; &lt;text
value="1-0-0-0" /&gt; &lt;/dosageInstruction&gt; &lt;dispenseRequest&gt;
&lt;quantity&gt; &lt;value value="1" /&gt; &lt;system
value="http://unitsofmeasure.org" /&gt; &lt;/quantity&gt;
&lt;/dispenseRequest&gt; &lt;substitution&gt; &lt;allowedBoolean
value="false" /&gt; &lt;/substitution&gt; &lt;/MedicationRequest&gt;
&lt;/resource&gt; &lt;/entry&gt; &lt;entry&gt; &lt;fullUrl
value="https://pvs.gematik.de/fhir/Medication/4521ce6e-27c3-4762-86db-e22bd4889918"
/&gt; &lt;resource&gt; &lt;Medication&gt; &lt;id
value="4521ce6e-27c3-4762-86db-e22bd4889918" /&gt; &lt;meta&gt;
&lt;profile
value="https://fhir.kbv.de/StructureDefinition/KBV_PR_ERP_Medication_PZN</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>1.0.2" /&gt; &lt;/meta&gt;
&lt;extension
url="https://fhir.kbv.de/StructureDefinition/KBV_EX_ERP_Medication_Category"&gt;
&lt;valueCoding&gt; &lt;system
value="https://fhir.kbv.de/CodeSystem/KBV_CS_ERP_Medication_Category"
/&gt; &lt;code value="00" /&gt; &lt;/valueCoding&gt; &lt;/extension&gt;
&lt;extension
url="https://fhir.kbv.de/StructureDefinition/KBV_EX_ERP_Medication_Vaccine"&gt;
&lt;valueBoolean value="false" /&gt; &lt;/extension&gt; &lt;extension
url="http://fhir.de/StructureDefinition/normgroesse"&gt; &lt;valueCode
value="NB" /&gt; &lt;/extension&gt; &lt;code&gt; &lt;coding&gt;
&lt;system value="http://fhir.de/CodeSystem/ifa/pzn" /&gt; &lt;code
value="23456789" /&gt; &lt;/coding&gt; &lt;text value="Schmerzmittel"
/&gt; &lt;/code&gt; &lt;form&gt; &lt;coding&gt; &lt;system
value="https://fhir.kbv.de/CodeSystem/KBV_CS_SFHIR_KBV_DARREICHUNGSFORM"
/&gt; &lt;code value="TAB" /&gt; &lt;/coding&gt; &lt;/form&gt;
&lt;amount&gt; &lt;numerator&gt; &lt;value value="1" /&gt; &lt;unit
value="Stk" /&gt; &lt;/numerator&gt; &lt;denominator&gt; &lt;value
value="1" /&gt; &lt;/denominator&gt; &lt;/amount&gt; &lt;/Medication&gt;
&lt;/resource&gt; &lt;/entry&gt; &lt;entry&gt; &lt;fullUrl
value="https://pvs.gematik.de/fhir/Patient/5691bb6d-36fe-48b0-97b7-f48bf7b0a395"
/&gt; &lt;resource&gt; &lt;Patient&gt; &lt;id
value="5691bb6d-36fe-48b0-97b7-f48bf7b0a395" /&gt; &lt;meta&gt;
&lt;profile
value="https://fhir.kbv.de/StructureDefinition/KBV_PR_FOR_Patient</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>1.0.3" /&gt; &lt;/meta&gt;
&lt;identifier&gt; &lt;type&gt; &lt;coding&gt; &lt;system
value="http://fhir.de/CodeSystem/identifier-type-de-basis" /&gt;
&lt;code value="PKV" /&gt; &lt;/coding&gt; &lt;/type&gt; &lt;system
value="http://www.acme.com/identifiers/patient" /&gt; &lt;value
value="X276456719" /&gt; &lt;assigner&gt; &lt;reference
value="Organization/30cd7fd9-40ea-4259-9fa7-131a7fb8c640" /&gt;
&lt;display value="KOA Sachsen-Anhalt" /&gt; &lt;/assigner&gt;
&lt;/identifier&gt; &lt;name&gt; &lt;use value="official" /&gt;
&lt;family value="Angermänn" /&gt; &lt;given value="Günther" /&gt;
&lt;/name&gt; &lt;birthDate value="1967-04-26" /&gt; &lt;address&gt;
&lt;type value="both" /&gt; &lt;line value="Pfeilshofstr. 28b 0 OG"&gt;
&lt;extension
url="http://hl7.org/fhir/StructureDefinition/iso21090-ADXP-houseNumber"&gt;
&lt;valueString value="28b" /&gt; &lt;/extension&gt; &lt;extension
url="http://hl7.org/fhir/StructureDefinition/iso21090-ADXP-streetName"&gt;
&lt;valueString value="Pfeilshofstr." /&gt; &lt;/extension&gt;
&lt;/line&gt; &lt;city value="Süd Madleendorf" /&gt; &lt;postalCode
value="41956" /&gt; &lt;country value="D" /&gt; &lt;/address&gt;
&lt;/Patient&gt; &lt;/resource&gt; &lt;/entry&gt; &lt;entry&gt;
&lt;fullUrl
value="https://pvs.gematik.de/fhir/Organization/7b02666d-b519-462d-b47b-8ec85203c25a"
/&gt; &lt;resource&gt; &lt;Organization&gt; &lt;id
value="7b02666d-b519-462d-b47b-8ec85203c25a" /&gt; &lt;meta&gt;
&lt;profile
value="https://fhir.kbv.de/StructureDefinition/KBV_PR_FOR_Organization</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>1.0.3" /&gt; &lt;/meta&gt;
&lt;identifier&gt; &lt;type&gt; &lt;coding&gt; &lt;system
value="http://terminology.hl7.org/CodeSystem/v2-0203" /&gt; &lt;code
value="BSNR" /&gt; &lt;/coding&gt; &lt;/type&gt; &lt;system
value="https://fhir.kbv.de/NamingSystem/KBV_NS_Base_BSNR" /&gt;
&lt;value value="714529330" /&gt; &lt;/identifier&gt; &lt;name
value="Arztpraxis Schraßer" /&gt; &lt;telecom&gt; &lt;system
value="phone" /&gt; &lt;value value="+49-3832-34098496" /&gt;
&lt;/telecom&gt; &lt;telecom&gt; &lt;system value="email" /&gt;
&lt;value value="nela.minah@neuendorf.org" /&gt; &lt;/telecom&gt;
&lt;address&gt; &lt;type value="both" /&gt; &lt;line
value="Pastor-Louis-Str. 3 Zimmer 320"&gt; &lt;extension
url="http://hl7.org/fhir/StructureDefinition/iso21090-ADXP-houseNumber"&gt;
&lt;valueString value="3" /&gt; &lt;/extension&gt; &lt;extension
url="http://hl7.org/fhir/StructureDefinition/iso21090-ADXP-streetName"&gt;
&lt;valueString value="Pastor-Louis-Str." /&gt; &lt;/extension&gt;
&lt;/line&gt; &lt;city value="Alt Lenjaburg" /&gt; &lt;postalCode
value="11892" /&gt; &lt;country value="D" /&gt; &lt;/address&gt;
&lt;/Organization&gt; &lt;/resource&gt; &lt;/entry&gt; &lt;entry&gt;
&lt;fullUrl
value="https://pvs.gematik.de/fhir/Coverage/65c00ca9-2998-42d2-8a2b-cfe548168b4d"
/&gt; &lt;resource&gt; &lt;Coverage&gt; &lt;id
value="65c00ca9-2998-42d2-8a2b-cfe548168b4d" /&gt; &lt;meta&gt;
&lt;profile
value="https://fhir.kbv.de/StructureDefinition/KBV_PR_FOR_Coverage</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>1.0.3" /&gt; &lt;/meta&gt;
&lt;extension
url="http://fhir.de/StructureDefinition/gkv/besondere-personengruppe"&gt;
&lt;valueCoding&gt; &lt;system
value="https://fhir.kbv.de/CodeSystem/KBV_CS_SFHIR_KBV_PERSONENGRUPPE"
/&gt; &lt;code value="00" /&gt; &lt;/valueCoding&gt; &lt;/extension&gt;
&lt;extension
url="http://fhir.de/StructureDefinition/gkv/dmp-kennzeichen"&gt;
&lt;valueCoding&gt; &lt;system
value="https://fhir.kbv.de/CodeSystem/KBV_CS_SFHIR_KBV_DMP" /&gt;
&lt;code value="00" /&gt; &lt;/valueCoding&gt; &lt;/extension&gt;
&lt;extension url="http://fhir.de/StructureDefinition/gkv/wop"&gt;
&lt;valueCoding&gt; &lt;system
value="https://fhir.kbv.de/CodeSystem/KBV_CS_SFHIR_ITA_WOP" /&gt;
&lt;code value="01" /&gt; &lt;/valueCoding&gt; &lt;/extension&gt;
&lt;extension
url="http://fhir.de/StructureDefinition/gkv/versichertenart"&gt;
&lt;valueCoding&gt; &lt;system
value="https://fhir.kbv.de/CodeSystem/KBV_CS_SFHIR_KBV_VERSICHERTENSTATUS"
/&gt; &lt;code value="1" /&gt; &lt;/valueCoding&gt; &lt;/extension&gt;
&lt;status value="active" /&gt; &lt;type&gt; &lt;coding&gt; &lt;system
value="http://fhir.de/CodeSystem/versicherungsart-de-basis" /&gt;
&lt;code value="PKV" /&gt; &lt;/coding&gt; &lt;/type&gt;
&lt;beneficiary&gt; &lt;reference
value="Patient/a72d8dbe-9d99-46ab-821a-4e81b980b9e3" /&gt;
&lt;/beneficiary&gt; &lt;payor&gt; &lt;identifier&gt; &lt;system
value="http://fhir.de/NamingSystem/arge-ik/iknr" /&gt; &lt;value
value="249753760" /&gt; &lt;/identifier&gt; &lt;display value="KOA
Nordwürttemberg" /&gt; &lt;/payor&gt; &lt;/Coverage&gt;
&lt;/resource&gt; &lt;/entry&gt; &lt;entry&gt; &lt;fullUrl
value="https://pvs.gematik.de/fhir/Practitioner/8aed3aa3-3d50-49d7-ba69-e707984c7c1c"
/&gt; &lt;resource&gt; &lt;Practitioner&gt; &lt;id
value="8aed3aa3-3d50-49d7-ba69-e707984c7c1c" /&gt; &lt;meta&gt;
&lt;profile
value="https://fhir.kbv.de/StructureDefinition/KBV_PR_FOR_Practitioner</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>1.0.3" /&gt; &lt;/meta&gt;
&lt;identifier&gt; &lt;type&gt; &lt;coding&gt; &lt;system
value="http://terminology.hl7.org/CodeSystem/v2-0203" /&gt; &lt;code
value="LANR" /&gt; &lt;/coding&gt; &lt;/type&gt; &lt;system
value="https://fhir.kbv.de/NamingSystem/KBV_NS_Base_ANR" /&gt; &lt;value
value="222791803" /&gt; &lt;/identifier&gt; &lt;name&gt; &lt;use
value="official" /&gt; &lt;family value="Schraßer" /&gt; &lt;given
value="Dr." /&gt; &lt;prefix value="Dr."&gt; &lt;extension
url="http://hl7.org/fhir/StructureDefinition/iso21090-EN-qualifier"&gt;
&lt;valueCode value="AC" /&gt; &lt;/extension&gt; &lt;/prefix&gt;
&lt;/name&gt; &lt;qualification&gt; &lt;code&gt; &lt;coding&gt;
&lt;system
value="https://fhir.kbv.de/CodeSystem/KBV_CS_FOR_Qualification_Type"
/&gt; &lt;code value="00" /&gt; &lt;/coding&gt; &lt;/code&gt;
&lt;/qualification&gt; &lt;qualification&gt; &lt;code&gt; &lt;text
value="Super-Facharzt für alles Mögliche" /&gt; &lt;/code&gt;
&lt;/qualification&gt; &lt;/Practitioner&gt; &lt;/resource&gt;
&lt;/entry&gt; &lt;entry&gt; &lt;fullUrl
value="https://pvs.gematik.de/fhir/Organization/30cd7fd9-40ea-4259-9fa7-131a7fb8c640"
/&gt; &lt;resource&gt; &lt;Organization&gt; &lt;id
value="30cd7fd9-40ea-4259-9fa7-131a7fb8c640" /&gt; &lt;meta&gt;
&lt;profile
value="https://fhir.kbv.de/StructureDefinition/KBV_PR_FOR_Organization</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>1.0.3" /&gt; &lt;/meta&gt;
&lt;identifier&gt; &lt;system
value="http://fhir.de/NamingSystem/arge-ik/iknr" /&gt; &lt;value
value="760457211" /&gt; &lt;/identifier&gt; &lt;name value="KOA
Sachsen-Anhalt" /&gt; &lt;telecom&gt; &lt;system value="phone" /&gt;
&lt;value value="(0693) 849005617" /&gt; &lt;/telecom&gt;
&lt;/Organization&gt; &lt;/resource&gt; &lt;/entry&gt; &lt;signature&gt;
&lt;type&gt; &lt;system value="urn:iso-astm:E1762-95:2013" /&gt;
&lt;code value="1.2.840.10065.1.12.1.1" /&gt; &lt;/type&gt; &lt;when
value="2023-03-07T15:41:28.934+00:00" /&gt; &lt;who&gt; &lt;reference
value="https://erp.dev2.erezepttest.net//Device/1" /&gt; &lt;/who&gt;
&lt;sigFormat value="application/pkcs7-mime" /&gt; &lt;data
value="MII1IgYJKo…" /&gt; &lt;/signature&gt; &lt;/Bundle&gt;
&lt;/resource&gt; &lt;/entry&gt; &lt;/Bundle&gt; ---- NOTE: Aus Gründen
der besseren Lesbarkeit ist das PKV-Abgabdedatenbundle hier nicht
vollständig dargestellt und wurde mit <code>...</code> abgekürzt. Es
kann aber vollständig unter <a
href="https://simplifier.net/erezept-patientenrechnung/~resources?category=Example&amp;exampletype=Bundle">https://simplifier.net/erezept-patientenrechnung/~resources?category=Example&amp;exampletype=Bundle</a>
eingesehen werden.</p>
<p>NOTE: Das <code>&lt;signature&gt;</code> Element enthält die Signatur
des Bundles über alle enthaltenen Objekte als Enveloping-CAdES-Signatur
in Base64-Codierung.</p></td>
</tr>
</tbody>
</table>

Status Codes

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
[small]#Die Anfrage wurde erfolgreich bearbeitet. Die angeforderte Ressource wird im ResponseBody bereitgestellt.#</code></pre></td>
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

# Anwendungsfall PKV-Abgabedatensatz ändern

Als Apotheke möchte ich einen von mir erstellten PKV-Abgabedatensatz auf
Wunsch des Versicherten ändern. Liegen die Daten im System nicht mehr
vor, übermittelt der Versicherte der Apotheke den AccessCode zum Ändern
mittels einer Nachricht über das E-Rezept-FdV oder durch Anzeige zum
Abscannen im E-Rezept-FdV. Der zuvor im E-Rezept-Fachdienst gespeicherte
PKV-Abgabedatensatz wird überschrieben. Es werden keine älteren
Versionen im E-Rezept-Fachdienst gespeichert.

Der Aufruf erfolgt als http-`PUT`-Operation auf die Ressource
`/ChargeItem/'PrescriptionID'`. Im Aufruf muss das während der
Authentisierung erhaltene ACCESS\_TOKEN im http-Request-Header
`Authorization` übergeben werden.

**Request**

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>¦URI
¦https://prescriptionserver.telematik/ChargeItem/200.086.824.605.539.20?ac=777bea0e13cc9c42ceec14aec3ddee2263325dc2c6c699db115f58fe423607ea
¦Method ¦PUT ¦HTTP Header ¦ ---- Authorization: Bearer
eyJraWQ.ewogImL2pA10Qql22ddtutrvx4FsDlz.rHQjEmB1lLmpqn9J ---- NOTE: Mit
dem ACCESS_TOKEN im <code>Authorization</code>-Header weist sich der
Zugreifende als Versicherter aus, im Token ist seine Versichertennummer
enthalten. Die Base64-Darstellung des Tokens ist stark gekürzt.</p>
<p>NOTE: In den Profilen ist unter meta.profile auch die Version mit
anzugeben. (Bsp.:
"https://gematik.de/fhir/erpchrg/StructureDefinition/GEM_ERPCHRG_PR_ChargeItem</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>1.0</strong>")</p>
<p>¦Payload ¦ [source,xml] ---- &lt;ChargeItem
xmlns="http://hl7.org/fhir"&gt; &lt;id
value="abc825bc-bc30-45f8-b109-1b343fff5c45" /&gt; &lt;meta&gt;
&lt;profile
value="https://gematik.de/fhir/erpchrg/StructureDefinition/GEM_ERPCHRG_PR_ChargeItem</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>1.0" /&gt; &lt;/meta&gt;
&lt;contained&gt; &lt;Binary&gt; &lt;id value="Abg456"/&gt;
&lt;contentType value="application/pkcs7-mime" /&gt; &lt;data value=
"bWVycnkgY2hyaXN0bWFz"/&gt; &lt;/Binary&gt; &lt;/contained&gt;
&lt;identifier&gt; &lt;system
value="https://gematik.de/fhir/erp/NamingSystem/GEM_ERP_NS_PrescriptionId"
/&gt; &lt;value value="200.086.824.605.539.20" /&gt; &lt;/identifier&gt;
&lt;status value="billable" /&gt; &lt;code&gt; &lt;coding&gt; &lt;system
value="http://terminology.hl7.org/CodeSystem/data-absent-reason" /&gt;
&lt;code value="not-applicable" /&gt; &lt;/coding&gt; &lt;/code&gt;
&lt;subject&gt; &lt;identifier&gt; &lt;system
value="http://fhir.de/sid/pkv/kvid-10"/&gt; &lt;value value="X234567890"
/&gt; &lt;assigner&gt; &lt;display value="Name einer privaten
Krankenversicherung" /&gt; &lt;/assigner&gt; &lt;/identifier&gt;
&lt;/subject&gt; &lt;enterer&gt; &lt;identifier&gt; &lt;system
value="https://gematik.de/fhir/sid/telematik-id" /&gt; &lt;value
value="3-15.2.1456789123.191" /&gt; &lt;/identifier&gt; &lt;/enterer&gt;
&lt;enteredDate value="2022-06-01T07:13:00+05:00"/&gt;
&lt;supportingInformation&gt; &lt;reference value="#Abg456"/&gt;
&lt;display value="Binary"/&gt; &lt;/supportingInformation&gt;
&lt;/ChargeItem&gt; ---- NOTE: In
<code>&lt;id value="Abg456"/&gt;</code> fügt die abgebende LEI ihren
geänderten Abgabedatensatz ein.</p></td>
</tr>
</tbody>
</table>

**Response**

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>¦HTTP Status Code¦200 OK ¦HTTP Header
¦Content-Type: application/fhir+xml;charset=utf-8 ¦Payload ¦
[source,xml] ---- &lt;ChargeItem xmlns="http://hl7.org/fhir"&gt; &lt;id
value="abc825bc-bc30-45f8-b109-1b343fff5c45" /&gt; &lt;meta&gt;
&lt;profile
value="https://gematik.de/fhir/erpchrg/StructureDefinition/GEM_ERPCHRG_PR_ChargeItem</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>1.0" /&gt; &lt;tag&gt; &lt;display
value="Example of an ChargeItem." /&gt; &lt;/tag&gt; &lt;/meta&gt;
&lt;identifier&gt; &lt;system
value="https://gematik.de/fhir/erp/NamingSystem/GEM_ERP_NS_PrescriptionId"
/&gt; &lt;value value="200.086.824.605.539.20" /&gt; &lt;/identifier&gt;
&lt;status value="billable" /&gt; &lt;code&gt; &lt;coding&gt; &lt;system
value="http://terminology.hl7.org/CodeSystem/data-absent-reason" /&gt;
&lt;code value="not-applicable" /&gt; &lt;/coding&gt; &lt;/code&gt;
&lt;subject&gt; &lt;identifier&gt; &lt;system
value="http://fhir.de/sid/pkv/kvid-10"/&gt; &lt;value value="X234567890"
/&gt; &lt;assigner&gt; &lt;display value="Name einer privaten
Krankenversicherung" /&gt; &lt;/assigner&gt; &lt;/identifier&gt;
&lt;/subject&gt; &lt;enterer&gt; &lt;identifier&gt; &lt;system
value="https://gematik.de/fhir/sid/telematik-id" /&gt; &lt;value
value="3-15.2.1456789123.191"/&gt; &lt;/identifier&gt; &lt;/enterer&gt;
&lt;enteredDate value="2022-06-01T07:13:00+05:00"/&gt;
&lt;supportingInformation&gt; &lt;reference
value="Bundle/f8ea6d29-d38a-41f0-839f-5ed02c1b3e41"/&gt; &lt;display
value="http://fhir.abda.de/eRezeptAbgabedaten/StructureDefinition/DAV-PKV-PR-ERP-AbgabedatenBundle"/&gt;
&lt;/supportingInformation&gt; &lt;/ChargeItem&gt; ----</p></td>
</tr>
</tbody>
</table>

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
[small]#Die Anfrage wurde erfolgreich bearbeitet. Die angeforderte Ressource wird im ResponseBody bereitgestellt.#</code></pre></td>
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
berechtigt ist oder weil keine Einwilligung vorliegt.</span></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>404</p></td>
<td style="text-align: left;"><p>Not found<br />
<span class="small">Die adressierte Ressource wurde nicht gefunden, die
übergebene ID ist ungültig oder die Abrechnungsinformationen wurden
gelöscht. Das kann auch dadurch begründet sein, dass der Consent des
Versicherten nach dem Bereitstellen der Abrechnungsinformationen
entzogen wurde.</span></p></td>
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
<tr class="odd">
<td style="text-align: left;"><p>512</p></td>
<td style="text-align: left;"><p>OCSP Backend Error<br />
<span class="small">Innerhalb der vom Server erlaubten Zeitspanne wurde
keine gültige Antwort des OCSP-Responders geliefert.</span></p></td>
</tr>
</tbody>
</table>

# Anwendungsfall Abrechnungsinformationen durch den Versicherten abrufen

Als Versicherter möchte ich auf meine Abrechnungsinformationen zugreifen
und diese in der E-Rezept-App einsehen können. Sind die
Abrechunngsinformationen nicht bekannt (z.B. beim Wechsel des
Smartphones), können diese mit einem GET-Befehl abgerufen werden. Werden
ein oder mehrere ChargeItems gefunden, erfolgt die Rückgabe als Liste
aller gefundenen ChargeItems ohne die im ChargeItem enthaltenen
Referenzen.

Der Aufruf erfolgt als http-`GET`-Operation auf die Ressource
`/ChargeItem`.

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
href="https://erp.zentral.erp.splitdns.ti-dienste.de/ChargeItem/">https://erp.zentral.erp.splitdns.ti-dienste.de/ChargeItem/</a></p></td>
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
</div></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>Payload</strong></p></td>
<td style="text-align: left;"><pre><code>-</code></pre></td>
</tr>
</tbody>
</table>

**Response**

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>¦HTTP Status Code¦200 OK ¦HTTP Header
¦Content-Type: application/fhir+json;charset=utf-8 ¦Payload ¦
[source,json] ---- { "resourceType": "Bundle", "id":
"200e3c55-b154-4335-a0ec-65addd39a3b6", "meta": { "lastUpdated":
"2021-09-02T11:38:42.557+00:00" }, "type": "searchset", "total": 2,
"entry": [ { "fullUrl":
"http://hapi.fhir.org/baseR4/ChargeItem/abc825bc-bc30-45f8-b109-1b343fff5c45",
"resource": { "resourceType": "ChargeItem", "id":
"abc825bc-bc30-45f8-b109-1b343fff5c45", "meta": { "profile": [
"https://gematik.de/fhir/erpchrg/StructureDefinition/GEM_ERPCHRG_PR_ChargeItem</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>1.0" ] }, "status": "billable",
"extension": [ { "url":
"https://gematik.de/fhir/erpchrg/StructureDefinition/GEM_ERPCHRG_EX_MarkingFlag",
"extension": [ { "url": "insuranceProvider", "valueBoolean": false }, {
"url": "subsidy", "valueBoolean": false }, { "url": "taxOffice",
"valueBoolean": false } ] } ], "identifier": [ { "system":
"https://gematik.de/fhir/erp/NamingSystem/GEM_ERP_NS_PrescriptionId",
"value": "200.086.824.605.539.20" }, { "system":
"https://gematik.de/fhir/erp/NamingSystem/GEM_ERP_NS_AccessCode",
"value":
"777bea0e13cc9c42ceec14aec3ddee2263325dc2c6c699db115f58fe423607ea" } ],
"code": { "coding": [ { "code": "not-applicable", "system":
"http://terminology.hl7.org/CodeSystem/data-absent-reason" } ] },
"subject": { "identifier": { "system": "http://fhir.de/sid/pkv/kvid-10",
"value": "X234567890", "assigner": { "display": "Name einer privaten
Krankenversicherung" } } }, "enteredDate": "2021-06-01T07:13:00+05:00",
"supportingInformation": [ { "display":
"https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_PR_Bundle" } ]
}, "search": { "mode": "match" } }, { "fullUrl":
"http://hapi.fhir.org/baseR4/ChargeItem/der124bc-bc30-45f8-b109-4h474wer2h89",
"resource": { "resourceType": "ChargeItem", "id":
"der124bc-bc30-45f8-b109-4h474wer2h89", "meta": { "profile": [
"https://gematik.de/fhir/erpchrg/StructureDefinition/GEM_ERPCHRG_PR_ChargeItem</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>1.0" ] }, "status": "billable",
"extension": [ { "url":
"https://gematik.de/fhir/erpchrg/StructureDefinition/GEM_ERPCHRG_EX_MarkingFlag",
"extension": [ { "url": "insuranceProvider", "valueBoolean": false }, {
"url": "subsidy", "valueBoolean": false }, { "url": "taxOffice",
"valueBoolean": false } ] } ], "identifier": [ { "system":
"https://gematik.de/fhir/erp/NamingSystem/GEM_ERP_NS_PrescriptionId",
"value": "200.086.824.605.539.20" }, { "system":
"https://gematik.de/fhir/erp/NamingSystem/GEM_ERP_NS_AccessCode",
"value":
"888bea0e13cc9c42ceec14aec3ddee2263325dc2c6c699db115f58fe423607ea" } ],
"code": { "coding": [ { "code": "not-applicable", "system":
"http://terminology.hl7.org/CodeSystem/data-absent-reason" } ] },
"subject": { "identifier": { "system": "http://fhir.de/sid/pkv/kvid-10",
"value": "X234567890", "assigner": { "display": "Name einer privaten
Krankenversicherung" } } }, "enteredDate": "2021-06-01T07:13:00+05:00",
"supportingInformation": [ { "display":
"https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_PR_Bundle" } ]
} } ] } ----</p>
<p>NOTE: Die angegebenen Referenzen werden in diesem Request nicht
mitgeliefert. Im folgenden Request der das Chargeitem nach der Id
abfragt sind diese Informationen dagegen enthalten.</p>
<p>NOTE: .enterer ist in diesem Aufruf nicht enthalten, um die
Performance im Fachdienst zu erhöhen.</p></td>
</tr>
</tbody>
</table>

Sind die ChargeItem-Instanzen in der App bekannt, kann direkt auf eine
konkrete Instanz zugegriffen werden. Es wird das ChargeItem mit den
referenzierten Bundles zurückgegeben.

Rückgabewert ist ein Bundle, welches das ChargeItem, den
Verordnungsdatensatz, den Abgabedatensatz und die Quittung beinhaltet.
An den drei Abrechnungsdatensätzen (Verordnungs-, Abgabedatensatz und an
der Quittung hängt die Signatur im CAdES-Enveloping-Format).

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
href="https://prescriptionserver.telematik/ChargeItem/200.086.824.605.539.20">https://prescriptionserver.telematik/ChargeItem/200.086.824.605.539.20</a></p></td>
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
</div></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>Payload</strong></p></td>
<td style="text-align: left;"></td>
</tr>
</tbody>
</table>

**Response**

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>¦HTTP Status Code¦200 OK ¦HTTP Header
¦Content-Type: application/fhir+json;charset=utf-8 ¦Payload ¦
[source,json] ---- { "resourceType": "Bundle", "id":
"Response-App-GETChargeItemById", "meta": { "lastUpdated":
"2021-09-02T11:38:42.557+00:00" }, "type": "searchset", "total": 4,
"entry": [ { "fullUrl":
"https://prescriptionserver.telematik/ChargeItem/200.086.824.605.539.20",
"resource": { "resourceType": "ChargeItem", "id":
"200.086.824.605.539.20", "meta": { "profile": [
"https://gematik.de/fhir/erpchrg/StructureDefinition/GEM_ERPCHRG_PR_ChargeItem</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>1.0" ] }, "extension": [ { "url":
"https://gematik.de/fhir/erpchrg/StructureDefinition/GEM_ERPCHRG_EX_MarkingFlag",
"extension": [ { "url": "insuranceProvider", "valueBoolean": false }, {
"url": "subsidy", "valueBoolean": false }, { "url": "taxOffice",
"valueBoolean": false } ] } ], "identifier": [ { "system":
"https://gematik.de/fhir/erp/NamingSystem/GEM_ERP_NS_PrescriptionId",
"value": "200.086.824.605.539.20" }, { "system":
"https://gematik.de/fhir/erp/NamingSystem/GEM_ERP_NS_AccessCode",
"value":
"777bea0e13cc9c42ceec14aec3ddee2263325dc2c6c699db115f58fe423607ea" } ],
"status": "billable", "code": { "coding": [ { "code": "not-applicable",
"system": "http://terminology.hl7.org/CodeSystem/data-absent-reason" } ]
}, "subject": { "identifier": { "system":
"http://fhir.de/sid/pkv/kvid-10", "value": "X234567890" } }, "enterer":
{ "identifier": { "system": "https://gematik.de/fhir/sid/telematik-id",
"value": "3-SMC-B-Testkarte-883110000095957" } }, "enteredDate":
"2021-06-01T07:13:00+05:00", "supportingInformation": [ { "reference":
"Bundle/414ca393-dde3-4082-9a3b-3752e629e4aa", "display":
"https://fhir.kbv.de/StructureDefinition/KBV_PR_ERP_Bundle" }, {
"reference": "Bundle/f548dde3-a319-486b-8624-6176ff41ad90", "display":
"http://fhir.abda.de/eRezeptAbgabedaten/StructureDefinition/DAV-PKV-PR-ERP-AbgabedatenBundle"
}, { "reference": "Bundle/dffbfd6a-5712-4798-bdc8-07201eb77ab8",
"display":
"https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_PR_Bundle" } ]
} }, { "fullUrl":
"https://prescriptionserver.telematik/Bundle/414ca393-dde3-4082-9a3b-3752e629e4aa",
"resource": { "resourceType": "Bundle", "id":
"414ca393-dde3-4082-9a3b-3752e629e4aa", "meta": { "lastUpdated":
"2022-05-20T08:30:00Z", "profile": [
"https://fhir.kbv.de/StructureDefinition/KBV_PR_ERP_Bundle</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>1.1.0" ] }, "identifier": { "system":
"https://gematik.de/fhir/erp/NamingSystem/GEM_ERP_NS_PrescriptionId",
"value": "200.086.824.605.539.20" }, … }, { "fullUrl":
"https://prescriptionserver.telematik/Bundle/f548dde3-a319-486b-8624-6176ff41ad90",
"resource": { "resourceType": "Bundle", "id":
"f548dde3-a319-486b-8624-6176ff41ad90", "meta": { "profile": [
"http://fhir.abda.de/eRezeptAbgabedaten/StructureDefinition/DAV-PKV-PR-ERP-AbgabedatenBundle</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>1.2" ] }, … }, { "fullUrl":
"https://prescriptionserver.telematik/Bundle/dffbfd6a-5712-4798-bdc8-07201eb77ab8",
"resource": { "resourceType": "Bundle", "id":
"dffbfd6a-5712-4798-bdc8-07201eb77ab8", "meta": { "profile": [
"https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_PR_Bundle</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>1.2" ], "tag": [ { "display": "Receipt
Bundle <em>Quittung</em> for completed dispensation of a prescription" }
] }, "type": "document", "identifier": { "system":
"https://gematik.de/fhir/erp/NamingSystem/GEM_ERP_NS_PrescriptionId",
"value": "200.086.824.605.539.20" }, "timestamp":
"2022-03-18T15:28:00+00:00", "entry": [ { "fullUrl":
"urn:uuid:c624cf47-e235-4624-af71-0a09dc9254dc", "resource": {
"resourceType": "Composition", "id":
"c624cf47-e235-4624-af71-0a09dc9254dc", "meta": { "profile": [
"https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_PR_Composition</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>1.2" ] }, "status": "final", "title":
"Quittung", "extension": [ { "url":
"https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_EX_Beneficiary",
"valueIdentifier": { "system":
"https://gematik.de/fhir/sid/telematik-id", "value":
"3-SMC-B-Testkarte-883110000129070" } } ], "type": { "coding": [ {
"code": "3", "system":
"https://gematik.de/fhir/erp/CodeSystem/GEM_ERP_CS_DocumentType",
"display": "Receipt" } ] }, "date": "2022-03-18T15:29:00+00:00",
"author": [ { "reference":
"https://erp.zentral.erp.splitdns.ti-dienste.de/Device/1" } ], "event":
[ { "period": { "start": "2022-03-18T15:28:00+00:00", "end":
"2022-03-18T15:29:00+00:00" } } ], "section": [ { "entry": [ {
"reference": "Binary/PrescriptionDigest-200.086.824.605.539.20" } ] } ]
} }, { "fullUrl":
"https://erp.zentral.erp.splitdns.ti-dienste.de/Device/1", "resource": {
"resourceType": "Device", "id": "1", "meta": { "profile": [
"https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_PR_Device</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>1.2" ] }, "status": "active",
"serialNumber": "1.4.0", "deviceName": [ { "name":
"E-Rezept-Fachdienst", "type": "user-friendly-name" } ], "version": [ {
"value": "1.4.0" } ], "contact": [ { "system": "email", "value":
"betrieb@gematik.de" } ] } }, { "fullUrl":
"https://erp.zentral.erp.splitdns.ti-dienste.de/Binary/PrescriptionDigest-200.086.824.605.539.20",
"resource": { "resourceType": "Binary", "id":
"PrescriptionDigest-200.086.824.605.539.20", "meta": { "profile": [
"https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_PR_Digest</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>1.2" ] }, "contentType":
"application/octet-stream", "data":
"tJg8c5ZtdhzEEhJ0ZpAsUVFx5dKuYgQFs5oKgthi17M=" } } ], "signature": {
"type": [ { "code": "1.2.840.10065.1.12.1.1", "system":
"urn:iso-astm:E1762-95:2013" } ], "when": "2022-03-18T15:28:00+00:00",
"who": { "reference":
"https://erp.zentral.erp.splitdns.ti-dienste.de/Device/1" },
"sigFormat": "application/pkcs7-mime", "data":
"dGhpcyBibG9iIGlzIHNuaXBwZWQ=" } } } ] } ----</p>
<p>NOTE: Das <code>signature</code> Element enthält die Signatur des
Bundles über alle enthaltenen Objekte als Enveloping-CAdES-Signatur in
Base64-Codierung.</p>
<p>NOTE: Aus Gründen der besseren Lesbarkeit ist das Bundle hier nicht
vollständig dargestellt und wurde mit <code>...</code> abgekürzt. Es
kann aber vollständig unter <a
href="https://simplifier.net/erezept-patientenrechnung/~resources?category=Example&amp;exampletype=Bundle">https://simplifier.net/erezept-patientenrechnung/~resources?category=Example&amp;exampletype=Bundle</a>
eingesehen werden.</p></td>
</tr>
</tbody>
</table>

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
[small]#Die Anfrage wurde erfolgreich bearbeitet. Die angeforderte Ressource wird im ResponseBody bereitgestellt.#</code></pre></td>
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

# Anwendungsfall Abrechnungsinformationen durch den Versicherten ändern

Als Versicherter möchte ich vorhandene Abrechnungsinformationen ändern,
indem ich markiere, ob ich meine Abrechnungsdaten bei Abrechnungsstellen
eingereicht habe.

Der Aufruf erfolgt als http-`PATCH`-Operation auf die Ressource
`/ChargeItem`.

**Request**

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>¦URI
¦https://prescriptionserver.telematik/ChargeItem/200.086.824.605.539.20
¦Method ¦PATCH ¦HTTP Header ¦ ---- Authorization: Bearer
eyJraWQ.ewogImL2pA10Qql22ddtutrvx4FsDlz.rHQjEmB1lLmpqn9J Content-Type:
application/fhir+json; charset=utf-8 ---- NOTE: Mit dem ACCESS_TOKEN im
<code>Authorization</code>-Header weist sich der Zugreifende als
Versicherter aus, im Token ist seine Versichertennummer enthalten. Die
Base64-Darstellung des Tokens ist stark gekürzt.</p>
<p>¦Payload ¦ [source,json] ---- { "resourceType": "Parameters",
"parameter": [ { "name": "operation", "part": [ { "name": "type",
"valueCode": "add" }, { "name": "path", "valueString":
"ChargeItem.extension(<em>https://gematik.de/fhir/erpchrg/StructureDefinition/GEM_ERPCHRG_EX_MarkingFlag</em>).extension(<em>taxOffice</em>)"
}, { "name": "name", "valueString": "valueBoolean" }, { "name": "value",
"valueBoolean": true } ] }, { "name": "operation", "part": [ { "name":
"type", "valueCode": "add" }, { "name": "path", "valueString":
"ChargeItem.extension(<em>https://gematik.de/fhir/erpchrg/StructureDefinition/GEM_ERPCHRG_EX_MarkingFlag</em>).extension(<em>insuranceProvider</em>)"
}, { "name": "name", "valueString": "valueBoolean" }, { "name": "value",
"valueBoolean": false } ] } ] } ---- NOTE: In
<code>"valueString": "ChargeItem.extension('https://gematik.de/fhir/erpchrg/StructureDefinition/GEM_ERPCHRG_EX_MarkingFlag').extension('taxOffice')"</code>
ist der Pfadanfang, an dem das zu ändernde Attribut hängt definiert.</p>
<p>NOTE: Im
<code>"valueString": "ChargeItem.extension('https://gematik.de/fhir/erpchrg/StructureDefinition/GEM_ERPCHRG_EX_MarkingFlag').extension('insuranceProvider')"</code>
Element, welches geändert werden soll.</p></td>
</tr>
</tbody>
</table>

**Response**

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>¦HTTP Status Code¦200 OK ¦HTTP Header
¦Content-Type: application/fhir+json;charset=utf-8 ¦Payload ¦
[source,json] ---- { "resourceType": "ChargeItem", "id":
"200.086.824.605.539.20", "meta": { "versionId": "1", "lastUpdated":
"2022-04-05T11:36:19.491+00:00", "source": "#V4se2kvNDlSKuefe",
"profile": [
"https://gematik.de/fhir/erpchrg/StructureDefinition/GEM_ERPCHRG_PR_ChargeItem</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>1.0" ] }, "extension": [ { "url":
"https://gematik.de/fhir/erpchrg/StructureDefinition/GEM_ERPCHRG_EX_MarkingFlag",
"extension": [ { "url": "insuranceProvider", "valueBoolean": true }, {
"url": "subsidy", "valueBoolean": false }, { "url": "taxOffice",
"valueBoolean": true } ] } ], "identifier": [ { "system":
"https://gematik.de/fhir/erp/NamingSystem/GEM_ERP_NS_PrescriptionId",
"value": "200.086.824.605.539.20" }, { "system":
"https://gematik.de/fhir/erp/NamingSystem/GEM_ERP_NS_AccessCode",
"value":
"555bjf73jr8d9si2ceec14aec3ddee2263325dc2c6c699db115f58fe423607ea" } ],
"status": "billable", "code": { "coding": [ { "system":
"http://terminology.hl7.org/CodeSystem/data-absent-reason", "code":
"not-applicable" } ] }, "subject": { "identifier": { "system":
"http://fhir.de/sid/pkv/kvid-10", "value": "X234567890" } }, "enterer":
{ "identifier": { "system": "https://gematik.de/fhir/sid/telematik-id",
"value": "3-SMC-B-Testkarte-883110000095957" } }, "enteredDate":
"2021-06-01T07:13:00+05:00", "supportingInformation": [ { "reference":
"Bundle/0428d416-149e-48a4-977c-394887b3d85c", "display":
"https://fhir.kbv.de/StructureDefinition/KBV_PR_ERP_Bundle" }, {
"reference": "Bundle/72bd741c-7ad8-41d8-97c3-9aabbdd0f5b4", "display":
"http://fhir.abda.de/eRezeptAbgabedaten/StructureDefinition/DAV-PKV-PR-ERP-AbgabedatenBundle"
}, { "reference": "Bundle/2fbc0103-1d1b-4be6-8ed8-6faf87bcc09b",
"display":
"https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_PR_Bundle" } ]
} ----</p></td>
</tr>
</tbody>
</table>

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
[small]#Die Anfrage wurde erfolgreich bearbeitet.#</code></pre></td>
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

# Anwendungsfall Löschen der Abrechnungsinformationen durch den Versicherten

Als Versicherter möchte ich eine durch die Apotheke eingestellte
Abrechnungsinformation löschen. Das Löschen erfolgt unwiederbringlich.

Der Aufruf erfolgt als http-`DELETE`-Operation auf die Ressource
`/ChargeItem`. Im Aufruf muss das während der Authentisierung erhaltene
ACCESS\_TOKEN im http-Request-Header `Authorization` übergeben werden,
der Fachdienst filtert die Consent-Einträge nach der im ACCESS\_TOKEN
enthaltenen KVNR des Versicherten.

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
href="https://prescriptionserver.telematik/ChargeItem/200.086.824.605.539.20">https://prescriptionserver.telematik/ChargeItem/200.086.824.605.539.20</a></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>Method</strong></p></td>
<td style="text-align: left;"><p>DELETE</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>HTTP Header</strong></p></td>
<td style="text-align: left;"><pre><code>Authorization: Bearer eyJraWQ.ewogImL2pA10Qql22ddtutrvx4FsDlz.rHQjEmB1lLmpqn9J
X-AccessCode: 777bea0e13cc9c42ceec14aec3ddee2263325dc2c6c699db115f58fe423607ea</code></pre>
<div class="note">
<p>Mit dem ACCESS_TOKEN im <code>Authorization</code>-Header weist sich
der Zugreifende als Versicherter aus, im Token ist seine
Versichertennummer enthalten. Die Base64-Darstellung des Tokens ist
stark gekürzt.</p>
</div></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>Payload</strong></p></td>
<td style="text-align: left;"></td>
</tr>
</tbody>
</table>

**Response**

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>¦HTTP Status Code¦204 No Content ¦HTTP
Header ¦- ¦Payload ¦-</p></td>
</tr>
</tbody>
</table>

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
