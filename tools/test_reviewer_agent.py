# pragma: no cover
import os

def collect_project_files():
    project_files = {}

    for root, dirs, files in os.walk("."):
        # Skip git and other irrelevant dirs
        if ".git" in root or ".github" in root or "venv" in root:
            continue

        for name in files:
            if name.endswith(".py"):
                path = os.path.join(root, name)
                with open(path, "r", encoding="utf-8") as f:
                    project_files[path] = f.read()

    return project_files

import subprocess

def get_changed_files():
    try:
        diff_output = subprocess.check_output(
            ["git", "diff", "--name-only", "origin/main...HEAD"]
        ).decode().strip().split("\n")
    except:
        try:
            diff_output = subprocess.check_output(
                ["git", "diff", "--name-only", "main...HEAD"]
            ).decode().strip().split("\n")
        except Exception:
            return []

    return [f for f in diff_output if f and f.endswith(".py")]


def match_changed_files(changed_files, project_files):
    """Return the list of keys from project_files that correspond to changed_files.

    Matching is done by normalizing path separators and comparing end-paths
    so git-relative paths match keys produced by os.walk on different platforms.
    """
    def norm(p):
        return p.replace("\\", "/").lstrip("./").lstrip("/")

    matched = set()
    norm_map = {path: norm(path) for path in project_files.keys()}

    for cf in changed_files:
        cn = norm(cf)
        for orig_path, kn in norm_map.items():
            if kn == cn or kn.endswith("/" + cn) or cn.endswith("/" + kn) or kn.endswith(cn) or os.path.basename(kn) == os.path.basename(cn):
                matched.add(orig_path)

    return sorted(matched)

from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()

client = OpenAI()  # automatically uses OPENAI_API_KEY

def review_tests(files, changed_files):
    prompt = (
        "You are a Test Reviewer Agent.\n"
        "You see the entire project (source + tests).\n"
        "You also get a list of files changed in this PR.\n"
        "Focus your analysis on the changed files, but consider all tests when judging coverage.\n\n"
        f"Changed files in this PR:\n{chr(10).join(changed_files) if changed_files else 'None'}\n\n"
        "Tasks:\n"
        "1. For the changed files, say which functions/classes are tested.\n"
        "2. For the changed files, say which are untested.\n"
        "3. Point out missing edge cases.\n"
        "4. Suggest concrete new tests (with code) that should be added.\n"
    )

    # Map changed files to the collected project files keys
    matched_changed = match_changed_files(changed_files, files) if changed_files else []

    # Collect test files (files under tests/ or starting with test_)
    test_files = []
    for path in files.keys():
        n = path.replace("\\", "/")
        if "/tests/" in n or os.path.basename(n).startswith("test_"):
            test_files.append(path)

    # Build the limited set of files to include: changed + tests
    include_paths = []
    if matched_changed:
        include_paths.extend(matched_changed)
    else:
        # If we couldn't detect changed files, include changed_files strings for context
        prompt += "\nNote: No changed files could be mapped to the project files.\n"

    # Always include tests to allow coverage judgement
    for p in test_files:
        if p not in include_paths:
            include_paths.append(p)

    # append file contents but limit size per file to avoid hitting token limits
    max_chars_per_file = 15000
    for path in include_paths:
        code = files.get(path, "")
        if len(code) > max_chars_per_file:
            code_snippet = code[:max_chars_per_file] + "\n\n# (truncated)"
        else:
            code_snippet = code
        prompt += f"\n--- FILE: {path} ---\n{code_snippet}\n"

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content
    except Exception as e:
        return f"Error calling OpenAI API: {e}"


if __name__ == "__main__":
    all_files = collect_project_files()
    changed_files = get_changed_files()

    report = review_tests(all_files, changed_files)
    print(report)