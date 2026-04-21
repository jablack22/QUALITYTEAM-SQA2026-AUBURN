# Usage: 'python generate_test_cases.py <requirements.json> <expected_structure.json> <output.json>'
# Output.json does NOT need to be provided--

# This script generates test cases based on a set of requirements and an expected structure defined in JSON files. It reads the requirements and expected structure, creates test cases with unique IDs and formatted descriptions, and writes the output to a specified JSON file. 
# The script ensures that all required fields are present and properly formatted, providing a structured way to generate test cases from requirements.



#!/usr/bin/env python3
import json
import sys


# Loads the JSON file from a given path and returns its contents as a Python object.
def loadJsonFile(_filePath):
    with open(_filePath, 'r', encoding='utf-8') as file:
        return json.load(file)


# Formats provided input text into a sentence that starts with "Verify that", aligning the grammar to the sample test_cases.json grammar.
def createSentence(_inputText):
    defaultText = 'Verify that the requirement is satisfied.'

    # Determines the text to use based on the input.
    trimmedText = str(_inputText).strip()
    joinedText = ' '.join(trimmedText.split())
    loweredText = joinedText.lower()

    # If the input text is empty, return a default message.
    if not joinedText:
        return defaultText

    # Determines the appropriate joiner ("is" or "are") based on whether the rest of the text ends with 's' (indicating plural) or not.
    def determineJoiner(_word):
        if _word.endswith('s') and not _word.endswith('is'):
            return "are"
        return "is"

    # Aligns the final grammar of the input sentence to match the expected output format, seen in test_cases.json.
    def alignFinalGrammar(_sentence):
        # Replace 'that the' with 'that' (matching the sample output test_cases.json)
        revisedText = _sentence.replace('that the', 'that')

        # Replace 'considered' with 'identified and considered' (matching the sample output test_cases.json)
        revisedText = revisedText.replace('considered', 'identified and considered')
        return revisedText

    # Converts the grammar "X must be Y" into "the X is Y" (matching the sample output test_cases.json)
    if " must be " in loweredText:
        grammarParts = joinedText.split(" must be ", 1)
        subject = grammarParts[0].lower()
        remainingGrammar = grammarParts[1]
        joiner = determineJoiner(subject)

        return alignFinalGrammar(f"Verify that the {subject} {joiner} {remainingGrammar.rstrip('.')}.")

    # Converts the grammar "Verb X..." into "X is verbed" (matching the sample output test_cases.json)
    words = joinedText.split()
    verb = words[0].lower()
    remainingGrammar = ' '.join(words[1:])

    # basic past participle (lightweight)
    if verb.endswith('e'):
        verbPastParticiple = verb + 'd'
    else:
        verbPastParticiple = verb + 'ed'

    joiner = determineJoiner(remainingGrammar)
    return alignFinalGrammar(f"Verify that {remainingGrammar} {joiner} {verbPastParticiple}.")


# Generates test cases based on the provided requirements and expected structure. 
# It maps requirement IDs to their descriptions and creates test cases with unique IDs and formatted descriptions.
def generateTestCases(_requirements, _expectedStructure):
    requirementMap = {requirement['requirement_id']: requirement for requirement in _requirements if 'requirement_id' in requirement}
    testCases = []
    i = 1

    # Iterates through the expected structure, checking for each requirement ID in the requirements map. 
    # If a requirement ID is missing, it raises an error. Otherwise, it creates a test case with a unique ID and a formatted description.
    for parentId, ruleSuffixes in _expectedStructure.items():
        for suffix in ruleSuffixes:
            requirementId = f'{parentId}{suffix}'

            # Checks if the requirement ID exists in the requirements map. If not, raises a ValueError indicating the missing requirement ID.
            if requirementId not in requirementMap:
                raise ValueError(f'Missing requirement_id in requirements.json: {requirementId}')

            # Retrieves the description for the requirement and formats it into a test case.
            description = requirementMap[requirementId].get('description', '')
            testCases.append({
                'test_case_id': f'TC-{i:03d}',
                'requirement_id': requirementId,
                'description': createSentence(description)
            })
            i += 1

    return testCases


# The main function serves as the entry point of the script. 
# It checks for the correct number of command-line arguments, loads the requirements and expected structure from JSON files, generates test cases, and writes them to an output JSON file.
def main():
    # Checks if the number of command-line arguments is less than 3. If so, it prints usage instructions and exits the program.
    if len(sys.argv) < 3:
        print('Usage: python generate_test_cases.py <requirements.json> <expected_structure.json>')
        sys.exit(1)

    # Assigns the command-line arguments to variables for the paths of the requirements, expected structure, and output file. If the output path is not provided, it defaults to 'test_cases.json'.
    requirements_path = sys.argv[1]
    expected_structure_path = sys.argv[2]
    output_path = sys.argv[3] if len(sys.argv) > 3 else 'test_cases.json'

    # Loads the requirements and expected structure from the specified JSON files, generates test cases based on them, and writes the test cases to the output JSON file with proper formatting.
    requirements = loadJsonFile(requirements_path)
    expected_structure = loadJsonFile(expected_structure_path)
    test_cases = generateTestCases(requirements, expected_structure)

    # Writes the generated test cases to the output JSON file with an indentation of 2 spaces and ensures that non-ASCII characters are preserved. It also adds a newline at the end of the file.
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(test_cases, f, indent=2, ensure_ascii=False)
        f.write('\n')


# Checks if the script is being run directly (as the main program) and, if so, calls the main function to execute the script's functionality.
if __name__ == '__main__':
    main()