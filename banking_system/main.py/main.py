"""Bank Management System.

This module provides a command-line interface for managing a simple banking
system, including customer and employee accounts, deposits, and withdrawals.
It handles persistence via JSON and logs activities to the console and file.
"""

import json
import logging
import os
from typing import Any, Dict

# Configuration Constants
DATA_FILE = "bank_data.json"
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "bank_errors.log")

# Setup project directories
os.makedirs(LOG_DIR, exist_ok=True)

# --- Logging Configuration ---
logger = logging.getLogger("BankSystem")
logger.setLevel(logging.DEBUG)

# File Handler: Captures warnings, errors, and critical failures
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setLevel(logging.WARNING)
file_format = logging.Formatter(
    "%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
)
file_handler.setFormatter(file_format)

# Console Handler: Streamlines basic app messages to the screen
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_format = logging.Formatter("%(message)s")
console_handler.setFormatter(console_format)

# Register handlers to the primary logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)


def load_data() -> Dict[str, Any]:
    """Loads banking customer and employee data from a local JSON file.

    Returns:
        Dict[str, Any]: A dictionary containing structured data for
        'customers' and 'employees'.
    """
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as err:
            logger.error("Data file corrupted. Reinitializing. Error: %s", err)
            return {"customers": {}, "employees": {}}
        except IOError as err:
            logger.critical("Failed to read system storage file: %s", err)
            return {"customers": {}, "employees": {}}
    return {"customers": {}, "employees": {}}


def save_data(data: Dict[str, Any]) -> None:
    """Saves the current state of banking records back into the JSON file.

    Args:
        data (Dict[str, Any]): The complete records object to persist.
    """
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    except IOError as err:
        logger.error("Could not write records data to disk: %s", err)


def create_customer_account(data: Dict[str, Any]) -> None:
    """Prompts terminal input to construct and save a new customer account."""
    acc_no = input("Enter account number: ").strip()
    if not acc_no:
        logger.info("⚠️ Account number cannot be blank.")
        return

    if acc_no in data["customers"]:
        logger.info("❌ Account already exists!")
        return

    first_name = input("Enter first name: ").strip()
    last_name = input("Enter last name: ").strip()

    try:
        balance = float(input("Enter initial deposit amount: $"))
        if balance < 0:
            logger.warning("Attempted negative deposit for account: %s", acc_no)
            logger.info("⚠️ Initial deposit cannot be negative.")
            return
    except ValueError:
        logger.warning("Invalid numerical deposit entered for input stream.")
        logger.info("⚠️ Invalid amount entered.")
        return

    # Commit structural record map
    data["customers"][acc_no] = {
        "first_name": first_name,
        "last_name": last_name,
        "balance": balance,
        "loan_balance": 0.0,
    }
    save_data(data)
    logger.info("✅ Customer account created for %s %s!", first_name, last_name)


def create_employee_account(data: Dict[str, Any]) -> None:
    """Gathers fields via console to index a new employee tracking entry."""
    emp_id = input("Enter unique employee ID: ").strip()
    if not emp_id:
        logger.info("⚠️ Employee ID cannot be blank.")
        return

    if emp_id in data["employees"]:
        logger.info("❌ Employee ID already exists!")
        return

    first_name = input("Enter employee first name: ").strip()
    last_name = input("Enter employee last name: ").strip()
    role = input("Enter job role / title: ").strip()

    data["employees"][emp_id] = {
        "first_name": first_name,
        "last_name": last_name,
        "role": role,
    }
    save_data(data)
    logger.info("✅ Employee profile created for %s %s (%s)!", first_name, last_name, role)


def deposit_money(data: Dict[str, Any]) -> None:
    """Adds valid funds directly onto verified target customer balance accounts."""
    acc_no = input("Enter account number: ").strip()
    if acc_no not in data["customers"]:
        logger.info("❌ Account number not found!")
        return

    try:
        amount = float(input("Enter deposit amount: $"))
        if amount <= 0:
            logger.warning("Negative or zero value transaction: %s on %s", amount, acc_no)
            logger.info("⚠️ Deposit amount must be greater than zero.")
            return
    except ValueError:
        logger.warning("Non-numeric tracking transaction input registered.")
        logger.info("⚠️ Invalid amount entered.")
        return

    data["customers"][acc_no]["balance"] += amount
    save_data(data)
    current_bal = data["customers"][acc_no]["balance"]
    logger.info("✅ Success! New balance: $%s", f"{current_bal:.2f}")


def withdraw_money(data: Dict[str, Any]) -> None:
    """Deducts positive balances while safely tracking overdraft validation exceptions."""
    acc_no = input("Enter account number: ").strip()
    if acc_no not in data["customers"]:
        logger.info("❌ Account number not found!")
        return

    try:
        amount = float(input("Enter withdrawal amount: $"))
        if amount <= 0:
            logger.info("⚠️ Withdrawal amount must be greater than zero.")
            return
        if amount > data["customers"][acc_no]["balance"]:
            logger.warning("Overdraft rejected for account %s (Requested: $%s)", acc_no, amount)
            logger.info("❌ Insufficient funds!")
            return
    except ValueError:
        logger.warning("Non-numeric processing input error during withdrawal.")
        logger.info("⚠️ Invalid amount entered.")
        return

    data["customers"][acc_no]["balance"] -= amount
    save_data(data)
    current_bal = data["customers"][acc_no]["balance"]
    logger.info("✅ Success! New balance: $%s", f"{current_bal:.2f}")


def view_account(data: Dict[str, Any]) -> None:
    """Displays stored balance structural details matching specific target ID key."""
    acc_no = input("Enter account number: ").strip()
    if acc_no not in data["customers"]:
        logger.info("❌ Account number not found!")
        return

    cust = data["customers"][acc_no]
    logger.info("\n--- Account Details ---")
    logger.info("Holder: %s %s", cust["first_name"], cust["last_name"])
    logger.info("Balance: $%s", f"{cust['balance']:.2f}")
    logger.info("Loan Balance: $%s", f"{cust['loan_balance']:.2f}")


def main() -> None:
    """Acts as the root driver engine running the dashboard application interface."""
    logger.info("Starting Bank Management System Engine...")
    data = load_data()

    while True:
        logger.info("\n=== Bank Management System ===")
        logger.info("1. Create Customer Account")
        logger.info("2. Create Employee Profile")
        logger.info("3. Deposit Money")
        logger.info("4. Withdraw Money")
        logger.info("5. View Account Details")
        logger.info("6. Exit")

        choice = input("Select an option (1-6): ").strip()
        if choice == "1":
            create_customer_account(data)
        elif choice == "2":
            create_employee_account(data)
        elif choice == "3":
            deposit_money(data)
        elif choice == "4":
            withdraw_money(data)
        elif choice == "5":
            view_account(data)
        elif choice == "6":
            logger.info("Closing operations. Goodbye!")
            break
        else:
            logger.info("⚠️ Invalid choice. Please try again.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\nSystem terminated abruptly via keyboard escape.")
