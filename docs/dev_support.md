# Tools für die Entwicklungsunterstützung

## Erstellung von Qualifizierten elektronischen Signaturen (QES)
Für die QES-Erstellung durch den Konnektor liegen im Unterordner [samples/qes](samples/qes) SOAP-Request/Responses zu den [Verordnungsbeispielen](https://simplifier.net/packages/kbv.ita.erp/1.0.1/~files) der KBV bereit. Spezialfälle (z.B. abgelaufene Zertifikate wegen Kartenwechsel o.ä.) stellen wir im Unterordner [samples/qes-cases](samples/qes-cases) bereit. Da die signierten Dokumente nicht verändert werden dürfen sind die Beispiele noch in Profilversionen, die nicht mehr im Produktivbetrieb des Fachdienstes unterstützt werden.

## Vergleich von FHIR Versionen

Wie Vergleiche zwischen FHIR Profilen (z.B. nach Versionsübergängen) vorgenommen werden können und den Verweis auf die Artefakte zum aktuellen Versionsübergang finden sich [auf dieser Seite](docs/erp_fhirversion_changes.adoc).

## Konvertierung von FHIR XML und JSON
Der FHIR Standard unterstützt für den Datenaustausch mehrere Formate. Die beiden vom E-Rezept Fachdienst unterstützten Formate sind XML (Content-Type: application/fhir+xml) und JSON (Content-Type: application/fhir+json). Der Fachdienst unterstützt an jedem Endpunkt beide Formate. Mit den Gesellschaftern wurde abgestimmt, dass bei der Kommunikation und Beschreibung der Endpunkte, die Primärsysteme betreffen, das Format XML genutzt wird. Das heißt, dass die Beispiele in der API und im [eRezept-Examples Repository](https://github.com/gematik/eRezept-Examples), die die Primärsysteme betreffen in XML dargestellt werden.
Der Datenaustausch zwischen dem Fachdienst und dem Frontend des Versicherten (FdV) dagegen geschieht im JSON-Format.

Folgende Tools können genutzt werden, um FHIR-Dokumente zwischen XML und JSON zu konvertieren:
* [Webseite zum Konvertieren](https://fhir-formats.github.io/)
* [FHIR tools VS Code Extension](https://marketplace.visualstudio.com/items?itemName=Yannick-Lagger.vscode-fhir-tools)
* [FHIR.js npm Package](https://www.npmjs.com/package/fhir)
* [Beschreibung zur Umwandlung mit HAPI (Java)](https://hapifhir.io/hapi-fhir/docs/model/parsers.html)