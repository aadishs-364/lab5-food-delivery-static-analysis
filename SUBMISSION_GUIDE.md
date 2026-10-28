# Lab 5 submission guide

## Contents to submit

- `delivery_system.py`: cleaned assigned program.
- `issues.md`: completed table with 12 tool-finding categories and 6 additional manual findings.
- `reflection.md`: four suggested reflection questions with draft answers. The actual question wording is absent from the provided PDF and README; check with your instructor before submitting this part.
- `reports/before/` and `reports/after/`: Pylint, Bandit and Flake8 reports, command exit codes, tool stderr and program output. The after folder also contains the regression-test log.
- Three fix commits on `main`, following the original starter import.

`original/delivery_system.py` preserves the exact source text for the issue-table line numbers. The original README says the program prompts for input, but this assigned script has no input() call. No interaction was required.

## Run and reproduce on Windows PowerShell

Run these commands from the submitted project directory:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-analysis.txt
.\.venv\Scripts\python.exe delivery_system.py
.\.venv\Scripts\python.exe -m unittest -v
.\.venv\Scripts\python.exe -m pylint --persistent=n delivery_system.py
.\.venv\Scripts\python.exe -m bandit -r delivery_system.py -f txt
.\.venv\Scripts\python.exe -m flake8 delivery_system.py
```

The program uses a built-in menu if `menu.json` is absent. It creates `orders.json` in the current directory. Expected revenue is 290. Asha's order is delivered; Ravi's is cooking. The timestamp varies. JSON backups replace the original pickle format; do not rename or load old pickle files as JSON.

For baseline reports, run the same analysis commands against `original/delivery_system.py`. Paths in those newly generated reports will differ from the preserved baseline, which was run at the original repository root before editing. A nonzero analyzer exit code before fixes indicates findings; all three after-analysis commands returned 0. A zero-byte after Flake8 report means no violations.

## GitHub submission

Repository: https://github.com/aadishs-364/lab5-food-delivery-static-analysis

The main branch contains the starter import followed by three fix commits, one for each tool's work. The commits were recreated through the connected GitHub API, so their IDs differ from the earlier local bundle. Their staged source changes and analysis evidence are preserved. Generated orders.json and orders.pkl runtime backups are excluded.

Clone the repository with:

```powershell
git clone https://github.com/aadishs-364/lab5-food-delivery-static-analysis.git
cd lab5-food-delivery-static-analysis
git log --oneline -4
```

Submit this repository link according to your instructor's process. Check the actual reflection question wording before submission.

## What this lab is about

The aim is to practice finding, explaining and fixing defects using source-code analysis. It is not primarily about building a food-delivery app: that app supplies realistic examples.

1. Preserve and run the starter to understand its behavior.
2. Run Pylint for code quality, Bandit for risky security patterns and Flake8 for style checks.
3. Interpret findings instead of blindly suppressing them. Prioritize security and correctness, then readability and formatting.
4. Document each issue, its source lines and the reason for the fix.
5. Rerun the tools, and use behavior tests for business rules the tools cannot infer.
6. Keep a commit history and before/after evidence that another person can reproduce.

A mutable default list is created once when the function is defined, so calls share it; `None` avoids that hidden state. A broad catch can make a program appear to succeed even when an operation failed. Pickle can reconstruct executable Python objects, whereas JSON stores data. A clean analyzer report is useful evidence, but it is not proof that every bug has been eliminated.
