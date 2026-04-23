import json
import re
import argparse
import os

# ---------- Arguments ----------
parser = argparse.ArgumentParser(description="Generate requirement JSON from CFR Markdown")
parser.add_argument("--input", "-i", required=True, help="Input Markdown file (.md)")
parser.add_argument("--output", "-o", required=True, help="Output JSON file")
parser.add_argument("--cfr", "-c", required=True, help="CFR section (e.g., 21 CFR 117.130)")
args = parser.parse_args()

INPUT_MD = args.input
OUTPUT_JSON = args.output
CFR_SECTION = args.cfr

# Derive path for expected_structure.json based on output directory
EXPECTED_STRUCT_JSON = os.path.join(os.path.dirname(OUTPUT_JSON), "expected_structure.json")

# ---------- Read File ----------
with open(INPUT_MD, "r") as f:
    lines = [line.strip() for line in f if line.strip()]

all_requirements = []
current_req = None

# ---------- Parse ----------
for line in lines:
    # Capture REQ ID
    req_match = re.search(r"→\s*(REQ-[\d\.]+-\d+)", line)
    if req_match:
        current_req = req_match.group(1)
        continue

    # Capture atomic rules
    atomic_match = re.match(r"^(.*?)\s*→\s*([A-Z]\d*)$", line)
    if atomic_match and current_req:
        raw_description = atomic_match.group(1).strip()
        
        # Ignore parent/child numbering in the Markdown
        clean_description = re.sub(r"^[-*]\s*(\([a-z0-9]+\))?\s*", "", raw_description).strip()
        
        suffix = atomic_match.group(2)
        requirement_id = f"{current_req}{suffix}"

        # Correctly assign parent/child relationships
        if len(suffix) == 1:
            parent = current_req
        else:
            parent = f"{current_req}{suffix[0]}"

        all_requirements.append({
            "requirement_id": requirement_id,
            "description": clean_description,
            "source": CFR_SECTION,
            "parent": parent,
            "suffix": suffix
        })

# Pick 10 atomic rules
selected_requirements = all_requirements[:10]

# Generate expected_structure.json mapping
expected_structure = {}
final_requirements = []

for req in selected_requirements:
    parent = req["parent"]
    suffix = req.pop("suffix")
    
    if parent not in expected_structure:
        expected_structure[parent] = []
    
    if suffix not in expected_structure[parent]:
        expected_structure[parent].append(suffix)
        
    final_requirements.append(req)

# ---------- Save Outputs ----------
with open(OUTPUT_JSON, "w") as f:
    json.dump(final_requirements, f, indent=2)

with open(EXPECTED_STRUCT_JSON, "w") as f:
    json.dump(expected_structure, f, indent=2)

print(f"Saved 10 requirements → {OUTPUT_JSON}")
print(f"Saved expected structure → {EXPECTED_STRUCT_JSON}")
