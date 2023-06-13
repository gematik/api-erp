# E-Rezept Entwicklerinformation <img src="images/gematik_logo.png" alt="gematik logo" width="150" style="float: right"/>

Diese Seite dient als Ausgangspunkt für Entwickler und Interessierte, um Informationen zum E-Rezept zu erhalten.

## Ankündigungen und Aktuelles

[comment]: <> (//TODO: Change Link to own repo)
Aktuelle Informationen zum Thema E-Rezept finden sie auf [GitHub Discussions](https://github.com/florianschoffke/test-openapi/discussions) in diesem Repository.

Hier befinden sich aktuelle [Informationen und Konfigurationen des Fachdienstes](./docs/ru_aas.md) zu finden

## Neu beim E-Rezept?

Falls Sie das E-Rezept noch nicht kennen und eine Einführung brauchen, schauen sie auf unserer [Einführung zum E-Rezept](./docs/erp_intro.md)


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
