# Lab 5 - Issue table

Source: SETAPESU26/L5_05_food_delivery, starter commit
`13d7380f0332e177d75a477d4af4a9b12d8c9127`.
All line numbers below refer to `original/delivery_system.py`.
Bandit severity is reported exactly as emitted; other priorities are review judgments, not Bandit ratings.

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Unsafe deserialization (Bandit B301; Medium) | Security | 49 | Loading an attacker-controlled pickle can execute code. | Replace pickle with JSON; validate loaded records and restore integer IDs. Old pickle backups are intentionally unsupported. |
| Mutable default (Pylint W0102; medium review priority) | Bug | 11, 17 | The same default history list is reused across calls. | Use `None`, then initialize a new list for that call. Explicit caller histories still work. |
| Broad fallback (Pylint W0718; medium review priority) | Reliability | 29-33 | Catching every Exception hides malformed configuration and unexpected programming errors. | Fall back only for FileNotFoundError; let invalid JSON and access errors be reported, and validate menu values. |
| Silent exception handling (Bandit B110 Low; Pylint W0702; Flake8 E722) | Error handling | 22-25 | A bare except/pass hides missing orders and other failures. | Check order existence and raise a clear KeyError; reject invalid statuses with ValueError. |
| Pickle import (Bandit B403; Low) | Security | 2 | Pickle use prompts a security review. | Remove the pickle dependency after switching both persistence functions to JSON. |
| Unclosed files (Pylint R1732) | Resource management | 30, 43, 49 | Files may remain open, especially if reading or writing fails. | Use `with open(...)` for every file operation. |
| Implicit text encoding (Pylint W1514) | Portability | 30 | Default encoding varies across computers. | Specify UTF-8 for menu and backup JSON. |
| Global reassignment (Pylint W0603) | Maintainability | 12, 28, 48 | Functions rebind module globals and maintain a separate ID counter. | Use named module dictionaries, update their contents, and derive the next ID from existing orders. State is still module-level; this is a small single-process lab program. |
| Missing documentation (Pylint C0114/C0116) | Readability | 1, 11, 21, 27, 35, 42, 47, 51, 56 | Module and functions lack explanations. | Add concise docstrings describing behavior and validation. |
| Names and string formatting (Pylint C0103/C0209) | Style | 7, 51-52 | Nonconforming names and old-style formatting reduce consistency. | Remove `next_id`, rename `printQueue` to `print_queue`, and use an f-string. |
| Blank-line spacing (Flake8 E302/E305) | Style | 11, 21, 27, 35, 42, 47, 51, 56, 70 | Top-level definitions and the final call are separated by too few blank lines. | Use two blank lines around top-level definitions. |
| Long lines (Flake8 E501) | Style | 16, 54 | Lines exceed the default 79-character limit. | Wrap the order dictionary and simplify queue printing. |

## Additional findings from manual review and behavior tests

These were not reported as domain bugs by the three tools, so they do not replace the tool-detected issues above.

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Unknown dish silently priced at 99 | Business logic | 15, 59 | `sushi` is accepted despite not being on the menu. | Reject unknown dishes before modifying the queue. |
| Empty customer and item list accepted | Validation | 11-16, 60 | An empty order is created and later marked delivered. | Require a nonblank customer and a nonempty list of valid dishes. |
| Invalid status accepted | Business logic | 9, 23, 62 | `teleported` is accepted even though allowed statuses are declared. | Enforce membership in VALID_STATUSES. This does not enforce a sequential state machine, which the starter does not specify. |
| ID counter not restored | Data integrity | 7, 18, 47-49 | Restoring a queue in a fresh process leaves next_id at 1 and can overwrite an order. | Derive the next ID as maximum stored ID plus one. |
| Caller can mutate stored items | Data ownership | 16 | Stored items refer to the caller's list. | Store a copy of the items. |
| Demo executes during import | Testability | 70 | Importing the module creates orders and writes a backup. | Add an `if __name__ == "__main__"` guard. |

## Verification

| Check | Before | After |
|---|---|---|
| Pylint 4.1.3 | 6.27/10; 22 messages | 10.00/10; no messages |
| Bandit 1.9.4 | 3 findings: 1 Medium, 2 Low, 0 High | 0 findings |
| Flake8 7.4.1 | 12 violations | 0 violations |

Raw outputs and exit codes are in `reports/before/` and `reports/after/`.
No rule suppressions or relaxed thresholds were used. Analysis targets the assigned `delivery_system.py`, not the preserved original or tests.
The final empty Flake8 report is expected: exit code 0 confirms a clean run.

The original demo produces revenue 290 but also displays an invalid status and an empty order. The revised demo keeps revenue 290 while creating two valid orders. Its changed sample inputs exercise the valid path; the regression tests explicitly verify rejection of the original invalid inputs.

JSON avoids pickle code execution; it does not authenticate backups. This lab solution is not a concurrent or production payment system, and writes are not crash-atomic.
