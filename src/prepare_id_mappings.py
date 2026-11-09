
import csv
from pathlib import Path

# Project folders
project_dir = Path(r"C:\Projects\healthcare-data-analytics")
input_file = project_dir / "data" / "raw" / "IDS_mapping.csv"
output_dir = project_dir / "data" / "processed"

output_dir.mkdir(parents=True, exist_ok=True)

# Each section's header and output filename
sections = {
    "admission_type_id": "admission_type_mapping.csv",
    "discharge_disposition_id": "discharge_disposition_mapping.csv",
    "admission_source_id": "admission_source_mapping.csv",
}

# Read the original file and separate its three sections
with input_file.open("r", encoding="utf-8-sig", newline="") as file:
    rows = list(csv.reader(file))

current_section = None
mapping_data = {key: [] for key in sections}

for row in rows:
    if not row or not any(cell.strip() for cell in row):
        continue

    first_cell = row[0].strip()

    # A section header identifies which mapping we are reading
    if first_cell in sections:
        current_section = first_cell
        continue

    # Skip rows that do not belong to a recognised section
    if current_section is None or len(row) < 2:
        continue

    mapping_id = row[0].strip()
    description = row[1].strip()

    if mapping_id:
        mapping_data[current_section].append([mapping_id, description])

# Save each section as a separate, clean CSV
for section, output_filename in sections.items():
    output_file = output_dir / output_filename

    with output_file.open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([section, "description"])
        writer.writerows(mapping_data[section])

    print(f"{output_filename}: {len(mapping_data[section])} mappings saved")

print("\nAll three mapping files have been created.")
