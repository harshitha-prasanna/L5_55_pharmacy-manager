# Static Code Analysis — Reflection

### 1. What did you learn from static analysis?

I learned that code can execute successfully and still contain security vulnerabilities, maintainability problems, and style violations. Static analysis tools help identify these issues before the application is deployed.

### 2. What was the role of each tool?

- **Pylint:** Identified code-quality problems, naming inconsistencies, missing documentation, and potential correctness issues.
- **Bandit:** Identified security risks, including unsafe expression evaluation, weak hashing, insecure random-number generation, unsafe serialization, and operating-system command execution.
- **Flake8:** Identified formatting and style violations, helping make the code more consistent and readable.

### 3. Which issues were most important to fix?

The most important issues were those that could compromise security or correctness. I removed unsafe eval() usage, replaced pickle-based loading with JSON, removed os.system() usage, replaced MD5 with SHA-256, and used the secrets module for sensitive random-number generation. I also removed the hardcoded password and improved input validation.

### 4. What challenges did you face?

Some fixes required more than changing a single line. Replacing unsafe expression evaluation required validating the permitted arithmetic operations. Loading stock records also required validating their types and values. After fixing the functional and security issues, I had to run the tools again and address the remaining style warnings.

### 5. How did you verify the fixes?

I reran Pylint, Bandit, and Flake8 against the updated pharmacy_manager.py file. The final Pylint score was 10.00/10, Bandit reported no issues, and Flake8 produced no reported violations.

### 6. How will static analysis help in future projects?

I will use static analysis during development and before committing code. Running multiple tools provides complementary checks for code quality, security, and formatting. Fixing issues early makes applications easier to maintain and reduces the risk of vulnerabilities reaching production.
