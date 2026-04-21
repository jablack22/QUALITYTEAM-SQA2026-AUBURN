import json
import logging

logging.basicConfig(
    filename='forensics.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.info("Validation started")

with open('requirements.json') as f:
    reqs = json.load(f)
    logging.info("Loaded requirements.json successfully")

with open('expected_structure.json') as f:
    expected = json.load(f)
    logging.info("Loaded expected_structure.json successfully")

parent = "REQ-HAZ-001"
logging.info(f"Validating structure for parent requirement {parent}")

expected_ids = expected[parent]
logging.info(f"Expected child suffixes: {expected_ids}")

found = []

for r in reqs:
    if r["parent"] == parent:
        suffix = r["requirement_id"][-1]
        found.append(suffix)
        logging.info(f"Found child requirement {r['requirement_id']} with suffix {suffix}")

for e in expected_ids:
    if e not in found:
        logging.error(f"Validation failed: missing requirement suffix {e} under parent {parent}")
        raise Exception(f"Missing requirement {e}")

logging.info("Validation completed successfully")
print("Validation Passed")
