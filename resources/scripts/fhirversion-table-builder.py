import os
import json
from datetime import datetime, timedelta

def generate_adoc(configurations, output_dir):
    """
    Generates .adoc files with tables of package versions grouped by their validFrom dates.
    Each .adoc file corresponds to a specific validFrom date.
    """
    # Prepare a dictionary to track which versions have already been listed
    listed_versions = {}

    # Prepare a dictionary to group packages by validFrom dates
    packages_by_date = {}

    # Iterate over configurations to group packages by validFrom dates
    for config in configurations:
        valid_from = config["validFrom"]
        valid_to = config.get("validTo", None)

        for package in config["packages"]:
            package_name = package["name"]
            for version in package["versions"]:
                # Skip if this version has already been listed in a previous table
                if package_name in listed_versions and version in listed_versions[package_name]:
                    continue

                # Add package details to the validFrom date group
                if valid_from not in packages_by_date:
                    packages_by_date[valid_from] = []

                # Determine the gültig bis (valid_to) date
                # Find the last configuration where the version appears
                last_valid_to = "-"
                for later_config in configurations:
                    if any(
                        p["name"] == package_name and version in p["versions"]
                        for p in later_config["packages"]
                    ):
                        last_valid_to = later_config.get("validTo", None)

                # If the version appears in the last configuration without a validTo, set gültig bis to "-"
                if last_valid_to is None:
                    last_valid_to = "-"

                # Format the dates
                valid_to_formatted = (
                    "-" if last_valid_to == "-" else datetime.strptime(last_valid_to, "%Y-%m-%d").strftime("%d.%m.%Y")
                )
                valid_from_formatted = datetime.strptime(valid_from, "%Y-%m-%d").strftime("%d.%m.%Y")

                # Add the package/version entry
                packages_by_date[valid_from].append({
                    "package": package_name,
                    "version": version,
                    "valid_from": valid_from_formatted,
                    "valid_to": valid_to_formatted,
                })

                # Mark this version as listed
                if package_name not in listed_versions:
                    listed_versions[package_name] = set()
                listed_versions[package_name].add(version)

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Generate an .adoc file for each validFrom date
    for valid_from, packages in sorted(packages_by_date.items()):
        # Format the validFrom date in German notation (dd.MM.yyyy)
        formatted_date = datetime.strptime(valid_from, "%Y-%m-%d").strftime("%d.%m.%Y")
        adoc_filename = os.path.join(output_dir, f"{valid_from}.adoc")

        with open(adoc_filename, "w", encoding="utf-8") as adoc_file:
            # Write the header
            adoc_file.write(f"== {formatted_date}\n\n")
            adoc_file.write(f"Ab dem {formatted_date} erfolgt ein Versionswechsel der FHIR-Profile.\n\n")
            adoc_file.write("Details zu den Änderungen sind hier zu finden.\n\n")

            # Write the table header
            adoc_file.write('[cols="h,a,a,a"]\n')
            adoc_file.write("|===\n")
            adoc_file.write("| |*Version und Releasenotes* |*Datum gültig ab* |*Datum gültig bis*\n\n")

            # Write the table rows
            for package in sorted(packages, key=lambda p: p["package"]):
                package_name = package["package"]
                version = package["version"]
                valid_from = package["valid_from"]
                valid_to = package["valid_to"]

                # Construct the Simplifier link
                simplifier_link = (
                    f"link:https://simplifier.net/packages/{package_name}/{version}[Package {version}^]"
                )

                # Write the row
                adoc_file.write(
                    f"|{package_name} |{simplifier_link} |{valid_from} |{valid_to}\n"
                )

            # Close the table
            adoc_file.write("|===\n")

        print(f"Generated {adoc_filename}")

def generate_transition_overview(configurations, output_file):
    """
    Generates a single .adoc file with a transition overview table for all packages and versions.
    Each package/version appears only once, with the correct gültig von and gültig bis dates.
    """
    # Prepare a dictionary to store the first and last occurrences of each package/version
    version_data = {}

    # Iterate over configurations to collect package/version data
    for config in configurations:
        valid_from = config["validFrom"]
        valid_to = config.get("validTo", None)

        for package in config["packages"]:
            package_name = package["name"]
            for version in package["versions"]:
                # If this version is not yet tracked, initialize its data
                if (package_name, version) not in version_data:
                    version_data[(package_name, version)] = {
                        "valid_from": valid_from,
                        "valid_to": valid_to,
                    }
                else:
                    # Update the valid_to to the most recent validTo
                    version_data[(package_name, version)]["valid_to"] = valid_to

    # Process the version data to determine the correct gültig bis (valid_to)
    overview_entries = []
    last_config = configurations[-1]
    last_config_valid_from = last_config["validFrom"]

    for (package_name, version), dates in version_data.items():
        valid_from = dates["valid_from"]
        valid_to = dates["valid_to"]

        # If the version appears in the last configuration without a validTo, set gültig bis to "-"
        if valid_to is None and valid_from == last_config_valid_from:
            valid_to = "-"

        # Format the dates
        valid_from_formatted = datetime.strptime(valid_from, "%Y-%m-%d").strftime("%d.%m.%Y")
        valid_to_formatted = (
            "-" if valid_to in [None, "-"] else datetime.strptime(valid_to, "%Y-%m-%d").strftime("%d.%m.%Y")
        )

        # Add the entry
        overview_entries.append({
            "package": package_name,
            "version": version,
            "valid_from": valid_from_formatted,
            "valid_to": valid_to_formatted,
        })

    # Sort the entries by package name and version
    overview_entries.sort(key=lambda e: (e["package"], e["version"]))

    # Write the transition overview table to the output file
    with open(output_file, "w", encoding="utf-8") as adoc_file:

        # Write the table header
        adoc_file.write('[cols="h,a,a,a"]\n')
        adoc_file.write("|===\n")
        adoc_file.write("|*FHIR Paket* |*Version* |*Gültig Von* |*Gültig Bis*\n\n")

        # Write the table rows
        for entry in overview_entries:
            package_name = entry["package"]
            version = entry["version"]
            valid_from = entry["valid_from"]
            valid_to = entry["valid_to"]

            # Write the row
            adoc_file.write(f"|{package_name} |{version} |{valid_from} |{valid_to}\n")

        # Close the table
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
