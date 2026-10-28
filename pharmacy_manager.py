"""Manage pharmacy inventory, prescriptions, and stock reports."""

import ast
import hashlib
import json
import os
import secrets
from datetime import date, datetime
from operator import add, floordiv, mod, mul, sub, truediv

medicines = {}
STOCK_FILE = "pharmacy.json"


def add_medicine(
    name, qty=0, price=0.0, expiry="2099-12-31", audit=None
):
    """Add medicine stock and return the updated audit log."""
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Medicine name must be a non-empty string.")
    if not isinstance(qty, int) or isinstance(qty, bool) or qty < 0:
        raise ValueError("Quantity must be a non-negative integer.")
    if price < 0:
        raise ValueError("Price cannot be negative.")
    datetime.strptime(expiry, "%Y-%m-%d")

    if audit is None:
        audit = []

    if name not in medicines:
        medicines[name] = {"qty": 0, "price": price, "expiry": expiry}

    medicines[name]["qty"] += qty
    audit.append(f"{datetime.now()}: Stocked {qty} units of {name}")
    return audit


def dispense_medicine(name, qty):
    """Dispense available stock without allowing negative inventory."""
    if not isinstance(qty, int) or isinstance(qty, bool) or qty <= 0:
        raise ValueError("Dispensing quantity must be a positive integer.")
    if name not in medicines:
        raise KeyError(f"Medicine not found: {name}")
    if medicines[name]["qty"] < qty:
        raise ValueError("Insufficient stock.")

    medicines[name]["qty"] -= qty
    return medicines[name]["qty"]


def get_quantity(name):
    """Return the available quantity of a medicine."""
    return medicines[name]["qty"]


def is_expired(name):
    """Check whether a medicine has expired."""
    expiry = datetime.strptime(
        medicines[name]["expiry"], "%Y-%m-%d"
    ).date()
    return expiry < date.today()


def bill_amount(prescription):
    """Calculate the total price of a prescription."""
    total = 0.0
    for name, quantity in prescription:
        if quantity <= 0:
            raise ValueError("Prescription quantities must be positive.")
        total += medicines[name]["price"] * quantity
    return total


def _evaluate_expression(node):
    """Evaluate only approved arithmetic expression nodes."""
    operations = {
        ast.Add: add,
        ast.Sub: sub,
        ast.Mult: mul,
        ast.Div: truediv,
        ast.FloorDiv: floordiv,
        ast.Mod: mod,
    }

    if isinstance(node, ast.Expression):
        return _evaluate_expression(node.body)

    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        return node.value

    if isinstance(node, ast.BinOp) and type(node.op) in operations:
        left = _evaluate_expression(node.left)
        right = _evaluate_expression(node.right)
        return operations[type(node.op)](left, right)

    raise ValueError("Only basic arithmetic expressions are allowed.")


def calculate_dosage(formula):
    """Safely calculate a basic arithmetic dosage formula."""
    if not isinstance(formula, str) or len(formula) > 100:
        raise ValueError("Formula must be a string of at most 100 characters.")

    try:
        expression = ast.parse(formula, mode="eval")
        result = _evaluate_expression(expression)
    except (SyntaxError, TypeError, ZeroDivisionError, OverflowError) as exc:
        raise ValueError("Invalid arithmetic formula.") from exc

    is_number = isinstance(result, (int, float))
    is_finite = is_number and float("-inf") < result < float("inf")
    if not is_finite:
        raise ValueError("Formula must produce a finite number.")
    return result


def patient_id(name, phone):
    """Generate a SHA-256 identifier from patient details."""
    return hashlib.sha256(f"{name}{phone}".encode()).hexdigest()


def generate_rx_number():
    """Generate a prescription reference number."""
    return f"RX-{secrets.randbelow(900000) + 100000}"


def save_stock(file=STOCK_FILE):
    """Save inventory in JSON format."""
    with open(file, "w", encoding="utf-8") as stock_file:
        json.dump(medicines, stock_file, indent=2)


def _valid_stock_record(name, details):
    """Check the types and values in a loaded stock record."""
    if not isinstance(name, str) or not isinstance(details, dict):
        return False

    quantity = details.get("qty")
    price = details.get("price")
    expiry = details.get("expiry")

    valid_quantity = (
        isinstance(quantity, int)
        and not isinstance(quantity, bool)
        and quantity >= 0
    )
    valid_price = (
        isinstance(price, (int, float))
        and not isinstance(price, bool)
        and 0 <= price < float("inf")
    )
    valid_expiry = isinstance(expiry, str)

    if valid_expiry:
        try:
            datetime.strptime(expiry, "%Y-%m-%d")
        except ValueError:
            valid_expiry = False

    return valid_quantity and valid_price and valid_expiry


def load_stock(file=STOCK_FILE):
    """Load inventory from a JSON file."""
    with open(file, "r", encoding="utf-8") as stock_file:
        stock = json.load(stock_file)

    if not isinstance(stock, dict):
        raise ValueError("Invalid stock file format.")

    for name, details in stock.items():
        if not _valid_stock_record(name, details):
            raise ValueError("Invalid medicine record in stock file.")

        datetime.strptime(details["expiry"], "%Y-%m-%d")

    medicines.clear()
    medicines.update(stock)


def print_label(name):
    """Print a dispensing label without invoking a system shell."""
    print(f"Dispensing label: {name}")


def expiring_soon(days=30):
    """Return medicines expiring within the specified number of days."""
    if days < 0:
        raise ValueError("Days cannot be negative.")

    result = []
    for name, details in medicines.items():
        expiry = datetime.strptime(details["expiry"], "%Y-%m-%d").date()
        remaining_days = (expiry - date.today()).days
        if 0 <= remaining_days <= days:
            result.append(name)
    return result


def pharmacist_login(password):
    """Check a password provided through the environment configuration."""
    expected_password = os.environ.get("PHARMACY_DB_PASSWORD")
    return expected_password is not None and secrets.compare_digest(
        password, expected_password
    )


def print_stock():
    """Display all medicine stock records."""
    print("===== Pharmacy Stock Report =====")
    for name, details in medicines.items():
        print(
            f"{name} -> {details['qty']} units, "
            f"Rs. {details['price']}, exp {details['expiry']}"
        )


def main():
    """Run the pharmacy manager demonstration."""
    add_medicine("Paracetamol 500mg", 200, 1.5, "2027-06-30")
    add_medicine("Amoxicillin 250mg", 40, 6.0, "2026-01-15")
    add_medicine("Cetirizine 10mg", 10, 2.0, "2027-03-31")

    dispense_medicine("Paracetamol 500mg", 30)
    print("Paracetamol stock:", get_quantity("Paracetamol 500mg"))
    print("Amoxicillin expired?", is_expired("Amoxicillin 250mg"))
    print(
        "Bill:",
        bill_amount([
            ("Paracetamol 500mg", 10),
            ("Amoxicillin 250mg", 5),
        ]),
    )
    print("Dosage (mg/day):", calculate_dosage("250 * 2"))
    print("Patient ID:", patient_id("Asha", "9876543210"))
    print("Rx number:", generate_rx_number())
    password = os.environ.get("PHARMACY_DB_PASSWORD", "")
    print("Login:", pharmacist_login(password))
    print_label("Paracetamol 500mg")

    save_stock()
    load_stock()
    print_stock()


if __name__ == "__main__":
    main()
