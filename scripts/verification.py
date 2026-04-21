import json
import logging

logging.basicConfig(
    filename='forensics.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.info("Verification started")

with open('requirements.json') as f:
    reqs = json.load(f)
    logging.info("Loaded requirements.json successfully")

with open('test_cases.json') as f:
    tests = json.load(f)
    logging.info("Loaded test_cases.json successfully")

req_ids = [r["requirement_id"] for r in reqs]
logging.info(f"Collected {len(req_ids)} requirement IDs")

for t in tests:
    tc_id = t.get("test_case_id", "UNKNOWN_TC")
    req_id = t.get("requirement_id", "MISSING_REQ_ID")
    logging.info(f"Checking test case {tc_id} linked to requirement {req_id}")

    if req_id not in req_ids:
        logging.error(f"Verification failed: {req_id} not found for test case {tc_id}")
        raise Exception(f"Test failed: {req_id} not found")

    logging.info(f"Verification passed for test case {tc_id}")

logging.info("Verification completed successfully")
print("Verification Passed")
