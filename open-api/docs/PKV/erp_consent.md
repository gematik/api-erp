Hier dokumentiert die gematik die Nutzung der Schnittstellen rund um das
E-Rezept für die Einwilligung zur elektronischen Verarbeitung und
Speicherung von Abrechnungsinformationen für PKV-Versicherte.

# Profilierung

Für diesen Anwendungsfall wird die FHIR-Ressource "Consent":
<http://hl7.org/fhir/consent.html> profiliert. Die Profile können als
JSON- oder XML-Datei hier eingesehen werden:
<https://simplifier.net/erezept-patientenrechnung/gem-erpchrg-pr-consent>

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
style="text-align: left;"><p><strong>Consent</strong></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>status</p></td>
<td style="text-align: left;"><p>Status der Einwilligung. Festgesetzt
auf "active"</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>scope</p></td>
<td style="text-align: left;"><p>Art der Einwilligung.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>scope.coding.code</p></td>
<td style="text-align: left;"><p>Festgelegt auf
"patient-privacy"</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>category</p></td>
<td style="text-align: left;"><p>Art der Einwilligung, festgelegt durch
ein von der gematik erstelltes Codesystem.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>patient</p></td>
<td style="text-align: left;"><p>Identifier des Patienten, zu welchem
die Einwilligung zugeordnet wird. GKV- und PKV-Profile sind
möglich.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>dateTime</p></td>
<td style="text-align: left;"><p>Zeitstempel der Erstellung der
Einwilligung</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>policyRule</p></td>
<td style="text-align: left;"><p>Angabe des Types einer
Einwilligung</p></td>
</tr>
</tbody>
</table>

In den folgenden Kapiteln wird erläutert, wann und wie die Befüllung
dieser Attribute erfolgt.

# Anwendungsfall Einwilligung zum Speichern der Abrechnungsinformationen durch den Versicherten erteilen

Als Versicherter möchte ich eine Einwilligung zur elektronischen
Speicherung meiner Abrechnungsinformationen erstellen und dem Fachdienst
übermitteln. Die Einwilligung wird über die FHIR-Ressource "Consent"
abgebildet.

