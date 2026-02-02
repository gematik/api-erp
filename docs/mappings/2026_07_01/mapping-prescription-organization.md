# Mapping der Organization für Verordnungsdaten - Implementation Guide E-Rezept-Fachdienst v1.6.1-draft

Implementation Guide

E-Rezept-Fachdienst

Version 1.6.1-draft - ci-build 

* [**Table of Contents**](toc.md)
* [**Vorgaben zum Mapping von FHIR-Instanzen**](mapping.md)
* [**Mapping von Verordnungsdaten**](mapping-prescription.md)
* **Mapping der Organization für Verordnungsdaten**

## Mapping der Organization für Verordnungsdaten

Diese Seite beschreibt Anforderungen und Umsetzungsunterstützung für das Mapping von

* [KBV_FOR_PR_Organization](https://simplifier.net/packages/kbv.ita.for/1.2.1/files/3157102)
* zum [OrganizationDirectory](https://simplifier.net/packages/de.gematik.fhir.directory/1.0.0/files/2970167).

## Wichtige Punkte beim Mapping der Organization Ressource

Die folgenden Punkte sind relevant für das Mapping der Organization Ressource:

* Telematik-ID, Name und professionOID der Organisation müssen aus dem Accesstoken der Anfrage bezogen werden (F_006b)
* Extensions aus der Adresse werden übernommen (F_007)

## Generelles Mapping des Profils

Die folgende Tabelle stellt generell das Mapping der beiden Profile gegenüber:

### Feld-Mappings

| | | | |
| :--- | :--- | :--- | :--- |
| `KBVPRFOROrganization.identifier` | `OrganizationDirectory.identifier` | Nicht Übertragen | Feld wird nicht gemappt | Quelle: Organization.identifier:Standortnummer |
| `KBVPRFOROrganization` | `OrganizationDirectory.identifier.assigner` | Nicht Übertragen | Feld wird nicht gemappt | Inherited from Organization.identifier:Standortnummer | Quelle: Organization.identifier:Standortnummer.assigner |
| `KBVPRFOROrganization.identifier.id` | `OrganizationDirectory.identifier.id` | Nicht Übertragen | Feld wird nicht gemappt | Inherited from Organization.identifier:Standortnummer | Quelle: Organization.identifier:Standortnummer.id |
| `KBVPRFOROrganization` | `OrganizationDirectory.identifier.period` | Nicht Übertragen | Feld wird nicht gemappt | Inherited from Organization.identifier:Standortnummer | Quelle: Organization.identifier:Standortnummer.period |
| `KBVPRFOROrganization.identifier.system` | `OrganizationDirectory.identifier.system` | Nicht Übertragen | Feld wird nicht gemappt | Inherited from Organization.identifier:Standortnummer | Quelle: Organization.identifier:Standortnummer.system |
| `KBVPRFOROrganization.identifier.type` | `OrganizationDirectory.identifier.type` | Nicht Übertragen | Feld wird nicht gemappt | Inherited from Organization.identifier:Standortnummer | Quelle: Organization.identifier:Standortnummer.type |
| `KBVPRFOROrganization.identifier.type.coding` | `OrganizationDirectory.identifier.type.coding` | Nicht Übertragen | Feld wird nicht gemappt | Inherited from Organization.identifier:Standortnummer.type | Quelle: Organization.identifier:Standortnummer.type.coding |
| `KBVPRFOROrganization.identifier.type.coding.code` | `OrganizationDirectory.identifier.type.coding.code` | Nicht Übertragen | Feld wird nicht gemappt | Inherited from Organization.identifier:Standortnummer.type.coding | Quelle: Organization.identifier:Standortnummer.type.coding.code |
| `KBVPRFOROrganization` | `OrganizationDirectory.identifier.type.coding.display` | Nicht Übertragen | Feld wird nicht gemappt | Inherited from Organization.identifier:Standortnummer.type.coding | Quelle: Organization.identifier:Standortnummer.type.coding.display |
| `KBVPRFOROrganization.identifier.type.coding.id` | `OrganizationDirectory.identifier.type.coding.id` | Nicht Übertragen | Feld wird nicht gemappt | Inherited from Organization.identifier:Standortnummer.type.coding | Quelle: Organization.identifier:Standortnummer.type.coding.id |
| `KBVPRFOROrganization.identifier.type.coding.system` | `OrganizationDirectory.identifier.type.coding.system` | Nicht Übertragen | Feld wird nicht gemappt | Inherited from Organization.identifier:Standortnummer.type.coding | Quelle: Organization.identifier:Standortnummer.type.coding.system |
| `KBVPRFOROrganization` | `OrganizationDirectory.identifier.type.coding.userSelected` | Nicht Übertragen | Feld wird nicht gemappt | Inherited from Organization.identifier:Standortnummer.type.coding | Quelle: Organization.identifier:Standortnummer.type.coding.userSelected |
| `KBVPRFOROrganization` | `OrganizationDirectory.identifier.type.coding.version` | Nicht Übertragen | Feld wird nicht gemappt | Inherited from Organization.identifier:Standortnummer.type.coding | Quelle: Organization.identifier:Standortnummer.type.coding.version |
| `KBVPRFOROrganization.identifier.type.id` | `OrganizationDirectory.identifier.type.id` | Nicht Übertragen | Feld wird nicht gemappt | Inherited from Organization.identifier:Standortnummer.type | Quelle: Organization.identifier:Standortnummer.type.id |
| `KBVPRFOROrganization` | `OrganizationDirectory.identifier.type.text` | Nicht Übertragen | Feld wird nicht gemappt | Inherited from Organization.identifier:Standortnummer.type | Quelle: Organization.identifier:Standortnummer.type.text |
| `KBVPRFOROrganization.identifier.use` | `OrganizationDirectory.identifier.use` | Nicht Übertragen | Feld wird nicht gemappt | Inherited from Organization.identifier:Standortnummer | Quelle: Organization.identifier:Standortnummer.use |
| `KBVPRFOROrganization.identifier.value` | `OrganizationDirectory.identifier.value` | Nicht Übertragen | Feld wird nicht gemappt | Inherited from Organization.identifier:Standortnummer | Quelle: Organization.identifier:Standortnummer.value |
| `KBVPRFOROrganization.identifier` | `OrganizationDirectory.identifier` | Nicht Übertragen | Feld wird nicht gemappt | Quelle: Organization.identifier:Telematik-ID |
| `KBVPRFOROrganization` | `OrganizationDirectory.identifier.assigner` | Nicht Übertragen | Feld wird nicht gemappt | Inherited from Organization.identifier:Telematik-ID | Quelle: Organization.identifier:Telematik-ID.assigner |
| `KBVPRFOROrganization.identifier.id` | `OrganizationDirectory.identifier.id` | Nicht Übertragen | Feld wird nicht gemappt | Inherited from Organization.identifier:Telematik-ID | Quelle: Organization.identifier:Telematik-ID.id |
| `KBVPRFOROrganization` | `OrganizationDirectory.identifier.period` | Nicht Übertragen | Feld wird nicht gemappt | Inherited from Organization.identifier:Telematik-ID | Quelle: Organization.identifier:Telematik-ID.period |
| `KBVPRFOROrganization.identifier.system` | `OrganizationDirectory.identifier.system` | Nicht Übertragen | Feld wird nicht gemappt | Inherited from Organization.identifier:Telematik-ID | Quelle: Organization.identifier:Telematik-ID.system |
| `KBVPRFOROrganization.identifier.type` | `OrganizationDirectory.identifier.type` | Nicht Übertragen | Feld wird nicht gemappt | Inherited from Organization.identifier:Telematik-ID | Quelle: Organization.identifier:Telematik-ID.type |
| `KBVPRFOROrganization.identifier.type.coding` | `OrganizationDirectory.identifier.type.coding` | Nicht Übertragen | Feld wird nicht gemappt | Inherited from Organization.identifier:Telematik-ID.type | Quelle: Organization.identifier:Telematik-ID.type.coding |
| `KBVPRFOROrganization.identifier.type.coding.code` | `OrganizationDirectory.identifier.type.coding.code` | Nicht Übertragen | Feld wird nicht gemappt | Inherited from Organization.identifier:Telematik-ID.type.coding | Quelle: Organization.identifier:Telematik-ID.type.coding.code |
| `KBVPRFOROrganization` | `OrganizationDirectory.identifier.type.coding.display` | Nicht Übertragen | Feld wird nicht gemappt | Inherited from Organization.identifier:Telematik-ID.type.coding | Quelle: Organization.identifier:Telematik-ID.type.coding.display |
| `KBVPRFOROrganization.identifier.type.coding.id` | `OrganizationDirectory.identifier.type.coding.id` | Nicht Übertragen | Feld wird nicht gemappt | Inherited from Organization.identifier:Telematik-ID.type.coding | Quelle: Organization.identifier:Telematik-ID.type.coding.id |
| `KBVPRFOROrganization.identifier.type.coding.system` | `OrganizationDirectory.identifier.type.coding.system` | Nicht Übertragen | Feld wird nicht gemappt | Inherited from Organization.identifier:Telematik-ID.type.coding | Quelle: Organization.identifier:Telematik-ID.type.coding.system |
| `KBVPRFOROrganization` | `OrganizationDirectory.identifier.type.coding.userSelected` | Nicht Übertragen | Feld wird nicht gemappt | Inherited from Organization.identifier:Telematik-ID.type.coding | Quelle: Organization.identifier:Telematik-ID.type.coding.userSelected |
| `KBVPRFOROrganization` | `OrganizationDirectory.identifier.type.coding.version` | Nicht Übertragen | Feld wird nicht gemappt | Inherited from Organization.identifier:Telematik-ID.type.coding | Quelle: Organization.identifier:Telematik-ID.type.coding.version |
| `KBVPRFOROrganization.identifier.type.id` | `OrganizationDirectory.identifier.type.id` | Nicht Übertragen | Feld wird nicht gemappt | Inherited from Organization.identifier:Telematik-ID.type | Quelle: Organization.identifier:Telematik-ID.type.id |
| `KBVPRFOROrganization` | `OrganizationDirectory.identifier.type.text` | Nicht Übertragen | Feld wird nicht gemappt | Inherited from Organization.identifier:Telematik-ID.type | Quelle: Organization.identifier:Telematik-ID.type.text |
| `KBVPRFOROrganization.identifier.use` | `OrganizationDirectory.identifier.use` | Nicht Übertragen | Feld wird nicht gemappt | Inherited from Organization.identifier:Telematik-ID | Quelle: Organization.identifier:Telematik-ID.use |
| `KBVPRFOROrganization.identifier.value` | `OrganizationDirectory.identifier.value` | Nicht Übertragen | Feld wird nicht gemappt | Inherited from Organization.identifier:Telematik-ID | Quelle: Organization.identifier:Telematik-ID.value |
| `KBVPRFOROrganization` | `OrganizationDirectory.identifier` | Manuell | Telematik-ID wird aus idNummer → aus dem ACCESS_TOKEN der Anfrage bezogen | Quelle: Organization.identifier:TelematikID |
| `KBVPRFOROrganization.meta` | `OrganizationDirectory.meta.profile` | Fester Wert | setzt festen Wert:`https://gematik.de/fhir/directory/StructureDefinition/OrganizationDirectory` |
| `KBVPRFOROrganization.name` | `OrganizationDirectory.name` | Manuell | organizationName → aus dem ACCESS_TOKEN der Anfrage beziehen | Quelle: Organization.name |
| `KBVPRFOROrganization` | `OrganizationDirectory.type` | Manuell | professionOID → aus dem ACCESS_TOKEN der Anfrage | Quelle: Organization.type:profession |

### Extensions

#### Extension: (ohne Bedingung)

| | | | |
| :--- | :--- | :--- | :--- |
| `KBVPRFOROrganization.identifier.extension` | `OrganizationDirectory.identifier.extension` | Nicht Übertragen | Feld wird nicht gemappt | Inherited from Organization.identifier:Standortnummer | Quelle: Organization.identifier:Standortnummer.extension |
| `KBVPRFOROrganization.identifier.type.coding.extension` | `OrganizationDirectory.identifier.type.coding.extension` | Nicht Übertragen | Feld wird nicht gemappt | Inherited from Organization.identifier:Standortnummer.type.coding | Quelle: Organization.identifier:Standortnummer.type.coding.extension |
| `KBVPRFOROrganization.identifier.type.extension` | `OrganizationDirectory.identifier.type.extension` | Nicht Übertragen | Feld wird nicht gemappt | Inherited from Organization.identifier:Standortnummer.type | Quelle: Organization.identifier:Standortnummer.type.extension |
| `KBVPRFOROrganization.identifier.extension` | `OrganizationDirectory.identifier.extension` | Nicht Übertragen | Feld wird nicht gemappt | Inherited from Organization.identifier:Telematik-ID | Quelle: Organization.identifier:Telematik-ID.extension |
| `KBVPRFOROrganization.identifier.type.coding.extension` | `OrganizationDirectory.identifier.type.coding.extension` | Nicht Übertragen | Feld wird nicht gemappt | Inherited from Organization.identifier:Telematik-ID.type.coding | Quelle: Organization.identifier:Telematik-ID.type.coding.extension |
| `KBVPRFOROrganization.identifier.type.extension` | `OrganizationDirectory.identifier.type.extension` | Nicht Übertragen | Feld wird nicht gemappt | Inherited from Organization.identifier:Telematik-ID.type | Quelle: Organization.identifier:Telematik-ID.type.extension |

## Transformationsregeln

Folgende zusätzliche Anmerkungen und Regeln sind für das Mapping zu umzusetzen:

#### Organization für provide Prescription

* ID: Beschreibung
  * `F_006b`: Bei provide Prescription ist die Organization aus der KBV_PR_FOR_Organization zu mappen.Der Transformator muss sicherstellen, dass bei Organization.identifier mindestens die TelematikID der Organisation enthalten, die auch im ACCESS_TOKEN der Anfrage angegeben ist. Dazu muss nach der A_25946 die TelematikId bei “identifier:TelematikID” durch die idNummer aus dem ACCESS_TOKEN des verwendeten Operationsaufrufes ersetzt werden bzw. erzeugt werden, wenn diese nicht vorhanden ist.Folgende Operationen sind zusätzlich zum Mapping der StructureMaps durchzuführen:Organization.identifier:TelematikID idNummer → aus dem ACCESS_TOKEN der AnfrageOrganization.name organizationName → aus dem ACCESS_TOKEN der AnfrageOrganization.type:profession professionOID → aus dem ACCESS_TOKEN der Anfrage
* ID: Profile
  * `F_006b`: * [OrganizationDirectory](https://simplifier.net/vzd-fhir-directory/organizationdirectorystrict)

* ID: Referenzen
  * `F_006b`: * [A_25946 - E-Rezept-Fachdienst - ePA - Mapping](https://gemspec.gematik.de/docs/gemF/gemF_eRp_ePA/gemF_eRp_ePA_V1.2.1/#A_25946)


#### Address Slices in Organization

* ID: Beschreibung
  * `F_007`: Beim Mapping der Organization bei providePrescription (siehe 006b) sollen die Extensions der Adresse:* Organization.address:Strassenanschrift.line.extension:Adresszusatz
* Organization.address:Strassenanschrift.line.extension:Hausnummer
* Organization.address:Strassenanschrift.line.extension:Strasse in das OpenSlicing des Organization-Profils des VZD übernommen werden, auch wenn diese nicht explizit dort modelliert sind.

* ID: Profile
  * `F_007`: * [KBV_PR_FOR_Organization](https://simplifier.net/for/kbv_pr_for_organization)
* [OrganizationDirectory](https://simplifier.net/vzd-fhir-directory/organizationdirectorystrict)

* ID: Referenzen
  * `F_007`: * [2024.05.28 - ePa Medikationsliste: Austausch IBM und PT Medical](https://wiki.gematik.de/display/ERPCHANGES/2024.05.28+-+ePa+Medikationsliste%3A+Austausch+IBM+und+PT+Medical)


