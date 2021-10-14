# Release 1.0.7
- update release notes on the release management page\n - fixed some typos\n

# Release 1.0.6
- added new page with the Release Management of all FHIR-Projects for realizing the german e-prescription (contains list of versions and release notes for each project) - added new page explaining the validator-service in "Titus" - added examples of Datamatrix-Codes (also evil codes) - added chapter for deleting messages

# Release 1.0.5
Changes\n - fixed sample of hash value and response in authentication flow\n - changed date format in example of MedicationDispense.whenHandedOver (to be used from 1.10.21)\n - receipt will contain hash value of original ePrescription\n - fixed typo in communication example

# Release 1.0.4
Changes
 Added implementation examples for encrypted VAU communication
 Fixed Payload in chapter for generating signature with SMC-B
 Added table of http-headers for inner and outer request in the authentication chapter


# Release 1.0.3
Changes
 Update and more details on the authentication workflow and the description
 Update on the communication responses (json payload for delivery and shipment)
 Update on workflowAuthentication.svg
 Added verifyCertificate for PTV4 ECC-Certificates
 Added note on http-RFC for VAU-inner http-Request
 Added note for UTC timestamp on Communications
 Added image to describe namingserver network overview for DNS
 Bugfixes on bundle type in erp_abrufen.adoc and erp_versicherter.adoc
 Little bugfix on the description of the SSO_TOKEN
 Fixed example of MedicationDispense


# Release 1.0.2
Changes
 - added .NET sample Code for VAU-Communication
 - information on network and DNS configuration for client systems
 - minor typo and inconsistency changes/fixes


# Release 1.0.1
#E-Rezept 1.0.1 - Release Notes Notes: Since April 2021 E-Rezept is no longer a part of a gematik document release package. Starting with E-Rezept v1.0.1 it will be developed in a separate branch (see also https://fachportal.gematik.de/anwendungen/elektronisches-rezept). - update and clarification on IDP authentication flow - added samples for qualified signatures on ePrescription-Bundles, see samples folder - additional headers on outer http-request - added configuration guide for installation issues on DNS resolving and routing issues - no delete prescription by representative allowed - minor typo and inconsistency changes/fixes

# Release 4.0.2-2
# Release 4.0.2-2 Changes -refactoring of authentication chapter -added PS-IDP-Flow.html for better description -minor fixes in communication chapter

# Release 4.0.2-1
# Release 4.0.2 Minor changes and bug fixes - removed not necessar masking charakters in links - correction of requests and responses in communication - deleted example and source folder. all files can be found on simplifier.net (link available on Readme)

# Release 4.0.2
# Release 4.0.2 Release to fit specification progress and new FHIR profiling corrections. Changes - update on all examples - spelling correction - changed canonical notation to UpperCamelCase (default in FHIR standard) - minor changes in descriptions

# Release 4.0.1
# Release 4.0.1 New features - Notification Service (Description on the REST-Operations) Changes - update on the IdP-Handshake - updated the Communication Ressources - updated the Medication Ressource - update on the 2D-Code structure - changed the layout of the Requests and Responses for better readability - fixed some error in examples

# Release 4.0.0-Pre1
- Aufhebung der Größenbeschränkung von Nachrichten
 - Optionale Integration des Clientmoduls in das PVS
 - Administrationsmodul für die Konfiguration
 - Unterstützung syntaktischer Nachrichtenkategorien


