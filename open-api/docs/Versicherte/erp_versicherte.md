Hier dokumentiert die gematik die Nutzung der Schnittstellen rund um das
E-Rezept aus Sicht der Versicherten, die ihre E-Rezepte verwalten und
einlösen möchten.

# Anwendungsfälle E-Rezept als Versicherter verwalten

Der Versicherte hat mit der E-Rezept-App die Möglichkeit, seine
E-Rezepte zu verwalten, Zugriffsprotokolle einzusehen und sich
zusätzliche Informationen über das herausgegebene Medikament
herunterzuladen.  
Verzichtet er bei der Handhabung des E-Rezepts auf einen Papierausdruck
in der Arztpraxis, erfolgt die Einlösung des E-Rezeptes ebenso über die
E-Rezept-App. Dafür generiert die E-Rezept-App aus den heruntergeladenen
E-Rezept-Daten einen 2D-Code (DataMatrix-Darstellung), den er in der
Apotheke vom Bildschirm seines Smartphones abscannen lässt. Mit den
abgescannten Informationen [erhält der Apotheker die Adresse und
Zugriffsberechtigung](./erp_abrufen.adoc) des E-Rezepts, um seinerseits
das E-Rezept herunterzuladen und den Versicherten dann mit dem
Medikament versorgen zu dürfen.  

Einige der nachfolgenden UseCases sind auch für Vertreter des
Versicherten vorgesehen, dabei sind sie bspw. berechtigt, ein E-Rezept
einzusehen bzw. herunterzuladen, wenn sie im Wissen um den zugehörigen
AccessCode sind, den sie vom Versicherten mitgeteilt bekommen (z.B.
durch Abscannen des 2D-Codes vom Smartphone des Versicherten).  

Die Kommunikation zwischen Versicherten und einer Apotheke über
E-Rezepte erfolgt ebenfalls über den Dienst zur Verwaltung der
E-Rezepte. Aus Gründen der besseren Lesbarkeit und der Darstellung der
Zusammenhänge zwischen Anfrage zur Verfügbarkeit eines Medikaments und
der Antwort einer Apotheke erfolgt die Beschreibung über das [an dieser
Stelle verlinkte Dokument](./erp_communication.adoc).

# Profilierung

In diesen Anwendungsfällen werden die FHIR-Resourcen "Task":
<http://hl7.org/fhir/task.html> und AuditEvent
<https://www.hl7.org/fhir/auditevent.html> verwendet. Die Ressource
Bundle <https://www.hl7.org/fhir/bundle.html> kommt in ihrem
Standardprofil als Suchergebnis und zusätzlich als signiertes Dokument
der Verordnung und als Quittung zur Anwendung. Diese werden für das
E-Rezept profiliert und werden hier spezifiziert:  
Task: <https://simplifier.net/erezept-workflow/gem_erp_pr_task>  
AuditEvent:
<https://simplifier.net/erezept-workflow/gem_erp_pr_auditevent>

# Alle E-Rezepte ansehen

Als Versicherter möchte ich all meine E-Rezepte einsehen.

Der Aufruf erfolgt als http-`GET`-Operation auf die Ressource `/Task`.
Im Aufruf muss das während der Authentisierung erhaltene ACCESS\_TOKEN
im http-Request-Header `Authorization` übergeben werden, der Fachdienst
filtert die Task-Einträge nach der im ACCESS\_TOKEN enthaltenen KVNR des
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
href="https://erp.app.ti-dienste.de/Task">https://erp.app.ti-dienste.de/Task</a></p></td>
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
      "link": [
        {
          "relation": "self",
          "url": "https://erp.app.ti-dienste.de/Task/"
        }
      ],
      "entry": [
        {
          "fullUrl": "https://erp.app.ti-dienste.de/Task/160.123.456.789.123.58",
          "resource": {
            "resourceType": "Task",
            "id": "160.123.456.789.123.58",
            "meta": {
              "versionId": "2",
              "lastUpdated": "2020-02-18T10:05:05.038+00:00",
              "source": "#AsYR9plLkvONJAiv",
              "profile": [
                "https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_PR_Task|1.2"
              ]
            },
            "identifier": [
              {
                "use": "official",
                "system": "https://gematik.de/fhir/erp/NamingSystem/GEM_ERP_NS_PrescriptionId",
                "value": "160.123.456.789.123.58"
              },
              {
                "use": "official",
                "system": "https://gematik.de/fhir/erp/NamingSystem/GEM_ERP_NS_AccessCode",
                "value": "777bea0e13cc9c42ceec14aec3ddee2263325dc2c6c699db115f58fe423607ea"
              }
            ],
            "intent": "order",
            "status": "ready",
            "extension": [
              {
                "url": "https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_EX_PrescriptionType",
                "valueCoding": {
                  "code": "160",
                  "system": "https://gematik.de/fhir/erp/CodeSystem/GEM_ERP_CS_FlowType",
                  "display": "Muster 16 (Apothekenpflichtige Arzneimittel)"
                }
              },
              {
                "url": "https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_EX_ExpiryDate",
                "valueDate": "2020-06-02"
              },
              {
                "url": "https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_EX_AcceptDate",
                "valueDate": "2020-04-01"
              }
            ],
            "authoredOn": "2020-03-02T08:25:05+00:00",
            "lastModified": "2020-03-02T08:45:05+00:00",
            "performerType": [
               {
                 "coding": [
                   {
                     "code": "urn:oid:1.2.276.0.76.4.54",
                     "system": "https://gematik.de/fhir/erp/CodeSystem/GEM_ERP_CS_OrganizationType",
                     "display": "Öffentliche Apotheke"
                   }
                 ]
               }
            ]
          }
        },
        {
          "fullUrl": "https://erp.app.ti-dienste.de/Task/160.123.456.789.123.78",
          "resource": {
            "resourceType": "Task",
            "id": "160.123.456.789.123.78",
            "meta": {
              "versionId": "2",
              "lastUpdated": "2020-02-18T10:06:05.038+00:00",
              "source": "#AsYR9plLkvONJAiv",
              "profile": [
                "https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_PR_Task|1.2"
              ]
            },
            "identifier": [
              {
                "use": "official",
                "system": "https://gematik.de/fhir/erp/NamingSystem/GEM_ERP_NS_PrescriptionId",
                "value": "160.123.456.789.123.78"
              },
              {
                "use": "official",
                "system": "https://gematik.de/fhir/erp/NamingSystem/GEM_ERP_NS_AccessCode",
                "value": "777bea0e13cc9c42ceec14aec3ddee8402643dc2c6c699db115f58fe423607ea"
              }
            ],
            "intent": "order",
            "status": "ready",
            "extension": [
              {
                "url": "https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_EX_PrescriptionType",
                "valueCoding": {
                  "code": "160",
                  "system": "https://gematik.de/fhir/erp/CodeSystem/GEM_ERP_CS_FlowType",
                  "display": "Muster 16 (Apothekenpflichtige Arzneimittel)"
                }
              },
              {
                "url": "https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_EX_ExpiryDate",
                "valueDate": "2020-06-02"
              },
              {
                "url": "https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_EX_AcceptDate",
                "valueDate": "2020-04-01"
              }
            ],
            "authoredOn": "2020-03-02T08:25:05+00:00",
            "lastModified": "2020-03-02T08:45:05+00:00",
            "performerType": [
               {
                 "coding": [
                   {
                     "code": "urn:oid:1.2.276.0.76.4.54",
                     "system": "https://gematik.de/fhir/erp/CodeSystem/GEM_ERP_CS_OrganizationType",
                     "display": "Öffentliche Apotheke"
                   }
                 ]
               }
            ]
          }
        }
      ]
    }

