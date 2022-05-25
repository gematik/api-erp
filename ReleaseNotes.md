# Release 1.1.9
Updated docs/erp_fhirversion.adoc with PKV ChargeItem informations

# Release 1.1.8
Added Information on RU-configuration for FHIR-profiles support in ePrescrioption backend

# Release 1.1.7
Update FHIR-release management
Overview http-statuscodes ePrescription-backend
Overview multiple prescriptions
Update sample prescriptions and other corrections

# Release 1.1.6
New Feature

- new document with status and error codes ‘erp_statuscodes’

Changes

- edited some error codes
- update on FHIR versioning in the versions overview
- bug fixing in notification document
- added code example in notification_avs
- added kbv blanko example

# Release 1.1.5
New Feature

- new PoC for verification of an prescription receipt signature outside the TI


Changes

- fixed example of request in $close-operation

- fixed get request of messages in an certain time range

# Release 1.1.4
Changes

- Update on FHIR-Profile overview

- APOVZD-interface switched from Organization (draft 2021) to Location (as used)

- Minor fixes on API-Parameters

# Release 1.1.3
New Feature PKV (private health insurance)
 
- added description on new workflowtype “200” for “pkv”. Described how to start the workflow for patients with private health insurance ($create-Operation) and what to do when finishing the workflow ($close-Operation)
 
- other functions and interfaces will follow in later releases
 

Changes
 
- update in FHIR-Realeses: added Release notes for 01.01.2022 in “DAV” line
 
- updated version numbers of examples
 
- updated and fixed examples
 

# Release 1.1.2
- added close-Operation with several MedicationDispenses 
 
- minor version fixes on examples
 
- added some notes
 


# Release 1.1.1
- fixed examples of receipt Bundle
 
- updated endpoint names
 
- updated version number of KBV canonicals in examples
 
- updated information in versioning management
  
- updated request and response in chapter for VAU-authentication
 
- fixed response of get/Bundle as patient, the endpoint in signature.who was wrong
 
- style fixes for images
 

