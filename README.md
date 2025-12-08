# E-Rezept API-Dokumentation <img src="images/gematik_logo.png" alt="gematik logo" width="150" style="float: right"/>
[PVS]: https://img.shields.io/badge/PVS/KIS-C30059
[AVS]: https://img.shields.io/badge/AVS-E30615
[FdV]: https://img.shields.io/badge/FdV-green
[KTR]: https://img.shields.io/badge/KTR-AE8E1C
[bfarm]: https://img.shields.io/badge/BfArM-197F71
Hier dokumentiert die gematik die Nutzung der Schnittstellen rund um das E-Rezept.

- [E-Rezept API-Dokumentation ](#e-rezept-api-dokumentation-)
  - [Einleitung](#einleitung)
  - [Aktuelles](#aktuelles)
    - [RSA zu ECC Umstellung](#rsa-zu-ecc-umstellung)
    - [Profilwechsel und Versionierung](#profilwechsel-und-versionierung)
  - [Umfang der Anwendung E-Rezept](#umfang-der-anwendung-e-rezept)
  - [Implementierungsunterstützung](#implementierungsunterstützung)
  - [Anwendungsfälle im E-Rezept](#anwendungsfälle-im-e-rezept)
    - [Allgemein](#allgemein)
    - [Anwendungsfälle Zugang zur TI](#anwendungsfälle-zugang-zur-ti)
    - [Anwendungsfälle Bedienung von E-Rezepten](#anwendungsfälle-bedienung-von-e-rezepten)
    - [Besondere Anwendungsfälle](#besondere-anwendungsfälle)
    - [Anwendungsfälle PKV](#anwendungsfälle-pkv)
  - [License](#license)
  - [Additional Notes and Disclaimer from gematik GmbH](#additional-notes-and-disclaimer-from-gematik-gmbh)

## Einleitung
Die gematik geht neue Wege und möchte auf diesem Weg die Nutzung der Schnittstellen rund um das E-Rezept vorstellen. Die Beschreibung dieser API ergänzt die normativen Dokumente der gematik sowie die Festlegungen über die [E-Rezept-Profile (inkl. Beispielen)](https://simplifier.net/erezept-workflow) des genutzten FHIR-Standards.

Auf den folgenden Seiten stellt die gematik die Nutzung der Schnittstellen durch die Primärsysteme der verordnenden Ärzte/Zahnärzte und der Apotheker sowie durch die E-Rezept-App vor.
Die E-Rezept-App wird durch die gematik bereitgestellt und ist zum Start des E-Rezepts in den App Stores der beiden Plattformen iOS und Android verfügbar.



## Aktuelles

### RSA zu ECC Umstellung
- Für die RSA - ECC umstellung wurde ein Leitfaden erstellt, der den Übergang unterstützen soll: [E-Rezept - RSA2ECC Umstellungsleitfaden für Entwickler](https://service.gematik.de/servicedesk/customer/kb/view/641653859)

### Profilwechsel und Versionierung

Ein Überblick über die Handhabung von Versionen und Packages im E-Rezept-Fachdienst können hier angesehen werden: [E-Rezept FHIR-Package Versionsmanagement](docs/erp_fhirversion.adoc)

Für das E-Rezept stehen folgende Veränderungen der FHIR-Profile an:

- [E-Rezept FHIR Veränderungen für 15.01.2025](docs/erp_fhirversion_change_20250115.adoc)
- [E-Rezept FHIR Veränderungen für 01.10.2025](docs/erp_fhirversion_change_20251001.adoc)

> [!WARNING]  
> Die API und deren Beispiele zeigen aktuell den Stand ab **01.10.2025** an. Für vorherige Versionen auf die entsprechenden wf-version Branches wechseln:
> - [Stand 15.01.2025 (u.A. Workflow 1.4)](https://github.com/gematik/api-erp/tree/wf-version/1.4/README.md)
> - [Stand 01.11.2024 (u.A. Workflow 1.3)](https://github.com/gematik/api-erp/tree/wf-version/1.3/README.md)


## Umfang der Anwendung E-Rezept
[Hier geht es zur Übersicht der Produkte, die über das E-Rezept verordnet werden können](docs/erp_implemented_features.adoc)

## Implementierungsunterstützung
[Hier geht es zur Informationsseite zur Implementierungsunterstützung bezüglich FHIR und allgemeiner Hinweise](docs/erp_fhir_infos.adoc)

## Anwendungsfälle im E-Rezept

In den nachfolgend verlinkten Abschnitten zeigen wir die Anwendungsfälle im E-Rezept Kontext auf.

### Allgemein
|Dokumentation<img width="430" height="1">| Zielgruppe<img width="70" height="1"> |
|-----|------------|
|[Endpunkte](docs/misc_api_endpoints.adoc)|![][PVS] ![][AVS] ![][FdV] ![][KTR]|
|[Fehlerbehandlung](docs/erp_statuscodes.adoc)|![][PVS] ![][AVS] ![][FdV] ![][KTR]|
|[FHIR-Package Änderungen bei Versionsübergängen](docs/erp_fhirversion_changes.adoc)|![][PVS] ![][AVS] ![][FdV] ![][KTR]|
|[FHIR-Package Versionsmanagement](docs/erp_fhirversion.adoc)|![][PVS] ![][AVS] ![][FdV] ![][KTR]|
|[FHIR-Validierung in Titus](docs/erp_validation.adoc)|![][PVS] ![][AVS] ![][FdV] ![][KTR]|

### Anwendungsfälle Zugang zur TI
|Dokumentation<img width="430" height="1">| Zielgruppe<img width="70" height="1"> |
|-----|------------|
|[Beschreibung des Verbindungsaufbaus zur Telematikinfrastruktur](docs/authentisieren.adoc)|![][PVS] ![][AVS] ![][FdV] ![][KTR]|
|[Fachdienst Health-Check](docs/erp_ps_probing.adoc)|![][PVS] ![][AVS] ![][KTR]|
|[TI-Konfiguration](docs/ti_configuration.adoc)|![][PVS] ![][AVS] ![][KTR]|
|[TI Lagebild](https://github.com/gematik/api-tilage/blob/main/content/Documentation.md)|![][PVS] ![][AVS] ![][KTR]|

### Anwendungsfälle Bedienung von E-Rezepten
|Dokumentation<img width="430" height="1">| Zielgruppe<img width="70" height="1"> |
|-----|------------|
|[Anwendungsfälle für Versicherte](docs/erp_versicherte.adoc)|![][FdV]|
|[Belieferung von E-Rezepten](docs/erp_abrufen.adoc)|![][AVS]|
|[Bereitstellung von E-Rezepten](docs/erp_bereitstellen.adoc)|![][PVS]|
|[Einlösung von E-Rezepten mit Gesundheitskarte mittels PoPP](docs/erp_abrufen_egk_popp.adoc)|![][AVS]|
|[Workflow-Steuerung durch Leistungserbringer](docs/erp_steuerung_durch_le.adoc)|![][PVS] ![][AVS] ![][FdV]|
|[Bedienen von DiGA-Verordnungen](docs/erp_diga.adoc)|![][PVS] ![][FdV] ![][KTR]|

### Besondere Anwendungsfälle
|Dokumentation<img width="430" height="1">| Zielgruppe<img width="70" height="1"> |
|-----|------------|
|[Benachrichtigungsdienst](docs/erp_notification.adoc)|![][FdV]|
|[Benachrichtigungen für Apotheken und Kostenträger](docs/erp_notification_avs.adoc)|![][AVS] ![][KTR]|
|[Einlösen ohne Anmeldung](docs/erp_alternative_zuweisung.adoc)|![][AVS] ![][FdV]|
|[Mehrfachverordnungen (MVO) für Versicherte](docs/erp_versicherte_mvo.adoc)|![][FdV]|
|[Nachrichtenaustausch](docs/erp_communication.adoc)|![][AVS] ![][FdV] ![][KTR]|
|[Suche nach Apotheken im FHIR VZD](docs/erp_fhirvzd_usage.adoc)|![][FdV]|
|[Zertifikatsprüfung](docs/erp_certificate_check.adoc)|![][FdV]|
|[Übertragung digitaler Durchschlag E-T-Rezept](docs/erp_bfarm.adoc)|![][bfarm]|
|[OpenApi Remote-FdV v1.2.1](docs/fdv-testdriver-openapi.adoc)|![][FdV]|

### Anwendungsfälle PKV
|Dokumentation<img width="430" height="1">| Zielgruppe<img width="70" height="1"> |
|-----|------------|
|[Abrechnungsinformationen](docs/erp_chargeItem.adoc)|![][AVS] ![][FdV]|
|[Einwilligung](docs/erp_consent.adoc)|![][AVS] ![][FdV]
|[Liste der PKV-Institutionskennzeichennummern](https://github.com/PKV-Verband/PKV-IK-Liste)|![][PVS]|

## License

Copyright 2022-2025 gematik GmbH

Apache License, Version 2.0

See the [LICENSE](./LICENSE) for the specific language governing permissions and limitations under the License

## Additional Notes and Disclaimer from gematik GmbH

1. Copyright notice: Each published work result is accompanied by an explicit statement of the license conditions for use. These are regularly typical conditions in connection with open source or free software. Programs described/provided/linked here are free software, unless otherwise stated.
2. Permission notice: Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
    1. The copyright notice (Item 1) and the permission notice (Item 2) shall be included in all copies or substantial portions of the Software.
    2. The software is provided "as is" without warranty of any kind, either express or implied, including, but not limited to, the warranties of fitness for a particular purpose, merchantability, and/or non-infringement. The authors or copyright holders shall not be liable in any manner whatsoever for any damages or other claims arising from, out of or in connection with the software or the use or other dealings with the software, whether in an action of contract, tort, or otherwise.
    3. We take open source license compliance very seriously. We are always striving to achieve compliance at all times and to improve our processes. If you find any issues or have any suggestions or comments, or if you see any other ways in which we can improve, please reach out to: ospo@gematik.de
3. Please note: Parts of this code may have been generated using AI-supported technology. Please take this into account, especially when troubleshooting, for security analyses and possible adjustments.