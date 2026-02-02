# Mapping der Arzneimitteldaten für Verordnungsdaten - Implementation Guide E-Rezept-Fachdienst v1.6.1-draft

Implementation Guide

E-Rezept-Fachdienst

Version 1.6.1-draft - ci-build 

* [**Table of Contents**](toc.md)
* [**Vorgaben zum Mapping von FHIR-Instanzen**](mapping.md)
* [**Mapping von Verordnungsdaten**](mapping-prescription.md)
* **Mapping der Arzneimitteldaten für Verordnungsdaten**

## Mapping der Arzneimitteldaten für Verordnungsdaten

Diese Seite beschreibt Anforderungen und Umsetzungsunterstützung für das Mapping von

* KBV Medication (aus dem [KBV_PR_ERP_Bundle](https://simplifier.net/erezept/kbv_pr_erp_bundle))
* zur [EPA Medication](https://gemspec.gematik.de/ig/fhir/epa-medication/1.3.0/StructureDefinition-epa-medication.html).

## Wichtige Punkte beim Mapping der Medication Ressource

Die folgenden Punkte sind relevant für das Mapping der Medication Ressource:

* Bei Rezepturen mit PZN-codierten Wirkstoffen sind zusätzliche `contained` Medications anzulegen und in `Medication.ingredient.itemReference` zu referenzieren (F_017)
* `Medication.extension:type` soll nach Möglichkeit erzeugt und korrekt belegt werden (F_020)

## Generelles Mapping des Profils

Die folgende Tabelle stellt generell das Mapping der beiden Profile gegenüber:

**Titel:** EPAMedication-Map

| | | | | | |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Beschreibung:**Router StructureMap for KBV_PR_ERP_Medication_Compounding | 1.3.2, KBV_PR_ERP_Medication_FreeText | 1.3.2, KBV_PR_ERP_Medication_Ingredient | 1.3.2, KBV_PR_ERP_Medication_PZN | 1.3.2 -> EPAMedication | 1.0.6-2 |

| | | |
| :--- | :--- | :--- |
| `KBVPRERPMedicationCompounding [Bedingung: meta.profile.exists(p | p = 'https://fhir.kbv.de/StructureDefinition/KBV_PR_ERP_Medication_Compounding')]` | **(wird bestimmt durch Kontext)** | Routes resources constrained by KBV_PR_ERP_Medication_Compounding |
| `KBVPRERPMedicationCompounding [Bedingung: meta.profile.exists(p | p = 'https://fhir.kbv.de/StructureDefinition/KBV_PR_ERP_Medication_Compounding')].KBVPRERPMedicationCompoundingKbvPrErpMedicationCompoundingRouted` | **(wird bestimmt durch Kontext)** | Verwendet Mapping:[KBV-PR-ERP-Medication-Compounding-Map](./StructureMap-KBV-PR-ERP-Medication-Compounding-Map.md) |
| `KBVPRERPMedicationCompounding [Bedingung: meta.profile.exists(p | p = 'https://fhir.kbv.de/StructureDefinition/KBV_PR_ERP_Medication_FreeText')]` | **(wird bestimmt durch Kontext)** | Routes resources constrained by KBV_PR_ERP_Medication_FreeText |
| `KBVPRERPMedicationCompounding [Bedingung: meta.profile.exists(p | p = 'https://fhir.kbv.de/StructureDefinition/KBV_PR_ERP_Medication_FreeText')].KBVPRERPMedicationCompoundingKbvPrErpMedicationFreetextRouted` | **(wird bestimmt durch Kontext)** | Verwendet Mapping:[KBV-PR-ERP-Medication-FreeText-Map](./StructureMap-KBV-PR-ERP-Medication-FreeText-Map.md) |
| `KBVPRERPMedicationCompounding [Bedingung: meta.profile.exists(p | p = 'https://fhir.kbv.de/StructureDefinition/KBV_PR_ERP_Medication_Ingredient')]` | **(wird bestimmt durch Kontext)** | Routes resources constrained by KBV_PR_ERP_Medication_Ingredient |
| `KBVPRERPMedicationCompounding [Bedingung: meta.profile.exists(p | p = 'https://fhir.kbv.de/StructureDefinition/KBV_PR_ERP_Medication_Ingredient')].KBVPRERPMedicationCompoundingKbvPrErpMedicationIngredientRouted` | **(wird bestimmt durch Kontext)** | Verwendet Mapping:[KBV-PR-ERP-Medication-Ingredient-Map](./StructureMap-KBV-PR-ERP-Medication-Ingredient-Map.md) |
| `KBVPRERPMedicationCompounding [Bedingung: meta.profile.exists(p | p = 'https://fhir.kbv.de/StructureDefinition/KBV_PR_ERP_Medication_PZN')]` | **(wird bestimmt durch Kontext)** | Routes resources constrained by KBV_PR_ERP_Medication_PZN |
| `KBVPRERPMedicationCompounding [Bedingung: meta.profile.exists(p | p = 'https://fhir.kbv.de/StructureDefinition/KBV_PR_ERP_Medication_PZN')].KBVPRERPMedicationCompoundingKbvPrErpMedicationPznRouted` | **(wird bestimmt durch Kontext)** | Verwendet Mapping:[KBV-PR-ERP-Medication-PZN-Map](./StructureMap-KBV-PR-ERP-Medication-PZN-Map.md) |

Die folgenden Unterseiten beschreiben die Mappings der verschiedenen KBV-Medication-Profile zu EPA Medication im Detail:

* [Mapping der PZN Medication](./mapping-prescription-medication-pzn.md)
* [Mapping der Wirkstoff Medication](./mapping-prescription-medication-ingredient.md)
* [Mapping der Rezeptur Medication](./mapping-prescription-medication-compounding.md)
* [Mapping der Freitext Medication](./mapping-prescription-medication-freetext.md)

## Transformationsregeln

Folgende zusätzliche Anmerkungen und Regeln sind für das Mapping zu umzusetzen:

### Mapping von KBV_PR_ERP_Medication_Compounding

* ID: Beschreibung
  * `F_017`: Handelt es sich bei der ingredient des QuellProfils um einen PZN Codierten Wirkstoff muss eine contained Medication vom Typ “EPA Medication Ingredient” hinzugefügt werden**Hinweis**: F_009 findet hier auch AnwendungDaher muss wenn Medication eine KBV_PR_ERP_Medication_Compounding ist:Für jedes ingredient:1. Wenn ingredient.itemCodeableConcept.coding.system=`http://fhir.de/CodeSystem/ifa/pzn`dann weiter zu 2.
1. Füge eine Medication (contained) hinzu vom Typ “EPA Medication Ingredient”:
```
  <Medication>
      <id value="MedicationHydrocortison-FD" />
      <meta>
          <profile value="https://gematik.de/fhir/epa-medication/StructureDefinition/epa-medication-pzn-ingredient" />
      </meta>
      <!-- "EPA Medication Ingredients" haben haben immer diese Extension -->
      <extension url="https://gematik.de/fhir/epa-medication/StructureDefinition/epa-medication-type-extension">
          <valueCoding>
              <system value="http://snomed.info/sct" />
              <version value="http://snomed.info/sct/900000000000207008/version/20240201" />
              <code value="781405001" />    
              <display value="Medicinal product package (product)" />
          </valueCoding>
      </extension>
      <code>
          <coding>
              <system value="http://fhir.de/CodeSystem/ifa/pzn" />
              <code value="03424249" />                       <!-- Wert von ingredient.itemCodeableConcept.coding.code -->
              <display value="Hydrocortison 1% Creme" />      <!-- Wert von ingredient.itemCodeableConcept.text -->
          </coding>
          <text value="Hydrocortison 1% Creme" />             <!-- Wert von ingredient.itemCodeableConcept.text -->
      </code>
  </Medication>

```
1. In der Ziel Medication.ingredient setze die itemReference:
```
<itemReference>
    <reference value="#MedicationHydrocortison-FD" />
</itemReference>

```
**Hinweise:**“EPA Medication Ingredients” haben haben immer die Extension:```
  <extension url="https://gematik.de/fhir/epa-medication/StructureDefinition/epa-medication-type-extension">
    <valueCoding>
        <system value="http://snomed.info/sct" />
        <version value="http://snomed.info/sct/900000000000207008/version/20240201" />
        <code value="781405001" />    
        <display value="Medicinal product package (product)" />            
    </valueCoding>
  </extension>

```
Die Werte in der EPA Medication Ingredients für `<code>` werden wie folgt gesetzt* code: Wert von ingredient.itemCodeableConcept.coding.code
* display: Wert von ingredient.itemCodeableConcept.text
* text: Wert von ingredient.itemCodeableConcept.text

* ID: Profile
  * `F_017`: * [EPA Medication](https://gemspec.gematik.de/ig/fhir/epa-medication/{{ site.data.constants.epa_med_service_version }}/StructureDefinition-epa-medication.md)
* [EPA Medication Ingredient](https://gemspec.gematik.de/ig/fhir/epa-medication/{{ site.data.constants.epa_med_service_version }}/StructureDefinition-epa-medication-pzn-ingredient.md)
* [EPA Pharmaceutical Product Medication](https://gemspec.gematik.de/ig/fhir/epa-medication/{{ site.data.constants.epa_med_service_version }}/StructureDefinition-epa-medication-pharmaceutical-product.md)

* ID: Referenzen
  * `F_017`: * [ANFERP-2911](https://service.gematik.de/browse/ANFERP-2911)


### Erzeugen von Medication.extension:type

* ID: Beschreibung
  * `F_020`: Bei der Erzeugung von* EPA Medication
* EPA Medication Ingredient
* EPA Pharmaceutical Product Medication
soll nach Möglichkeit `Medication.extension:type` erzeugt und mit dem korrekten Wert belegt werden.Folgende Optionen stehen für ePA 3.0 zur Verfügung (s. EPAMedicationTypeVS):
| | | |
| :--- | :--- | :--- |
| 781405001 | Medicinal product package (product) | Fertigarzneimittel |
| 1208954007 | Extemporaneous preparation (product) | Rezeptur |
| 373873005 | Pharmaceutical / biologic product (product) | Komponente einer Kombipackung |
Für folgende Konstellationen sind die Codes entsprechend zu setzen:
| | | | | | | |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | PZN Verordnung | `KBV_PR_ERP_Medication_PZN` | `.form.code != KPG` | **Fertigarzneimittel**(`781405001`,**Medicinal product package (product)**) | n/a | n/a |
| 2 | PZN Verordnung einer Kombipackung | `KBV_PR_ERP_Medication_PZN` | `.form.code = KPG` | Extension nicht setzen (wird über`.form.code`erkannt) | n/a | n/a |
| 3 | Wirkstoffverordnung | `KBV_PR_ERP_Medication_Ingredient` | — | **Fertigarzneimittel**(`781405001`,**Medicinal product package (product)**) | n/a | n/a |
| 4 | Freitextverordnung | `KBV_PR_ERP_Medication_FreeText` | — | Extension nicht setzen | n/a | n/a |
| 5 | Rezeptur ohne PZNs in Rezepturbestandteilen | `KBV_PR_ERP_Medication_Compounding` | `.ingredient.itemCodeableConcept.text` | **Rezeptur**(`1208954007`,**Extemporaneous preparation (product)**) | n/a | n/a |
| 6 | Rezeptur mit PZNs in Rezepturbestandteilen | `KBV_PR_ERP_Medication_Compounding` | `.ingredient.itemCodeableConcept.coding.code:pzn` | **Rezeptur**(`1208954007`,**Extemporaneous preparation (product)**) | **Fertigarzneimittel**(`781405001`,**Medicinal product package (product)**) | n/a |

* ID: Profile
  * `F_020`: * [EPA Medication](https://gemspec.gematik.de/ig/fhir/epa-medication/{{ site.data.constants.epa_med_service_version }}/StructureDefinition-epa-medication.md)
* [EPA Medication Ingredient](https://gemspec.gematik.de/ig/fhir/epa-medication/{{ site.data.constants.epa_med_service_version }}/StructureDefinition-epa-medication-pzn-ingredient.md)
* [EPA Pharmaceutical Product Medication](https://gemspec.gematik.de/ig/fhir/epa-medication/{{ site.data.constants.epa_med_service_version }}/StructureDefinition-epa-medication-pharmaceutical-product.md)


