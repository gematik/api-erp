import os
import json
from datetime import datetime, timedelta

# Configure ignore list for "in PU einstellbar bis" column.
# Any package name (case-insensitive match) listed here will show "-" in that column.
IN_PU_IGNORE_PACKAGES = {
    "de.abda.erezeptabgabedaten",  # example from your request
    # add more package names as needed
}

def to_date(s):
    return None if s in (None, "-", "") else datetime.strptime(s, "%Y-%m-%d")

def fmt_date(d):
    return "-" if d is None else d.strftime("%d.%m.%Y")

def add_days(d, days):
    return None if d is None else d + timedelta(days=days)

def compute_in_pu_einstellbar_bis(package_name, valid_to_str):
    """
    Ermittelt 'in PU einstellbar bis' anhand definierter Nachhalte-Logik.
    Berücksichtigt eine Ignore-Liste, bei der die Spalte als '-' ausgewiesen wird.

    Regeln:
    - Ignore-Liste: alle in IN_PU_IGNORE_PACKAGES aufgeführten Pakete → "-"
    - de.gematik.erezept-workflow.r4:
        normaler Grenzfall: validTo + 192 Tage
        (MVO-Sonderfall 365+100 wird hier bewusst nicht automatisch verlängert)
    - de.abda.eRezeptAbgabedatenPKV:
        validTo + (10 Jahre + 1 Monat) -> 10*365 + 1*30 ≈ 3680 Tage (vereinfachte Arithmetik)
      Hinweis: Für exakte Monats-/Jahresarithmetik ggf. dateutil.relativedelta verwenden.
    - Alle anderen Pakete:
        Standard: kein zusätzlicher Puffer → validTo (identisch)
    """
    # Ignore-Liste prüfen (case-insensitive)
    if package_name.lower() in IN_PU_IGNORE_PACKAGES:
        return "-"

    valid_to = to_date(valid_to_str)  # expects '%Y-%m-%d' or None
    if valid_to is None:
        # Kein Ende gesetzt → nicht begrenzbar
        return "-"

    name = package_name.lower()

    if name == "kbv.ita.erp":
        # Ende Gültigkeit + 10 Tage für $create + 10 Tage Löschfrist im Status 'draft'
        return fmt_date(add_days(valid_to, 10))

    if name == "de.gematik.erezept-workflow.r4":
        # Ende Gültigkeit + 3 Monate (≈ 92 Tage) + 100 Tage = 192 Tage (Grenzfall normal)
        return fmt_date(add_days(valid_to, 192))

    if name == "de.abda.erezeptabgabedatenpkv":
        # 10 Jahre + 1 Monat (vereinfachte Arithmetik: 10*365 + 30 Tage)
        return fmt_date(add_days(valid_to, 3680))

    # Default: kein Zusatzpuffer
    return fmt_date(valid_to)

def generate_adoc(configurations, output_dir):
    """
    Generates .adoc files with tables of package versions grouped by their validFrom dates.
    Each .adoc file corresponds to a specific validFrom date.

    Ergänzt um die Spalte 'in PU einstellbar bis' und eine Ignore-Liste.
    """
    listed_versions = {}
    packages_by_date = {}

    # Group by validFrom
    for config in configurations:
        valid_from = config["validFrom"]

        for package in config["packages"]:
            package_name = package["name"]
            for version in package["versions"]:
                # Skip if already listed
                if package_name in listed_versions and version in listed_versions[package_name]:
                    continue

                if valid_from not in packages_by_date:
                    packages_by_date[valid_from] = []

                # Determine "gültig bis" by finding last config where the version appears
                last_valid_to = "-"
                for later_config in configurations:
                    if any(p["name"] == package_name and version in p["versions"]
                           for p in later_config["packages"]):
                        last_valid_to = later_config.get("validTo", None)

                if last_valid_to is None:
                    last_valid_to = "-"

                # Compute "in PU einstellbar bis"
                in_pu_until = compute_in_pu_einstellbar_bis(
                    package_name,
                    last_valid_to if last_valid_to != "-" else None
                )

                # Format dates for table
                valid_to_formatted = "-" if last_valid_to == "-" else datetime.strptime(
                    last_valid_to, "%Y-%m-%d"
                ).strftime("%d.%m.%Y")
                valid_from_formatted = datetime.strptime(
                    valid_from, "%Y-%m-%d"
                ).strftime("%d.%m.%Y")

                packages_by_date[valid_from].append({
                    "package": package_name,
                    "version": version,
                    "valid_from": valid_from_formatted,
                    "valid_to": valid_to_formatted,
                    "in_pu_bis": in_pu_until,
                })

                # Mark as listed
                if package_name not in listed_versions:
                    listed_versions[package_name] = set()
                listed_versions[package_name].add(version)

    os.makedirs(output_dir, exist_ok=True)

    # Generate an .adoc file per validFrom date
    for valid_from, packages in sorted(packages_by_date.items()):
        formatted_date = datetime.strptime(valid_from, "%Y-%m-%d").strftime("%d.%m.%Y")
        adoc_filename = os.path.join(output_dir, f"{valid_from}.adoc")

        with open(adoc_filename, "w", encoding="utf-8") as adoc_file:
            # Header
            adoc_file.write(f"== {formatted_date}\n\n")
            adoc_file.write(f"Ab dem {formatted_date} erfolgt ein Versionswechsel der FHIR-Profile.\n\n")
            adoc_file.write("Details zu den Änderungen sind hier zu finden.\n\n")

            # Table header (added column)
            adoc_file.write('[cols="h,a,a,a,a"]\n')
            adoc_file.write("|===\n")
            adoc_file.write("| |*Version und Releasenotes* |*Datum gültig ab* |*Datum gültig bis* |*in PU einstellbar bis*\n\n")

            # Rows
            for package in sorted(packages, key=lambda p: p["package"]):
                package_name = package["package"]
                version = package["version"]
                valid_from = package["valid_from"]
                valid_to = package["valid_to"]
                in_pu_bis = package["in_pu_bis"]

                simplifier_link = (
                    f"link:https://simplifier.net/packages/{package_name}/{version}[Package {version}^]"
                )

                adoc_file.write(
                    f"|{package_name} |{simplifier_link} |{valid_from} |{valid_to} |{in_pu_bis}\n"
                )

            adoc_file.write("|===\n")

        print(f"Generated {adoc_filename}")

