import json
import logging
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REQ_FILE = os.path.join(BASE_DIR, 'requirements.json')
STRUCTURE_FILE = os.path.join(BASE_DIR, 'expected_structure.json')
LOG_FILE = os.path.join(BASE_DIR, 'forensics.log')

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.info("Validation started")

with open(REQ_FILE) as f:
    reqs = json.load(f)

    logging.info("Loaded requirements.json successfully")

with open(STRUCTURE_FILE) as f:
    expected = json.load(f)
    logging.info("Loaded expected_structure.json successfully")

for parent, expected_ids in expected.items():
    logging.info(f"Validating structure for parent requirement {parent}")
    logging.info(f"Expected child suffixes: {expected_ids}")

    found = []

    for r in reqs:
        if r.get("parent") == parent:
            suffix = r["requirement_id"][-1]
            found.append(suffix)
            logging.info(f"Found child requirement {r['requirement_id']} with suffix {suffix}")
    
    for e in expected_ids:
        if e not in found:
            logging.error(f"Validation failed: missing requirement suffix {e} under parent {parent}")
            raise Exception(f"Missing requirement {e} under parent {parent}")

logging.info("Validation completed successfully")
print("Validation Passed")

