# Static Code Analysis — Issue Table

**Project:** Pharmacy Manager
**File:** `pharmacy_manager.py`
**Tools:** Pylint, Bandit, Flake8

| Issue | Type | Original line(s) | Description | Fix approach |
|---|---|---:|---|---|
| Mutable default argument | Bug | 13 | The default list could be shared across function calls. | Use None and initialize a new list inside the function. |
| Hardcoded password | Security | 11 | A password was stored directly in source code. | Read the password from an environment variable. |
| Unsafe expression evaluation | Security | 48 | Evaluating untrusted expressions can execute unintended code. | Use a restricted AST-based arithmetic evaluator. |
| Weak MD5 hashing | Security | 51 | MD5 is unsuitable for security-sensitive hashing. | Replace MD5 with SHA-256. |
| Insecure random number generation | Security | 54 | The random module is not intended for security-sensitive values. | Use the secrets module. |
| Unsafe pickle deserialization | Security | 64 | Loading untrusted pickle data can execute arbitrary code. | Use JSON for stock-data serialization. |
| Operating-system command execution | Security | 68 | Shell command execution introduces avoidable security risk. | Use Python functionality such as print() instead. |
| Overly broad exception handling | Reliability | 27 | A bare exception can hide unexpected errors. | Catch specific exceptions and handle them explicitly. |
| Missing documentation | Maintainability | 13 | Functions lacked descriptive documentation. | Add docstrings describing their purpose. |
| Nonstandard naming | Maintainability | 13 | CamelCase function names did not follow Python function naming conventions. | Rename functions using snake_case. |
| Unused imports | Maintainability | 2 | Unused imports added unnecessary code. | Remove imports that are not needed. |
| Formatting and line-length violations | Style | See Flake8 baseline report | Flake8 identified whitespace and line-length violations. | Correct blank lines, spacing, and long statements. |

## Verification results

- **Pylint:** 10.00/10.
- **Bandit:** No issues identified in the final scan.
- **Flake8:** No reported violations in the final scan.
- **Execution:** `python pharmacy_manager.py` ran successfully.

Line numbers refer to the original starter file where the matching code was found. For style findings, consult `flake8_report_before.txt` for the original reported line numbers.