Mit dem AccessCode
`"value":"777bea0e13cc9c42ceec14aec3ddee2263325dc2c6c699db115f58fe423607ea"`
wird der Zugriff für Vertreter und Apotheker gesteuert, in dem der
Versicherte diesen AccessCode z.B. als QR-Code weitergibt

Der Prozesstyp referenziert die Workflow-Definition, in diesem Fall den
Prozess für apothekenpflichtige Arzneimittel mit
`"url":"https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_EX_PrescriptionType"`

Mit der Angabe `"display":"Apotheke"` kann dem Versicherten ein Hinweis
angezeigt werden, wo er das E-Rezept einlösen kann (bspw. Apotheke oder
Sanitätshaus).

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

# Ein einzelnes E-Rezept abrufen und in der Apotheke einlösen

Der Zugriff auf ein einzelnes E-Rezept ist durch den Versicherten mit
Nachweis seiner Identität immer zulässig. Als Vertreter ist der Zugriff
auf ein E-Rezept eines anderen Versicherten nur gestattet, wenn der
Vertreter in Kenntnis des beim Einstellen des E-Rezepts erzeugten
AccessCodes ist.

Der Aufruf erfolgt als http-`GET`-Operation auf eine konkrete Ressource
`/Task/<task_id>`. Im Aufruf muss das während der Authentisierung
erhaltene ACCESS\_TOKEN im http-Request-Header `Authorization` übergeben
werden. Der Aufruf kann auch durch einen Vertreter des Versicherten
erfolgen, hierbei wird lediglich die Rolle `Versicherter` im
ACCESS\_TOKEN geprüft. Um die Berechtigung für den Zugriff auf einen
Task mit einer fremden KVNR nachzuweisen, muss der Zugreifende den
richtigen AccessCode im http-Request-Header `X-AccessCode` übergeben.
Die Rückgabe eines Tasks erfolgt immer zusammen mit dem entsprechenden,
signierten E-Rezept-Datensatz zu diesem Task, welcher die
Verordnungsinformationen des E-Rezepts enthält.

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
href="https://erp.app.ti-dienste.de/Task/160.123.456.789.123.58">https://erp.app.ti-dienste.de/Task/160.123.456.789.123.58</a></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>Method</strong></p></td>
<td style="text-align: left;"><p>GET</p></td>
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
</div>
<div class="note">
<p>Als Vertreter (wenn im E-Rezept eine andere Versichertennummer als im
Token des Zugreifenden angegeben ist) muss im http-Header der
<code>AccessCode</code> übergeben werden</p>
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

