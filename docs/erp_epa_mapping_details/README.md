# E-Rezept zu ePA Profile Mapping Tabellen

## Erläuterung
Die folgenden Tabellen geben eine detaillierte Auskunft über das Mapping der aus dem E-Rezept Kontext verwendeten Ressourcen zu den im Medication Service der ePA verwendeten Ressourcen.

## Mapping Tabellen der Operationen im E-Rezept-Fachdienst
- [Mapping: KBV_PR_FOR_Organization\|1.1.0 -> OrganizationDirectory\|0.11.7](https://gematik.github.io/api-erp/erp_epa_mapping_details/KBV_PR_FOR_Organization|1.1.0_to_OrganizationDirectory|0.11.7.html)
- [Mapping: KBV_PR_FOR_Practitioner\|1.1.0 -> PractitionerDirectory\|0.11.7](https://gematik.github.io/api-erp/erp_epa_mapping_details/KBV_PR_FOR_Practitioner|1.1.0_to_PractitionerDirectory|0.11.7.html)
- [Mapping: KBV_PR_ERP_Prescription\|1.1.0 -> EPAMedicationRequest\|1.0.2-rc1](https://gematik.github.io/api-erp/erp_epa_mapping_details/KBV_PR_ERP_Prescription|1.1.0_to_EPAMedicationRequest|1.0.2-rc1.html)
- [Mapping: KBV_PR_ERP_Medication_Compounding\|1.1.0, KBV_PR_ERP_Medication_FreeText\|1.1.0, KBV_PR_ERP_Medication_Ingredient\|1.1.0, KBV_PR_ERP_Medication_PZN\|1.1.0 -> EPAMedication\|1.0.2-rc1](https://gematik.github.io/api-erp/erp_epa_mapping_details/KBV_PR_ERP_Medication_Compounding|1.1.0_KBV_PR_ERP_Medication_FreeText|1.1.0_KBV_PR_ERP_Medication_Ingredient|1.1.0_KBV_PR_ERP_Medication_PZN|1.1.0_to_EPAMedication|1.0.2-rc1.html)

Während der Übergangszeit wird der E-Rezept-Fachdienst auch folgendes Mapping ausführen:
- [Mapping: GEM_ERP_PR_MedicationDispense\|1.2 oder GEM_ERP_PR_MedicationDispense\|1.3.1 -> EPAMedicationDispense\|1.0.2-rc1](https://gematik.github.io/api-erp/erp_epa_mapping_details/GEM_ERP_PR_MedicationDispense|1.3.1_to_EPAMedicationDispense|1.0.2-rc1.html)

Immer nach der Übergangszeit wird der E-Rezept-Fachdienst folgendes Mapping ausführen:
- [Mapping: GEM_ERP_PR_MedicationDispense\|1.4.0-rc1 -> EPAMedicationDispense\|1.0.2-rc1](https://gematik.github.io/api-erp/erp_epa_mapping_details/GEM_ERP_PR_MedicationDispense|1.4.0-rc1_to_EPAMedicationDispense|1.0.2-rc1.html)

## Mapping-Tabellen zur Unterstützung der Implementierungen im AVS

- [Mapping: KBV_PR_ERP_Medication_Compounding\|1.1.0, KBV_PR_ERP_Medication_FreeText\|1.1.0, KBV_PR_ERP_Medication_Ingredient\|1.1.0, KBV_PR_ERP_Medication_PZN\|1.1.0 -> GEM_ERP_PR_Medication\|1.4.0-rc1](https://gematik.github.io/api-erp/erp_epa_mapping_details/KBV_PR_ERP_Medication_Compounding|1.1.0_KBV_PR_ERP_Medication_FreeText|1.1.0_KBV_PR_ERP_Medication_Ingredient|1.1.0_KBV_PR_ERP_Medication_PZN|1.1.0_to_GEM_ERP_PR_Medication|1.4.0-rc1.html)
- [Mapping: GEM_ERP_PR_MedicationDispense\|1.3.1 -> GEM_ERP_PR_MedicationDispense\|1.4.0-rc1](https://gematik.github.io/api-erp/erp_epa_mapping_details/GEM_ERP_PR_MedicationDispense|1.3.1_to_GEM_ERP_PR_MedicationDispense|1.4.0-rc1.html)