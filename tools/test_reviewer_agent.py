import os

def load_python_files(root_dir):
    files = {}
    for dirpath, _, filenames in os.walk(root_dir):
        for name in filenames:
            if name.endswith(".py"):
                full_path = os.path.join(dirpath, name)
                with open(full_path, "r", encoding="utf-8") as f:
                    files[full_path] = f.read()
    return files


from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()

client = OpenAI()  # automatically uses OPENAI_API_KEY

def review_tests(files):
    prompt = (
        "You are a Test Reviewer Agent.\n"
        "Your job is to analyze the project's Python code and its tests.\n"
        "Identify:\n"
        "1. Which functions/classes are tested\n"
        "2. Which are untested\n"
        "3. Missing edge cases\n"
        "4. Suggested new test cases\n\n"
    )

    for path, code in files.items():
        prompt += f"\n--- FILE: {path} ---\n{code}\n"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    project_root = "."  # or "src" if you want to limit scope
    files = load_python_files(project_root)
    report = review_tests(files)
    print(report)