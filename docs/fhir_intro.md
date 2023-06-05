# E-Rezept on FHIR

## Beteiligte Organisationen im E-Rezept

Die KBV definiert die FHIR-Profile des Verordnungsdatensatzes im simplifier-Projekt [E-Rezept-Verordnung](https://simplifier.net/erezept). 

Die Festlegungen zu Abgabe- und Abrechnungsdaten der Apotheken werden im DAV-Projekt [Abgabedaten](https://simplifier.net/erezeptabgabedaten) 

Der GKV-SV stellt das FHIR-Repository für die [Abrechnungsdaten](https://simplifier.net/eRezeptAbrechnungsdaten) bereit.

Die gematik veröffentlicht das [Workflow package](https://simplifier.net/erezept-workflow), womit ein Rezept durch den Fachdienst geleitet wird.

[Auf dieser Seite](docs/erp_fhirversion.adoc) finden sie ReleaseNotes der FHIR-Releases der beteiligten Organisationen.

## Informationen zum aktuellen Versionsübergang 01.07.2023

Wichtige Informationen zum Verhalten des Fachdienstes während der Übergangszeit und danach finden sich [auf dieser Seite](docs/erp_versionsuebergang.adoc)

## FHIR-Releases

Die Veröffentlichung an dieser Stelle erfolgt übergangsweise, bis ein gemeinsames Repository 'oberhalb' der API-Beschreibung gefunden ist.

Das Titus-Testportal wird in den Anwendungsfällen zum E-Rezept um einen Validator erweitert. Zukünftig werden *alle* Requests vor der Weiterverarbeitung online validiert.
Details dazu finden sich [auf der folgenden Seite](docs/erp_validation.adoc).

Wie Vergleiche zwischen FHIR Profilen (z.B. nach Versionsübergängen) vorgenommen werden können und den Verweis auf die Artefakte zum aktuellen Versionsübergang finden sich [auf dieser Seite](docs/erp_fhirversion_changes.adoc).