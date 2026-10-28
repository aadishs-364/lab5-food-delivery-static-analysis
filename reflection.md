# Lab 5 - Suggested reflection answers

The supplied three-page PDF mentions reflection questions but does not list them. The repository README refers to four questions without giving their wording. The four questions below are suggested prompts aligned with the stated learning outcomes, not quotations from the handout. Review these draft answers and adapt them to your own understanding; replace the prompts if your instructor supplies the actual questions.

## 1. What is static analysis, and how did the tools complement each other?

Static analysis examines source code without running the application. Pylint identified quality and maintainability issues such as mutable defaults, broad exceptions, missing documentation and file handling. Bandit identified risky pickle deserialization and silent exception handling. Flake8 identified formatting problems and a bare except. Their checks overlap, but each emphasizes a different aspect of code quality.

## 2. Which issues deserved priority, and how were they fixed?

The medium-severity Bandit B301 finding deserved early attention because loading an untrusted pickle can execute code. Both backup and restore now use JSON, with validation before the live queue is replaced. The shared default history list was changed to `None`, and missing orders now raise an explicit exception instead of disappearing into `except: pass`. Configuration fallback is limited to a missing file so corrupt data is visible. Lower-priority documentation, naming and formatting issues were then addressed.

## 3. How were the fixes verified, and what did the tools miss?

All three tools were run before and after the changes. Pylint improved from 6.27 to 10.00, Bandit findings fell from three to zero, and Flake8 violations fell from twelve to zero. The raw reports were retained. Behavior tests additionally check invalid inputs, revenue, independent histories, backup round trips, ID allocation after restoring, and preservation of state after invalid data. The tools did not identify the business error of charging 99 for an unknown dish or accepting a delivery status of `teleported`; those required manual review and tests.

## 4. What are the benefits and limitations of static analysis?

Static analysis provides repeatable feedback early, makes code easier to maintain, and helps prevent common bugs and unsafe patterns. It is useful during development and in automated checks before merging changes. However, a perfect score does not prove the application is correct or secure. Tools do not know all business rules, may report false positives, and do not replace tests or human review. This exercise shows why automated findings should be interpreted, fixed according to risk, and followed by behavior checks.