**Response** HTTP/1.1 200 OK Content-Type:
application/fhir+json;charset=utf-8

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
        "url": "https://erp.app.ti-dienste.de/Task/160.123.456.789.123.58"
      }],
      "entry": [{
        "fullUrl": "https://erp.app.ti-dienste.de/Task/160.123.456.789.123.58",
        "resource": {
            "resourceType": "Task",
            "id": "160.123.456.789.123.58",
            "meta": {
              "versionId": "2",
              "lastUpdated": "2020-02-18T10:05:05.038+00:00",
              "source": "#AsYR9plLkvONJAiv",
              "profile": [
                "https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_PR_Task|1.2"
              ]
            },
            "identifier": [
              {
                "use": "official",
                "system": "https://gematik.de/fhir/erp/NamingSystem/GEM_ERP_NS_PrescriptionId",
                "value": "160.123.456.789.123.58"
              },
              {
                "use": "official",
                "system": "https://gematik.de/fhir/erp/NamingSystem/GEM_ERP_NS_AccessCode",
                "value": "777bea0e13cc9c42ceec14aec3ddee2263325dc2c6c699db115f58fe423607ea"
              }
            ],
            "intent": "order",
            "status": "ready",
            "extension": [
              {
                "url": "https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_EX_PrescriptionType",
                "valueCoding": {
                  "code": "160",
                  "system": "https://gematik.de/fhir/erp/CodeSystem/GEM_ERP_CS_FlowType",
                  "display": "Muster 16 (Apothekenpflichtige Arzneimittel)"
                }
              },
              {
                "url": "https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_EX_ExpiryDate",
                "valueDate": "2020-06-02"
              },
              {
                "url": "https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_EX_AcceptDate",
                "valueDate": "2020-04-01"
              }
            ],
            "authoredOn": "2020-03-02T08:25:05+00:00",
            "lastModified": "2020-03-02T08:45:05+00:00",
            "performerType": [
               {
                 "coding": [
                   {
                     "code": "urn:oid:1.2.276.0.76.4.54",
                     "system": "https://gematik.de/fhir/erp/CodeSystem/GEM_ERP_CS_OrganizationType",
                     "display": "Öffentliche Apotheke"
                   }
                 ]
               }
            ],
            "input": [{
            "type": {
              "coding": [{
                "system":"https://gematik.de/fhir/erp/CodeSystem/GEM_ERP_CS_DocumentType",
                "code":"2"
              }]
            },
            "valueString": "f8c2298f-7c00-4a68-af29-8a2862d55d43"
          }]
          }
      },{
        "resource": {
            "resourceType": "Bundle",
            "id": "414ca393-dde3-4082-9a3b-3752e629e4aa",
            "meta": {
              "lastUpdated": "2022-05-20T08:30:00Z",
              "profile": [
                "https://fhir.kbv.de/StructureDefinition/KBV_PR_ERP_Bundle|1.1.0"
              ]
            },
            "identifier": {
              "system": "https://gematik.de/fhir/erp/NamingSystem/GEM_ERP_NS_PrescriptionId",
              "value": "200.086.824.605.539.20"
            },
            [...]
          "signature": {
            "type": {
              "system": "http://hl7.org/fhir/ValueSet/signature-type",
              "code": "1.2.840.10065.1.12.1.1"
            },
            "when": "2020-03-20T07:31:34.328+00:00",
            "who": "https://erp.app.ti-dienste.de/signature/verification",
            "data": "eyJ0eXAiOiJKV1MiLCJhbGciOiJFUzI1NiIsIng1dSI6Imh0dHBzOi8vcHJlc2NyaXB0aW9uc2VydmVyLnRlbGVtYXRpay9zaWduYXR1cmUvY2VydGlmaWNhdGUifQ
            .
            eyJyZXNvdXJjZVR5cGUiOiJCdW5kbGUiLCJpZCI6ImY4YzIyOThmLTdjMDAtNGE2OC1hZjI5LThhMjg2MmQ1NWQ0MyIsImlkZW50aWZpZXIiOnsic3lzdGVtIjoiaHR0cHM6Ly9nZW1hdGlrLmRlL1ZhbHVlU2V0L0VSWF9QUkVTQ 1JJUFRJT05fSUQiLCJ2YWx1ZSI6Ik0xNi4xMjMuNDU2Ljc4OS4xMjMuMTMifSwidHlwZSI6ImRvY3VtZW50IiwiZW50cnkiOlt7ImZ1bGxVcmwiOiJodHRwOi8vcHZzLnByYXhpcy10b3BwLWdsdWVja2xpY2gubG9jYWwvZmhpci 9Db21wb3NpdGlvbi9lZDUyYzFlMy1iNzAwLTQ0OTctYWUxOS1iMjM3NDRlMjk4NzYiLCJyZXNvdXJjZSI6eyJyZXNvdXJjZVR5cGUiOiJDb21wb3NpdGlvbiJ9fSx7ImZ1bGxVcmwiOiJodHRwOi8vcHZzLnByYXhpcy10b3BwLWd sdWVja2xpY2gubG9jYWwvZmhpci9NZWRpY2F0aW9uUmVxdWVzdC9lOTMwY2RlZS05ZWI1LTRiNDQtODhiNS0yYTE4YjY5ZjNiOWEiLCJyZXNvdXJjZSI6eyJyZXNvdXJjZVR5cGUiOiJNZWRpY2F0aW9uUmVxdWVzdCJ9fV19
            .
            SSBhbSBhIHNpZ25hdHVyZSE="
          }
        }
      }]
    }

Mit dem AccessCode in
`"value":"777bea0e13cc9c42ceec14aec3ddee2263325dc2c6c699db115f58fe423607ea"`
wird der Zugriff für Vertreter und Apotheker gesteuert, in dem der
Versicherte diesen AccessCode z.B. als QR-Code weitergibt.

Bei `"value":"X123456789"` ist die KVNR des Versicherten enthalten, nach
welcher die Rezept-Tasks gefiltert wurden. Im Ergebnis wurde nur ein
einzelnes E-Rezept gefunden.

Der Prozesstyp in
`"url":"https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_EX_PrescriptionType"`
referenziert die Workflow-Definition, in diesem Fall den Prozess für
apothekenpflichtige Arzneimittel.

Mit der Angabe \` "display":"Apotheke"\` kann dem Versicherten ein
Hinweis angezeigt werden, wo er das E-Rezept einlösen kann (bspw.
Apotheke oder Sanitätshaus).

Mit `"valueString": "f8c2298f-7c00-4a68-af29-8a2862d55d43"` verweist der
Task auf das signierte E-Rezept-Bundle im zurückgegebenen Bundle.

Aus Gründen der besseren Lesbarkeit ist das E-Rezept-Bundle hier nicht
vollständig dargestellt. Ein komplettes Beispiel kann hier eingesehen
werden:
<https://simplifier.net/eRezept/0428d416-149e-48a4-977c-394887b3d85c/~json>.

Bei der Rückgabe an den Versicherten wird der ärztliche Signaturanteil
in \` "signature"\` des E-Rezept-Bundles durch eine serverseitige
Signatur in JWS-Format ersetzt. Aus Gründen der besseren Lesbarkeit mit
separaten Zeilenumbrüchen zwischen den "."-separierten
`Header.Payload.Signature` .

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

# Informationen an den Apotheker übergeben

Um den Apotheker in die Lage zu versetzen, das E-Rezept einsehen zu
können, müssen ihm die folgenden zwei Parameter für seinen Abruf
übergeben werden, z.B. in Form eines QR-Codes oder DataMatrix-Codes:

-   AccessCode:
    `777bea0e13cc9c42ceec14aec3ddee2263325dc2c6c699db115f58fe423607ea`

-   Adresse des Tasks unter dem das E-Rezept geführt wird:
    `https://erp.app.ti-dienste.de/Task/160.123.456.789.123.58`

Diese Informationen lassen sich nach den Vorgaben in
`ISO/IEC 18004:2015` in einen QR-Code oder gemäß ISO/IEC 16022:2006 in
einen DataMatrix-Code transformieren.

