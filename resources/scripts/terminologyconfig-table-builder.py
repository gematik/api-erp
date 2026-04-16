import json
import sys
from pathlib import Path
from datetime import datetime, timedelta

RED = "\033[31m"
RESET = "\033[0m"

# Define the paths
resources_path = Path(__file__).resolve().parent.parent
base_path = resources_path / "configuration_terminology"
output_path = resources_path / "scripts" / "output_adoc"
output_file = output_path / "terminology_table.adoc"

# Ensure the output directory exists
output_path.mkdir(parents=True, exist_ok=True)

# Helper function to reformat date to German format
def format_date(date_str):
    if date_str == "-":
        return "-"
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%d.%m.%Y")
    except ValueError:
        return date_str

# Helper function to parse date strings
def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d") if date_str != "-" else None
    except ValueError:
        return None


def earliest_date_str(date_a, date_b):
    if date_a == "-":
        return date_b
    if date_b == "-":
        return date_a

    parsed_a = parse_date(date_a)
    parsed_b = parse_date(date_b)
    if parsed_a and parsed_b:
        return date_a if parsed_a <= parsed_b else date_b
    return date_a


# Global registry to track terminologies and versions
terminology_registry = {}

# Sanity check functions
def check_unique_transition_names(file_data):
    transition_names = [data.get("name", "") for data in file_data]
    if len(transition_names) != len(set(transition_names)):
        raise ValueError("Duplicate transition names found across files.")

def check_configuration_name_continuity(file_data):
    previous_last_name = None
    for data in file_data:
        configurations = data.get("terminology_configurations", [])
        if not configurations:
            continue

        first_name = configurations[0].get("name", "")
        if previous_last_name and first_name != previous_last_name:
            raise ValueError(f"Configuration name mismatch: {first_name} does not match previous {previous_last_name}.")

        previous_last_name = configurations[-1].get("name", "")

def check_terminologies_in_mappings(data):
    terminology_mappings = {mapping.get("terminology", "") for mapping in data.get("terminologyMappings", [])}
    for config in data.get("terminology_configurations", []):
        for terminology in config.get("terminologies", []):
            if terminology.get("name", "") not in terminology_mappings:
                raise ValueError(f"Terminology {terminology.get('name', '')} is not listed in terminologyMappings.")

def check_date_consistency(data):
    for terminology_name, configs in group_configurations_by_terminology(data).items():
        previous_valid_to = None
        # Sort by validFrom to make checks independent from input ordering.
        sorted_configs = sorted(configs, key=lambda cfg: parse_date(cfg[1]) or datetime.min)
        for _, valid_from, valid_to in sorted_configs:
            valid_from_date = parse_date(valid_from)
            valid_to_date = parse_date(valid_to)

            if previous_valid_to and valid_from_date != previous_valid_to + timedelta(days=1):
                raise ValueError(f"Date gap or inconsistency found for terminology {terminology_name}: {previous_valid_to} to {valid_from_date}.")

            previous_valid_to = valid_to_date


def normalize_terminologies(config):
    normalized = {}
    for terminology in config.get("terminologies", []):
        terminology_name = terminology.get("name", "")
        terminology_version = terminology.get("version", "")

        if terminology_name in normalized and normalized[terminology_name] != terminology_version:
            raise ValueError(
                f"Terminology {terminology_name} has conflicting versions "
                f"({normalized[terminology_name]} and {terminology_version}) in configuration {config.get('name', '')}."
            )

        normalized[terminology_name] = terminology_version

    return normalized


def check_cross_file_configuration_continuity(file_entries):
    previous_file_name = None
    previous_last_config = None

    for file_name, data in file_entries:
        configurations = data.get("terminology_configurations", [])
        if not configurations:
            continue

        first_config = configurations[0]
        if previous_last_config is not None:
            previous_name = previous_last_config.get("name", "")
            current_name = first_config.get("name", "")
            if current_name != previous_name:
                raise ValueError(
                    f"Cross-file configuration name mismatch between {previous_file_name} and {file_name}: "
                    f"first configuration '{current_name}' does not match previous last configuration '{previous_name}'."
                )

            previous_valid_from = previous_last_config.get("validFrom", "-")
            current_valid_from = first_config.get("validFrom", "-")
            if current_valid_from != previous_valid_from:
                raise ValueError(
                    f"Cross-file validFrom mismatch between {previous_file_name} and {file_name} "
                    f"for configuration '{current_name}': {current_valid_from} != {previous_valid_from}."
                )

            previous_terminologies = normalize_terminologies(previous_last_config)
            current_terminologies = normalize_terminologies(first_config)
            if current_terminologies != previous_terminologies:
                missing = sorted(set(previous_terminologies) - set(current_terminologies))
                added = sorted(set(current_terminologies) - set(previous_terminologies))
                changed = sorted(
                    terminology_name
                    for terminology_name in set(previous_terminologies).intersection(current_terminologies)
                    if previous_terminologies[terminology_name] != current_terminologies[terminology_name]
                )

                raise ValueError(
                    f"Cross-file terminology/version mismatch between {previous_file_name} and {file_name} "
                    f"for configuration '{current_name}'. "
                    f"Missing: {missing or '-'}, Added: {added or '-'}, "
                    f"Changed versions: {changed or '-'}"
                )

        previous_last_config = configurations[-1]
        previous_file_name = file_name

