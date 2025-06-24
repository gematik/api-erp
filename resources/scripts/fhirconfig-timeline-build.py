import os
import json
from datetime import datetime, timedelta
from packaging.version import parse as parse_version

def validate_unique_configuration_names(configurations, filename):
    """
    Validates that all configurations have unique names.
    """
    errors = []
    seen_names = set()
    for config in configurations:
        if config["name"] in seen_names:
            errors.append(f"Duplicate configuration name found: '{config['name']}' in '{filename}'.")
        seen_names.add(config["name"])
    return errors

def validate_dates(configurations):
    """
    Validates the `validFrom` and `validTo` dates for each configuration.
    Ensures that configurations are sequential and valid.
    """
    errors = []
    for i in range(len(configurations) - 1):
        current = configurations[i]
        next_config = configurations[i + 1]

        # Parse dates
        current_valid_to = datetime.strptime(current["validTo"], "%Y-%m-%d")
        next_valid_from = datetime.strptime(next_config["validFrom"], "%Y-%m-%d")

        # Check if the dates are consecutive
        if current_valid_to + timedelta(days=1) != next_valid_from:
            errors.append(
                f"Configuration '{current['name']}' (validTo: {current['validTo']}) "
                f"and '{next_config['name']}' (validFrom: {next_config['validFrom']}) are not consecutive."
            )

        # Check if validTo is before validFrom
        if current_valid_to < datetime.strptime(current["validFrom"], "%Y-%m-%d"):
            errors.append(
                f"Configuration '{current['name']}' has validTo earlier than validFrom."
            )

    return errors

def validate_package_mappings(configurations, package_mappings):
    """
    Validates that every package in the configurations has a corresponding mapping.
    """
    mapped_packages = {mapping["package"] for mapping in package_mappings}
    missing_packages = set()

    for config in configurations:
        for package in config["packages"]:
            if package["name"] not in mapped_packages:
                missing_packages.add(package["name"])

    return missing_packages

def validate_package_versions(configurations):
    """
    Validates the versions of packages across configurations.
    Rules:
    - A version may appear for the first time in any configuration (first appearances are allowed).
    - A version must not reappear after being absent in an intermediate configuration.
    - A package cannot have multiple versions with the same minor version in a single configuration.
    """
    errors = []
    package_versions = {}  # Tracks active versions for each package

    for i, config in enumerate(configurations):
        for package in config["packages"]:
            package_name = package["name"]
            current_versions = package["versions"]

            # Check for duplicate minor versions in the current configuration
            seen_minors = set()
            for version in current_versions:
                parsed_version = parse_version(version)
                minor_version = (parsed_version.major, parsed_version.minor)
                if minor_version in seen_minors:
                    errors.append(
                        f"Configuration '{config['name']}' contains multiple versions "
                        f"of package '{package_name}' with the same minor version: {version}"
                    )
                seen_minors.add(minor_version)

            # Check for gaps in versions across configurations
            if package_name not in package_versions:
                # First time seeing this package, initialize its active versions
                package_versions[package_name] = set(current_versions)
            else:
                previous_versions = package_versions[package_name]

                # Check if any previously active version is missing in the current configuration
                for version in previous_versions:
                    if version not in current_versions:
                        # Ensure the version is not reappearing in a later configuration
                        for later_config in configurations[i + 1:]:
                            later_package_versions = [
                                p["versions"]
                                for p in later_config["packages"]
                                if p["name"] == package_name
                            ]
                            if later_package_versions and version in later_package_versions[0]:
                                errors.append(
                                    f"Version '{version}' of package '{package_name}' reappears in "
                                    f"configuration '{later_config['name']}' after being absent."
                                )

                # Update active versions for the package
                package_versions[package_name].update(current_versions)

    return errors