<table style="width:99%;">
<colgroup>
<col style="width: 49%" />
<col style="width: 49%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><div class="sourceCode" id="cb1"><pre
class="sourceCode json"><code class="sourceCode json"><span id="cb1-1"><a href="#cb1-1" aria-hidden="true" tabindex="-1"></a><span class="fu">{</span></span>
<span id="cb1-2"><a href="#cb1-2" aria-hidden="true" tabindex="-1"></a>  <span class="dt">&quot;urls&quot;</span><span class="fu">:</span> <span class="ot">[</span> <span class="st">&quot;Task/160.123.456.789.123.58/$accept?ac=777bea0e13cc9c42ceec14aec3ddee2263325dc2c6c699db115f58fe423607ea&quot;</span> <span class="ot">]</span></span>
<span id="cb1-3"><a href="#cb1-3" aria-hidden="true" tabindex="-1"></a><span class="fu">}</span></span></code></pre></div></td>
<td style="text-align: center;"><pre><code>image:datamatrix_sample.png[width=250px]</code></pre>
<p>In DataMatrix-Darstellung gemäß ISO/IEC 16022:2006</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><pre><code>Sammlung von drei E-Rezept-Referenzen in einem 2D-Code +</code></pre>
<div class="sourceCode" id="cb4"><pre
class="sourceCode json"><code class="sourceCode json"><span id="cb4-1"><a href="#cb4-1" aria-hidden="true" tabindex="-1"></a><span class="fu">{</span></span>
<span id="cb4-2"><a href="#cb4-2" aria-hidden="true" tabindex="-1"></a>  <span class="dt">&quot;urls&quot;</span><span class="fu">:</span> <span class="ot">[</span></span>
<span id="cb4-3"><a href="#cb4-3" aria-hidden="true" tabindex="-1"></a>    <span class="st">&quot;Task/160.123.456.789.123.58/$accept?ac=777bea0e13cc9c42ceec14aec3ddee2263325dc2c6c699db115f58fe423607ea&quot;</span><span class="ot">,</span></span>
<span id="cb4-4"><a href="#cb4-4" aria-hidden="true" tabindex="-1"></a>    <span class="st">&quot;Task/160.346.135.722.516.16/$accept?ac=0936cfa582b447144b71ac89eb7bb83a77c67c99d4054f91ee3703acf5d6a629&quot;</span><span class="ot">,</span></span>
<span id="cb4-5"><a href="#cb4-5" aria-hidden="true" tabindex="-1"></a>    <span class="st">&quot;Task/160.880.966.157.248.22/$accept?ac=d3e6092ae3af14b5225e2ddbe5a4f59b3939a907d6fdd5ce6a760ca71f45d8e5&quot;</span></span>
<span id="cb4-6"><a href="#cb4-6" aria-hidden="true" tabindex="-1"></a>  <span class="ot">]</span></span>
<span id="cb4-7"><a href="#cb4-7" aria-hidden="true" tabindex="-1"></a><span class="fu">}</span></span></code></pre></div></td>
<td style="text-align: center;"><pre><code>image:datamatrix_sample_3.png[width=250px]</code></pre>
<p>In DataMatrix-Darstellung gemäß ISO/IEC 16022:2006</p></td>
</tr>
</tbody>
</table>

Aktuell unterstüten die Apothekenverwaltungssysteme auf Basis des
SecurPharm-System in jedem Fall das DataMatrix-Format.

**\***

# Eine Apotheke aus dem Apotheken-Verzeichnis auswählen

Als Versicherter möchte ich eine Apotheke aus einem Verzeichnis wählen,
um ihr eine Verfügbarkeitsanfrage zu meinem E-Rezept zu schicken oder
ihr ein E-Rezept direkt zuzuweisen. Der Verzeichnisdienst der
Telematikinfrastruktur führt eine Liste aller (Zahn-)Arztpraxen,
Krankenhäuser und Apotheken in Deutschland, in der nach einer Apotheke
über z.B. den Namen oder die Postleitzahl für eine Umgebungssuche
gesucht werden kann. Im folgenden Beispiel wird die Suche nach Apotheken
im Umkreis von `7 km` um den aktuellen Standort ausgeführt.  
`https://apovzd.app.ti-dienste.de/api/Location?near=48.13129322109354%7C11.563464055060686%7C999%7Ckm`

Folgende Suchalternativen sind ebenfalls möglich:

-   Suche nach einer Apotheke mit konkretem Namen "Apotheke um die
    Ecke"  
    `https://apovzd.app.ti-dienste.de/api/Location?name=Apotheke%20um%20die%20Ecke`

-   Suche nach allen Apotheken in "Berlin"  
    `https://apovzd.app.ti-dienste.de/api/Location?address-city=Berlin`

Der Aufruf erfolgt als http-`GET`-Operation am Apothekenverzeichnis der
Telematikinfrastruktur für die Ressource `/Location`. Eine
Authentifizierung der App-Nutzer erfolgt nicht, eine Absicherung
gegenüber unberechtigte Zugriffe erfolgt mitels API-Key. Der
Verzeichnisdienst liefert eine Liste von Apotheken, welche den ggfs.
angegebenen Suchparametern entsprechen. Liefert die gewählte Suchanfrage
eine zu große Ergebnismenge, bricht der Verzeichnisdienst bei einer
technischen Obergrenze von max. `100` Ergebniseinträgen ab.

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
href="https://apovzd.app.ti-dienste.de/api/Location?name=Adler">https://apovzd.app.ti-dienste.de/api/Location?name=Adler</a></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>Method</strong></p></td>
<td style="text-align: left;"><p>GET</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>Request</strong></p></td>
<td style="text-align: left;"><pre><code>GET /api/Location?name=Adler HTTP/1.1
Host: apovzd.app.ti-dienste.de
Pragma: no-cache
Cache-Control: no-cache</code></pre>
<div class="tip">
<p>Dieser Request ist NICHT zusätzlich VAU-verschlüsselt, sondern wird
plain an das Apothekenverzeichnis geschickt.</p>
</div></td>
</tr>
</tbody>
</table>

In der Aufruf-Adresse können Suchparameter gemäß
<https://www.hl7.org/fhir/organization.html#search> angegeben werden
(wie hier in `GET /api/Location?name=Adler HTTP/1.1`). Im konkreten
Beispiel soll nach Apotheken (`Location`) mit `Adler` im Namen gefiltert
werden. Weitere Suchparameter können z.B. eine Ortsangabe (z.B.
`address-city=Köln` bzw. `address-city=K%C3%B6ln`) umfassen. Mehrere
Suchparameter werden über das `&`-Zeichen miteinander kombiniert.