def group_configurations_by_terminology(data):
    grouped = {}
    for config in data.get("terminology_configurations", []):
        valid_from = config.get("validFrom", "-")
        valid_to = config.get("validTo", "-")
        for terminology in config.get("terminologies", []):
            terminology_name = terminology.get("name", "")
            version = terminology.get("version", "")

            if terminology_name not in grouped:
                grouped[terminology_name] = []

            grouped[terminology_name].append((version, valid_from, valid_to))

    return grouped

def update_registry(terminology_name, version, valid_from, valid_to):
    global terminology_registry

    # Check if the terminology and version already exist
    if (terminology_name, version) in terminology_registry:
        # Merge validity range across all configurations using the same version.
        previous_entry = terminology_registry[(terminology_name, version)]
        previous_entry["validFrom"] = earliest_date_str(previous_entry["validFrom"], valid_from)
        previous_entry["validTo"] = valid_to
    else:
        # Add a new entry to the registry
        terminology_registry[(terminology_name, version)] = {
            "validFrom": valid_from,
            "validTo": valid_to
        }

def rebuild_table_from_registry():
    # Group the registry by terminologywechsel for table rendering
    grouped_by_transition = {}
    for (terminology_name, version), dates in terminology_registry.items():
        valid_from = dates["validFrom"]
        valid_to = dates["validTo"]

        if valid_from not in grouped_by_transition:
            grouped_by_transition[valid_from] = {}

        if terminology_name not in grouped_by_transition[valid_from]:
            grouped_by_transition[valid_from][terminology_name] = []

        grouped_by_transition[valid_from][terminology_name].append((version, valid_from, valid_to))

    # Return a deterministically sorted structure for stable output.
    sorted_grouped = {}
    for transition in sorted(grouped_by_transition.keys(), key=lambda d: parse_date(d) or datetime.max):
        sorted_grouped[transition] = {}
        for terminology_name in sorted(grouped_by_transition[transition].keys()):
            versions = grouped_by_transition[transition][terminology_name]
            sorted_versions = sorted(
                versions,
                key=lambda item: ((parse_date(item[1]) or datetime.max), item[0])
            )
            sorted_grouped[transition][terminology_name] = sorted_versions

    return sorted_grouped

# Helper function to format merged table rows
def format_merged_row(terminologywechsel, terminologies_with_versions):
    # Calculate the total number of rows for this Terminologiewechsel
    total_rows = sum(len(versions) for versions in terminologies_with_versions.values())

    # Merge the first column (Terminologiewechsel)
    row = f".{total_rows}+| {terminologywechsel} \n\n"

    # Add rows for each terminology and its versions
    for terminology_name, versions in terminologies_with_versions.items():
        # Merge the second column (Terminologien)
        row += f"  .{len(versions)}+| {terminology_name} \n"

        # Add individual rows for each version
        for version, valid_from, valid_to in versions:
            row += f"    | {version} | {format_date(valid_from)} | {format_date(valid_to)} \n"

    return row

def main():
    global terminology_registry
    terminology_registry = {}

    # Load all JSON files
    file_entries = []
    for json_file in sorted(base_path.glob("*.json")):
        with open(json_file, "r", encoding="utf-8") as file:
            file_entries.append((json_file.name, json.load(file)))

    file_data = [data for _, data in file_entries]

    # Perform sanity checks
    check_unique_transition_names(file_data)
    check_configuration_name_continuity(file_data)
    check_cross_file_configuration_continuity(file_entries)
    for data in file_data:
        check_terminologies_in_mappings(data)
        check_date_consistency(data)

    # Initialize the table content
    table_content = "|===\n| Terminologiewechsel | Terminologien | Version | Gültig ab | Gültig bis\n\n"

    # Iterate through all JSON files to update the registry
    for _, data in file_entries:
        terminology_configurations = data.get("terminology_configurations", [])

        # Update the registry with all terminologies and their versions
        for config in terminology_configurations:
            valid_from = config.get("validFrom", "-")
            valid_to = config.get("validTo", "-")
            for terminology in config.get("terminologies", []):
                terminology_name = terminology.get("name", "")
                version = terminology.get("version", "")
                update_registry(terminology_name, version, valid_from, valid_to)

    # Rebuild the table from the updated registry
    grouped_registry = rebuild_table_from_registry()
    for terminologywechsel, terminologies_with_versions in grouped_registry.items():
        table_content += format_merged_row(terminologywechsel, terminologies_with_versions)
        table_content += "\n"

    # Close the table
    table_content += "|===\n"

    # Write the table to the output file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(table_content)


if __name__ == "__main__":
    try:
        main()
    except ValueError as error:
        print(f"{RED}ERROR: {error}{RESET}", file=sys.stderr)
        sys.exit(1)
    except Exception as error:
        print(f"{RED}ERROR: Unexpected failure: {error}{RESET}", file=sys.stderr)
        sys.exit(1)