Der Aufruf erfolgt als http-`POST`-Operation auf die Ressource
`/Consent`. Im Aufruf muss das während der Authentisierung erhaltene
ACCESS\_TOKEN im http-Request-Header `Authorization` übergeben werden.

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
href="https://prescriptionserver.telematik/Consent">https://prescriptionserver.telematik/Consent</a></p></td>
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
</div></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>Payload</strong></p></td>
<td style="text-align: left;"><div class="sourceCode" id="cb2"><pre
class="sourceCode json"><code class="sourceCode json"><span id="cb2-1"><a href="#cb2-1" aria-hidden="true" tabindex="-1"></a><span class="fu">{</span></span>
<span id="cb2-2"><a href="#cb2-2" aria-hidden="true" tabindex="-1"></a>    <span class="dt">&quot;resourceType&quot;</span><span class="fu">:</span> <span class="st">&quot;Consent&quot;</span><span class="fu">,</span></span>
<span id="cb2-3"><a href="#cb2-3" aria-hidden="true" tabindex="-1"></a>    <span class="dt">&quot;meta&quot;</span><span class="fu">:</span> <span class="fu">{</span></span>
<span id="cb2-4"><a href="#cb2-4" aria-hidden="true" tabindex="-1"></a>        <span class="dt">&quot;profile&quot;</span><span class="fu">:</span>  <span class="ot">[</span></span>
<span id="cb2-5"><a href="#cb2-5" aria-hidden="true" tabindex="-1"></a>            <span class="st">&quot;https://gematik.de/fhir/erpchrg/StructureDefinition/GEM_ERPCHRG_PR_Consent&quot;</span></span>
<span id="cb2-6"><a href="#cb2-6" aria-hidden="true" tabindex="-1"></a>        <span class="ot">]</span></span>
<span id="cb2-7"><a href="#cb2-7" aria-hidden="true" tabindex="-1"></a>    <span class="fu">},</span></span>
<span id="cb2-8"><a href="#cb2-8" aria-hidden="true" tabindex="-1"></a>    <span class="dt">&quot;status&quot;</span><span class="fu">:</span> <span class="st">&quot;active&quot;</span><span class="fu">,</span></span>
<span id="cb2-9"><a href="#cb2-9" aria-hidden="true" tabindex="-1"></a>    <span class="dt">&quot;scope&quot;</span><span class="fu">:</span> <span class="fu">{</span></span>
<span id="cb2-10"><a href="#cb2-10" aria-hidden="true" tabindex="-1"></a>        <span class="dt">&quot;coding&quot;</span><span class="fu">:</span>  <span class="ot">[</span></span>
<span id="cb2-11"><a href="#cb2-11" aria-hidden="true" tabindex="-1"></a>            <span class="fu">{</span></span>
<span id="cb2-12"><a href="#cb2-12" aria-hidden="true" tabindex="-1"></a>                <span class="dt">&quot;code&quot;</span><span class="fu">:</span> <span class="st">&quot;patient-privacy&quot;</span><span class="fu">,</span></span>
<span id="cb2-13"><a href="#cb2-13" aria-hidden="true" tabindex="-1"></a>                <span class="dt">&quot;system&quot;</span><span class="fu">:</span> <span class="st">&quot;http://terminology.hl7.org/CodeSystem/consentscope&quot;</span><span class="fu">,</span></span>
<span id="cb2-14"><a href="#cb2-14" aria-hidden="true" tabindex="-1"></a>                <span class="dt">&quot;display&quot;</span><span class="fu">:</span> <span class="st">&quot;Privacy Consent&quot;</span></span>
<span id="cb2-15"><a href="#cb2-15" aria-hidden="true" tabindex="-1"></a>            <span class="fu">}</span></span>
<span id="cb2-16"><a href="#cb2-16" aria-hidden="true" tabindex="-1"></a>        <span class="ot">]</span></span>
<span id="cb2-17"><a href="#cb2-17" aria-hidden="true" tabindex="-1"></a>    <span class="fu">},</span></span>
<span id="cb2-18"><a href="#cb2-18" aria-hidden="true" tabindex="-1"></a>    <span class="dt">&quot;category&quot;</span><span class="fu">:</span>  <span class="ot">[</span></span>
<span id="cb2-19"><a href="#cb2-19" aria-hidden="true" tabindex="-1"></a>        <span class="fu">{</span></span>
<span id="cb2-20"><a href="#cb2-20" aria-hidden="true" tabindex="-1"></a>            <span class="dt">&quot;coding&quot;</span><span class="fu">:</span>  <span class="ot">[</span></span>
<span id="cb2-21"><a href="#cb2-21" aria-hidden="true" tabindex="-1"></a>                <span class="fu">{</span></span>
<span id="cb2-22"><a href="#cb2-22" aria-hidden="true" tabindex="-1"></a>                    <span class="dt">&quot;code&quot;</span><span class="fu">:</span> <span class="st">&quot;CHARGCONS&quot;</span><span class="fu">,</span></span>
<span id="cb2-23"><a href="#cb2-23" aria-hidden="true" tabindex="-1"></a>                    <span class="dt">&quot;system&quot;</span><span class="fu">:</span> <span class="st">&quot;https://gematik.de/fhir/erpchrg/CodeSystem/GEM_ERPCHRG_CS_ConsentType&quot;</span><span class="fu">,</span></span>
<span id="cb2-24"><a href="#cb2-24" aria-hidden="true" tabindex="-1"></a>                    <span class="dt">&quot;display&quot;</span><span class="fu">:</span> <span class="st">&quot;Saving electronic charge item.&quot;</span></span>
<span id="cb2-25"><a href="#cb2-25" aria-hidden="true" tabindex="-1"></a>                <span class="fu">}</span></span>
<span id="cb2-26"><a href="#cb2-26" aria-hidden="true" tabindex="-1"></a>            <span class="ot">]</span></span>
<span id="cb2-27"><a href="#cb2-27" aria-hidden="true" tabindex="-1"></a>        <span class="fu">}</span></span>
<span id="cb2-28"><a href="#cb2-28" aria-hidden="true" tabindex="-1"></a>    <span class="ot">]</span><span class="fu">,</span></span>
<span id="cb2-29"><a href="#cb2-29" aria-hidden="true" tabindex="-1"></a>    <span class="dt">&quot;patient&quot;</span><span class="fu">:</span> <span class="fu">{</span></span>
<span id="cb2-30"><a href="#cb2-30" aria-hidden="true" tabindex="-1"></a>        <span class="dt">&quot;identifier&quot;</span><span class="fu">:</span> <span class="fu">{</span></span>
<span id="cb2-31"><a href="#cb2-31" aria-hidden="true" tabindex="-1"></a>            <span class="dt">&quot;type&quot;</span><span class="fu">:</span> <span class="fu">{</span></span>
<span id="cb2-32"><a href="#cb2-32" aria-hidden="true" tabindex="-1"></a>                <span class="dt">&quot;coding&quot;</span><span class="fu">:</span>  <span class="ot">[</span></span>
<span id="cb2-33"><a href="#cb2-33" aria-hidden="true" tabindex="-1"></a>                    <span class="fu">{</span></span>
<span id="cb2-34"><a href="#cb2-34" aria-hidden="true" tabindex="-1"></a>                        <span class="dt">&quot;system&quot;</span><span class="fu">:</span> <span class="st">&quot;http://fhir.de/CodeSystem/identifier-type-de-basis&quot;</span><span class="fu">,</span></span>
<span id="cb2-35"><a href="#cb2-35" aria-hidden="true" tabindex="-1"></a>                        <span class="dt">&quot;code&quot;</span><span class="fu">:</span> <span class="st">&quot;PKV&quot;</span></span>
<span id="cb2-36"><a href="#cb2-36" aria-hidden="true" tabindex="-1"></a>                    <span class="fu">}</span></span>
<span id="cb2-37"><a href="#cb2-37" aria-hidden="true" tabindex="-1"></a>                <span class="ot">]</span></span>
<span id="cb2-38"><a href="#cb2-38" aria-hidden="true" tabindex="-1"></a>            <span class="fu">},</span></span>
<span id="cb2-39"><a href="#cb2-39" aria-hidden="true" tabindex="-1"></a>            <span class="dt">&quot;system&quot;</span><span class="fu">:</span> <span class="st">&quot;http://fhir.de/sid/pkv/kvid-10&quot;</span><span class="fu">,</span></span>
<span id="cb2-40"><a href="#cb2-40" aria-hidden="true" tabindex="-1"></a>            <span class="dt">&quot;value&quot;</span><span class="fu">:</span> <span class="st">&quot;X234567890&quot;</span></span>
<span id="cb2-41"><a href="#cb2-41" aria-hidden="true" tabindex="-1"></a>        <span class="fu">}</span></span>
<span id="cb2-42"><a href="#cb2-42" aria-hidden="true" tabindex="-1"></a>    <span class="fu">},</span></span>
<span id="cb2-43"><a href="#cb2-43" aria-hidden="true" tabindex="-1"></a>    <span class="dt">&quot;dateTime&quot;</span><span class="fu">:</span> <span class="st">&quot;2021-06-01T07:13:00+05:00&quot;</span><span class="fu">,</span></span>
<span id="cb2-44"><a href="#cb2-44" aria-hidden="true" tabindex="-1"></a>    <span class="dt">&quot;policyRule&quot;</span><span class="fu">:</span> <span class="fu">{</span></span>
<span id="cb2-45"><a href="#cb2-45" aria-hidden="true" tabindex="-1"></a>        <span class="dt">&quot;coding&quot;</span><span class="fu">:</span>  <span class="ot">[</span></span>
<span id="cb2-46"><a href="#cb2-46" aria-hidden="true" tabindex="-1"></a>            <span class="fu">{</span></span>
<span id="cb2-47"><a href="#cb2-47" aria-hidden="true" tabindex="-1"></a>                <span class="dt">&quot;code&quot;</span><span class="fu">:</span> <span class="st">&quot;OPTIN&quot;</span><span class="fu">,</span></span>
<span id="cb2-48"><a href="#cb2-48" aria-hidden="true" tabindex="-1"></a>                <span class="dt">&quot;system&quot;</span><span class="fu">:</span> <span class="st">&quot;http://terminology.hl7.org/CodeSystem/v3-ActCode&quot;</span></span>
<span id="cb2-49"><a href="#cb2-49" aria-hidden="true" tabindex="-1"></a>            <span class="fu">}</span></span>
<span id="cb2-50"><a href="#cb2-50" aria-hidden="true" tabindex="-1"></a>        <span class="ot">]</span></span>
<span id="cb2-51"><a href="#cb2-51" aria-hidden="true" tabindex="-1"></a>    <span class="fu">}</span></span>
<span id="cb2-52"><a href="#cb2-52" aria-hidden="true" tabindex="-1"></a><span class="fu">}</span></span></code></pre></div></td>
</tr>
</tbody>
</table>