**Response**

    HTTP/1.1 200 OK
    Content-Type: application/fhir+json;charset=utf-8

    ...

    {
      "id": "2b50e07d-ace1-4f83-ae8f-e2845e291cc3",
      "meta": {
        "lastUpdated": "2021-11-23T10:33:52.590809+02:00"
      },
      "resourceType": "Bundle",
      "type": "searchset",
      "total": 2,
      "link": [
        {
          "relation": "self",
          "url": "Bundle2b50e07d-ace1-4f83-ae8f-e2845e291cc3"
        }
      ],
      "entry": [
        {
          "resource": {
            "id": "5a403761-3a18-4ae9-bca8-9ed8abada08a",
            "resourceType": "Location",
            "address": {
              "use": "work",
              "type": "physical",
              "line": [
                "Friedrichstr. 136"
              ],
              "postalCode": "10117",
              "city": "Berlin",
              "country": "de"
            },
            "identifier": [
              {
                "system": "https://gematik.de/fhir/sid/telematik-id",
                "value": "3-1.54.10123404"
              }
            ],
            "name": "Adlerapotheke",
            "position": {
              "latitude": 52.522575,
              "longitude": 13.387884
            },
            "status": "active",
            "telecom": [
              {
                "system": "email",
                "value": "service@gematik.de"
              },
              {
                "system": "phone",
                "value": "030 40041 0"
              },
              {
                "system": "url",
                "value": "www.gematik.de"
              }
            ],
            "type": [
              {
                "coding": [
                  {
                    "system": "http://terminology.hl7.org/CodeSystem/v3-RoleCode",
                    "code": "PHARM",
                    "display": "pharmacy"
                  }
                ]
              },
              {
                "coding": [
                  {
                    "system": "http://terminology.hl7.org/CodeSystem/v3-RoleCode",
                    "code": "MOBL",
                    "display": "Mobile Services"
                  }
                ]
              }
            ]
          },
          "search": {
            "mode": "match"
          }
        },
        {
          "resource": {
            "id": "354d16fa-ceff-4a18-b1b7-c583ee211cea",
            "meta": {
              "lastUpdated": "2021-10-12T11:54:29+02:00"
            },
            "resourceType": "Location",
            "contained": [
              {
                "id": "8fe0eea1-6379-41ce-bb51-efd33f02e853",
                "resourceType": "HealthcareService",
                "active": true,
                "coverageArea": [
                  {
                    "extension": [
                      {
                        "url": "https://ngda.de/fhir/extensions/ServiceCoverageRange",
                        "valueQuantity": {
                          "value": 5000,
                          "unit": "m"
                        }
                      }
                    ]
                  }
                ],
                "location": [
                  {
                    "reference": "/Location/354d16fa-ceff-4a18-b1b7-c583ee211cea"
                  }
                ],
                "type": [
                  {
                    "coding": [
                      {
                        "system": "http://terminology.hl7.org/CodeSystem/service-type",
                        "code": "498",
                        "display": "Mobile Services"
                      }
                    ]
                  }
                ]
              }
            ],
            "address": {
              "use": "work",
              "type": "physical",
              "line": [
                "Adlerstr. 21"
              ],
              "postalCode": "10178",
              "city": "Berlin",
              "country": "de"
            },
            "hoursOfOperation": [
              {
                "daysOfWeek": [
                  "mon"
                ],
                "openingTime": "08:30:00",
                "closingTime": "13:30:00"
              },
              {
                "daysOfWeek": [
                  "mon"
                ],
                "openingTime": "14:30:00",
                "closingTime": "18:30:00"
              },
              {
                "daysOfWeek": [
                  "tue"
                ],
                "openingTime": "08:30:00",
                "closingTime": "13:30:00"
              },
              {
                "daysOfWeek": [
                  "tue"
                ],
                "openingTime": "14:30:00",
                "closingTime": "18:30:00"
              },
              {
                "daysOfWeek": [
                  "wed"
                ],
                "openingTime": "08:30:00",
                "closingTime": "13:30:00"
              },
              {
                "daysOfWeek": [
                  "wed"
                ],
                "openingTime": "14:30:00",
                "closingTime": "18:30:00"
              },
              {
                "daysOfWeek": [
                  "thu"
                ],
                "openingTime": "08:30:00",
                "closingTime": "13:30:00"
              },
              {
                "daysOfWeek": [
                  "thu"
                ],
                "openingTime": "14:30:00",
                "closingTime": "18:30:00"
              },
              {
                "daysOfWeek": [
                  "fri"
                ],
                "openingTime": "08:30:00",
                "closingTime": "13:30:00"
              },
              {
                "daysOfWeek": [
                  "fri"
                ],
                "openingTime": "14:30:00",
                "closingTime": "18:30:00"
              },
              {
                "daysOfWeek": [
                  "sat"
                ],
                "openingTime": "08:30:00",
                "closingTime": "14:00:00"
              }
            ],
            "identifier": [
              {
                "system": "https://gematik.de/fhir/sid/telematik-id",
                "value": "3-10.2.0123456100.10.228"
              },
              {
                "system": "https://ngda.de/fhir/NamingSystem/NID",
                "value": "APO1234642"
              }
            ],
            "name": "Apotheke am Adler",
            "position": {
              "latitude": 52.523044,
              "longitude": 13.411917
            },
            "status": "active",
            "telecom": [
              {
                "system": "phone",
                "value": "030/400410"
              },
              {
                "system": "email",
                "value": "erezept@gematik.de"
              },
              {
                "system": "url",
                "value": "https://www.gematik.de"
              }
            ],
            "type": [
              {
                "coding": [
                  {
                    "system": "http://terminology.hl7.org/CodeSystem/v3-RoleCode",
                    "code": "PHARM",
                    "display": "pharmacy"
                  }
                ]
              },
              {
                "coding": [
                  {
                    "system": "http://terminology.hl7.org/CodeSystem/v3-RoleCode",
                    "code": "OUTPHARM",
                    "display": "outpatient pharmacy"
                  }
                ]
              }
            ]
          },
          "search": {
            "mode": "match"
          }
        }
      ]
    }

Die Suchanfrage nach `Adler`-Apotheken liefert genau zwei Treffer.

Die `Telematik-ID` ist die eindeutige Kennung der Apotheke, um an diese
bspw. eine Nachricht zu schicken.

Der Name der Apotheke, unter dem sie im Verzeichnis geführt wird findet
sich unter z.B.`"name": "Apotheke am Adler"`

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
<span class="small">Es wurde kein passender Verzeichniseintrag
gefunden.</span></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>500</p></td>
<td style="text-align: left;"><p>Server Errors<br />
<span class="small">Unerwarteter Serverfehler</span></p></td>
</tr>
</tbody>
</table>

Mit dem Suchergebnis kennt der Versicherte nun die Apotheken in seinem
Umkreis. Eine Navigationsanwendung könnte ihm nun den kürzesten Weg zu
einer der beiden Apotheken berechnen, unter folgendem Link stellen wir
dar, wie der [Apotheke eine Nachricht geschickt werden
kann](./erp_communication.adoc).

