# Bank Management System

A Python console application that manages customer ledger metrics alongside localized workplace profiles. Records automatically persist using JSON format, and unexpected application exceptions are handled gracefully.

---

## Architecture and Program Workflow

1. **Initialization (`load_data`)**: The program initializes and checks for `bank_data.json`. It instantiates blank operational dict arrays if files are empty or corrupted.
2. **Interactive Event Main Driver Loop (`main`)**: Provides a menu interface to manage customer and employee profiles, process transactions, and view account statuses.
3. **Data Verification**: Transactions convert raw input into floating-point numbers within `try/except` statements to neutralize system processing bugs.
4. **Program Exiting Loop**: Saving events execute sequentially upon completing mutations. Data writes to disk instantly, preventing records from dropping out of sync during manual system stops.

---

## File Layout and Setup Instruction Guide

├── logs/
│   └── bank_errors.log
├── bank_data.json
└── main.py
