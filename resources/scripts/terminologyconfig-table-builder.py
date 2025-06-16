import os
import json
from pathlib import Path
from datetime import datetime, timedelta

# Define the paths
base_path = Path("../configuration_terminology")
output_path = Path("output_adoc")
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
        for _, valid_from, valid_to in configs:
            valid_from_date = parse_date(valid_from)
            valid_to_date = parse_date(valid_to)

            if previous_valid_to and valid_from_date != previous_valid_to + timedelta(days=1):
                raise ValueError(f"Date gap or inconsistency found for terminology {terminology_name}: {previous_valid_to} to {valid_from_date}.")

            previous_valid_to = valid_to_date

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
        # Update the validTo of the previous entry if the new validTo is later
        previous_entry = terminology_registry[(terminology_name, version)]
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

    return grouped_by_transition

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

# Load all JSON files
file_data = []
for json_file in sorted(base_path.glob("*.json")):
    with open(json_file, "r", encoding="utf-8") as file:
        file_data.append(json.load(file))

# Perform sanity checks
check_unique_transition_names(file_data)
check_configuration_name_continuity(file_data)
for data in file_data:
    check_terminologies_in_mappings(data)
    check_date_consistency(data)

# Initialize the table content
table_content = "|===\n| Terminologiewechsel | Terminologien | Version | Gültig ab | Gültig bis\n\n"

# Iterate through all JSON files to update the registry
for json_file in sorted(base_path.glob("*.json")):
    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)

        terminologywechsel = data.get("name", "-")
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