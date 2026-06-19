"""
Code Climate CLI Tool
---------------------
This program analyzes a Python file and generates a "health score"
based on:
1. Line statistics (total, blank, code, comments)
2. Code complexity (control structures)
3. Comment usage (including docstrings)
4. Variable naming conventions

"""

import re
import json
import sys


# FUNCTION 1: LINE ANALYSIS
def analyze_lines(lines):
#Counts total lines, blank lines, and code lines.
    total = len(lines)
    blank = sum(1 for line in lines if line.strip() == "")
    code = total - blank
    return total, blank, code


# FUNCTION 2: COMPLEXITY CHECK
def check_complexity(lines):
    #Counts control flow keywords to estimate complexity.
    keywords = ["if", "elif", "else", "for", "while"]
    counts = {key: 0 for key in keywords}

    for line in lines:
        stripped = line.strip()

        # Ignore comments
        if stripped.startswith("#"):
            continue

        for key in keywords:
            if re.search(rf"\b{key}\b", line):
                counts[key] += 1

    return counts


# FUNCTION 3: COMMENT COUNTING (FIXED)
def count_comments(lines):
    """
    Counts all comments including:
    - Single line comments (#)
    - Multi-line docstrings (triple quotes)
    """
    comment_lines = 0
    in_docstring = False

    for line in lines:
        stripped = line.strip()

        # Detect start/end of docstrings
        if stripped.startswith('"""') or stripped.startswith("'''"):
            in_docstring = not in_docstring
            comment_lines += 1

        elif in_docstring:
            comment_lines += 1

        elif stripped.startswith("#"):
            comment_lines += 1

    return comment_lines


# FUNCTION 4: VARIABLE CHECK
SKIP_KEYWORDS = {
    "if", "elif", "else", "for", "while", "return",
    "True", "False", "None", "and", "or", "not", "in",
    "import", "from", "class", "def", "lambda", "self", "cls"
}


def check_variables(lines):
    #Detects variables that do NOT follow snake_case naming.
    pattern = re.compile(r"^\s*([a-zA-Z_]\w*)\s*(?<!=)=(?!=)")
    snake_case = re.compile(r"^[a-z_][a-z0-9_]*$")
    invalid_vars = set()

    for line in lines:
        stripped = line.strip()

        # Ignore empty lines and comments
        if not stripped or stripped.startswith("#"):
            continue

        match = pattern.match(line)

        if match:
            var = match.group(1)

            if var not in SKIP_KEYWORDS and not snake_case.match(var):
                invalid_vars.add(var)

    return list(invalid_vars)


# FUNCTION 5: HEALTH SCORE
def compute_health_score(comment_ratio, complexity, invalid_vars):
    """
    Calculates a score out of 100 based on:
    - Comment ratio
    - Complexity
    - Variable naming
    """
    score = 100

    # Penalize low comments
    if comment_ratio < 10:
        score -= 15

    # Penalize high complexity
    if sum(complexity.values()) > 10:
        score -= 25

    # Penalize bad variable names
    if len(invalid_vars) > 0:
        score -= 25

    return round(score)


# MAIN ANALYSIS FUNCTION
def analyze_file(filename):
    """
    Reads file and generates full report.
    """
    try:
        with open(filename, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("Error: File not found.")
        sys.exit(1)

    total, blank, code = analyze_lines(lines)
    comment_lines = count_comments(lines)
    complexity = check_complexity(lines)
    invalid_vars = check_variables(lines)

    # Calculate comment ratio
    comment_ratio = (comment_lines / total) * 100 if total > 0 else 0

    # Compute final health score
    health_score = compute_health_score(comment_ratio, complexity, invalid_vars)

    result = {
        "health_score": health_score,
        "total_lines": total,
        "blank_lines": blank,
        "code_lines": code,
        "comment_lines": comment_lines,
        "comment_ratio": round(comment_ratio, 2),
        "complexity": complexity,
        "invalid_variables": invalid_vars,
        "status": "Good" if health_score >= 75 else "Needs Improvement"
    }

    return result


# CLI ENTRY POINT
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python name_contact_assignment.py <python_file>")
    else:
        filename = sys.argv[1]
        report = analyze_file(filename)
        print(json.dumps(report, indent=4))