# E-Rezept API-Dokumentation <img src="images/gematik_logo.png" alt="gematik logo" width="150" style="float: right"/>
[PVS]: https://img.shields.io/badge/PVS/KIS-C30059
[AVS]: https://img.shields.io/badge/AVS-E30615
[FdV]: https://img.shields.io/badge/FdV-green
[KTR]: https://img.shields.io/badge/KTR-AE8E1C
Hier dokumentiert die gematik die Nutzung der Schnittstellen rund um das E-Rezept.

- [E-Rezept API-Dokumentation ](#e-rezept-api-dokumentation-)
  - [Einleitung](#einleitung)
  - [Aktuelles](#aktuelles)
  - [Umfang der Anwendung E-Rezept](#umfang-der-anwendung-e-rezept)
  - [Implementierungsunterstützung](#implementierungsunterstützung)
  - [Anwendungsfälle im E-Rezept](#anwendungsfälle-im-e-rezept)
    - [Allgemein](#allgemein)
    - [Anwendungsfälle Zugang zur TI](#anwendungsfälle-zugang-zur-ti)
    - [Anwendungsfälle Bedienung von E-Rezepten](#anwendungsfälle-bedienung-von-e-rezepten)
    - [Besondere Anwendungsfälle](#besondere-anwendungsfälle)
    - [Anwendungsfälle PKV](#anwendungsfälle-pkv)
  - [Lizenzbedingungen](#lizenzbedingungen)

## Einleitung
Die gematik geht neue Wege und möchte auf diesem Weg die Nutzung der Schnittstellen rund um das E-Rezept vorstellen. Die Beschreibung dieser API ergänzt die normativen Dokumente der gematik sowie die Festlegungen über die [E-Rezept-Profile (inkl. Beispielen)](https://simplifier.net/erezept-workflow) des genutzten FHIR-Standards.

Auf den folgenden Seiten stellt die gematik die Nutzung der Schnittstellen durch die Primärsysteme der verordnenden Ärzte/Zahnärzte und der Apotheker sowie durch die E-Rezept-App vor.
Die E-Rezept-App wird durch die gematik bereitgestellt und ist zum Start des E-Rezepts in den App Stores der beiden Plattformen iOS und Android verfügbar.



## Aktuelles
Für das E-Rezept stehen folgende Veränderungen der FHIR-Profile an:

[Aktueller Status des E-Rezept-Fachdienst Exporters](docs/erp_eml-mapping-status.adoc)

[E-Rezept FHIR Veränderungen für 15.01.2025](docs/erp_fhirversion_change_20250115.adoc)


## Umfang der Anwendung E-Rezept
[Hier geht es zur Übersicht der Produkte, die über das E-Rezept verordnet werden können](docs/erp_implemented_features.adoc)

## Implementierungsunterstützung
[Hier geht es zur Informationsseite zur Implementierungsunterstützung bezüglich FHIR und allgemeiner Hinweise](docs/erp_fhir_infos.adoc)

## Anwendungsfälle im E-Rezept

In den nachfolgend verlinkten Abschnitten zeigen wir die Anwendungsfälle im E-Rezept Kontext auf.

### Allgemein
|Dokumentation<img width="430" height="1">| Zielgruppe<img width="70" height="1"> |
|-----|------------|
|[Endpunkte](docs/misc_api_endpoints.adoc)|![][PVS] ![][AVS] ![][FdV]|
|[Fehlerbehandlung](docs/erp_statuscodes.adoc)|![][PVS] ![][AVS] ![][FdV]|
|[FHIR-Package Änderungen bei Versionsübergängen](docs/erp_fhirversion_changes.adoc)|![][PVS] ![][AVS] ![][FdV]|
|[FHIR-Package Versionsmanagement](docs/erp_fhirversion.adoc)|![][PVS] ![][AVS] ![][FdV]|
|[FHIR-Validierung in Titus](docs/erp_validation.adoc)|![][PVS] ![][AVS] ![][FdV]|

### Anwendungsfälle Zugang zur TI
|Dokumentation<img width="430" height="1">| Zielgruppe<img width="70" height="1"> |
|-----|------------|
|[Beschreibung des Verbindungsaufbaus zur Telematikinfrastruktur](docs/authentisieren.adoc)|![][PVS] ![][AVS] ![][FdV]|
|[Fachdienst Health-Check](docs/erp_ps_probing.adoc)|![][PVS] ![][AVS]|
|[TI-Konfiguration](docs/ti_configuration.adoc)|![][PVS] ![][AVS]
|[TI Lagebild](docs/erp_ps_probing_lagebild.adoc)|![][PVS] ![][AVS]|

### Anwendungsfälle Bedienung von E-Rezepten
|Dokumentation<img width="430" height="1">| Zielgruppe<img width="70" height="1"> |
|-----|------------|
|[Anwendungsfälle für Versicherte](docs/erp_versicherte.adoc)|![][FdV]|
|[Belieferung von E-Rezepten](docs/erp_abrufen.adoc)|![][AVS]|
|[Bereitstellung von E-Rezepten](docs/erp_bereitstellen.adoc)|![][PVS]|
|[Einlösung von E-Rezepten mit Gesundheitskarte](docs/erp_abrufen_egk.adoc)|![][AVS]|
|[Workflow-Steuerung durch Leistungserbringer](docs/erp_steuerung_durch_le.adoc)|![][PVS] ![][AVS] ![][FdV]|
|[Bedienen von DiGA-Verordnungen](docs/erp_diga.adoc)|![][PVS] ![][KTR] ![][FdV]|

### Besondere Anwendungsfälle
|Dokumentation<img width="430" height="1">| Zielgruppe<img width="70" height="1"> |
|-----|------------|
|[Benachrichtigungsdienst](docs/erp_notification.adoc)|![][FdV]|
|[Benachrichtigungen für Apotheken](docs/erp_notification_avs.adoc)|![][AVS]|
|[Einlösen ohne Anmeldung](docs/erp_alternative_zuweisung.adoc)|![][AVS] ![][FdV]|
|[Mehrfachverordnungen (MVO) für Versicherte](docs/erp_versicherte_mvo.adoc)|![][FdV]|
|[Nachrichtenaustausch](docs/erp_communication.adoc)|![][AVS] ![][FdV]|
|[Suche nach Apotheken im FHIR VZD](docs/erp_fhirvzd_usage.adoc)|![][FdV]|
|[Zertifikatsprüfung](docs/certificate_check.adoc)|![][FdV]|

### Anwendungsfälle PKV
|Dokumentation<img width="430" height="1">| Zielgruppe<img width="70" height="1"> |
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