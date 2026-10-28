# Static Code Analysis — Issue Table

**Project:** Pharmacy Manager  
**Tools used:** Pylint, Bandit, Flake8  
**File analyzed:** pharmacy_manager.py

| No. | Tool | Issue identified | Severity / category | Fix implemented |
|---:|---|---|---|---|
| 1 | Pylint | Missing module and function docstrings | Code quality | Added appropriate documentation strings. |
| 2 | Pylint | Function and variable names did not follow Python naming conventions | Maintainability | Renamed identifiers using snake_case. |
| 3 | Pylint | Mutable list used as a default argument | Correctness | Removed the mutable default argument to prevent shared state between calls. |
| 4 | Pylint | Bare exception handling | Reliability | Replaced broad exception handling with specific exceptions. |
| 5 | Pylint / Bandit | Unsafe use of eval() | Security | Replaced eval() with restricted arithmetic-expression parsing. |
| 6 | Pylint / Flake8 | Unused imports and formatting violations | Code quality | Removed unused imports and corrected spacing and line lengths. |
| 7 | Bandit | MD5 used for hashing | Security | Replaced MD5 with SHA-256. |
| 8 | Bandit | random.randint() used to generate prescription numbers | Security | Used the secrets module for secure random-number generation. |
| 9 | Bandit | Pickle used to load serialized data | Security | Replaced pickle serialization with JSON. |
| 10 | Bandit | os.system() used to display output | Security | Replaced the system command with Python's print() function. |
| 11 | Bandit | Hardcoded password | Security | Read the password from the PHARMACY_DB_PASSWORD environment variable and used a constant-time comparison. |
| 12 | Pylint | Files were opened and closed manually | Resource management | Used context managers where file operations are performed. |
| 13 | Bandit | Exceptions were caught and silently ignored | Reliability | Removed silent exception handling and validated loaded data. |
| 14 | Flake8 | Excessive blank lines and long lines | Style | Corrected blank-line spacing and wrapped long statements. |

## Final verification

- Pylint score: 10.00/10
- Bandit: No issues identified.
- Flake8: No reported violations.

The final reports should be retained alongside the original baseline reports as evidence of the improvements.
