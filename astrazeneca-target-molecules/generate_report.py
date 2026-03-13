#!/usr/bin/env python3
import json
import os
import glob
from pathlib import Path

# Configuration
TOPIC = "astrazeneca-target-molecules"
RESULTS_DIR = os.path.expanduser("~/.openclaw/workspace/astrazeneca-target-molecules/results")
OUTPUT_FILE = os.path.expanduser("~/.openclaw/workspace/astrazeneca-target-molecules/report.md")

# Category mapping for different possible key names
CATEGORY_MAPPING = {
    "basic_info": ["basic_info", "Basic Info"],
    "development": ["development", "Development"],
    "mechanism": ["mechanism", "Mechanism"],
    "clinical": ["clinical", "Clinical"],
    "market": ["market", "Market"],
}

def find_field(data, possible_keys):
    """Find a field using possible keys, searching through nested structure"""
    if isinstance(data, dict):
        for key in possible_keys:
            if key in data:
                return data[key]
        # Search recursively
        for value in data.values():
            result = find_field(value, possible_keys)
            if result is not None:
                return result
    return None

def format_value(value, indent=0):
    """Format a value for markdown display"""
    if value is None or value == "":
        return None
    
    if isinstance(value, bool):
        return "Yes" if value else "No"
    
    if isinstance(value, (int, float)):
        return str(value)
    
    if isinstance(value, list):
        if not value:
            return None
        # Check if list of dicts
        if isinstance(value[0], dict):
            return "; ".join([", ".join([f"{k}: {v}" for k, v in d.items()]) for d in value])
        # Regular list
        return ", ".join(str(v) for v in value)
    
    if isinstance(value, dict):
        items = []
        for k, v in value.items():
            formatted = format_value(v)
            if formatted:
                items.append(f"{k}: {formatted}")
        return " | ".join(items) if items else None
    
    # String - check for uncertain marker
    value_str = str(value)
    if "[uncertain]" in value_str:
        return None
    return value_str

def get_all_fields(json_data):
    """Extract all fields from JSON, handling nested structure"""
    fields = {}
    
    def extract_from_dict(d, prefix=""):
        if not isinstance(d, dict):
            return
        for key, value in d.items():
            if key == "uncertain" or key.startswith("_"):
                continue
            full_key = f"{prefix}{key}" if prefix else key
            if isinstance(value, dict):
                extract_from_dict(value, f"{full_key}.")
            else:
                fields[full_key] = value
    
    extract_from_dict(json_data)
    return fields

# Main execution
print(f"Generating report for {TOPIC}...")

# Read fields.yaml to get field structure
fields_yaml = {}
if os.path.exists(f"./{TOPIC}/fields.yaml"):
    import yaml
    try:
        with open(f"./{TOPIC}/fields.yaml", 'r') as f:
            fields_yaml = yaml.safe_load(f)
    except:
        pass

# Get all JSON files
json_files = sorted(glob.glob(f"{RESULTS_DIR}/*.json"))
print(f"Found {len(json_files)} JSON files")

# Parse all results
results = []
for json_file in json_files:
    with open(json_file, 'r') as f:
        data = json.load(f)
        
    # Extract key fields for TOC
    name = find_field(data, ["name", "Name"]) or os.path.basename(json_file).replace(".json", "").replace("_", " ")
    target = find_field(data, ["target", "Target"])
    therapeutic_area = find_field(data, ["therapeutic_area", "therapeuticArea", "Therapeutic Area"])
    development_stage = find_field(data, ["development_stage", "developmentStage", "Development Stage"])
    drug_modality = find_field(data, ["drug_modality", "drugModality", "Drug Modality"])
    approval_year = find_field(data, ["approval_year", "approvalYear", "Approval Year"])
    
    # Get all fields for detail section
    all_fields = get_all_fields(data)
    
    # Get uncertain fields
    uncertain_fields = data.get("uncertain", [])
    
    results.append({
        "name": name,
        "target": target,
        "therapeutic_area": therapeutic_area,
        "development_stage": development_stage,
        "drug_modality": drug_modality,
        "approval_year": approval_year,
        "all_fields": all_fields,
        "uncertain_fields": uncertain_fields
    })

# Generate markdown report
md_content = f"""# {TOPIC.replace("-", " ").title()} - Research Report

Generated: {__import__('datetime').datetime.now().strftime('%Y-%m-%d')}

---

## Table of Contents

| # | Molecule | Target | Therapeutic Area | Stage | Modality | Approval |
|---|----------|--------|------------------|-------|----------|----------|
"""

for i, r in enumerate(results, 1):
    target = r["target"] or "-"
    therapeutic = r["therapeutic_area"] or "-"
    stage = r["development_stage"] or "-"
    modality = r["drug_modality"] or "-"
    approval = r["approval_year"] or "-"
    
    # Create anchor
    anchor = r["name"].lower().replace(" ", "-").replace("(", "").replace(")", "").replace("/", "-")
    
    md_content += f"| {i} | [{r['name']}](#{anchor}) | {target} | {therapeutic} | {stage} | {modality} | {approval} |\n"

md_content += "\n---\n\n"

# Add detailed sections
for r in results:
    anchor = r["name"].lower().replace(" ", "-").replace("(", "").replace(")", "").replace("/", "-")
    
    md_content += f"## {r['name']}\n\n"
    md_content += f"- **Target:** {r['target'] or '-'}\n"
    md_content += f"- **Therapeutic Area:** {r['therapeutic_area'] or '-'}\n"
    md_content += f"- **Development Stage:** {r['development_stage'] or '-'}\n"
    md_content += f"- **Drug Modality:** {r['drug_modality'] or '-'}\n"
    md_content += f"- **Approval Year:** {r['approval_year'] or '-'}\n\n"
    
    # Add all other fields
    for field_name, field_value in r["all_fields"].items():
        # Skip already displayed fields
        if field_name in ["target", "therapeutic_area", "development_stage", "drug_modality", "approval_year", "name", "company"]:
            continue
        # Skip uncertain
        if field_value and "[uncertain]" in str(field_value):
            continue
        
        formatted = format_value(field_value)
        if formatted:
            # Make field name readable
            readable_name = field_name.replace("_", " ").replace(".", " - ").title()
            md_content += f"- **{readable_name}:** {formatted}\n"
    
    md_content += "\n---\n\n"

# Write report
with open(OUTPUT_FILE, 'w') as f:
    f.write(md_content)

print(f"Report generated: {OUTPUT_FILE}")
print(f"Total molecules: {len(results)}")
