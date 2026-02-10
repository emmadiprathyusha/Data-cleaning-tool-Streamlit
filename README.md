# Data-cleaning-tool-Streamlit
# Excel and CSV Data Cleaning Tool (Streamlit)

A Streamlit-based Python application to clean messy Excel and CSV files
containing empty rows, inconsistent data types, extra spaces, and formatting issues.

## Features
- Upload Excel or CSV files
- Select and preview sheets
- Remove empty rows and columns
- Trim extra spaces from text columns
- Auto-cast numeric columns
- Handle messy real-world Excel data
- Export cleaned data to Excel

## Tech Stack
- Python
- Pandas
- Streamlit

## How to Run
```bash
python -m streamlit run app.py

## Advantages
📂 File Upload Support

Upload Excel (.xlsx) and CSV (.csv) files

Automatically detects file type

Supports multi-sheet Excel files

📑 Sheet Selection & Preview

Automatically lists available Excel sheets

Displays a preview of raw data before cleaning

Prevents errors before a sheet is selected

🧹 Automatic Data Cleaning

The app performs multiple cleaning steps in one click:

✔ Remove Empty Rows & Columns

Drops fully empty rows

Drops fully empty columns

✔ Trim Extra Spaces

Removes leading/trailing spaces from all text columns

Fixes common issues caused by manual Excel entry

✔ Handle Missing Values Safely

Prevents crashes caused by blank cells or gaps

Ensures clean DataFrame output.

🔢 Smart Data Type Casting

Automatically converts numeric-looking columns to numbers

Handles values saved as text (e.g., "1000" → 1000)

Prevents None / NaN issues in numeric columns