def generate_gantt(configurations, package_mappings):
    """
    Generates a PlantUML Gantt diagram from the JSON configurations, including sections for packages.
    """
    # Start the Gantt diagram
    puml = ["@startgantt"]

    
    # Add updated color definitions
    puml.append("!define kbvcolor #ff8c42")
    puml.append("!define evdgacolor #ffb685")
    puml.append("!define davpkvcolor #6abf69")
    puml.append("!define davcolor #91d891")
    puml.append("!define gkvsvcolor #A8111E")
    puml.append("!define gematikcolor #4a90e2")
    puml.append("!define gematikcolor_fdv #5a6fa5")
    puml.append("!define gematikcolor_patrn #88d4d8")
    puml.append("!define gematikcolor_eu #b3cde3")
    puml.append("!define erpfdcolor #90a4ae")
    puml.append("")
    puml.append("!define datelinecolor #f2b6b6")
    puml.append("")

    # Add updated style and metadata
    puml.append("<style>")
    puml.append("document {")
    puml.append("   BackGroundColor #f5f5f5")
    puml.append("}")
    puml.append("ganttDiagram {")
    puml.append("   task {")
    puml.append("      BackGroundColor GreenYellow")  # Default task color
    puml.append("      LineColor Green")
    puml.append("      FontColor #333333")
    puml.append("      FontSize 18")
    puml.append("      FontStyle bold")
    puml.append("   }")
    puml.append("}")
    puml.append("</style>")
    puml.append("")
    puml.append("title Zeitleiste der Versionsübergänge der FHIR-Profile")
    puml.append('footer Zuletzt verändert am %date("dd.MM.yyyy")')
    puml.append("")

    # Map package names to colors
    package_colors = {
        "kbv.ita.erp": "kbvcolor",
        "kbv.itv.evdga": "evdgacolor",
        "de.gematik.erezept-workflow.r4": "gematikcolor",
        "de.gematik.erezept-workflow.r4(FdV)": "gematikcolor_fdv",
        "de.gematik.erezept-patientenrechnung.r4": "gematikcolor_patrn",
        "de.gematik.erezept.eu.r4": "gematikcolor_eu",
        "de.abda.erezeptabgabedatenpkv": "davpkvcolor",
        "de.abda.erezeptabgabedaten": "davcolor",
        "de.gkvsv.eRezeptAbrechnungsdaten": "gkvsvcolor"
    }

    # Set project scale and start date with padding
    first_valid_from = datetime.strptime(configurations[0]["validFrom"], "%Y-%m-%d")
    project_start = (first_valid_from - timedelta(days=10)).strftime("%Y-%m-%d")
    puml.append("projectscale monthly zoom 3")
    puml.append(f"Project starts {project_start}")
    puml.append("")

    # Calculate the global end date
    last_config = configurations[-1]
    last_config_valid_from = datetime.strptime(last_config["validFrom"], "%Y-%m-%d")
    global_end_date = (last_config_valid_from + timedelta(days=60)).strftime("%Y-%m-%d")

    # Add configurations section
    puml.append("-- ERP-FD Konfigurationen --")
    puml.append("")
    for index, config in enumerate(configurations):
        valid_from = config["validFrom"]
        valid_to = config.get("validTo", None)

        # Add date markers
        if index != 0:
            puml.append(f"{valid_from} is colored datelinecolor")
        if valid_to:
            puml.append(f"{valid_to} is colored datelinecolor")
        # else:
        #     puml.append(f"{global_end_date} is colored datelinecolor")
        puml.append("")

        # Add configuration markers
        start_marker = (
            f"[Start Gültigkeit {config['name']} ({valid_from[8:10]}.{valid_from[5:7]}.{valid_from[:4]})] "
            f"happens on {valid_from}"
        )
        if index != 0:
            puml.append(start_marker)
        if valid_to:
            end_marker = (
                f"[Ende Gültigkeit {config['name']} ({valid_to[8:10]}.{valid_to[5:7]}.{valid_to[:4]})] "
                f"happens on {valid_to}"
            )
        # else:
        #     end_marker = (
        #         f"[Ende Gültigkeit {config['name']} ({global_end_date[8:10]}.{global_end_date[5:7]}.{global_end_date[:4]})] "
        #         f"happens on {global_end_date}"
        #     )
        puml.append(end_marker)
        puml.append("")

        # Add configuration task
        puml.append(f"[{config['name']}] starts {valid_from}")
        if valid_to:
            puml.append(f"[{config['name']}] ends {valid_to}")
        else:
            puml.append(f"[{config['name']}] ends {global_end_date}")
        puml.append(f"[{config['name']}] is colored in erpfdcolor")
        puml.append("")

    # Add package sections
    for mapping in package_mappings:
        package_name = mapping["package"]
        display_name = mapping["display"]
        package_color = package_colors.get(package_name, "kbvcolor")  # Default to kbvcolor if not mapped

        puml.append(f"-- {display_name} --")
        puml.append("")

        # Process versions of the package across all configurations
        package_versions = {}
        for config in configurations:
            valid_from = config["validFrom"]
            valid_to = config.get("validTo", None)

            for package in config["packages"]:
                if package["name"] == package_name:
                    for version in package["versions"]:
                        if version not in package_versions:
                            package_versions[version] = {
                                "start": valid_from,
                                "end": valid_to,
                            }
                        else:
                            package_versions[version]["end"] = valid_to

        # Add Gantt tasks for each version of the package
        for version, dates in package_versions.items():
            start_date = dates["start"]
            end_date = dates["end"]

            # Use the global end date if the last occurrence does not have a validTo
            if not end_date:
                end_date = global_end_date

            puml.append(f"[{package_name} {version}] starts {start_date} and ends {end_date}")
            puml.append(f"[{package_name} {version}] is colored in {package_color}")
            puml.append("")

    # End the Gantt diagram
    puml.append("@endgantt")
    return "\n".join(puml)

