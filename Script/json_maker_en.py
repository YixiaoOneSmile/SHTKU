import os
import json
import re

# Define the path to the directory containing .md files
md_directory = 'SHTKUQuestionBank'  # Replace with your folder path

# JSON output list
output = []
id_counter = 1

# Retrieve all .md files in the directory and manually sort them in natural order
files = [f for f in os.listdir(md_directory) if f.endswith('.md')]

# Sort files in natural order (to handle numbering like '1.1', '1.2', '2.1')
files.sort(key=lambda f: [int(x) if x.isdigit() else x for x in re.split(r'(\d+)', f)])

# Iterate over the sorted .md files
for filename in files:
    file_path = os.path.join(md_directory, filename)

    # Open and read the content of the .md file
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Extract question information from each file
    question = None
    answers = []
    correct_answer = None
    title = None

    for i, line in enumerate(lines):
        line = line.strip()

        # Identify the question title (starts with ###)
        if line.startswith("###"):
            title = re.sub(r"^\d+(\.\d+)?\s*", "", line.lstrip("# ").replace("**", "").replace(". ", "").strip())

        # Identify the question stem (next line after "- " prefix)
        elif line.startswith("- ") and title:
            # Combine title and question stem
            question = f"{title}: {line[2:].strip()}"
            answers = []
            correct_answer = None
            title = None  # Reset title

        # Identify answer options (starting with "- A.", "- B.", etc.)
        elif re.match(r"- [A-D]\.", line):
            label = line[2]  # Get the option label (A, B, C, D)
            text = line[5:].strip()  # Get the option text
            answers.append({"label": label, "text": text})

        # Identify the correct answer (starting with "**Correct Answer:")
        elif line.startswith("- **Correct Answer:"):
            correct_answer = line.split(":")[-1].replace("**", "").strip()

        # If the current line is empty and a question is complete, save the question info
        if line == "" and question:
            output.append({
                "id": id_counter,
                "question": question,
                "answers": answers,
                "correct_answer": correct_answer
            })
            id_counter += 1
            question = None

    # Handle the last question in the file
    if question:
        output.append({
            "id": id_counter,
            "question": question,
            "answers": answers,
            "correct_answer": correct_answer
        })

# Convert to JSON format
json_output = json.dumps(output, indent=4, ensure_ascii=False)

# Print or save as JSON file
output_file = os.path.join(md_directory, 'question_bank.json')
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(json_output)

print(f"JSON file created: {output_file}")