# Abgabeinformationen abrufen

Als Versicherter möchte ich die Abgabeinformationen aus der Apotheke zu
meinem belieferten E-Rezept erhalten, um mir darüber einen digitalen
Beipackzettel herunterzuladen und weitere Anwendungshinweise für mein
Medikament zu erhalten.

Der Aufruf erfolgt als http-`GET`-Operation auf die Ressource
`/MedicationDispense`. Im Aufruf muss das während der Authentisierung
erhaltene ACCESS\_TOKEN im http-Request-Header `Authorization` übergeben
werden, der Fachdienst filtert die MedicationDispense-Einträge nach der
im ACCESS\_TOKEN enthaltenen KVNR des Versicherten und ggfs. in der
Aufrufadresse angegebenen weiteren Suchparametern. Die Rückgabe erfolgt
als Liste im `Bundle` eines oder mehrerer MedicationDispenses, welche
den ggfs. angegebenen Suchparametern entsprechen.

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
href="https://erp.app.ti-dienste.de/MedicationDispense?whenhandedover=gt2020-03-01">https://erp.app.ti-dienste.de/MedicationDispense?whenhandedover=gt2020-03-01</a><br />
</p>
<div class="note">
<p>In der Aufruf-Adresse können Suchparameter gemäß
<code>https://www.hl7.org/fhir/medicationdispense.html#search</code>
angegeben werden. Im konkreten Beispiel soll nach
Dispensierinformationen zu Medikamenten mit einem Abholdatum
<code>whenhandedover</code> größer (<code>gt</code>) dem Datum
<code>01.03.2020</code> gesucht werden.</p>
</div></td>
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
Versichertennummer enthalten nach welcher die Einträge gefiltert werden.
Die Base64-Darstellung des Tokens ist stark gekürzt.</p>
</div>
<div class="note">
<p>Im http-Header des äußeren http-Requests an die VAU (POST /VAU) sind
die Header <code>X-erp-user: v</code> und
<code>X-erp-resource: MedicationDispense</code> zu setzen.</p>
</div></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>Payload</strong></p></td>
<td style="text-align: left;"><pre><code>-</code></pre></td>
</tr>
</tbody>
</table>

**Response** HTTP/1.1 200 OK Content-Type:
application/fhir+json;charset=utf-8

    {
      "resourceType": "Bundle",
      "id": "187dc298-c2b8-40f5-8938-c6c4078660ed",
      "meta": {
        "lastUpdated": "2020-04-07T08:05:42.225+00:00"
      },
      "type": "searchset",
      "total": 1,
      "link": [
        {
          "relation": "self",
          "url": "https://erp.app.ti-dienste.de/MedicationDispense?whenhandedover=gt2020-01-01"
        }
      ],
      "entry": [
        {
          "fullUrl": "https://erp.app.ti-dienste.de/MedicationDispense/1093629",
          "resource": {
            "status": "completed",
            "id": "1093629",
            "identifier": [
              {
                "value": "160.123.456.789.123.58",
                "system": "https://gematik.de/fhir/erp/NamingSystem/GEM_ERP_NS_PrescriptionId"
              }
            ],
            "resourceType": "MedicationDispense",
            "medicationReference": {
              "display": "Sumatriptan-1a Pharma 100 mg Tabletten",
              "reference": "#med0314"
            },
            "meta": {
              "profile": [
                "https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_PR_MedicationDispense|1.2"
              ]
            },
            "contained": [
              {
                "meta": {
                  "profile": [
                    "https://fhir.kbv.de/StructureDefinition/KBV_PR_ERP_Medication_PZN|1.1.0"
                  ]
                },
                "id": "med0314",
                "code": {
                  "coding": [
                    {
                      "code": "06313728",
                      "system": "http://fhir.de/CodeSystem/ifa/pzn"
                    }
                  ],
                  "text": "Sumatriptan-1a Pharma 100 mg Tabletten"
                },
                "extension": [
                  {
                    "url": "https://fhir.kbv.de/StructureDefinition/KBV_EX_Base_Medication_Type",
                    "valueCodeableConcept": {
                      "coding": [
                        {
                          "display": "Medicinal product (product)",
                          "system": "http://snomed.info/sct",
                          "version": "http://snomed.info/sct/900000000000207008/version/20220331",
                          "code": "763158003"
                        }
                      ]
                    }
                  },
                  {
                    "url": "https://fhir.kbv.de/StructureDefinition/KBV_EX_ERP_Medication_Category",
                    "valueCoding": {
                      "code": "00",
                      "system": "https://fhir.kbv.de/CodeSystem/KBV_CS_ERP_Medication_Category"
                    }
                  },
                  {
                    "url": "https://fhir.kbv.de/StructureDefinition/KBV_EX_ERP_Medication_Vaccine",
                    "valueBoolean": false
                  }
                ],
                "resourceType": "Medication",
                "amount": {
                  "denominator": {
                    "value": 1
                  },
                  "numerator": {
                    "unit": "Tabletten",
                    "extension": [
                      {
                        "url": "https://fhir.kbv.de/StructureDefinition/KBV_EX_ERP_Medication_PackagingSize",
                        "valueString": "10"
                      }
                    ],
                    "system": "http://unitsofmeasure.org",
                    "code": "{tbl}"
                  }
                },
                "form": {
                  "coding": [
                    {
                      "code": "TAB",
                      "system": "https://fhir.kbv.de/CodeSystem/KBV_CS_SFHIR_KBV_DARREICHUNGSFORM"
                    }
                  ]
                }
              }
            ],
            "dosageInstruction": [
              {
                "text": "1-0-1-0"
              }
            ],
            "performer": [
              {
                "actor": {
                  "identifier": {
                    "value": "3-SMC-B-Testkarte-883110000129070",
                    "system": "https://gematik.de/fhir/sid/telematik-id"
                  }
                }
              }
            ],
            "whenHandedOver": "2020-03-20",
            "quantity": {
              "system": "http://unitsofmeasure.org",
              "value": 1,
              "code": "{Package}"
            },
            "subject": {
              "identifier": {
                "value": "X123456789",
                "system": "http://fhir.de/sid/gkv/kvid-10"
              }
            }
          },
          "search": {
            "mode": "match"
          }
        }
      ]
    }

