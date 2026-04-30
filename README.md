**SQA2026 Quality Team Group Report**

**Reproducability**

Windows (from project root):
- python scripts/generate_requirements.py -i "Input_CFR_File/CFR-117.130.md" -o "output.json" -c "21 CFR 117.130"
- python scripts/generate_test_cases.py requirements.json expected_structure.json test_cases.json
- python scripts/validation.py
- python scripts/verification.py

Mac (from project root):
- python3 script_name.py
- python3 scripts/generate_test_cases.py requirements.json expected_structure.json test_cases.json
- python3 scripts/validation.py
- python3 scripts/verification.py

**End Result:**

Expected files produced: 
- output.json: A list of generated requirements from the input CFR file
- test_cases.json: A list of generated test cases
- expected_structure.json: The expected structure of the generated requirements and test cases, used for validation
- forensics.log: A log file containing the results of the validation and verification processes, including any discrepancies found and the final outcomes of each step.

Expected logs (printed in terminal):
- "Saved 10 requirements -> output.json"
- "Validation Passed"
- "Verification Passed"

**Objectives:**
- The objectives of this project are to develop a CI/CD pipeline for the verification and validation of requirements, ensuring that the generated test cases are consistent with the specified requirements and that the results are logged for traceability.


**Groupmates**:

Jack Blackmon
- Activities I performed:
  - I built the GitHub Actions CI/CD pipeline seen in .github/workflows.
- What I've learned: 
  - I learned how to setup the main.yml file to automate our V&V scripts on every push.

Maxwell Achanti
- Activities I performed:
  - .
- What I've learned: 
  - .

SJ Han
- Activities I performed:
  - I implemented the verification and validation scripts and integrated forensic logging.
- What I've learned:
  - I learned how to ensure requirement consistency and apply logging in CI workflows.

Rayce Giles
- Activities I performed:
  - I implemented the test case generation for the project, seen in generate_test_cases.py.
- What I've learned: 
  - I learned how to tailor test cases for LLM generation and processing.
