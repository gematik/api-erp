# ![gematik logo](images/gematik_logo.png) E-Rezept API-Dokumentation

Hier dokumentiert die gematik die Nutzung der Schnittstellen rund um das E-Rezept.

Die gematik geht neue Wege und möchte auf diesem Weg die Nutzung der Schnittstellen rund um das E-Rezept vorstellen. Die Beschreibung dieser API ergänzt die normativen Dokumente der gematik sowie die Festlegungen über die [E-Rezept-Profile (inkl. Beispielen)](https://simplifier.net/erezept-workflow) des genutzten FHIR-Standards.

Auf den folgenden Seiten stellt die gematik die Nutzung der Schnittstellen durch die Primärsysteme der verordnenden Ärzte/Zahnärzte und der Apotheker sowie durch die E-Rezept-App vor.
Die E-Rezept-App wird durch die gematik bereitgestellt und ist zum Start des E-Rezepts in den App Stores der beiden Plattformen iOS und Android verfügbar.

Die KBV definiert die FHIR-Profile des Verordnungsdatensatzes im simplifier-Projekt [E-Rezept-Verordnung](https://simplifier.net/erezept). Die Festlegungen zu Abgabe- und Abrechnungsdaten der Apotheken werden im DAV-Projekt [Abgabedaten](https://simplifier.net/erezeptabgabedaten) und im GKV-Projekt [Abrechnungsdaten](https://simplifier.net/eRezeptAbrechnungsdaten) getroffen.

Für die QES-Erstellung durch den Konnektor liegen im Unterordner [samples/qes](samples/qes) SOAP-Request/Responses zu den [Verordnungsbeispielen](https://simplifier.net/erezept/~resources?category=Example&exampletype=Bundle) der KBV bereit. Spezialfälle (z.B. abgelaufene Zertifikate wegen Kartenwechsel o.ä.) stellen wir im Unterordner [samples/qes-cases](samples/qes-cases) bereit.

Durchgängige Beispieldatensätze von der Verordnung und qualifizierter Signatur über Quittung bis zu den Abrechnungsdaten stellt der Deutsche Apothekerverband in seinem github-Projekt [
eRezept-Beispiele](https://github.com/DAV-ABDA/eRezept-Beispiele/tree/v1.0.0) zur Verfügung.

In den nachfolgend verlinkten Abschnitten zeigen wir, wie sich verordnende Ärzte/Zahnärzte und Versicherte [mit der der TI verbinden](docs/authentisieren.adoc). Wir zeigen detailliert den Ablauf der [Erstellung eines E-Rezepts](docs/erp_bereitstellen.adoc) in der verordnenden Praxis und [wie Apotheker auf den Fachdienst zugreifen](docs/erp_abrufen.adoc), um ein E-Rezept zu beliefern. Für Versicherte stellen wir dar, wie die [Einsicht in die vorhandenen E-Rezepte](docs/erp_versicherte.adoc) und [Abgabeinformationen eingelöster Rezepte](docs/erp_versicherte.adoc) erfolgt, wie die [Kommunikation mit der Apotheke](docs/erp_communication.adoc) ablaufen kann und wie der Versicherte [Einsicht in das Zugriffsprotokoll](docs/erp_versicherte.adoc) auf alle seine E-Rezepte nehmen kann. Schließlich zeigen wir, wie der [Ablauf der Rezept-Einlösung](docs/erp_versicherte.adoc) für Versicherte mit dem E-Rezept funktioniert.

## FHIR-Releases

[Auf dieser Seite veröffentlichen die E-Rezept-Beteiligten {KBV, DAV, GKV, PKV und gematik} gemeinsam ihre FHIR-Release-Festlegungen.](docs/erp_fhirversion.adoc)

Die Veröffentlichung an dieser Stelle erfolgt übergangsweise, bis ein gemeinsames Repository 'oberhalb' der API-Beschreibung gefunden ist.

Das Titus-Testportal wird in den Anwendungsfällen zum E-Rezept um einen Validator erweitert. Zukünftig werden *alle* Requests vor der Weiterverarbeitung online validiert.  
Details dazu finden sich [auf der folgenden Seite](docs/erp_validation.adoc).

Wie Vergleiche zwischen FHIR Profilen (z.B. nach Versionsübergängen) vorgenommen werden können und den Verweis auf die Artefakte zum aktuellen Versionsübergang finden sich [auf dieser Seite](docs/erp_fhirversion_changes.adoc).

## Zugang zu Diensten der Telematikinfrastruktur

[Hier geht es zur Beschreibung des Verbindungsaufbaus zur Telematikinfrastruktur](docs/authentisieren.adoc)

[Hier geht es zur notwendigen Netzwerkkonfiguration für Primärsysteme](docs/ti_configuration.adoc)

[Hier gibt es eine Übersicht der in der API verwendeten http-Status- und Fehlercodes](docs/erp_statuscodes.adoc)

[Hinweise und Festlegungen zu Health-Checks und Verfügbarkeits-Probes](docs/erp_ps_probing.adoc)

## Anwendungsfälle E-Rezept in der Praxis

[Hier geht es zu den Anwendungsfällen in der (Zahn-)Arztpraxis zur Verordnung von E-Rezepten](docs/erp_bereitstellen.adoc)

[Hier geht es zu den Anwendungsfällen für die direkte Zuweisung eines E-Rezeptes an eine Apotheke](docs/erp_steuerung_durch_le.adoc)

[Hier geht es zu der vorabveröffentlichten und unvollständigen Liste der PKV-Institutionskennzeichen](docs/pkv_ik_numbers.adoc)

## Besonderheiten der Mehrfachverordnung (MVO)

[Hier geht es zu den Besonderheiten der Mehrfachverordnung (MVO)](docs/erp_versicherte_mvo.adoc)

## Anwendungsfälle E-Rezept in der Apotheke

[Hier geht es zu den Anwendungsfällen in der Apotheke, wie ein E-Rezept bedient wird](docs/erp_abrufen.adoc)

[++NEU++ Hier ist der Anwendungsfall zur Alternativen Zuweisung an die Apotheke beschrieben](docs/erp_alternative_zuweisung.adoc)

[Hier folgt die Beschreibung der Benachrichtigungsschnittstelle für Apothekensysteme](docs/erp_notification_avs.adoc)

## Anwendungsfälle für Versicherte

[Hier geht es zu den Anwendungsfällen für Versicherte, um ihre E-Rezepte zu verwalten und einzulösen](docs/erp_versicherte.adoc)

### PKV Versicherte

[Hier geht es zu den Anwendungsfällen für die elektronische Verwaltung der Abrechnungsinformationen](docs/erp_chargeItem.adoc)

[Hier geht es zu den Anwendungsfällen für das Verwalten der Einwilligung](docs/erp_consent.adoc)

## Anwendungsfälle für den Nachrichtenaustausch zwischen Versicherten und Apotheken

[Hier geht es zu den Anwendungsfällen für den Nachrichtenaustausch zwischen Versicherten und Apotheken](docs/erp_communication.adoc)

## Lizenzbedingungen

Copyright (c) 2022 gematik GmbH

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

<http://www.apache.org/licenses/LICENSE-2.0>

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