Der Task wird unter `"reference":"Task/160.880.966.157.248.22"` des
eingelösten E-Rezepts referenziert. Über den Link können weitere
Informationen wie E-Rezept-Datensatz und ggfs. die Quittung abgerufen
werden.

Unter `"performer"` findet sich der Name und die Betriebsstättennummer
Telematik-ID der Apotheke, bei der das E-Rezept eingelöst wurde.

\` "whenHandedOver"\` wurde als Filterkriterium verwendet, das
Medikament wurde hier am 20.03.2020 ausgehändigt (`whenhandedover`) und
ist damit vom Datumswert "größer" als das Datum des Filterkriteriums der
Suchanfrage 01.01.2020 (`whenhandedover=gt2020-01-01`)

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
<span class="small">Es wurde kein passender Verzeichniseintrag
gefunden.</span></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>500</p></td>
<td style="text-align: left;"><p>Server Errors<br />
<span class="small">Unerwarteter Serverfehler</span></p></td>
</tr>
</tbody>
</table>

# Ein E-Rezept löschen

Als Versicherter möchte ich ein E-Rezept löschen können, um mein Recht
auf informationelle Selbstbestimmung wahrzunehmen.

Der Aufruf erfolgt als http-`POST`-Operation auf eine konkrete Ressource
`/Task/<task_id>` mit dem Zusatz der FHIR-Operation `$abort`. Im Aufruf
muss das während der Authentisierung erhaltene ACCESS\_TOKEN im
http-Request-Header `Authorization` übergeben werden. Der Aufruf kann
auch durch einen Vertreter des Versicherten erfolgen, hierbei wird
lediglich die Rolle `Versicherter` im ACCESS\_TOKEN geprüft. Um die
Berechtigung für den Zugriff auf einen Task mit einer fremden KVNR
nachzuweisen, muss der Zugreifende den richtigen AccessCode im
http-Request-Header `X-AccessCode` übergeben. Die Operation löscht alle
personenbezogenen und medizinischen Daten.

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
href="https://erp.app.ti-dienste.de/Task/160.880.966.157.248.22/$abort">https://erp.app.ti-dienste.de/Task/160.880.966.157.248.22/$abort</a></p></td>
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
berechtigt ist. Beispielsweise ist das Rezept grade in der Belieferung
durch eine Apotheke.</span></p></td>
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

# Einsicht in das Zugriffsprotokoll

Als Versicherter möchte ich Einsicht in das Zugriffsprotokoll meiner
Daten im E-Rezept-Fachdienst nehmen, um Zugriffe nachvollziehen zu
können und eine unberechtigte Einsicht in meine Daten zu prüfen.

Der Aufruf erfolgt als http-`GET`-Operation auf die Ressource
`/AuditEvent`. Im Aufruf muss das während der Authentisierung erhaltene
ACCESS\_TOKEN im http-Request-Header `Authorization` übergeben werden,
der Fachdienst filtert die AuditEvent-Einträge nach der im ACCESS\_TOKEN
enthaltenen KVNR des Versicherten. Der E-Rezept-Fachdienst liefert eine
Liste von Protokolleinträgen, die mit einem zusätzlichen Suchparameter
in der Anfrage-URL sortiert werden kann.
`https://erp.app.ti-dienste.de/AuditEvent?_sort=-date` sortiert die
Protokolleinträge nach dem Protokollierungszeitpunkt `recorded` gemäß
<https://www.hl7.org/fhir/auditevent.html#search>, das Minuszeichen in
`-date` bewirkt die absteigende Sortierung (jüngster Eintrag zuerst).

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
href="https://erp.app.ti-dienste.de/AuditEvent">https://erp.app.ti-dienste.de/AuditEvent</a></p></td>
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
Versichertennummer enthalten, nach der die Protokolleinträge gefiltert
werden. Die Base64-Darstellung des Tokens ist stark gekürzt.</p>
</div>
<div class="note">
<p>Im http-Header des äußeren http-Requests an die VAU (POST /VAU) sind
die Header <code>X-erp-user: v</code> und
<code>X-erp-resource: AuditEvent</code> zu setzen.</p>
</div>
<div class="warning">
<p>In einigen Fällen kann der Versichtungstyp (GKV/PKV) nicht eindeutig
vom Fachdienst bestimmt werden. Hier setzt der Fachdienst per default
den Wert "GKV".</p>
</div></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>Payload</strong></p></td>
<td style="text-align: left;"><pre><code>-</code></pre></td>
</tr>
</tbody>
</table>

