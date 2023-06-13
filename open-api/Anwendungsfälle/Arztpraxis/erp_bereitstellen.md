
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

1. PrescriptionID und AccessCode vom E-Rezept Fachdienst anfordern ([POST /Task/$create](open-api/openapi/openapi_erezpt.yaml/paths/~1Task~1$create/post))
2. Verordnungsdatensatz erstellen
3. Verordnungsdatensatz signieren
4. Verordnungsdatensatz im E-Rezept Fachdienst einstellen ([POST /Task/$activate](open-api/openapi/openapi_erezpt.yaml/paths/~1Task~1{task_id}~1$activate/post))
5. Optional ist auch das Löschen eines E-Rezepts für den Verordnenden möglich ([POST /Task/{id}/$abort](open-api/openapi/openapi_erezpt.yaml/paths/~1Task~1{task_id}~1$abort))

![width=100%](../../assets/images/api_rezept_einstellen.png)

## Profilierung

Für diesen Anwendungsfall wird die FHIR-Resource "Task" profiliert. Für die Nutzung im E-Rezept relevante Felder sind als "Must Support" (MS) gekennzeichnet. 
<https://simplifier.net/erezept-workflow/gem_erp_pr_task>.

In den folgenden Kapiteln wird erläutert, wann und wie die Befüllung
dieser Attribute erfolgt.

## E-Rezept erstellen

[API-Endpunkt: POST /Task/$create](open-api/openapi/openapi_erezpt.yaml/paths/~1Task~1$create/post)
[Absoluter Link Beispiel: POST /Task/$create](https://gematiktest.stoplight.io/docs/gematik-api-erp/e2fbe0e57ab74-create)

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

Nachdem ein gültiger Verordnungsdatensatz gemäß den Vorgaben der KBV erstellt wurde, liegt im Primärsystem ein E-Rezept-Datensatz als FHIR-Bundle vor. Im vorhergehenden Schritt hat das
Primärsystem einen Task im E-Rezept-Fachdienst erzeugt, um
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

[API-Endpoint: POST /Task/$activate](open-api/openapi/openapi_erezpt.yaml/paths/~1Task~1{task_id}~1$activate/post)

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

## Ein E-Rezept löschen

[API-Endpoint: POST /Task/$activate](open-api/openapi/openapi_erezpt.yaml/paths/~1Task~1{task_id}~1$activate/post)

Als verordnender Leistungserbringer möchte ich ein E-Rezept löschen
können, um den Patienten vor dem Bezug und der Einnahme eines fälschlich
verordneten Medikaments zu schützen.

Der Aufruf erfolgt als http-POST-Operation mit der FHIR-Operation
`$abort`. Im http-Request-Header `Authorization` müssen das während der
Authentisierung erhaltene ACCESS\_TOKEN und der AccessCode im Header
`X-AccessCode` für die Berechtigungsprüfung übergeben werden.