# Main script
if __name__ == "__main__":
    # Define the paths
    root_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the script
    config_dir = os.path.join(root_dir, "../configuration")
    output_dir = os.path.join(root_dir, "../../puml")

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Iterate through all JSON files in the configuration directory
    for filename in os.listdir(config_dir):
        if filename.endswith(".json"):
            config_path = os.path.join(config_dir, filename)
            output_file = os.path.splitext(filename)[0] + "_timeline.puml"
            output_path = os.path.join(output_dir, output_file)

            # Load JSON data
            try:
                with open(config_path, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    package_mappings = data["packageMappings"]
                    configurations = data["fhir_configurations"]
            except FileNotFoundError:
                print(f"Error: Configuration file not found at {config_path}")
                continue
            except json.JSONDecodeError as e:
                print(f"Error: Failed to parse JSON file {filename}. {e}")
                continue

            # Run sanity checks
            name_errors = validate_unique_configuration_names(configurations, filename)
            if name_errors:
                print(f"Configuration Name Errors in {filename}:")
                for error in name_errors:
                    print(f"  - {error}")
                continue
            
            errors = validate_dates(configurations)
            if errors:
                print(f"Sanity Check Errors in {filename}:")
                for error in errors:
                    print(f"  - {error}")
                continue

            # Validate package mappings
            missing_packages = validate_package_mappings(configurations, package_mappings)
            if missing_packages:
                print(f"Missing Package Mappings in {filename}:")
                for package in missing_packages:
                    print(f"  - {package}")
                continue

            # Validate package versions
            version_errors = validate_package_versions(configurations)
            if version_errors:
                print(f"Package Version Errors in {filename}:")
                for error in version_errors:
                    print(f"  - {error}")
                continue

            # Generate Gantt diagram
            gantt_output = generate_gantt(configurations, package_mappings)

            # Save Gantt output to file
            try:
                with open(output_path, "w", encoding="utf-8") as file:
                    file.write(gantt_output)
                print(f"Gantt diagram for {filename} saved to {output_path}")
            except Exception as e:
                print(f"Error: Failed to save Gantt file for {filename}. {e}")