**Response**

    HTTP/1.1 201 Created
    Content-Type: application/fhir+json;charset=utf-8

    {
        "resourceType": "Consent",
        "id": "0dcc5d4c-bf24-4c06-b02e-be5bc24587e2",
        "meta": {
            "profile":  [
                "https://gematik.de/fhir/erpchrg/StructureDefinition/GEM_ERPCHRG_PR_Consent"
            ]
        },
        "status": "active",
        "scope": {
            "coding":  [
                {
                    "code": "patient-privacy",
                    "system": "http://terminology.hl7.org/CodeSystem/consentscope",
                    "display": "Privacy Consent"
                }
            ]
        },
        "category":  [
            {
                "coding":  [
                    {
                        "code": "CHARGCONS",
                        "system": "https://gematik.de/fhir/erpchrg/CodeSystem/GEM_ERPCHRG_CS_ConsentType",
                        "display": "Saving electronic charge item."
                    }
                ]
            }
        ],
        "patient": {
            "identifier": {
                "type": {
                    "coding":  [
                        {
                            "system": "http://fhir.de/CodeSystem/identifier-type-de-basis",
                            "code": "PKV"
                        }
                    ]
                },
                "system": "http://fhir.de/sid/pkv/kvid-10",
                "value": "X234567890"
            }
        },
        "dateTime": "2021-06-01T07:13:00+05:00",
        "policyRule": {
            "coding":  [
                {
                    "code": "OPTIN",
                    "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode"
                }
            ]
        }
    }

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
<td style="text-align: left;"><p>201</p></td>
<td style="text-align: left;"><pre><code> Created +
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
[small]#Die Anfrage wurde unter falschen Annahmen gestellt, bspw. weil
bereits eine Einwilligung mit der Kategorie Consent.category.coding.code
= CHARGCONS vorhanden ist.</p></td>
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