def generate_transition_overview(configurations, output_file):
    """
    Generates a single .adoc file with a transition overview table for all packages and versions.
    Each package/version appears only once, with the correct gültig von and gültig bis dates.

    Ergänzt um die Spalte 'in PU einstellbar bis' und die Ignore-Liste.
    """
    version_data = {}

    # Collect first/last occurrences
    for index, config in enumerate(configurations):
        valid_from = config["validFrom"]
        valid_to = config.get("validTo", None)

        for package in config["packages"]:
            package_name = package["name"]
            for version in package["versions"]:
                if (package_name, version) not in version_data:
                    version_data[(package_name, version)] = {
                        "valid_from": valid_from,
                        "valid_to": valid_to,
                    }
                else:
                    # Update last valid_to seen
                    version_data[(package_name, version)]["valid_to"] = valid_to

    overview_entries = []
    first_config = configurations[0]
    first_config_valid_from = first_config["validFrom"]
    last_config = configurations[-1]
    last_config_valid_from = last_config["validFrom"]

    for (package_name, version), dates in version_data.items():
        valid_from = dates["valid_from"] if dates["valid_from"] != first_config_valid_from else "-"
        valid_to = dates["valid_to"]

        # If appears in last config without validTo, set "-" (open-ended)
        if valid_to is None and dates["valid_from"] == last_config_valid_from:
            valid_to = "-"

        # Compute "in PU einstellbar bis"
        in_pu_until = compute_in_pu_einstellbar_bis(
            package_name,
            valid_to if valid_to not in (None, "-") else None
        )

        # Format dates for table
        valid_from_formatted = (
            "-" if valid_from in [None, "-"] else datetime.strptime(valid_from, "%Y-%m-%d").strftime("%d.%m.%Y")
        )
        valid_to_formatted = (
            "-" if valid_to in [None, "-"] else datetime.strptime(valid_to, "%Y-%m-%d").strftime("%d.%m.%Y")
        )

        overview_entries.append({
            "package": package_name,
            "version": version,
            "valid_from": valid_from_formatted,
            "valid_to": valid_to_formatted,
            "in_pu_bis": in_pu_until,
        })

    overview_entries.sort(key=lambda e: (e["package"], e["version"]))

    with open(output_file, "w", encoding="utf-8") as adoc_file:
        # Table header (added column)
        adoc_file.write('[cols="h,a,a,a,a"]\n')
        adoc_file.write("|===\n")
        adoc_file.write("|*FHIR Paket* |*Version* |*Gültig Von* |*Gültig Bis* |*in PU einstellbar bis*\n\n")

        for entry in overview_entries:
            adoc_file.write(
                f"|{entry['package']} |{entry['version']} |{entry['valid_from']} |{entry['valid_to']} |{entry['in_pu_bis']}\n"
            )

        adoc_file.write("|===\n")

    print(f"Generated transition overview table: {output_file}")

# Main script
if __name__ == "__main__":
    # Define paths
    root_dir = os.path.dirname(os.path.abspath(__file__))
    config_dir = os.path.join(root_dir, "../configuration/")
    output_base_dir = os.path.join(root_dir, "./output_adoc")

    # Iterate through all JSON configuration files in the configuration directory
    for config_file in os.listdir(config_dir):
        if config_file.endswith(".json"):
            config_path = os.path.join(config_dir, config_file)
            config_name = os.path.splitext(config_file)[0]  # Remove the .json extension
            output_dir = os.path.join(output_base_dir, config_name)

            # Load JSON data
            try:
                with open(config_path, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    configurations = data["fhir_configurations"]
            except FileNotFoundError:
                print(f"Error: Configuration file not found at {config_path}")
                continue
            except json.JSONDecodeError as e:
                print(f"Error: Failed to parse JSON file {config_file}. {e}")
                continue

            # Generate the .adoc files for this configuration
            generate_adoc(configurations, output_dir)

            # Generate the transition overview table for this configuration
            transition_overview_file = os.path.join(output_dir, "transition-overview.adoc")
            generate_transition_overview(configurations, transition_overview_file)
