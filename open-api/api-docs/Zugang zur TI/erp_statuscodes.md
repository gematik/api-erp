Folgende http Status Codes können Clients bei der Benutzung der
Schnittstellen des E-Rezept-Fachdienstes erwarten. Fehler können sowohl
im inneren http-Requests (bei fachlichen Fehlern) als auch im äußeren
http-Request auftreten.

# Status Codes am Endpunkt /VAU

Fehler in der Übertragung auf der Netzwerkstrecke oder eine syntaktisch
"falsche" Verschlüsselung des inneren http-Requests führen zu Fehlern am
Endpunkt /VAU. Konnte der Verarbeitungskontext innerhalb der VAU den
Request entschlüsseln, liefert er bei nutzbarem Antwortschlüssel
(AES256-GCM-konform) immer eine verschlüsselte Antwort. Bei fachlichen
Fehlern kann diese allerdings selbst einen Fehlercode enthalten (siehe
unten).

<table>
<colgroup>
<col style="width: 30%" />
<col style="width: 10%" />
<col style="width: 60%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p><strong>http
Operation</strong></p></td>
<td style="text-align: left;"><p><strong>Mögliche http Status
Codes</strong></p></td>
<td
style="text-align: left;"><p><strong>Bedeutung/Fehlerdetails</strong></p></td>
</tr>
<tr class="even">
<td colspan="3"
style="text-align: left;"><p><strong>Erfolgsfall</strong></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>POST /VAU/*</p></td>
<td style="text-align: left;"><p>200</p></td>
<td style="text-align: left;"><p>Der Server konnte den Request
entschlüsseln und verarbeiten. Details befinden sich im verschlüsselten
inneren http-Response, welcher im Body dieser http-Response enthalten
ist.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>GET /VAUCertificate</p></td>
<td style="text-align: left;"><p>200</p></td>
<td style="text-align: left;"><p>Das VAU-Entschlüsselungszertifikat
konnte erfolgreich heruntergeladen werden</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>GET
/VAUCertificateOCSPResponse</p></td>
<td style="text-align: left;"><p>200</p></td>
<td style="text-align: left;"><p>Die OCSP-Statusauskunft zum
VAU-Entschlüsselungszertifikat konnte erfolgreich heruntergeladen
werden</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>GET /TSL.xml</p></td>
<td style="text-align: left;"><p>200</p></td>
<td style="text-align: left;"><p>Die Liste der CA-Zertifikate zum
Aufspannen des Vertrauensraums der TI konnte erfolgreich heruntergeladen
werden</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>GET /TSL.sha2</p></td>
<td style="text-align: left;"><p>200</p></td>
<td style="text-align: left;"><p>Der Hashwert zur Prüfung der Integrität
der TSL konnte erfolgreich heruntergeladen werden</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>GET /CertList</p></td>
<td style="text-align: left;"><p>200</p></td>
<td style="text-align: left;"><p>Die Zertifikatskette der
E-Rezept-Serverzertifikate konnte erfolgreich heruntergeladen
werden</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>GET /OCSPList</p></td>
<td style="text-align: left;"><p>200</p></td>
<td style="text-align: left;"><p>Die Liste der OCSP-Statusauskünfte der
E-Rezept-Serverzertifikate konnte erfolgreich heruntergeladen
werden</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>POST /ocspf</p></td>
<td style="text-align: left;"><p>200</p></td>
<td style="text-align: left;"><p>Die OCSP-Statusanfrage zu einem
TI-Zertifikat konnte erfolgreich an den passenden OCSP-Responder
weitergeleitet werden</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>GET /metadata</p></td>
<td style="text-align: left;"><p>200</p></td>
<td style="text-align: left;"><p>Die CapabilityStement der
FHIR-Schnittstelle konnte erfolgreich heruntergeladen werden</p></td>
</tr>
<tr class="even">
<td colspan="3"
style="text-align: left;"><p><strong>Fehlerfälle</strong></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>POST /VAU/*</p></td>
<td style="text-align: left;"><p>400</p></td>
<td style="text-align: left;"><p>Der http-Request enthält ungültige
Daten, die im VAU-Kontext nicht verarbeitet werden können. Z.B.
fehlerhafte Verschlüsselung, syntaktisch falsch aufgebauter inner
http-Request oder falsches Nutzerpseudonym "NP"</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>401</p></td>
<td style="text-align: left;"><p>Die Berechtigung zum Zugriff auf die
Schnittstelle konnte nicht geprüft werden.</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>405</p></td>
<td style="text-align: left;"><p>Unzulässige http-Operation PUT
o.ä.</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>408</p></td>
<td style="text-align: left;"><p>Der Client überträgt Daten zu
langsam</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>504</p></td>
<td style="text-align: left;"><p>Der ausgelastete Server kann den
Request aktuell nicht bearbeiten.<br />
Ein Retry gemäß Exponential Backoff ist zulässig.</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>GET /VAUCertificate</p></td>
<td style="text-align: left;"><p>400</p></td>
<td style="text-align: left;"><p>ungültiger http-Request (Pfad, Header,
Content-Type, etc.)</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>401</p></td>
<td style="text-align: left;"><p>Die Berechtigung zum Zugriff auf die
Schnittstelle konnte nicht geprüft werden.</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>405</p></td>
<td style="text-align: left;"><p>Unzulässige http-Operation POST, PUT
o.ä.</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>GET
/VAUCertificateOCSPResponse</p></td>
<td style="text-align: left;"><p>400</p></td>
<td style="text-align: left;"><p>ungültiger http-Request (Pfad, Header,
Content-Type, etc.)</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>401</p></td>
<td style="text-align: left;"><p>Die Berechtigung zum Zugriff auf die
Schnittstelle konnte nicht geprüft werden.</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>405</p></td>
<td style="text-align: left;"><p>Unzulässige http-Operation POST, PUT
o.ä.</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>GET /TSL.xml</p></td>
<td style="text-align: left;"><p>400</p></td>
<td style="text-align: left;"><p>ungültiger http-Request (Pfad, Header,
Content-Type, etc.)</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>GET /TSL.sha2</p></td>
<td style="text-align: left;"><p>400</p></td>
<td style="text-align: left;"><p>ungültiger http-Request (Pfad, Header,
Content-Type, etc.)</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>GET /CertList</p></td>
<td style="text-align: left;"><p>400</p></td>
<td style="text-align: left;"><p>ungültiger http-Request (Pfad, Header,
Content-Type, etc.)</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>GET /OCSPList</p></td>
<td style="text-align: left;"><p>400</p></td>
<td style="text-align: left;"><p>ungültiger http-Request (Pfad, Header,
Content-Type, etc.)</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>POST /ocspf</p></td>
<td style="text-align: left;"><p>400</p></td>
<td style="text-align: left;"><p>Der http-Request enthält ungültige
Zertifikatsdaten, die nicht für eine OCSP-Responderanfrage verarbeitet
werden können.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>401</p></td>
<td style="text-align: left;"><p>Die Berechtigung zum Zugriff auf die
Schnittstelle konnte nicht geprüft werden.</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>&lt;in allen Operationen&gt;</p></td>
<td style="text-align: left;"><p>500</p></td>
<td style="text-align: left;"><p>Internal Server Error<br />
<strong>Client-Failover angeraten: Ja</strong></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>501</p></td>
<td style="text-align: left;"><p>Not Implemented<br />
<strong>Client-Failover angeraten: Ja</strong></p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>502</p></td>
<td style="text-align: left;"><p>Bad Gateway<br />
<strong>Client-Failover angeraten: Ja</strong></p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>503</p></td>
<td style="text-align: left;"><p>Service Unavailable<br />
<strong>Client-Failover angeraten: Ja</strong></p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>504</p></td>
<td style="text-align: left;"><p>Gateway Timeout<br />
<strong>Client-Failover angeraten: Ja</strong></p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>505</p></td>
<td style="text-align: left;"><p>HTTP Version not supported<br />
Client-Failover angeraten: Nein</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>506</p></td>
<td style="text-align: left;"><p>Variant Also Negotiates<br />
Client-Failover angeraten: Nein</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>507</p></td>
<td style="text-align: left;"><p>Insufficient Storage<br />
<strong>Client-Failover angeraten: Ja</strong></p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>508</p></td>
<td style="text-align: left;"><p>Loop Detected<br />
Client-Failover angeraten: Nein</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>509</p></td>
<td style="text-align: left;"><p>Bandwidth Limit Exceeded<br />
<strong>Client-Failover angeraten: Ja</strong></p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>510</p></td>
<td style="text-align: left;"><p>Not Extended<br />
Client-Failover angeraten: Nein</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>511</p></td>
<td style="text-align: left;"><p>Network Authentication Required<br />
Client-Failover angeraten: Nein</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>512</p></td>
<td style="text-align: left;"><p>OCSP Backend Error<br />
<strong>Client-Failover angeraten: Ja</strong></p></td>
<td></td>
</tr>
</tbody>
</table>

# Status Codes an der inneren FHIR-Schnittstelle innerhalb des VAU-Transports

<table>
<colgroup>
<col style="width: 30%" />
<col style="width: 10%" />
<col style="width: 60%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p><strong>http
Operation</strong></p></td>
<td style="text-align: left;"><p><strong>Mögliche http Status
Codes</strong></p></td>
<td
style="text-align: left;"><p><strong>Bedeutung/Fehlerdetails</strong></p></td>
</tr>
<tr class="even">
<td colspan="3"
style="text-align: left;"><p><strong>Erfolgsfälle</strong></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>GET /Task</p></td>
<td style="text-align: left;"><p>200</p></td>
<td style="text-align: left;"><p>Tasks konnten erfolgreich gelesen
werden</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>GET /Task/&lt;id&gt;</p></td>
<td style="text-align: left;"><p>200</p></td>
<td style="text-align: left;"><p>Task konnte erfolgreich gelesen
werden</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>POST /Task/$create</p></td>
<td style="text-align: left;"><p>201</p></td>
<td style="text-align: left;"><p>Task konnte für den angeforderten
FlowType erfolgreich initialisiert werden</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>POST
/Task/&lt;id&gt;/$activate</p></td>
<td style="text-align: left;"><p>200</p></td>
<td style="text-align: left;"><p>Task konnte mit der bereitgestellten
Verordnung aktiviert werden (QES gültig und Datensatz
FHIR-konform)</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>202</p></td>
<td style="text-align: left;"><p>Task konnte aktiviert werden,
<strong>Übergangsweise wird eine fachliche Abweichung in der Nutzung
unspezifizierter Extensions im Verordnungsdatensatz akzeptiert
(Accepted)</strong></p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>POST /Task/&lt;id&gt;/$accept</p></td>
<td style="text-align: left;"><p>200</p></td>
<td style="text-align: left;"><p>Task wurde erfolgreich einer Apotheke
zugewiesen</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>POST /Task/&lt;id&gt;/$reject</p></td>
<td style="text-align: left;"><p>204</p></td>
<td style="text-align: left;"><p>Task wurde von der zugewiesenen
Apotheke zurückgewiesen</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>POST /Task/&lt;id&gt;/$close</p></td>
<td style="text-align: left;"><p>200</p></td>
<td style="text-align: left;"><p>Task wurde erfolgreich beendet</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>POST /Task/&lt;id&gt;/$abort</p></td>
<td style="text-align: left;"><p>204</p></td>
<td style="text-align: left;"><p>Task wurde erfolgreich
gelöscht</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>GET /MedicationDispense</p></td>
<td style="text-align: left;"><p>200</p></td>
<td style="text-align: left;"><p>Dispensierinformationen wurden
erfolgreich gelesen</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>GET
/MedicationDispense/&lt;id&gt;</p></td>
<td style="text-align: left;"><p>200</p></td>
<td style="text-align: left;"><p>Dispensierinformationen wurden
erfolgreich gelesen</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>GET /Communication</p></td>
<td style="text-align: left;"><p>200</p></td>
<td style="text-align: left;"><p>E-Rezeptnachrichten erfolgreich
gelesen</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>GET /Communication/&lt;id&gt;</p></td>
<td style="text-align: left;"><p>200</p></td>
<td style="text-align: left;"><p>E-Rezeptnachricht erfolgreich
gelesen</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>POST /Communication</p></td>
<td style="text-align: left;"><p>201</p></td>
<td style="text-align: left;"><p>E-Rezeptnachrichten erfolgreich
versendet</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>DELETE
/Communication/&lt;id&gt;</p></td>
<td style="text-align: left;"><p>204</p></td>
<td style="text-align: left;"><p>E-Rezeptnachricht erfolgreich
gelöscht</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>GET /AuditEvent</p></td>
<td style="text-align: left;"><p>200</p></td>
<td style="text-align: left;"><p>E-Rezeptereignisse erfolgreich
gelesen</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>GET /AuditEvent/&lt;id&gt;</p></td>
<td style="text-align: left;"><p>200</p></td>
<td style="text-align: left;"><p>E-Rezeptereignis erfolgreich
gelesen</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>DELETE /ChargeItem/&lt;id&gt;</p></td>
<td style="text-align: left;"><p>204</p></td>
<td style="text-align: left;"><p>PKV-Abgabedaten erfolgreich
gelöscht</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>GET /ChargeItem</p></td>
<td style="text-align: left;"><p>200</p></td>
<td style="text-align: left;"><p>PKV-Abgabedaten erfolgreich
heruntergeladen</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>GET /ChargeItem/&lt;id&gt;</p></td>
<td style="text-align: left;"><p>200</p></td>
<td style="text-align: left;"><p>PKV-Abgabedaten erfolgreich
heruntergeladen</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>POST /ChargeItem</p></td>
<td style="text-align: left;"><p>201</p></td>
<td style="text-align: left;"><p>PKV-Abgabedaten erfolgreich
hochgeladen</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>PUT /ChargeItem/&lt;id&gt;</p></td>
<td style="text-align: left;"><p>200</p></td>
<td style="text-align: left;"><p>PKV-Abgabedaten erfolgreich
geändert</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>DELETE /Consent/&lt;id&gt;</p></td>
<td style="text-align: left;"><p>204</p></td>
<td style="text-align: left;"><p>Einwilligung erfolgreich
gelöscht</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>GET /Consent</p></td>
<td style="text-align: left;"><p>200</p></td>
<td style="text-align: left;"><p>Einwilligung erfolgreich
gelesen</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>POST /Consent</p></td>
<td style="text-align: left;"><p>201</p></td>
<td style="text-align: left;"><p>Einwilligung erolgreich
erteilt</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>GET /Device</p></td>
<td style="text-align: left;"><p>200</p></td>
<td style="text-align: left;"><p>Fachdienstinformationen erfolgreich
gelesen</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>GET /metadata</p></td>
<td style="text-align: left;"><p>200</p></td>
<td style="text-align: left;"><p>FHIR-CapabilityStatement erfolgreich
gelesen</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>POST /Subscription</p></td>
<td style="text-align: left;"><p>200</p></td>
<td style="text-align: left;"><p>Notifications-Kanal erfolgreich
aufgebaut</p></td>
</tr>
<tr class="odd">
<td colspan="3"
style="text-align: left;"><p><strong>Fehlerfälle</strong></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>GET /Task</p></td>
<td style="text-align: left;"><p>400</p></td>
<td style="text-align: left;"><p>Ungültiger http-Request</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>401</p></td>
<td style="text-align: left;"><p>Ungültiges/Abgelaufenes
AccessToken</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>403</p></td>
<td style="text-align: left;"><p>Unzulässige fachliche Rolle</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>406</p></td>
<td style="text-align: left;"><p>Angefragter Mime-Type im
<code>Accept</code>-Header kann nicht bedient werden</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>408</p></td>
<td style="text-align: left;"><p>Timeout</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>429</p></td>
<td style="text-align: left;"><p>Zuviele Anfragen pro Zeiteinheit durch
diesen Nutzer</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>GET /Task/&lt;id&gt;</p></td>
<td style="text-align: left;"><p>400</p></td>
<td style="text-align: left;"><p>Ungültiger http-Request</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>401</p></td>
<td style="text-align: left;"><p>Ungültiges/Abgelaufenes
AccessToken</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>403</p></td>
<td style="text-align: left;"><p>Unzulässige fachliche Rolle</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>404</p></td>
<td style="text-align: left;"><p>E-Rezept-Task wurde nicht
gefunden</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>406</p></td>
<td style="text-align: left;"><p>Angefragter Mime-Type im
<code>Accept</code>-Header kann nicht bedient werden</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>408</p></td>
<td style="text-align: left;"><p>Timeout</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>410</p></td>
<td style="text-align: left;"><p>E-Rezept-Task wurde zwischenzeitlich
gelöscht</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>429</p></td>
<td style="text-align: left;"><p>Zuviele Anfragen pro Zeiteinheit durch
diesen Nutzer</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>POST /Task/$create</p></td>
<td style="text-align: left;"><p>400</p></td>
<td style="text-align: left;"><ul>
<li><p>Unzulässiger workFlowType</p></li>
<li><p>Fehlerhafte XML-Struktur</p></li>
<li><p>Ungültiger http-Request</p></li>
</ul></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>401</p></td>
<td style="text-align: left;"><p>Ungültiges/Abgelaufenes
AccessToken</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>403</p></td>
<td style="text-align: left;"><p>Unzulässige fachliche Rolle</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>406</p></td>
<td style="text-align: left;"><p>Angefragter Mime-Type im
<code>Accept</code>-Header kann nicht bedient werden</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>408</p></td>
<td style="text-align: left;"><p>Timeout</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>415</p></td>
<td style="text-align: left;"><p>Der Client hat einen nicht
unterstützten Content-Type gesendet</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>429</p></td>
<td style="text-align: left;"><p>Zuviele Anfragen pro Zeiteinheit durch
diesen Nutzer</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>POST /Task/id/$activate</p></td>
<td style="text-align: left;"><p>400</p></td>
<td style="text-align: left;"><ul>
<li><p>Ungültige qualifizierte Arztsignatur</p></li>
<li><p>Fehler in der FHIR-Validierung</p></li>
<li><p>Fehlerhafte XML-Struktur</p></li>
<li><p>Verstoß gegen zusätzliche fachliche Prüfregel</p>
<ul>
<li><p>Ausschluss BtM</p></li>
<li><p>Flowtype nicht passend zum Coverage.type.coding.code</p></li>
<li><p>authoredOn ungleich Signaturdatum</p></li>
</ul></li>
</ul></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>401</p></td>
<td style="text-align: left;"><p>Ungültiges/Abgelaufenes
AccessToken</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>403</p></td>
<td style="text-align: left;"><ul>
<li><p>Ungültiger AccessCode</p></li>
<li><p>Unzulässige fachliche Rolle</p></li>
</ul></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>404</p></td>
<td style="text-align: left;"><p>E-Rezept-Task wurde nicht
gefunden</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>406</p></td>
<td style="text-align: left;"><p>Angefragter Mime-Type im
<code>Accept</code>-Header kann nicht bedient werden</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>408</p></td>
<td style="text-align: left;"><p>Timeout</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>410</p></td>
<td style="text-align: left;"><p>E-Rezept-Task wurde zwischenzeitlich
gelöscht</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>415</p></td>
<td style="text-align: left;"><p>Der Client hat einen nicht
unterstützten Content-Type gesendet</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>429</p></td>
<td style="text-align: left;"><p>Zuviele Anfragen pro Zeiteinheit durch
diesen Nutzer</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>POST /Task/id/$accept</p></td>
<td style="text-align: left;"><p>400</p></td>
<td style="text-align: left;"><p>Ungültiger http-Request</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>401</p></td>
<td style="text-align: left;"><p>Ungültiges/Abgelaufenes
AccessToken</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>403</p></td>
<td style="text-align: left;"><ul>
<li><p>Ungültiger AccessCode/Secret</p></li>
<li><p>Unzulässige fachliche Rolle</p></li>
</ul></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>404</p></td>
<td style="text-align: left;"><p>E-Rezept-Task wurde nicht
gefunden</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>406</p></td>
<td style="text-align: left;"><p>Angefragter Mime-Type im
<code>Accept</code>-Header kann nicht bedient werden</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>408</p></td>
<td style="text-align: left;"><p>Timeout</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>409</p></td>
<td style="text-align: left;"><p>Task befindet sich im falschen Zustand
(ungleich <code>ready</code>) für diese Operation<br />
Im OperationOutcome werden weitere Informationen gegeben:<br />
"Task has invalid status completed"<br />
"Task has invalid status in-progress"<br />
"Task has invalid status draft"</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>410</p></td>
<td style="text-align: left;"><p>E-Rezept-Task wurde zwischenzeitlich
gelöscht</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>429</p></td>
<td style="text-align: left;"><p>Zuviele Anfragen pro Zeiteinheit durch
diesen Nutzer</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>POST /Task/id/$reject</p></td>
<td style="text-align: left;"><p>400</p></td>
<td style="text-align: left;"><p>Ungültiger http-Request</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>401</p></td>
<td style="text-align: left;"><p>Ungültiges/Abgelaufenes
AccessToken</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>403</p></td>
<td style="text-align: left;"><ul>
<li><p>Ungültiges Secret</p></li>
<li><p>Unzulässige fachliche Rolle</p></li>
<li><p>Task befindet sich im falschen Zustand für diese
Operation</p></li>
</ul></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>404</p></td>
<td style="text-align: left;"><p>E-Rezept-Task wurde nicht
gefunden</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>408</p></td>
<td style="text-align: left;"><p>Timeout</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>410</p></td>
<td style="text-align: left;"><p>E-Rezept-Task wurde zwischenzeitlich
gelöscht</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>429</p></td>
<td style="text-align: left;"><p>Zuviele Anfragen pro Zeiteinheit durch
diesen Nutzer</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>POST /Task/id/$close</p></td>
<td style="text-align: left;"><p>400</p></td>
<td style="text-align: left;"><p>Ungültiger http-Request</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>401</p></td>
<td style="text-align: left;"><p>Ungültiges/Abgelaufenes
AccessToken</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>403</p></td>
<td style="text-align: left;"><ul>
<li><p>Ungültiges Secret</p></li>
<li><p>Unzulässige fachliche Rolle</p></li>
<li><p>Task befindet sich im falschen Zustand für diese
Operation</p></li>
</ul></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>404</p></td>
<td style="text-align: left;"><p>E-Rezept-Task wurde nicht
gefunden</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>406</p></td>
<td style="text-align: left;"><p>Angefragter Mime-Type im
<code>Accept</code>-Header kann nicht bedient werden</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>408</p></td>
<td style="text-align: left;"><p>Timeout</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>410</p></td>
<td style="text-align: left;"><p>E-Rezept-Task wurde zwischenzeitlich
gelöscht</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>415</p></td>
<td style="text-align: left;"><p>Der Client hat einen nicht
unterstützten Content-Type gesendet</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>429</p></td>
<td style="text-align: left;"><p>Zuviele Anfragen pro Zeiteinheit durch
diesen Nutzer</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>POST /Task/id/$abort</p></td>
<td style="text-align: left;"><p>400</p></td>
<td style="text-align: left;"><p>Ungültiger http-Request</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>401</p></td>
<td style="text-align: left;"><p>Ungültiges/Abgelaufenes
AccessToken</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>403</p></td>
<td style="text-align: left;"><ul>
<li><p>Ungültiger AccessCode/Secret</p></li>
<li><p>Unzulässige fachliche Rolle</p></li>
<li><p>Task befindet sich im falschen Zustand
(<strong>rollenabhängig</strong>) für diese Operation</p></li>
</ul></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>404</p></td>
<td style="text-align: left;"><p>E-Rezept-Task wurde nicht
gefunden</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>408</p></td>
<td style="text-align: left;"><p>Timeout</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>410</p></td>
<td style="text-align: left;"><p>E-Rezept-Task wurde zwischenzeitlich
gelöscht</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>429</p></td>
<td style="text-align: left;"><p>Zuviele Anfragen pro Zeiteinheit durch
diesen Nutzer</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>GET /MedicationDispense</p></td>
<td style="text-align: left;"><p>400</p></td>
<td style="text-align: left;"><p>Ungültiger http-Request</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>401</p></td>
<td style="text-align: left;"><p>Ungültiges/Abgelaufenes
AccessToken</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>403</p></td>
<td style="text-align: left;"><p>Unzulässige fachliche Rolle</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>406</p></td>
<td style="text-align: left;"><p>Angefragter Mime-Type im
<code>Accept</code>-Header kann nicht bedient werden</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>408</p></td>
<td style="text-align: left;"><p>Timeout</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>429</p></td>
<td style="text-align: left;"><p>Zuviele Anfragen pro Zeiteinheit durch
diesen Nutzer</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>GET
/MedicationDispense/&lt;id&gt;</p></td>
<td style="text-align: left;"><p>400</p></td>
<td style="text-align: left;"><p>Ungültiger http-Request</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>401</p></td>
<td style="text-align: left;"><p>Ungültiges/Abgelaufenes
AccessToken</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>403</p></td>
<td style="text-align: left;"><p>Unzulässige fachliche Rolle</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>404</p></td>
<td style="text-align: left;"><p>Dispensierinformationen wurden nicht
gefunden</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>406</p></td>
<td style="text-align: left;"><p>Angefragter Mime-Type im
<code>Accept</code>-Header kann nicht bedient werden</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>408</p></td>
<td style="text-align: left;"><p>Timeout</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>429</p></td>
<td style="text-align: left;"><p>Zuviele Anfragen pro Zeiteinheit durch
diesen Nutzer</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>GET /Communication</p></td>
<td style="text-align: left;"><p>400</p></td>
<td style="text-align: left;"><p>Ungültiger http-Request</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>401</p></td>
<td style="text-align: left;"><p>Ungültiges/Abgelaufenes
AccessToken</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>403</p></td>
<td style="text-align: left;"><p>Unzulässige fachliche Rolle</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>406</p></td>
<td style="text-align: left;"><p>Angefragter Mime-Type im
<code>Accept</code>-Header kann nicht bedient werden</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>408</p></td>
<td style="text-align: left;"><p>Timeout</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>429</p></td>
<td style="text-align: left;"><p>Zuviele Anfragen pro Zeiteinheit durch
diesen Nutzer</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>GET /Communication/&lt;id&gt;</p></td>
<td style="text-align: left;"><p>400</p></td>
<td style="text-align: left;"><p>Ungültiger http-Request</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>401</p></td>
<td style="text-align: left;"><p>Ungültiges/Abgelaufenes
AccessToken</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>403</p></td>
<td style="text-align: left;"><p>Unzulässige fachliche Rolle</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>404</p></td>
<td style="text-align: left;"><p>E-Rezeptnachricht wurden nicht
gefunden</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>406</p></td>
<td style="text-align: left;"><p>Angefragter Mime-Type im
<code>Accept</code>-Header kann nicht bedient werden</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>408</p></td>
<td style="text-align: left;"><p>Timeout</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>429</p></td>
<td style="text-align: left;"><p>Zuviele Anfragen pro Zeiteinheit durch
diesen Nutzer</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>POST /Communication</p></td>
<td style="text-align: left;"><p>400</p></td>
<td style="text-align: left;"><ul>
<li><p>Fehler in der FHIR-Validierung</p></li>
<li><p>Fehlerhafte XML-Struktur</p></li>
<li><p>Verstoß gegen zusätzliche fachliche Prüfregel (z.B. Existenz
Task)</p></li>
</ul></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>401</p></td>
<td style="text-align: left;"><p>Ungültiges/Abgelaufenes
AccessToken</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>403</p></td>
<td style="text-align: left;"><p>Unzulässige fachliche Rolle</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>406</p></td>
<td style="text-align: left;"><p>Angefragter Mime-Type im
<code>Accept</code>-Header kann nicht bedient werden</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>408</p></td>
<td style="text-align: left;"><p>Timeout</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>415</p></td>
<td style="text-align: left;"><p>Der Client hat einen nicht
unterstützten Content-Type gesendet</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>429</p></td>
<td style="text-align: left;"><p>Zuviele Anfragen pro Zeiteinheit durch
diesen Nutzer</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>DELETE /Communication/id</p></td>
<td style="text-align: left;"><p>400</p></td>
<td style="text-align: left;"><p>Ungültiger http-Request</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>401</p></td>
<td style="text-align: left;"><p>Ungültiges/Abgelaufenes
AccessToken</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>403</p></td>
<td style="text-align: left;"><p>Unzulässige fachliche Rolle</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>404</p></td>
<td style="text-align: left;"><p>E-Rezeptnachricht wurden nicht
gefunden</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>408</p></td>
<td style="text-align: left;"><p>Timeout</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>429</p></td>
<td style="text-align: left;"><p>Zuviele Anfragen pro Zeiteinheit durch
diesen Nutzer</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>GET /AuditEvent</p></td>
<td style="text-align: left;"><p>400</p></td>
<td style="text-align: left;"><p>Ungültiger http-Request</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>401</p></td>
<td style="text-align: left;"><p>Ungültiges/Abgelaufenes
AccessToken</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>403</p></td>
<td style="text-align: left;"><p>Unzulässige fachliche Rolle</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>406</p></td>
<td style="text-align: left;"><p>Angefragter Mime-Type im
<code>Accept</code>-Header kann nicht bedient werden</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>408</p></td>
<td style="text-align: left;"><p>Timeout</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>429</p></td>
<td style="text-align: left;"><p>Zuviele Anfragen pro Zeiteinheit durch
diesen Nutzer</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>GET /AuditEvent/&lt;id&gt;</p></td>
<td style="text-align: left;"><p>400</p></td>
<td style="text-align: left;"><p>Ungültiger http-Request</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>401</p></td>
<td style="text-align: left;"><p>Ungültiges/Abgelaufenes
AccessToken</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>403</p></td>
<td style="text-align: left;"><p>Unzulässige fachliche Rolle</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>404</p></td>
<td style="text-align: left;"><p>E-Rezeptereignis wurden nicht
gefunden</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>406</p></td>
<td style="text-align: left;"><p>Angefragter Mime-Type im
<code>Accept</code>-Header kann nicht bedient werden</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>408</p></td>
<td style="text-align: left;"><p>Timeout</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>429</p></td>
<td style="text-align: left;"><p>Zuviele Anfragen pro Zeiteinheit durch
diesen Nutzer</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>DELETE /ChargeItem/&lt;id&gt;</p></td>
<td style="text-align: left;"><p>400</p></td>
<td style="text-align: left;"><p>Ungültiger http-Request</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>401</p></td>
<td style="text-align: left;"><p>Ungültiges/Abgelaufenes
AccessToken</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>403</p></td>
<td style="text-align: left;"><p>Unzulässige fachliche Rolle</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>404</p></td>
<td style="text-align: left;"><p>PKV-Abgabedaten wurden nicht
gefunden</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>408</p></td>
<td style="text-align: left;"><p>Timeout</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>429</p></td>
<td style="text-align: left;"><p>Zuviele Anfragen pro Zeiteinheit durch
diesen Nutzer</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>GET /ChargeItem</p></td>
<td style="text-align: left;"><p>400</p></td>
<td style="text-align: left;"><p>Ungültiger http-Request</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>401</p></td>
<td style="text-align: left;"><p>Ungültiges/Abgelaufenes
AccessToken</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>403</p></td>
<td style="text-align: left;"><p>Unzulässige fachliche Rolle</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>406</p></td>
<td style="text-align: left;"><p>Angefragter Mime-Type im
<code>Accept</code>-Header kann nicht bedient werden</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>408</p></td>
<td style="text-align: left;"><p>Timeout</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>429</p></td>
<td style="text-align: left;"><p>Zuviele Anfragen pro Zeiteinheit durch
diesen Nutzer</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>GET /ChargeItem/&lt;id&gt;</p></td>
<td style="text-align: left;"><p>400</p></td>
<td style="text-align: left;"><p>Ungültiger http-Request</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>401</p></td>
<td style="text-align: left;"><p>Ungültiges/Abgelaufenes
AccessToken</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>403</p></td>
<td style="text-align: left;"><p>Unzulässige fachliche Rolle</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>404</p></td>
<td style="text-align: left;"><p>PKV-Abgabedaten wurden nicht
gefunden</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>406</p></td>
<td style="text-align: left;"><p>Angefragter Mime-Type im
<code>Accept</code>-Header kann nicht bedient werden</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>408</p></td>
<td style="text-align: left;"><p>Timeout</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>429</p></td>
<td style="text-align: left;"><p>Zuviele Anfragen pro Zeiteinheit durch
diesen Nutzer</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>POST /ChargeItem</p></td>
<td style="text-align: left;"><p>400</p></td>
<td style="text-align: left;"><ul>
<li><p>Fehler in der FHIR-Validierung</p></li>
<li><p>Fehlerhafte XML-Struktur</p></li>
<li><p>Verstoß gegen zusätzliche fachliche Prüfregel (z.B. Existenz
Task)</p></li>
</ul></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>401</p></td>
<td style="text-align: left;"><p>Ungültiges/Abgelaufenes
AccessToken</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>403</p></td>
<td style="text-align: left;"><p>Unzulässige fachliche Rolle</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>406</p></td>
<td style="text-align: left;"><p>Angefragter Mime-Type im
<code>Accept</code>-Header kann nicht bedient werden</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>408</p></td>
<td style="text-align: left;"><p>Timeout</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>409</p></td>
<td style="text-align: left;"><p>Der referenzierte Task ist nicht im
Zustand <code>completed</code></p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>415</p></td>
<td style="text-align: left;"><p>Der Client hat einen nicht
unterstützten Content-Type gesendet</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>429</p></td>
<td style="text-align: left;"><p>Zuviele Anfragen pro Zeiteinheit durch
diesen Nutzer</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>PUT/PATCH
/ChargeItem/&lt;id&gt;</p></td>
<td style="text-align: left;"><p>400</p></td>
<td style="text-align: left;"><p>Ungültiger http-Request</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>401</p></td>
<td style="text-align: left;"><p>Ungültiges/Abgelaufenes
AccessToken</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>403</p></td>
<td style="text-align: left;"><p>Unzulässige fachliche Rolle</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>404</p></td>
<td style="text-align: left;"><p>PKV-Abgabedaten wurden nicht
gefunden</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>406</p></td>
<td style="text-align: left;"><p>Angefragter Mime-Type im
<code>Accept</code>-Header kann nicht bedient werden</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>408</p></td>
<td style="text-align: left;"><p>Timeout</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>415</p></td>
<td style="text-align: left;"><p>Der Client hat einen nicht
unterstützten Content-Type gesendet</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>429</p></td>
<td style="text-align: left;"><p>Zuviele Anfragen pro Zeiteinheit durch
diesen Nutzer</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>DELETE /Consent/&lt;id&gt;</p></td>
<td style="text-align: left;"><p>400</p></td>
<td style="text-align: left;"><p>Ungültiger http-Request</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>401</p></td>
<td style="text-align: left;"><p>Ungültiges/Abgelaufenes
AccessToken</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>403</p></td>
<td style="text-align: left;"><p>Unzulässige fachliche Rolle</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>404</p></td>
<td style="text-align: left;"><p>Einwilligung wurden nicht
gefunden</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>408</p></td>
<td style="text-align: left;"><p>Timeout</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>429</p></td>
<td style="text-align: left;"><p>Zuviele Anfragen pro Zeiteinheit durch
diesen Nutzer</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>GET /Consent</p></td>
<td style="text-align: left;"><p>400</p></td>
<td style="text-align: left;"><p>Ungültiger http-Request</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>401</p></td>
<td style="text-align: left;"><p>Ungültiges/Abgelaufenes
AccessToken</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>403</p></td>
<td style="text-align: left;"><p>Unzulässige fachliche Rolle</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>406</p></td>
<td style="text-align: left;"><p>Angefragter Mime-Type im
<code>Accept</code>-Header kann nicht bedient werden</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>408</p></td>
<td style="text-align: left;"><p>Timeout</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>429</p></td>
<td style="text-align: left;"><p>Zuviele Anfragen pro Zeiteinheit durch
diesen Nutzer</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>POST /Consent</p></td>
<td style="text-align: left;"><p>400</p></td>
<td style="text-align: left;"><p>Ungültiger http-Request</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>401</p></td>
<td style="text-align: left;"><p>Ungültiges/Abgelaufenes
AccessToken</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>403</p></td>
<td style="text-align: left;"><p>Unzulässige fachliche Rolle</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>406</p></td>
<td style="text-align: left;"><p>Angefragter Mime-Type im
<code>Accept</code>-Header kann nicht bedient werden</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>408</p></td>
<td style="text-align: left;"><p>Timeout</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>409</p></td>
<td style="text-align: left;"><p>Einwilligung existiert bereits für
diesen Nutzer</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>415</p></td>
<td style="text-align: left;"><p>Der Client hat einen nicht
unterstützten Content-Type gesendet</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>429</p></td>
<td style="text-align: left;"><p>Zuviele Anfragen pro Zeiteinheit durch
diesen Nutzer</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>GET /Device</p></td>
<td style="text-align: left;"><p>400</p></td>
<td style="text-align: left;"><p>Ungültiger http-Request</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>401</p></td>
<td style="text-align: left;"><p>Ungültiges/Abgelaufenes
AccessToken</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>406</p></td>
<td style="text-align: left;"><p>Angefragter Mime-Type im
<code>Accept</code>-Header kann nicht bedient werden</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>GET /metadata</p></td>
<td style="text-align: left;"><p>400</p></td>
<td style="text-align: left;"><p>Ungültiger http-Request</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>401</p></td>
<td style="text-align: left;"><p>Ungültiges/Abgelaufenes
AccessToken</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>406</p></td>
<td style="text-align: left;"><p>Angefragter Mime-Type im
<code>Accept</code>-Header kann nicht bedient werden</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>POST /Subscription</p></td>
<td style="text-align: left;"><p>400</p></td>
<td style="text-align: left;"><p>Ungültiger http-Request</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>401</p></td>
<td style="text-align: left;"><p>Ungültiges/Abgelaufenes
AccessToken</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>403</p></td>
<td style="text-align: left;"><p>Unzulässige fachliche Rolle</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>406</p></td>
<td style="text-align: left;"><p>Angefragter Mime-Type im
<code>Accept</code>-Header kann nicht bedient werden</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>408</p></td>
<td style="text-align: left;"><p>Timeout</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>415</p></td>
<td style="text-align: left;"><p>Der Client hat einen nicht
unterstützten Content-Type gesendet</p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>429</p></td>
<td style="text-align: left;"><p>Zuviele Anfragen pro Zeiteinheit durch
diesen Nutzer</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>UNKNOWN</p></td>
<td style="text-align: left;"><p>400</p></td>
<td style="text-align: left;"><p>Ungültiger http-Request</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>401</p></td>
<td style="text-align: left;"><p>Ungültiges/Abgelaufenes
AccessToken</p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>405</p></td>
<td style="text-align: left;"><p>Diese http-Methode ist nicht
erlaubt</p></td>
<td></td>
</tr>
</tbody>
</table>
