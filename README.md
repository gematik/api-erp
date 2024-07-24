# E-Rezept API-Dokumentation <img src="images/gematik_logo.png" alt="gematik logo" width="150" style="float: right"/>
[PVS]: https://img.shields.io/badge/PVS/KIS-C30059
[AVS]: https://img.shields.io/badge/AVS-E30615
[FdV]: https://img.shields.io/badge/FdV-green
<style>
    table {
        width: 100%;
    }
</style>
Hier dokumentiert die gematik die Nutzung der Schnittstellen rund um das E-Rezept.

## Inhaltsverzeichnis
- [E-Rezept API-Dokumentation ](#e-rezept-api-dokumentation-)
  - [Inhaltsverzeichnis](#inhaltsverzeichnis)
  - [FHIR-Releases](#fhir-releases)
    - [Zukunftige FHIR-Releases](#zukunftige-fhir-releases)
  - [Implementierungsunterstützung](#implementierungsunterstützung)
    - [FHIR-Beispiele](#fhir-beispiele)
    - [Konvertierung von FHIR XML und JSON](#konvertierung-von-fhir-xml-und-json)
  - [Umfang der Anwendung E-Rezept](#umfang-der-anwendung-e-rezept)
  - [Anwendungsfälle im E-Rezept](#anwendungsfälle-im-e-rezept)
    - [Allgemein](#allgemein)
    - [Anwendungsfälle Zugang zur TI](#anwendungsfälle-zugang-zur-ti)
    - [Anwendungsfälle Bedienung von E-Rezepten](#anwendungsfälle-bedienung-von-e-rezepten)
    - [Besondere Anwendungsfälle](#besondere-anwendungsfälle)
    - [Anwendungsfälle PKV](#anwendungsfälle-pkv)
  - [Lizenzbedingungen](#lizenzbedingungen)


Die gematik geht neue Wege und möchte auf diesem Weg die Nutzung der Schnittstellen rund um das E-Rezept vorstellen. Die Beschreibung dieser API ergänzt die normativen Dokumente der gematik sowie die Festlegungen über die [E-Rezept-Profile (inkl. Beispielen)](https://simplifier.net/erezept-workflow) des genutzten FHIR-Standards.

Auf den folgenden Seiten stellt die gematik die Nutzung der Schnittstellen durch die Primärsysteme der verordnenden Ärzte/Zahnärzte und der Apotheker sowie durch die E-Rezept-App vor.
Die E-Rezept-App wird durch die gematik bereitgestellt und ist zum Start des E-Rezepts in den App Stores der beiden Plattformen iOS und Android verfügbar.

Die KBV definiert die FHIR-Profile des Verordnungsdatensatzes im simplifier-Projekt [E-Rezept-Verordnung](https://simplifier.net/erezept). Die Festlegungen zu Abgabe- und Abrechnungsdaten der Apotheken werden im DAV-Projekt [Abgabedaten](https://simplifier.net/erezeptabgabedaten) und im GKV-Projekt [Abrechnungsdaten](https://simplifier.net/eRezeptAbrechnungsdaten) getroffen.

Für die QES-Erstellung durch den Konnektor liegen im Unterordner [samples/qes](samples/qes) SOAP-Request/Responses zu den [Verordnungsbeispielen](https://simplifier.net/packages/kbv.ita.erp/1.0.1/~files) der KBV bereit. Spezialfälle (z.B. abgelaufene Zertifikate wegen Kartenwechsel o.ä.) stellen wir im Unterordner [samples/qes-cases](samples/qes-cases) bereit. Da die signierten Dokumente nicht verändert werden dürfen sind die Beispiele noch in Profilversionen, die nicht mehr im Produktivbetrieb des Fachdienstes unterstützt werden.

Durchgängige Beispieldatensätze von der Verordnung und qualifizierter Signatur über Quittung bis zu den Abrechnungsdaten stellt der Deutsche Apothekerverband in seinem github-Projekt [
eRezept-Beispiele](https://github.com/DAV-ABDA/eRezept-Beispiele/tree/v1.0.0) zur Verfügung.

In den nachfolgend verlinkten Abschnitten zeigen wir, wie sich verordnende Ärzte/Zahnärzte und Versicherte [mit der der TI verbinden](docs/authentisieren.adoc). Wir zeigen detailliert den Ablauf der [Erstellung eines E-Rezepts](docs/erp_bereitstellen.adoc) in der verordnenden Praxis und [wie Apotheker auf den Fachdienst zugreifen](docs/erp_abrufen.adoc), um ein E-Rezept zu beliefern. Für Versicherte stellen wir dar, wie die [Einsicht in die vorhandenen E-Rezepte](docs/erp_versicherte.adoc) und [Abgabeinformationen eingelöster Rezepte](docs/erp_versicherte.adoc) erfolgt, wie die [Kommunikation mit der Apotheke](docs/erp_communication.adoc) ablaufen kann und wie der Versicherte [Einsicht in das Zugriffsprotokoll](docs/erp_versicherte.adoc) auf alle seine E-Rezepte nehmen kann. Schließlich zeigen wir, wie der [Ablauf der Rezept-Einlösung](docs/erp_versicherte.adoc) für Versicherte mit dem E-Rezept funktioniert.

## FHIR-Releases

[Auf dieser Seite veröffentlichen die E-Rezept-Beteiligten {KBV, DAV, GKV, PKV und gematik} gemeinsam ihre FHIR-Release-Festlegungen.](docs/erp_fhirversion.adoc)

Die Veröffentlichung an dieser Stelle erfolgt übergangsweise, bis ein gemeinsames Repository 'oberhalb' der API-Beschreibung gefunden ist.

Das Titus-Testportal wird in den Anwendungsfällen zum E-Rezept um einen Validator erweitert. Zukünftig werden *alle* Requests vor der Weiterverarbeitung online validiert.
Details dazu finden sich [auf der folgenden Seite](docs/erp_validation.adoc).

Wie Vergleiche zwischen FHIR Profilen (z.B. nach Versionsübergängen) vorgenommen werden können und den Verweis auf die Artefakte zum aktuellen Versionsübergang finden sich [auf dieser Seite](docs/erp_fhirversion_changes.adoc).

### Zukunftige FHIR-Releases
Diese Seiten erklären, was für die bevorstehenden zukünftigen FHIR-Releases zu erwarten ist:

[E-Rezept FHIR Veränderungen für 01.11.2024](docs/erp_fhirversion_change_20241101.adoc)

[E-Rezept FHIR Veränderungen für 15.01.2025](docs/erp_fhirversion_change_20250115.adoc)

## Implementierungsunterstützung

### FHIR-Beispiele
Für die Implementierung des E-Rezeptes stehen Beispiele im FHIR-Format zur Verfügung.

Im [gemeinsamen Beispiel-Repository](https://github.com/gematik/eRezept-Examples) der Gesellschafter sind sowohl Einzelbeispiele von Profilen, wie auch Beispiele von Ende zu Ende Szenarien dokumentiert.

Wir wünschen uns an dieser Stelle auch ein reges Mitwirken der Industrie bei der Erstellung dieser Beispiele. Über Pull-Requests und andere Formen der Kollaboration freuen wir uns.

### Konvertierung von FHIR XML und JSON
Der FHIR Standard unterstützt für den Datenaustausch mehrere Formate. Die beiden vom E-Rezept Fachdienst unterstützten Formate sind XML (Content-Type: application/fhir+xml) und JSON (Content-Type: application/fhir+json). Der Fachdienst unterstützt an jedem Endpunkt beide Formate. Mit den Gesellschaftern wurde abgestimmt, dass bei der Kommunikation und Beschreibung der Endpunkte, die Primärsysteme betreffen, das Format XML genutzt wird. Das heißt, dass die Beispiele in der API und im [eRezept-Examples Repository](https://github.com/gematik/eRezept-Examples), die die Primärsysteme betreffen in XML dargestellt werden.
Der Datenaustausch zwischen dem Fachdienst und dem Frontend des Versicherten (FdV) dagegen geschieht im JSON-Format.

Folgende Tools können genutzt werden, um FHIR-Dokumente zwischen XML und JSON zu konvertieren:
* [Webseite zum Konvertieren](https://fhir-formats.github.io/)
* [FHIR tools VS Code Extension](https://marketplace.visualstudio.com/items?itemName=Yannick-Lagger.vscode-fhir-tools)
* [FHIR.js npm Package](https://www.npmjs.com/package/fhir)
* [Beschreibung zur Umwandlung mit HAPI (Java)](https://hapifhir.io/hapi-fhir/docs/model/parsers.html)

## Umfang der Anwendung E-Rezept
[Hier geht es zur Übersicht der Produkte, die über das E-Rezept verordnet werden können](docs/erp_implemented_features.adoc)

## Anwendungsfälle im E-Rezept
### Allgemein
|Dokumentation| Zielgruppe |
|-----|------------|
|[Endpunkte](docs/misc_api_endpoints.adoc)|![][PVS] ![][AVS] ![][FdV]|
|[Fehlerbehandlung](docs/erp_statuscodes.adoc)|![][PVS] ![][AVS] ![][FdV]|
|[FHIR-Package Änderungen bei Versionsübergängen](docs/erp_fhirversion_changes.adoc)|![][PVS] ![][AVS] ![][FdV]|
|[FHIR-Package Versionsmanagement](docs/erp_fhirversion.adoc)|![][PVS] ![][AVS] ![][FdV]|
|[FHIR-Validierung in Titus](docs/erp_validation.adoc)|![][PVS] ![][AVS] ![][FdV]|

### Anwendungsfälle Zugang zur TI
|Dokumentation| Zielgruppe |
|-----|------------|
|[Beschreibung des Verbindungsaufbaus zur Telematikinfrastruktur](docs/authentisieren.adoc)|![][PVS] ![][AVS] ![][FdV]|
|[Fachdienst Health-Check](docs/erp_ps_probing.adoc)|![][PVS] ![][AVS]|
|[TI-Konfiguration](docs/ti_configuration.adoc)|![][PVS] ![][AVS]
|[TI Lagebild](docs/erp_ps_probing_lagebild.adoc)|![][PVS] ![][AVS]|


### Anwendungsfälle Bedienung von E-Rezepten
|Dokumentation| Zielgruppe |
|-----|------------|
|[Anwendungsfälle für Versicherte](docs/erp_versicherte.adoc)|![][FdV]|
|[Belieferung von E-Rezepten](docs/erp_abrufen.adoc)|![][AVS]|
|[Bereitstellung von E-Rezepten](docs/erp_bereitstellen.adoc)|![][PVS]|
|[Einlösung von E-Rezepten mit Gesundheitskarte](docs/erp_abrufen_egk.adoc)|![][AVS]|
|[Workflow-Steuerung durch Leistungserbringer](docs/erp_steuerung_durch_le.adoc)|![][PVS] ![][AVS] ![][FdV]|

### Besondere Anwendungsfälle
|Dokumentation| Zielgruppe |
|-----|------------|
|[Benachrichtigungsdienst](docs/erp_notification.adoc)|![][FdV]|
|[Benachrichtigungen für Apotheken](docs/erp_notification_avs.adoc)|![][AVS]|
|[Einlösen ohne Anmeldung](docs/erp_alternative_zuweisung.adoc)|![][AVS] ![][FdV]|
|[Mehrfachverordnungen (MVO) für Versicherte](docs/erp_versicherte_mvo.adoc)|![][FdV]|
|[Nachrichtenaustausch](docs/erp_communication.adoc)|![][AVS] ![][FdV]|
|[Suche nach Apotheken im FHIR VZD](docs/erp_fhirvzd_usage.adoc)|![][FdV]|
|[Zertifikatsprüfung](docs/certificate_check.adoc)|![][FdV]|

### Anwendungsfälle PKV
|Dokumentation| Zielgruppe |
|-----|------------|
|[Abrechnungsinformationen](docs/erp_chargeItem.adoc)|![][AVS] ![][FdV]|
|[Einwilligung](docs/erp_consent.adoc)|![][AVS] ![][FdV]
|[Liste der PKV-Institutionskennzeichennummern](docs/pkv_ik_numbers.adoc)|![][PVS]|

## Lizenzbedingungen

Copyright (c) 2024 gematik GmbH

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

<http://www.apache.org/licenses/LICENSE-2.0>

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.