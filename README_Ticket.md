# Ticket Sales Data Pipeline

A Python-based ETL (Extract, Transform, Load) pipeline that reads ticket transaction data from a local CSV file, cleanses and formats the fields, imports the data into a local MySQL database, and outputs quick sales metrics.

## Features
* **Automated Setup**: Dynamically creates the target database (`Sam`) and table (`sales`) if they don't already exist.
* **Data Cleansing**: Transforms string-based CSV rows into optimized database types, converting text dates into both native SQL formats and `YYYYMMDD` integer tracking IDs.
* **Bulk Aggregation**: Automatically runs analytics to calculate and display the top two most popular events based on absolute ticket volume sales.

---

## Prerequisites

### 1. Python Environment
Make sure Python (or Anaconda) is installed. You will need the MySQL native interface module. Run the following command in your terminal:
```bash
pip install mysql-connector-python
```

### 2. MySQL Server
Ensure your local MySQL Community Server is installed and running on your machine (default port `3306`). 

---

## File Structure
Ensure your script and data file sit in the exact same directory:
```text
C:\Users\samue\Projects\UML\
  ├── Tickets.py               # The Python pipeline application script
  └── load_third_party.csv     # Raw source transaction data file
```

### Expected CSV Layout
Your source `load_third_party.csv` data file must contain a header row followed by exactly 10 data columns:
```csv
ticket_id,trans_date,event_id,event_name,event_date,event_type,event_city,customer_id,price,num_tickets
1,2026-06-01,101,Rock Concert,2026-07-15,Music,Austin,5005,85.50,2
```

---

## How to Run

1. Open **Visual Studio Code** inside your project folder directory.
2. Open a fresh terminal window to clear out any old shell history loops.
3. Open `Tickets.py` and click the **Play Button (Run Python File)** in the top right corner of the screen.
4. The terminal will prompt you interactive connection configuration questions. **Press Enter** to accept default localhost options, or input your custom password when requested:
   * **Database Username**: (Default: `root`)
   * **Database Password**: Input your local root password
   * **Port**: (Default: `3306`)
   * **Localhost**: (Default: `127.0.0.1`)
   * **Database Name**: (Default: `Sam`)

---

## Database Target Schema
The pipeline automatically provisions your database table using these strict relational configurations:


| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `ticket_id` | `INT` | Unique Transaction ID |
| `trans_date` | `INT` | Date of purchase formatted as an integer (`YYYYMMDD`) |
| `event_id` | `INT` | Internal Event Registration Key |
| `event_name` | `VARCHAR(255)` | Public name of the show/event |
| `event_date` | `DATE` | Native SQL calendar date of the performance |
| `event_type` | `VARCHAR(100)` | Event Category |
| `event_city` | `VARCHAR(100)` | Location City |
| `customer_id` | `INT` | Buyer account index number |
| `price` | `DECIMAL(10,2)` | Single ticket face-value price |
| `num_tickets` | `INT` | Quantitative volume of seats bought |

---

## Troubleshooting

### Error: Table 'sam.sales' doesn't exist
This happens if your script connects but skipped table creation. The script now includes `CREATE TABLE IF NOT EXISTS` inside the core database builder function to resolve this problem permanently.

### Error: ModuleNotFoundError: No module named 'mysql'
This means your script is executing inside an isolated virtual environment (like Anaconda) that doesn't have the library downloaded. Fix this by pointing your terminal explicitly to your running interpreter and re-installing:
```bash
C:\Users\samue\anaconda3\python.exe -m pip install mysql-connector-python
```
