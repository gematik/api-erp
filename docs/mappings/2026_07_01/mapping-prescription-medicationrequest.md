# Mapping der Verschreibung für Verordnungsdaten am E-Rezept-Fachdienst ab dem 01.07.2026


* [**Table of Contents**](toc.md)
* [**Vorgaben zum Mapping von FHIR-Instanzen**](mapping.md)
* [**Mapping von Verordnungsdaten**](mapping-prescription.md)
* **Mapping der Verschreibung für Verordnungsdaten**

## Mapping der Verschreibung für Verordnungsdaten

Diese Seite beschreibt Anforderungen und Umsetzungsunterstützung für das Mapping von

* KBV MedicationRequest (aus dem [KBV_PR_ERP_Bundle](https://simplifier.net/erezept/kbv_pr_erp_bundle))
* zur [EPA MedicationRequest](https://gemspec.gematik.de/ig/fhir/epa-medication/1.3.0/StructureDefinition-epa-medication-request.html).

## Wichtige Punkte beim Mapping der MedicationRequest Ressource

Die folgenden Punkte sind relevant für das Mapping der MedicationRequest Ressource:

* `MedicationRequest.subject.identifier` wird aus der Patienten-KVNR befüllt (F_010)

## Generelles Mapping des Profils

Die folgende Tabelle stellt generell das Mapping der beiden Profile gegenüber:

### Feld-Mappings

| | | | |
| :--- | :--- | :--- | :--- |
| `KBVPRERPPrescription.meta` | `EPAMedicationRequest.meta.profile` | Fester Wert | setzt festen Wert:`https://gematik.de/fhir/epa-medication/StructureDefinition/epa-medication-request` |
| `KBVPRERPPrescription.subject` | `EPAMedicationRequest.subject` | Manuell | Transformationsregel F_007: Wird aus KBV_PR_FOR_Patient.identifier:versichertenId übernommen. | Quelle: MedicationRequest.subject |
| `KBVPRERPPrescription` | `EPAMedicationRequest.subject.identifier` | Manuell | Befüllen von .subject nach Transformationsregel F_010 | Quelle: MedicationRequest.subject.identifier |

### Extensions

#### Extension: KBV_EX_FOR_SER

Bedingung: url = `https://fhir.kbv.de/StructureDefinition/KBV_EX_FOR_SER`

| | | | |
| :--- | :--- | :--- | :--- |
| `KBVPRERPPrescription.extension``[Bedingung: url = 'https://fhir.kbv.de/StructureDefinition/KBV_EX_FOR_SER']` | `EPAMedicationRequest.extension.url` | Fester Wert | setzt festen Wert:`https://gematik.de/fhir/epa-medication/StructureDefinition/indicator-ser-extension` |

#### Extension: KBV_EX_ERP_Multiple_Prescription

Bedingung: url = `https://fhir.kbv.de/StructureDefinition/KBV_EX_ERP_Multiple_Prescription`

| | | | |
| :--- | :--- | :--- | :--- |
| `KBVPRERPPrescription.extension``[Bedingung: url = 'https://fhir.kbv.de/StructureDefinition/KBV_EX_ERP_Multiple_Prescription']` | `EPAMedicationRequest.extension.url` | Fester Wert | setzt festen Wert:`https://gematik.de/fhir/epa-medication/StructureDefinition/multiple-prescription-extension` |

#### Extension: Nummerierung

| | | | |
| :--- | :--- | :--- | :--- |
| `KBVPRERPPrescription.extension.extension``[Bedingung: url = 'Nummerierung']` | `EPAMedicationRequest.extension.extension.url` | Fester Wert | setzt festen Wert:`counter` |

#### Extension: ID

| | | | |
| :--- | :--- | :--- | :--- |
| `KBVPRERPPrescription.extension.extension``[Bedingung: url = 'ID']` | `EPAMedicationRequest.extension.extension.url` | Fester Wert | setzt festen Wert:`id` |

#### Extension: Kennzeichen

| | | | |
| :--- | :--- | :--- | :--- |
| `KBVPRERPPrescription.extension.extension``[Bedingung: url = 'Kennzeichen']` | `EPAMedicationRequest.extension.extension.url` | Fester Wert | setzt festen Wert:`indicator` |

#### Extension: Zeitraum

| | | | |
| :--- | :--- | :--- | :--- |
| `KBVPRERPPrescription.extension.extension``[Bedingung: url = 'Zeitraum']` | `EPAMedicationRequest.extension.extension.url` | Fester Wert | setzt festen Wert:`period` |

#### Extension: KBV_EX_ERP_Narcotic

Bedingung: url = `https://fhir.kbv.de/StructureDefinition/KBV_EX_ERP_Narcotic`

| | | | |
| :--- | :--- | :--- | :--- |
| `KBVPRERPPrescription.extension``[Bedingung: url = 'https://fhir.kbv.de/StructureDefinition/KBV_EX_ERP_Narcotic']` | `EPAMedicationRequest.extension.url` | Fester Wert | setzt festen Wert:`https://gematik.de/fhir/epa-medication/StructureDefinition/narcotics-extension` |

#### Extension: ErgaenzendeAngabenSubstitutionsmittel

| | | | |
| :--- | :--- | :--- | :--- |
| `KBVPRERPPrescription.extension.extension``[Bedingung: url = 'ErgaenzendeAngabenSubstitutionsmittel']` | `EPAMedicationRequest.extension.extension.url` | Fester Wert | setzt festen Wert:`additional-information-substitutes` |

#### Extension: BtM-Sonderkennzeichen

| | | | |
| :--- | :--- | :--- | :--- |
| `KBVPRERPPrescription.extension.extension``[Bedingung: url = 'BtM-Sonderkennzeichen']` | `EPAMedicationRequest.extension.extension.url` | Fester Wert | setzt festen Wert:`narcotics-markings` |

#### Extension: KBV_EX_ERP_Patient_ID

Bedingung: url = `https://fhir.kbv.de/StructureDefinition/KBV_EX_ERP_Patient_ID`

| | | | |
| :--- | :--- | :--- | :--- |
| `KBVPRERPPrescription.extension``[Bedingung: url = 'https://fhir.kbv.de/StructureDefinition/KBV_EX_ERP_Patient_ID']` | `EPAMedicationRequest.extension.url` | Fester Wert | setzt festen Wert:`https://gematik.de/fhir/epa-medication/StructureDefinition/patient-id-extension` |

#### Extension: KBV_EX_ERP_Prescriber_ID

Bedingung: url = `https://fhir.kbv.de/StructureDefinition/KBV_EX_ERP_Prescriber_ID`

| | | | |
| :--- | :--- | :--- | :--- |
| `KBVPRERPPrescription.extension``[Bedingung: url = 'https://fhir.kbv.de/StructureDefinition/KBV_EX_ERP_Prescriber_ID']` | `EPAMedicationRequest.extension.url` | Fester Wert | setzt festen Wert:`https://gematik.de/fhir/epa-medication/StructureDefinition/prescriber-id-extension` |

#### Extension: extension-MedicationRequest.renderedDosageInstruction

Bedingung: url = `http://hl7.org/fhir/5.0/StructureDefinition/extension-MedicationRequest.renderedDosageInstruction`

| | | | |
| :--- | :--- | :--- | :--- |
| `KBVPRERPPrescription.extension``[Bedingung: url = 'http://hl7.org/fhir/5.0/StructureDefinition/extension-MedicationRequest.renderedDosageInstruction']` | `EPAMedicationRequest.extension.url` | Fester Wert | setzt festen Wert:`http://hl7.org/fhir/5.0/StructureDefinition/extension-MedicationRequest.renderedDosageInstruction` |

#### Extension: KBV_EX_ERP_Teratogenic

Bedingung: url = `https://fhir.kbv.de/StructureDefinition/KBV_EX_ERP_Teratogenic`

| | | | |
| :--- | :--- | :--- | :--- |
| `KBVPRERPPrescription.extension``[Bedingung: url = 'https://fhir.kbv.de/StructureDefinition/KBV_EX_ERP_Teratogenic']` | `EPAMedicationRequest.extension.url` | Fester Wert | setzt festen Wert:`https://gematik.de/fhir/epa-medication/StructureDefinition/teratogenic-extension` |

#### Extension: GebaerfaehigeFrau

| | | | |
| :--- | :--- | :--- | :--- |
| `KBVPRERPPrescription.extension.extension``[Bedingung: url = 'GebaerfaehigeFrau']` | `EPAMedicationRequest.extension.extension.url` | Fester Wert | setzt festen Wert:`childbearing-potential` |

#### Extension: ErklaerungSachkenntnis

| | | | |
| :--- | :--- | :--- | :--- |
| `KBVPRERPPrescription.extension.extension``[Bedingung: url = 'ErklaerungSachkenntnis']` | `EPAMedicationRequest.extension.extension.url` | Fester Wert | setzt festen Wert:`declaration-of-expertise` |

#### Extension: AushaendigungInformationsmaterialien

| | | | |
| :--- | :--- | :--- | :--- |
| `KBVPRERPPrescription.extension.extension``[Bedingung: url = 'AushaendigungInformationsmaterialien']` | `EPAMedicationRequest.extension.extension.url` | Fester Wert | setzt festen Wert:`hand-out-information-material` |

#### Extension: Off-Label

| | | | |
| :--- | :--- | :--- | :--- |
| `KBVPRERPPrescription.extension.extension``[Bedingung: url = 'Off-Label']` | `EPAMedicationRequest.extension.extension.url` | Fester Wert | setzt festen Wert:`off-label` |

#### Extension: EinhaltungSicherheitsmassnahmen

| | | | |
| :--- | :--- | :--- | :--- |
| `KBVPRERPPrescription.extension.extension``[Bedingung: url = 'EinhaltungSicherheitsmassnahmen']` | `EPAMedicationRequest.extension.extension.url` | Fester Wert | setzt festen Wert:`security-compliance` |

## Transformationsregeln

Folgende zusätzliche Anmerkungen und Regeln sind für das Mapping zu umzusetzen:

#### Eintrag für MedicationRequest.subject

* ID: Beschreibung
  * `F_010`: Das Befüllen des MedicationRequest.subject muss erfolgen, indem die Werte von* Patient.identifier.system
* Patient.identifier.value
aus dem KbvBundle.patient.identifier übernommen werden und in der folgenden Form im ePA MedicationRequest angegeben werden:```
  <subject>
    <identifier>
      <system value="http://fhir.de/sid/gkv/kvid-10" />
      <value value="X110411319" />
    </identifier>
  </subject>

```

* ID: Profile
  * `F_010`: * [KBV_PR_FOR_Patient](https://simplifier.net/for/kbv_pr_for_patient)
* [EPA MedicationRequest](https://gemspec.gematik.de/ig/fhir/epa-medication/{{ site.data.constants.epa_med_service_version }}/StructureDefinition-epa-medication-request.md)

* ID: Referenzen
  * `F_010`: * [ANFERP-2638](https://service.gematik.de/browse/ANFERP-2638)


