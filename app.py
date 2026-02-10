import streamlit as st
import pandas as pd
from io import BytesIO

from cleaning.cleaning_utils import clean_dataframe


# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Data Cleaning Tool", layout="wide")
st.title("🧹 Data Cleaning Tool")

# ---------- FILE UPLOAD ----------
uploaded_file = st.file_uploader(
    "Upload Excel or CSV file",
    type=["xlsx", "xls", "csv"]
)

# ---------- STOP IF NO FILE ----------
if uploaded_file is None:
    st.info("Please upload a file to start cleaning")
    st.stop()

# ---------- READ FILE ----------
if uploaded_file.name.endswith(".csv"):
    sheets = {"Sheet1": pd.read_csv(uploaded_file)}
else:
    sheets = pd.read_excel(
        uploaded_file,
        sheet_name=None,
        engine="openpyxl",
        engine_kwargs={"data_only": True}
    )

st.success(f"Loaded {len(sheets)} sheet(s)")

cleaned_sheets = {}
summary_rows = []

# ---------- CLEANING LOOP ----------
for sheet_name, df in sheets.items():

    if df is None or df.empty:
        continue

    cleaned_df, clean_summary = clean_dataframe(df)
    cleaned_sheets[sheet_name] = cleaned_df

    summary_rows.append({
        "Sheet": sheet_name,
        "Rows before": clean_summary["rows_before"],
        "Rows removed": clean_summary["rows_removed"],
        "Trimmed cells": clean_summary["trimmed_cells"],
        "Numeric columns fixed": ", ".join(
            clean_summary["numeric_columns_converted"]
        )
    })

    st.subheader(f"📄 Sheet: {sheet_name}")
    st.dataframe(cleaned_df, use_container_width=True)

# ---------- SUMMARY ----------
if summary_rows:
    st.subheader("📊 Cleaning Summary")
    summary_df = pd.DataFrame(summary_rows)
    st.dataframe(summary_df, use_container_width=True)

# ---------- EXPORT ----------
if cleaned_sheets:
    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        for sheet_name, df in cleaned_sheets.items():
            df.to_excel(
                writer,
                sheet_name=sheet_name[:31],  # Excel limit
                index=False
            )

    output.seek(0)

    st.download_button(
        label="⬇️ Download Cleaned Excel",
        data=output,
        file_name="cleaned_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
