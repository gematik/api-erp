Auf dieser Seite dokumentiert die gematik die Schnittstellen des
E-Rezept-Fachdienstes für Apotheken, über welche sie sich für
Benachrichtigungen bei neuen Communications, registrieren können.

# Funktionsweise

Die Umsetzung der Notification-Schnittstelle des E-Rezept-Fachdienstes
folgt den Vorgaben des
[FHIR-Standards^](https://www.hl7.org/fhir/subscription.html#2.46.7.2).
![width=100%](../images/notification_avs_overview.png)

Das AVS sendet eine Registrierungsanforderung an die VAU des
E-Rezept-Fachdienstes, dieser generiert ein Pseudonym auf Basis der
Telematik-ID und ein Bearer Token.

Mit diesem Bearer Token baut das AVS eine Websocket-Verbindung an der
Subscription-Schnittstelle des Fachdienstes auf und erhält je neu
vorliegender Communications-Ressource für die Telematik-ID ein `Ping`.
Das `Ping` ist dann Trigger für das [Abrufen der ungelesenen
Communications](erp_communication.adoc#user-content-anwendungsfall-auf-neue-nachrichten-im-e-rezept-fachdienst-prüfen).

![width=50%](../images/notification_avs_sequence.png)

# Registrierung

Der Aufbau der WebSocket-Verbindung erfolgt zweistufig. Als erstes
erfolgt die Authentisierung durch die VAU. Diese stellt ein eigenes
Bearer-Token aus, das im zweiten Schritt beim Aufbau der eigentlichen
Socketverbindung an den Subscription-Service übergeben wird.

## Pseudonymgenerierung in der VAU (Authentisierung)

Zunächst muss für die Apotheke als authentisierter Client (gültiges
AccessToken des IDP) ein Subscription-Request an die VAU gesendet
werden.

**Request**

<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p><strong>URI</strong></p></td>
<td style="text-align: left;"><p>/Subscription</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>Method</strong></p></td>
<td style="text-align: left;"><p>POST</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>Request</strong></p></td>
<td style="text-align: left;"><div class="sourceCode" id="cb1"><pre
class="sourceCode xml"><code class="sourceCode xml"><span id="cb1-1"><a href="#cb1-1" aria-hidden="true" tabindex="-1"></a>POST /Subscription HTTP/1.1</span>
<span id="cb1-2"><a href="#cb1-2" aria-hidden="true" tabindex="-1"></a>Host: erp.zentral.erp.splitdns.ti-dienste.de</span>
<span id="cb1-3"><a href="#cb1-3" aria-hidden="true" tabindex="-1"></a>User-Agent: Avs/1.0 AvSoft/GEMAvwepokrpxnwiorlc</span>
<span id="cb1-4"><a href="#cb1-4" aria-hidden="true" tabindex="-1"></a>Cache-Control: no-cache</span>
<span id="cb1-5"><a href="#cb1-5" aria-hidden="true" tabindex="-1"></a>Authorization: Bearer eyJraWQ.ewogImL2pA10Qql22ddtutrvx4FsDlz.rHQjEmB1lLmpqn9J</span>
<span id="cb1-6"><a href="#cb1-6" aria-hidden="true" tabindex="-1"></a>Content-Type: application/fhir+xml; charset=UTF-8</span>
<span id="cb1-7"><a href="#cb1-7" aria-hidden="true" tabindex="-1"></a>Accept: application/fhir+xml; charset=utf-8</span>
<span id="cb1-8"><a href="#cb1-8" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb1-9"><a href="#cb1-9" aria-hidden="true" tabindex="-1"></a>&lt;<span class="kw">Subscription</span><span class="ot"> xmlns=</span><span class="st">&quot;http://hl7.org/fhir&quot;</span>&gt;</span>
<span id="cb1-10"><a href="#cb1-10" aria-hidden="true" tabindex="-1"></a>    &lt;<span class="kw">status</span><span class="ot"> value=</span><span class="st">&quot;requested&quot;</span>/&gt;</span>
<span id="cb1-11"><a href="#cb1-11" aria-hidden="true" tabindex="-1"></a>    &lt;<span class="kw">reason</span><span class="ot"> value=</span><span class="st">&quot;Communication notifications&quot;</span> /&gt;</span>
<span id="cb1-12"><a href="#cb1-12" aria-hidden="true" tabindex="-1"></a>    &lt;<span class="kw">criteria</span><span class="ot"> value=</span><span class="st">&quot;Communication?received=null</span><span class="dv">&amp;amp;</span><span class="st">recipient=3-abc-12345678&quot;</span>/&gt;</span>
<span id="cb1-13"><a href="#cb1-13" aria-hidden="true" tabindex="-1"></a>    &lt;<span class="kw">channel</span>&gt;</span>
<span id="cb1-14"><a href="#cb1-14" aria-hidden="true" tabindex="-1"></a>        &lt;<span class="kw">type</span><span class="ot"> value=</span><span class="st">&quot;websocket&quot;</span>/&gt;</span>
<span id="cb1-15"><a href="#cb1-15" aria-hidden="true" tabindex="-1"></a>    &lt;/<span class="kw">channel</span>&gt;</span>
<span id="cb1-16"><a href="#cb1-16" aria-hidden="true" tabindex="-1"></a>&lt;/<span class="kw">Subscription</span>&gt;</span></code></pre></div>
<div class="note">
<p>Im http-Header des äußeren http-Requests an die VAU (POST /VAU) sind
die Header <code>X-erp-user: l</code> und
<code>X-erp-resource: Subscription</code> zu setzen.</p>
</div></td>
</tr>
</tbody>
</table>

Das Feld \` &lt;criteria value="**"\` benennt die Suchparameter, bei
denen eine Notification verschickt werden soll. Das sind zum einen
`received=null` für ungelesene Nachrichten und
`recipient=3-abc-12345678` die Telematik-ID der Apotheke, die mit der
Telematik-ID des IDP-AccessToken übereinstimmen muss. Andere Parameter
werden aktuell nicht unterstützt. \*ACHTUNG: das "&" muss als "&amp;"
codiert werden.**

**Response**

    HTTP/1.1 200 OK
    Content-Length: 510
    Content-Type: application/fhir+xml;charset=utf-8

    <Subscription>
        <id value="df694c098c2fb373524150461cfd9d23"/>
        <status value="active"/>
        <end value="2022-01-01T00:00:00Z"/>
        <reason value="Communication notifications" />
        <criteria value="Communication?received=null&amp;recipient=3-abc-12345678"/>
        <channel>
            <type value="websocket"/>
            <header value="Authorization: Bearer eyJhbGciOiAiYnJhaW5wb29sUDI1NnIxIiwidHlwIjogIkpXVCJ9.eyJpc3MiOiAiTWF0aGlzIGJyYWlucG9vbCBqd3QiLCJpYXQiOiAxNjMyMjk0MzY1LCJleHAiOiAxNjYzODMwMzY1LCJhdWQiOiAibG9jYWxob3N0Iiwic3ViIjogIm15VXNlcm5hbWUiLCJzdWJzY3JpcHRpb25JZCI6ICIxMjNhYmMifQ.MEUCIAKqlB50xqNhnHkP6qoOoll33l3rWQ-_b5XfQJAUErnFAiEAlGR-cEl7DCzaoHqifh0drreFInsqo1xVy3SrWSMmNCI"/>
        </channel>
    </Subscription>

In \` &lt;id value="df694c098c2fb373524150461cfd9d23"/&gt;\` ist eine
eindeutige ID (Pseudonym der Telematik-ID) hinterlegt

Der timestamp in
`` <end value="2022-01-01T00:00:00Z"/> ` errechnet sich aus jetzt + 12h (UTC Timestamp) + [red]#In Klärung für RU: `jetzt + 1h ``
um den Verbinungsabbau nach Ablauf zu testen#

die Header müssen in \` &lt;header value="\*"\` beim Web Socket Upgrade
mitgegeben werden

Die Schnittstelle antwortet mit den typischen http-StatusCodes des
RESTful-Paradigmas

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
<td style="text-align: left;"><p>Created</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>Code</strong></p></td>
<td style="text-align: left;"><p><strong>Type Error</strong></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>400</p></td>
<td style="text-align: left;"><p>Bad Request</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>401</p></td>
<td style="text-align: left;"><p>Unauthorized</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>403</p></td>
<td style="text-align: left;"><p>Forbidden</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>429</p></td>
<td style="text-align: left;"><p>Too Many Requests</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>500</p></td>
<td style="text-align: left;"><p>Server Errors</p></td>
</tr>
</tbody>
</table>

## Websocket an Subscription-Endpunkt

Nach der Registrierung der Subscription wird eine WebSocket-Verbindung
zum eigentlichen NotificationService aufgebaut.

**Request**

<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p><strong>URI</strong></p></td>
<td style="text-align: left;"><p>subscription</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><strong>Method</strong></p></td>
<td style="text-align: left;"><p>GET</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><strong>Request</strong></p></td>
<td style="text-align: left;"><pre><code>GET /subscription HTTP/1.1
Host: subscription.zentral.erp.splitdns.ti-dienste.de
Authorization: Bearer eyJhbGciOiAiYnJhaW5wb29sUDI1NnIxIiwidHlwIjogIkpXVCJ9.eyJpc3MiOiAiTWF0aGlzIGJyYWlucG9vbCBqd3QiLCJpYXQiOiAxNjMyMjk0MzY1LCJleHAiOiAxNjYzODMwMzY1LCJhdWQiOiAibG9jYWxob3N0Iiwic3ViIjogIm15VXNlcm5hbWUiLCJzdWJzY3JpcHRpb25JZCI6ICIxMjNhYmMifQ.MEUCIAKqlB50xqNhnHkP6qoOoll33l3rWQ-_b5XfQJAUErnFAiEAlGR-cEl7DCzaoHqifh0drreFInsqo1xVy3SrWSMmNCI
Connection: Upgrade
Pragma: no-cache
Cache-Control: no-cache
Upgrade: websocket
Sec-WebSocket-Version: 13
Sec-WebSocket-Key: q4xkcO32u266gldTuKaSOw==</code></pre>
<div class="tip">
<p>Dieser Request ist NICHT zusätzlich VAU-verschlüsselt, sondern wird
TLS-verschlüsselt an den Subscription-Endpunkt geschickt.</p>
</div>
<div class="tip">
<p>Je nach eingesetztem Framework lautet die Zieladresse dann
<code>wss://subscription.zentral.erp.splitdns.ti-dienste.de:443</code><br />
bzw. zum Test in der TI-Referenzumgebung RU =
<code>wss://subscription-ref.zentral.erp.splitdns.ti-dienste.de:443</code></p>
</div></td>
</tr>
</tbody>
</table>

In `Authorization:` wird das von der VAU generierte Bearer Token mit dem
Pseudonym über die Telematik-ID übergeben.

In `Sec-WebSocket-Key` werden clientseitig generierte Nonce (16-Byte
Zufallswert in base64-Codierung), siehe [RFC-6455 Seite 18, Punkt
7](https://www.rfc-editor.org/rfc/rfc6455#page-18)

**Response**

    HTTP/1.1 101 Switching Protocols
    Upgrade: websocket
    Connection: Upgrade
    Sec-WebSocket-Accept: fA9dggdnMPU79lJgAE3W4TRnyDM=

Der Subscription-Service antwortet mit einem `Connection: Upgrade`

Der Subscription-Service antwortet beim Schließen der
Websocket-Verbindung mit den Status-Codes gemäß
[RFC-6455](https://datatracker.ietf.org/doc/html/rfc6455#section-7.4),
bspw. mit Status `1000` wenn ein abgelaufenes Bearer Token übergeben
wird.  
Beendet der Service die WebSocket-Verbindung aufgrund eines (internen)
Fehlers, liefert er einen http-Status \[502 Bad Gateway, 504 Gateway
Timeout\].

**Der Websocket-Client MUSS eine zufällig gewählte Pause zw. 5 - 60
Sekunden warten, bevor eine neue Websocket-Verbindung aufgebaut wird.**

## Regisitrierung der Subscription in der Websocket-Verbindung

Das AVS registriert sich für die Subscription aus dem vorherigen
Schritt, in dem eine `bind` Text Nachricht über die Websocket-Verbindung
an den Subscription-Service geschickt wird.

    bind: df694c098c2fb373524150461cfd9d23

Im Value für `bind` befindet sich die `Subscription.id`

Der Subscription Service antwortet mit einer "bound" um die Einrichtung
der Subscription zu bestätigen.

    bound: df694c098c2fb373524150461cfd9d23

`Subscription.id`

# Benachrichtigung

Ist eine neue Communication eingegangen, benachrichtigt der
Subscription-Service das AVS, indem eine `ping <Subscription.id>`
Text-Nachricht über die Websocket-Verbindung gesendet wird.

    ping: df694c098c2fb373524150461cfd9d23

`Subscription.id`

Hinweis: die Nachricht `ping: df694c098c2fb373524150461cfd9d23` ist
**KEIN** `Ping` der Ping/Pong Control Frames für das Aufrechterhalten
der Verbindung (siehe
<https://datatracker.ietf.org/doc/html/rfc6455#section-5.5>).

Empfängt das AVS nun ein `ping: df694c098c2fb373524150461cfd9d23`, liegt
eine neue Nachricht vor, die über das VAU-Protokoll zum [Abrufen neuer
Nachrichten](erp_communication.adoc#user-content-anwendungsfall-auf-neue-nachrichten-im-e-rezept-fachdienst-prüfen)
heruntergeladen werden kann. Über die Websockets werden selbst keine
Nachrichten oder andere E-Rezept-bezogenen Daten verschickt.

# Beispielhafte Implementierung für Primärsysteme

    using System;
    using System.Net.WebSockets;
    using System.Text;
    using System.Threading;

    class Program {
        static void Main() {
            //subscriptionId und bearertoken aus VAU-Request /Subcription extrahieren
            CreateSocket("df694c098c2fb373524150461cfd9d23",
                "Bearer eyJhbGciOiJFUzI1NiJ9.CnsKInN1YnNjcmlwdGlvbklkIjogImRmNjk0YzA5OGMyZmIzNzM1MjQxNTA0NjFjZmQ5ZDI…");
        }

        private static void CreateSocket(string subscriptionId, string bearertoken) {
            var _websocketObj = new ClientWebSocket();
            _websocketObj.Options.SetRequestHeader("Authorization", bearertoken);
            //url RU: "wss://subscription-ref.zentral.erp.splitdns.ti-dienste.de" und PU: "wss://subscription.zentral.erp.splitdns.ti-dienste.de"
            _websocketObj.ConnectAsync(new Uri("wss://subscription-ref.zentral.erp.splitdns.ti-dienste.de/subscription"), CancellationToken.None)
                .Wait();

            if (_websocketObj.State != WebSocketState.Open) {
                throw new Exception("Websocket ist nicht geöffnet");
            }

            {
                var bind = $"bind: {subscriptionId}";
                _websocketObj.SendAsync(new ArraySegment<byte>(Encoding.UTF8.GetBytes(bind)), WebSocketMessageType.Text, true, CancellationToken.None)
                    .Wait();
                Console.Out.WriteLine($"Websocket-Bind: {bind}");

                var buffer = new ArraySegment<byte>(new byte[2048]);
                WebSocketReceiveResult wsr = _websocketObj.ReceiveAsync(buffer, CancellationToken.None).Result;
                var res = Encoding.UTF8.GetString(buffer.Array, buffer.Offset, wsr.Count);
                Console.Out.WriteLine($"Websocket-Bound: {res}");
            }

            while (true) {
                var buffer = new ArraySegment<byte>(new byte[2048]);
                WebSocketReceiveResult wsr = _websocketObj.ReceiveAsync(buffer, CancellationToken.None).Result;
                // ReSharper disable once AssignNullToNotNullAttribute
                var res = Encoding.UTF8.GetString(buffer.Array, buffer.Offset, wsr.Count);
                if (wsr.Count > 0) {
                    Console.Out.WriteLine($"Websocket-Empfangen: {res} ({wsr.Count} Bytes) -> es liegen neue Nachrichten bereit!");
                }
            }
        }
    }

# ⇒ Wichtige Hinweise ⇐

Jede eingestellte Nachricht führt zu einem Ping, ggfs. im
Millisekundenbereich, wenn viele Nachrichten an einen Empfänger
gerichtet werden. In Abhängigkeit von der Implementierung kann dieses
Verhalten zu einer Überlastung des PS führen, wenn bspw. jedes einzelne
Ping den Anwendungsfall "Nachrichten von Versicherten empfangen"
triggert.  
Im Zweifel ist eine Wartezeit im AVS hilfreich, in der die zuletzt
abgerufenen Nachrichten bearbeitet werden. Zwischenzeitlich "gepingte"
Nachrichten gehen nicht verloren, da sie beim nächsten Abruf ungelesener
Nachrichten gesammelt heruntergeladen werden.

Wird die WebSocket-Verbindung aufgrund eines Fehlers unerwartet
terminiert, MUSS der Websocket-Client eine zufällig gewählte Pause zw.
5 - 60 Sekunden warten, bevor eine neue Websocket-Verbindung aufgebaut
wird.

Je Telematik-ID ist nur ein Websocket möglich

Die Websocket-Verbindung wird nach 12h automatisch geschlossen und muss
neu registriert werden.
