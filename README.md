# E-Rezept Entwicklerinformation <img src="images/gematik_logo.png" alt="gematik logo" width="150" style="float: right"/>

Diese Seite dient als Ausgangspunkt für Entwickler, um Informationen zum E-Rezept zu erhalten.

## Ankündigungen und Aktuelles

//TODO: change link

Aktuelle Informationen zum Thema E-Rezept finden sie auf [GitHub Discussions](https://github.com/florianschoffke/test-openapi/discussions) in diesem Repository.

Hier befinden sich aktuelle [Informationen und Konfigurationen des Fachdienstes](./docs/ru_aas.md) zu finden

### Sprechstunde

Die Sprechstunde zum E-Rezept findet Montags 11:00 - 12:00 statt. Sie können unter diesem [Teams-Link](https://teams.microsoft.com/l/meetup-join/19%3ameeting_ODZlNTUyZjUtZjNjNy00NzI3LWI2NGMtMDI4OTgyYzJkN2Vk%40thread.v2/0?context=%7b%22Tid%22%3a%2230092c62-4dbf-43bf-a33f-10d21b5b660a%22%2c%22Oid%22%3a%226ffbeb95-9578-4047-93a2-fb302f6b9f53%22%7d) teilnehmen. 

Auf unserem Confluence Portal befinden sich [Protokolle vergangener Sprechstunden](https://wiki.gematik.de/pages/viewpage.action?pageId=459882758#)

## Fachportal

Im Fachportal veröffentlicht die gematik normative Spezifikationen. Es sind auch wesentliche Dokumente und weiterführende Informationen zum E-Rezept zu finden: [Fachportal E-Rezept](https://fachportal.gematik.de/anwendungen/elektronisches-rezept)

## E-Rezept on FHIR

Der Datenaustausch zum E-Rezept basiert auf dem internationalen Austauschformat [FHIR](https://hl7.org/fhir/R4/). Informationen zu den FHIR-Profilen finden sich auf der entsprechenden [Übersichtsseite](./docs/fhir_intro.md)

## Schnittstellenbeschreibung

Der E-Rezept-Fachdienst ist einer der zentralen Dienste der Telematik Infrastruktur, der die Verwaltung von E-Rezepten umsetzt. Hier finden sie eine OpenAPI der [Schnittstellen des E-Rezept-Fachdienstes](https://gematiktest.stoplight.io/docs/test-openapi/95201cd74824d-intro-open-api-beschreibung)

## Beispiel Dateien

Für die Implementierung des E-Rezeptes stehen Beispiele im FHIR-Format zur Verfügung.

Im [gemeinsamen Beispiel-Repository](https://github.com/gematik/eRezept-Examples) der Gesellschafter sind sowohl Einzelbeispiele von Profilen, wie auch Beispiele von Ende zu Ende Szenarien dokumentiert.

Wir wünschen uns an dieser Stelle auch ein reges Mitwirken der Industrie bei der Erstellung dieser Beispiele. Über Pull-Requests und andere Formen der Kollaboration freuen wir uns.

## Umfang der Anwendung E-Rezept
[Hier geht es zur Übersicht der Produkte, die über das E-Rezept verordnet werden können](docs/erp_implemented_features.adoc)

## Bekannte Fehler im Fachdienst
* Referenzen in einigen responses des Fachdienstes sind noch nicht FHIR konform (bsp: Task.input oder erneutes Abrufen der Quittung). Da dies ein breaking change ist, wird dies in einer späteren Version behoben


## Lizenzbedingungen

Copyright (c) 2023 gematik GmbH

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

<http://www.apache.org/licenses/LICENSE-2.0>

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
