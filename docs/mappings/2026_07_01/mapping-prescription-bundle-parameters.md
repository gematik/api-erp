# Mapping des Bundles zu Parameters für Verordnungsdaten - Implementation Guide E-Rezept-Fachdienst v1.6.1-draft

Implementation Guide

E-Rezept-Fachdienst

Version 1.6.1-draft - ci-build 

* [**Table of Contents**](toc.md)
* [**Vorgaben zum Mapping von FHIR-Instanzen**](mapping.md)
* [**Mapping von Verordnungsdaten**](mapping-prescription.md)
* **Mapping des Bundles zu Parameters für Verordnungsdaten**

## Mapping des Bundles zu Parameters für Verordnungsdaten

Diese Seite beschreibt Anforderungen und Umsetzungsunterstützung für das Mapping vom

* [KBV_ERP_PR_Bundle](https://simplifier.net/packages/kbv.ita.erp/1.4.0/files/3113155)
* zum [EPAOpProvidePrescriptionERPInputParameters](https://gemspec.gematik.de/ig/fhir/epa-medication/1.3.0/StructureDefinition-epa-op-provide-prescription-erp-input-parameters.html).

## Wichtige Punkte beim Mapping

Die folgenden Punkte sind relevant für das Mapping der Bundle Ressource:

* Parameters.prescriptionId wird aus der Bundle.identifier.value übernommen
* Parameters.authoredOn wird aus MedicationRequest.authoredOn übernommen
* Die Ressourcen werden entsprechend der Mappings der jeweiligen Ressource gemappt

## Generelles Mapping des Profils

Die folgende Tabelle stellt generell das Mapping der beiden Profile gegenüber:

### Feld-Mappings

| | | | |
| :--- | :--- | :--- | :--- |
| `KBVPRERPBundle` | `EPAOpProvidePrescriptionERPInputParameters.parameter.name` | Fester Wert | setzt festen Wert:`rxPrescription` |
| `KBVPRERPBundle` | `EPAOpProvidePrescriptionERPInputParameters.parameter.part.name` | Fester Wert | setzt festen Wert:`authoredOn` |
| `KBVPRERPBundle.entry.resource.authoredOn``[Bedingung: resource.meta.profile.where($this.contains('https://fhir.kbv.de/StructureDefinition/KBV_PR_ERP_Prescription')).exists()]` | `EPAOpProvidePrescriptionERPInputParameters.parameter.part.value` | Kopiert | übernimmt Wert aus Quellvariable |
| `KBVPRERPBundle` | `EPAOpProvidePrescriptionERPInputParameters.parameter.part.name` | Fester Wert | setzt festen Wert:`medication` |
| `KBVPRERPBundle.entry``[Bedingung: resource is Medication]` | — | Dokumentiert | Bundle.entry:RezeptierdatenPZNVerordnung.resource -> .parameter:rxPrescription.part:medication.resource using KBV_PR_ERP_Medication_PZN|1.4.0 -> EPAMedication|1.3.0 |
| `KBVPRERPBundle.entry.resource``[Bedingung: resource is Medication]` | `EPAOpProvidePrescriptionERPInputParameters.parameter.part.resource` | Erstellt · Delegiert | Verwendet StructureMap:[KBVPrErpMedicationPznMap](./StructureMap-KBVPrErpMedicationPznMap.md)Ressource: Medicationerstellt neues https://gematik.de/fhir/epa-medication/StructureDefinition/epa-medication |
| `KBVPRERPBundle.entry``[Bedingung: resource is Medication]` | — | Dokumentiert | Bundle.entry:RezeptierdatenWirkstoffverordnung.resource -> .parameter:rxPrescription.part:medication.resource using KBV_PR_ERP_Medication_Ingredient|1.4.0 -> EPAMedication|1.3.0 |
| `KBVPRERPBundle.entry.resource``[Bedingung: resource is Medication]` | `EPAOpProvidePrescriptionERPInputParameters.parameter.part.resource` | Erstellt · Delegiert | Verwendet StructureMap:[KBVPrErpMedicationIngredientMap](./StructureMap-KBVPrErpMedicationIngredientMap.md)Ressource: Medicationerstellt neues https://gematik.de/fhir/epa-medication/StructureDefinition/epa-medication |
| `KBVPRERPBundle.entry``[Bedingung: resource is Medication]` | — | Dokumentiert | Bundle.entry:RezeptierdatenRezepturverordnung.resource -> .parameter:rxPrescription.part:medication.resource using KBV_PR_ERP_Medication_Compounding|1.4.0 -> EPAMedication|1.3.0 |
| `KBVPRERPBundle.entry.resource``[Bedingung: resource is Medication]` | `EPAOpProvidePrescriptionERPInputParameters.parameter.part.resource` | Erstellt · Delegiert | Verwendet StructureMap:[KBVPrErpMedicationCompoundingMap](./StructureMap-KBVPrErpMedicationCompoundingMap.md)Ressource: Medicationerstellt neues https://gematik.de/fhir/epa-medication/StructureDefinition/epa-medication |
| `KBVPRERPBundle.entry``[Bedingung: resource is Medication]` | — | Dokumentiert | Bundle.entry:RezeptierdatenFreitextverordnung.resource -> .parameter:rxPrescription.part:medication.resource using KBV_PR_ERP_Medication_FreeText|1.4.0 -> EPAMedication|1.3.0 |
| `KBVPRERPBundle.entry.resource``[Bedingung: resource is Medication]` | `EPAOpProvidePrescriptionERPInputParameters.parameter.part.resource` | Erstellt · Delegiert | Verwendet StructureMap:[KBVPrErpMedicationFreetextMap](./StructureMap-KBVPrErpMedicationFreetextMap.md)Ressource: Medicationerstellt neues https://gematik.de/fhir/epa-medication/StructureDefinition/epa-medication |
| `KBVPRERPBundle` | `EPAOpProvidePrescriptionERPInputParameters.parameter.part.name` | Fester Wert | setzt festen Wert:`medicationRequest` |
| `KBVPRERPBundle.entry``[Bedingung: resource is MedicationRequest]` | — | Dokumentiert | Bundle.entry:VerordnungArzneimittel.resource -> .parameter:rxPrescription.part:medicationRequest.resource using KBV_PR_ERP_Prescription|1.4.0 -> EPAMedicationRequest|1.3.0 |
| `KBVPRERPBundle.entry.resource``[Bedingung: resource is MedicationRequest]` | `EPAOpProvidePrescriptionERPInputParameters.parameter.part.resource` | Erstellt · Delegiert | Verwendet StructureMap:[KBVPrErpPrescriptionMap](./StructureMap-KBVPrErpPrescriptionMap.md)Ressource: MedicationRequesterstellt neues https://gematik.de/fhir/epa-medication/StructureDefinition/epa-medication-request |
| `KBVPRERPBundle` | `EPAOpProvidePrescriptionERPInputParameters.parameter.part.name` | Fester Wert | setzt festen Wert:`organization` |
| `KBVPRERPBundle.entry``[Bedingung: resource is Organization]` | — | Dokumentiert | Bundle.entry:Einrichtung.resource -> .parameter:rxPrescription.part:organization.resource using KBV_PR_FOR_Organization|1.3.0 -> OrganizationDirectory|1.0.0 |
| `KBVPRERPBundle.entry.resource``[Bedingung: resource is Organization]` | `EPAOpProvidePrescriptionERPInputParameters.parameter.part.resource` | Erstellt · Delegiert | Verwendet StructureMap:[KBVPrForOrganizationMap](./StructureMap-KBVPrForOrganizationMap.md)Ressource: Organizationerstellt neues https://gematik.de/fhir/directory/StructureDefinition/OrganizationDirectory |
| `KBVPRERPBundle` | `EPAOpProvidePrescriptionERPInputParameters.parameter.part.name` | Fester Wert | setzt festen Wert:`practitioner` |
| `KBVPRERPBundle.entry``[Bedingung: resource is Practitioner]` | — | Dokumentiert | Bundle.entry:AusstellendeVerschreibendeVerantwortlichePerson.resource -> .parameter:rxPrescription.part:practitioner.resource using KBV_PR_FOR_Practitioner|1.3.0 -> PractitionerDirectory|1.0.0 |
| `KBVPRERPBundle.entry.resource``[Bedingung: resource is Practitioner]` | `EPAOpProvidePrescriptionERPInputParameters.parameter.part.resource` | Erstellt · Delegiert | Verwendet StructureMap:[KBVPrForPractitionerMap](./StructureMap-KBVPrForPractitionerMap.md)Ressource: Practitionererstellt neues https://gematik.de/fhir/directory/StructureDefinition/PractitionerDirectory |
| `KBVPRERPBundle` | `EPAOpProvidePrescriptionERPInputParameters.parameter.part.name` | Fester Wert | setzt festen Wert:`prescriptionId` |
| `KBVPRERPBundle.identifier.value` | `EPAOpProvidePrescriptionERPInputParameters.parameter.part.value` | Kopiert | übernimmt Wert aus Quellvariable |

## Transformationsregeln

Folgende zusätzliche Anmerkungen und Regeln sind für das Mapping zu umzusetzen:

### Mapping des korrekten Practitioners

* ID: Beschreibung
  * `F_016`: Im https://simplifier.net/erezept/kbv_pr_erp_bundle sind zwei Practitioner erlaubt (AusstellendeVerschreibendeVerantwortlichePerson). Beim Mapping für provide-prescription muss der Practitioner übernommen werden, welcher in der Composition (https://simplifier.net/erezept/kbvprerpcomposition) unter “author” referenziert wird:```
  <author> 
    <reference value="Practitioner/667ffd79-42a3-4002-b7ca-6b9098f20ccb"/> 
    <type value="Practitioner"/> 
  </author> 
  <attester> 
    <mode value="legal"/> 
    <party> 
      <reference value="Practitioner/d6f3b55d-3095-4655-96dc-da3bec21271c"/> 
    </party> 
  </attester>

```

* ID: Profile
  * `F_016`: * [KBV_PR_ERP_Bundle](https://simplifier.net/erezept/kbv_pr_erp_bundle)
* [EPAOpProvidePrescriptionERPInputParameters](https://gemspec.gematik.de/ig/fhir/epa-medication/{{ site.data.constants.epa_med_service_version }}/StructureDefinition-epa-op-provide-prescription-erp-input-parameters.md)
* [KBV_PR_FOR_Practitioner](https://simplifier.net/for/kbv_pr_for_practitioner)
* [PractitionerDirectory](https://simplifier.net/vzd-fhir-directory/practitionerdirectorystrict)

* ID: Referenzen
  * `F_016`: * [ANFERP-2780](https://service.gematik.de/browse/ANFERP-2780)