**Response** HTTP/1.1 200 OK Content-Type:
application/fhir+json;charset=utf-8

    {
      "resourceType": "Bundle",
      "id": "12653b13-5fca-4e3b-860c-9558bdfef9a1",
      "meta": {
        "lastUpdated": "2020-03-29T13:44:18.783+00:00"
      },
      "type": "searchset",
      "link": [ {
        "relation": "self",
        "url": "https://erp.app.ti-dienste.de/AuditEvent"
      }, {
        "relation": "next",
        "url": "https://erp.app.ti-dienste.de/AuditEvent?_getpages=12653b13-5fca-4e3b-860c-9558bdfef9a1&_getpagesoffset=20&_count=20"
      } ],
      "entry": [ {
        "fullUrl": "https://erp.app.ti-dienste.de/AuditEvent/58862",
        "resource": {
          "resourceType": "AuditEvent",
          "id": "58862",
          "meta": {
            "versionId": "1",
            "lastUpdated": "2020-02-27T08:04:27.434+00:00",
            "source": "#IkMt252YovlsJTAE",
            "profile": [
              "https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_PR_AuditEvent|1.2"
            ]
          },
          "text": {
            "status": "generated",
            "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">Praxis Dr. Müller, Bahnhofstr. 78 hat ein E-Rezept 160.123.456.789.123.58 eingestellt</div>"
          },
          "type": {
            "system": "http://terminology.hl7.org/CodeSystem/audit-event-type",
            "code": "rest"
          },
          "subtype": [ {
            "system": "http://hl7.org/fhir/restful-interaction",
            "code": "create"
          } ],
          "action": "C",
          "recorded": "2020-02-27T08:04:27.434+00:00",
          "outcome": "0",
          "agent": [ {
            "type": {
              "coding": [ {
                "system": "http://terminology.hl7.org/CodeSystem/extra-security-role-type",
                "code": "humanuser",
                "display": "Human User"
              } ]
            },
            "who": {
              "identifier": {
                "system": "https://gematik.de/fhir/sid/telematik-id",
                "value": "1-1.54.102323123404"
              }
            },
            "name": "Praxis Dr. Müller",
            "requestor": false
          }],
          "source": {
            "site": "E-Rezept Fachdienst",
            "observer": {
              "reference": "Device/1234"
            }
          },
          "entity": [ {
            "what": {
              "reference": "https://erp.app.ti-dienste.de/Task/160.123.456.789.123.58",
              "identifier": {
                "use":"official",
                "system":"https://gematik.de/fhir/erp/NamingSystem/GEM_ERP_NS_PrescriptionId",
                "value":"160.123.456.789.123.58"
              }
            },
            "name": "X123456789",
            "description": "*160.123.456.789.123.58*"
          } ]
        },
        "search": {
          "mode": "match"
        }
      }, {
        "fullUrl": "https://erp.app.ti-dienste.de/AuditEvent/58863",
        "resource": {
          "resourceType": "AuditEvent",
          "id": "58863",
          "meta": {
            "versionId": "1",
            "lastUpdated": "2020-02-27T09:04:27.434+00:00",
            "source": "#IkMt252YovlsJTAE",
            "profile": [
              "https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_PR_AuditEvent|1.2"
            ]
          },
          "text": {
            "status": "generated",
            "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">Max Mustermann hat ein E-Rezept 160.123.456.789.123.58 heruntergeladen</div>"
          },
          "type": {
            "system": "http://terminology.hl7.org/CodeSystem/audit-event-type",
            "code": "rest"
          },
          "subtype": [ {
            "system": "http://hl7.org/fhir/restful-interaction",
            "code": "read"
          } ],
          "action": "R",
          "recorded": "2020-02-27T09:04:27.434+00:00",
          "outcome": "0",
          "agent": [ {
            "type": {
              "coding": [ {
                "system": "http://terminology.hl7.org/CodeSystem/extra-security-role-type",
                "code": "humanuser",
                "display": "Human User"
              } ]
            },
            "who": {
              "identifier": {
                "system": "https://gematik.de/fhir/sid/telematik-id",
                "value": "3-1.54.10123404"
              }
            },
            "name": "Ihre Apotheke um die Ecke, Hauptstraße 1",
            "requestor": false
          }],
          "source": {
            "site": "E-Rezept Fachdienst",
            "observer": {
              "reference": "Device/5678"
            }
          },
          "entity": [ {
            "what": {
              "reference": "https://erp.app.ti-dienste.de/Task/160.123.456.789.123.58",
              "identifier": {
                "use":"official",
                "system":"https://gematik.de/fhir/erp/NamingSystem/GEM_ERP_NS_PrescriptionId",
                "value":"160.123.456.789.123.58"
              }
            },
            "name": "X123456789",
             "description": "*160.123.456.789.123.58*"
          } ]
        },
        "search": {
          "mode": "match"
        }
      }, {
        "fullUrl": "https://erp.app.ti-dienste.de/AuditEvent/620049",
        "resource": {
          "resourceType": "AuditEvent",
          "id": "620049",
          "meta": {
            "versionId": "1",
            "lastUpdated": "2020-02-27T10:04:27.434+00:00",
            "source": "#IkMt252YovlsJTAE",
            "profile": [
              "https://gematik.de/fhir/erp/StructureDefinition/GEM_ERP_PR_AuditEvent|1.2"
            ]
          },
          "text": {
            "status": "generated",
            "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">Ihre Apotheke um die Ecke, Hauptstraße 1 hat ein E-Rezept 160.123.456.789.123.58 beliefert</div>"
          },
          "type": {
            "system": "http://terminology.hl7.org/CodeSystem/audit-event-type",
            "code": "rest"
          },
          "subtype": [ {
            "system": "http://hl7.org/fhir/restful-interaction",
            "code": "update"
          } ],
          "action": "U",
          "recorded": "2020-02-27T10:04:27.434+00:00",
          "outcome": "0",
          "agent": [ {
            "type": {
              "coding": [ {
                "system": "http://terminology.hl7.org/CodeSystem/extra-security-role-type",
                "code": "humanuser",
                "display": "Human User"
              } ]
            },
            "who": {
              "identifier": {
                "system": "https://gematik.de/fhir/sid/telematik-id",
                "value": "3-1.54.10123404"
              }
            },
            "name": "Ihre Apotheke um die Ecke, Hauptstraße 1",
            "requestor": false
          }],
          "source": {
            "site": "E-Rezept Fachdienst",
            "observer": {
              "reference": "Device/1234"
            }
          },
          "entity": [ {
            "what": {
               "reference": "https://erp.app.ti-dienste.de/Task/160.123.456.789.123.58",
              "identifier": {
                "use":"official",
                "system":"https://gematik.de/fhir/erp/NamingSystem/GEM_ERP_NS_PrescriptionId",
                "value":"160.123.456.789.123.58"
              }
            },
            "name": "X123456789",
            "description": "*160.123.456.789.123.58*"
          } ]
        },
        "search": {
          "mode": "match"
        }
      } ]
    }

Beim Abrufen der Protokolleinträge erfolgt die Rückgabe als `Bundle`, in
dem die Protokolleinträge mit Bezug zum authentifizierten Versicherten
über dessen KVNR aufgelistet werden. In diesem vereinfachten Beispiel
werden nur drei Einträge dargestellt.

Für eine komfortable Darstellung vieler Protokolleinträge und zur
Reduktion der übertragenen Datenmenge kommt ein Paging-Mechanismus zum
Einsatz. Über diese `url` können die nächsten 20 Protokolleinträge
abgerufen werden (sofern weitere vorhanden)

Die Darstellung eines Protokolleintrags erfolgt als `AuditEvent`

Unter
`"div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">Praxis Dr. Müller, Bahnhofstr. 78 hat ein E-Rezept 160.123.456.789.123.58 eingestellt</div>"`
wird eine lesbare Darstellung in HTML-Format bereitgestellt.

Der Versichertenbezug wird über die Versichertennummer des jeweils
gelesenen/eingestellten/gelöschten E-Rezept in `"name": "X123456789"`
oder auch MedicationDispense hergestellt.

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
[small]#Die Anfrage wurde erfolgreich bearbeitet.  Die angeforderte Ressource wird im ResponseBody bereitgestellt.#</code></pre></td>
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