# Anwendungsfall Einwilligung zum Speichern der Abrechnungsinformationen durch den Versicherten einsehen

Als Versicherter möchte ich meine erteilte Einwilligung zur
elektronischen Speicherung meiner Abrechnungsinformationen einsehen.

Der Aufruf erfolgt als http-`GET`-Operation auf die Ressource
`/Consent`. Im Aufruf muss das während der Authentisierung erhaltene
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
href="https://prescriptionserver.telematik/Consent">https://prescriptionserver.telematik/Consent</a></p></td>
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
</div></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>Payload</strong></p></td>
<td style="text-align: left;"></td>
</tr>
</tbody>
</table>

**Response**

    HTTP/1.1 200 OK
    Content-Type: application/fhir+json;charset=utf-8

    {
      "resourceType": "Bundle",
      "id": "a14623ad-0b89-4d8e-9719-87e07e3af560",
      "type": "searchset",
      "timestamp": "2023-02-15T15:19:19.394+00:00",
      "total": 0,
      "entry": [
        {
          "fullUrl": "https://erp-dev.zentral.erp.splitdns.ti-dienste.de/Consent/CHARGCONS-X234567890",
          "resource": {
            "resourceType": "Consent",
            "id": "CHARGCONS-X234567890",
            "meta": {
              "profile": [
                "https://gematik.de/fhir/erpchrg/StructureDefinition/GEM_ERPCHRG_PR_Consent"
              ]
            },
            "status": "active",
            "scope": {
              "coding": [
                {
                  "code": "patient-privacy",
                  "system": "http://terminology.hl7.org/CodeSystem/consentscope",
                  "display": "Privacy Consent"
                }
              ]
            },
            "category": [
              {
                "coding": [
                  {
                    "code": "CHARGCONS",
                    "system": "https://gematik.de/fhir/erpchrg/CodeSystem/GEM_ERPCHRG_CS_ConsentType",
                    "display": "Saving electronic charge item."
                  }
                ]
              }
            ],
            "patient": {
              "identifier": {
                "type": {
                  "coding": [
                    {
                      "system": "http://fhir.de/CodeSystem/identifier-type-de-basis",
                      "code": "PKV"
                    }
                  ]
                },
                "system": "http://fhir.de/sid/pkv/kvid-10",
                "value": "X234567890"
              }
            },
            "dateTime": "2021-06-01T07:13:00+05:00",
            "policyRule": {
              "coding": [
                {
                  "code": "OPTIN",
                  "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode"
                }
              ]
            }
          }
        }
      ]
    }

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

# Anwendungsfall Einwilligung zum Speichern der Abrechnungsinformationen durch den Versicherten widerrufen

Als Versicherter möchte ich meine erteilte Einwilligung zur
elektronischen Speicherung meiner Abrechnungsinformationen widerrufen.
Mit dem Widerruf der Einwilligung werden bereits gespeicherte
Abrechnungsinformationen gelöscht.

Der Aufruf erfolgt als http-`DELETE`-Operation auf die Ressource
`/Consent`. Im Aufruf muss das während der Authentisierung erhaltene
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
href="https://prescriptionserver.telematik/Consent?category=CHARGCONS">https://prescriptionserver.telematik/Consent?category=CHARGCONS</a></p></td>
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

    HTTP/1.1 204 No Content

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
