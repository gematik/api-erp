# Mapping des Verordnenden für Verordnungsdaten - Implementation Guide E-Rezept-Fachdienst v1.6.1-draft

Implementation Guide

E-Rezept-Fachdienst

Version 1.6.1-draft - ci-build 

* [**Table of Contents**](toc.md)
* [**Vorgaben zum Mapping von FHIR-Instanzen**](mapping.md)
* [**Mapping von Verordnungsdaten**](mapping-prescription.md)
* **Mapping des Verordnenden für Verordnungsdaten**

## Mapping des Verordnenden für Verordnungsdaten

Diese Seite beschreibt Anforderungen und Umsetzungsunterstützung für das Mapping vom

* [KBV_FOR_PR_Practitioner](https://simplifier.net/packages/kbv.ita.for/1.2.1/files/3157104)
* zum [PractitionerDirectory](https://simplifier.net/packages/de.gematik.fhir.directory/1.0.0/files/2970193).

## Wichtige Punkte beim Mapping der Practitioner Ressource

Die folgenden Punkte sind relevant für das Mapping der Practitioner Ressource:

* Die Telematik-ID wird aus dem Accesstoken der Anfrage bezogen (F_013)
* Der Name des Practitioners muss aus Bestandteilen zusammengesetzt werden (F_011)
* Es muss überprüft werden, welcher Practitioner zu mappen ist (F_016)
* Die Qualifikation des Practitioners darf nicht übertragen werden

## Generelles Mapping des Profils

Die folgende Tabelle stellt generell das Mapping der beiden Profile gegenüber:

### Feld-Mappings

| | | | |
| :--- | :--- | :--- | :--- |
| `KBVPRFORPractitioner.meta` | `PractitionerDirectory.meta.profile` | Fester Wert | setzt festen Wert:`https://gematik.de/fhir/directory/StructureDefinition/PractitionerDirectory` |
| `KBVPRFORPractitioner.name` | `PractitionerDirectory.name` | Manuell | Zum Erzeugen von name.text siehe Transformationsregel F_011 | Quelle: Practitioner.name.text |
| `KBVPRFORPractitioner.qualification` | `PractitionerDirectory.qualification` | Nicht Übertragen | Feld wird nicht gemappt | Quelle: Practitioner.qualification:ASV-Fachgruppennummer |
| `KBVPRFORPractitioner.qualification` | `PractitionerDirectory.qualification` | Nicht Übertragen | Feld wird nicht gemappt | Quelle: Practitioner.qualification:Berufsbezeichnung |
| `KBVPRFORPractitioner.qualification` | `PractitionerDirectory.qualification` | Nicht Übertragen | Feld wird nicht gemappt | Quelle: Practitioner.qualification:Typ |

## Transformationsregeln

Folgende zusätzliche Anmerkungen und Regeln sind für das Mapping zu umzusetzen:

#### Befüllung von Practitioner.name

* ID: Beschreibung
  * `F_011`: Der Practitioner.name.text ist ein Pflichtfeld und muss aus den Namensinformationen erzeugt werden.Dabei ist folgende Bildungsregel anzuwenden:```
def build_practitioner_name(practitioner):
  # Verknüpft Elemente einer Liste zu einem String, getrennt durch Leerzeichen
  def join_with_space(elements):
    return " ".join(elements)

  # Hilfsfunktion zum Abrufen des Werts einer Extension
  def get_extension_value(extensions, url):
    for ext in extensions:
      if ext.get("url") == url:
        return ext.get("valueString") or ext.get("valueCode", "")
    return ""

  # Namenszusätze und Präfix-Qualifier URLs
  namenszusatz_url = "http://hl7.org/fhir/StructureDefinition/humanname-namenszusatz"
  nachname_url = "http://hl7.org/fhir/StructureDefinition/humanname-own-name"
  vorsatzwort_url = "http://hl7.org/fhir/StructureDefinition/humanname-own-prefix"
  prefix_qualifier_url = "http://hl7.org/fhir/StructureDefinition/iso21090-EN-qualifier"

  # Zusätzliche Namenskomponenten aus den Extensions abrufen
  family_extensions = practitioner["name"][0]["family"]["extension"]
  namenszusatz = get_extension_value(family_extensions, namenszusatz_url)
  nachname = get_extension_value(family_extensions, nachname_url)
  vorsatzwort = get_extension_value(family_extensions, vorsatzwort_url)
  prefix_extensions = practitioner["name"][0].get("prefix", [{}])[0].get("extension", [])
  prefix_qualifier = get_extension_value(prefix_extensions, prefix_qualifier_url)

  # Zusammensetzung des Namens
  prefix = join_with_space([practitioner["name"][0].get("prefix", {}).get("value", "")])
  given_name = practitioner["name"][0].get("given", "")
  family_name = f"{vorsatzwort} {nachname} {namenszusatz}".strip()

  # Zusammensetzen des vollständigen Namens mit Leerzeichen dazwischen
  full_name = f"{prefix_qualifier} {prefix} {given_name} {family_name}".strip()

  return full_name


# Beispielhafte Verwendung
practitioner_example = {
  "name": [
    {
      "use": "official",
      "family": {
        "extension": [
          {
            "url": "http://hl7.org/fhir/StructureDefinition/humanname-namenszusatz",
            "valueString": "von",
          },
          {
            "url": "http://hl7.org/fhir/StructureDefinition/humanname-own-name",
            "valueString": "Müller",
          },
          {
            "url": "http://hl7.org/fhir/StructureDefinition/humanname-own-prefix",
            "valueString": "Dr.",
          },
        ],
        "family": "Müller",
      },
      "given": "Hans",
      "prefix": [
        {
          "extension": [
            {
              "url": "http://hl7.org/fhir/StructureDefinition/iso21090-EN-qualifier",
              "valueCode": "AC",
            }
          ],
          "value": "Prof.",
        }
      ],
    }
  ]
}

print(build_practitioner_name(practitioner_example))

```

* ID: Profile
  * `F_011`: * [KBV_PR_FOR_Practitioner](https://simplifier.net/for/kbv_pr_for_practitioner)
* [PractitionerDirectory](https://simplifier.net/vzd-fhir-directory/practitionerdirectorystrict)

* ID: Referenzen
  * `F_011`: * [ANFERP-2639](https://service.gematik.de/browse/ANFERP-2639)


#### Befüllung der Telematik-ID des Arztes

* ID: Beschreibung
  * `F_013-01`: Die Telematik-ID des Arztes wird wie folgt ermittelt und gesetzt:* Primär: Aus der QES-Signatur des Zertifikats.
* Fallback: Wenn keine Telematik-ID in der QES-Signatur vorhanden ist, wird die Seriennummer des Zertifikats (Subject Serial Number) ausgelesen und die zugehörige Telematik-ID über die Nachschlagetabelle ermittelt.
* Fehlerfall: Kann die Telematik-ID nicht ermittelt werden, wird die Verordnung nicht übertragen

* ID: Profile
  * `F_013-01`: * [PractitionerDirectory](https://simplifier.net/vzd-fhir-directory/practitionerdirectorystrict)

* ID: Referenzen
  * `F_013-01`: * [A_25946 - E-Rezept-Fachdienst - ePA Mapping](https://gemspec.gematik.de/docs/gemF/gemF_eRp_ePA/gemF_eRp_ePA_V1.2.1/#A_25946)


#### Mapping des korrekten Practitioners

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


