import pandas as pd
import numpy as np
import re


def clean_dataframe(df: pd.DataFrame):
    """
    Standard cleaning pipeline:
    - Fix missing/blank column names
    - Remove fully empty rows
    - Trim text columns
    - Clean currency symbols ($, €, £, ₹)
    - Auto-cast numeric columns
    - Return cleaned df + summary
    """

    summary = {
        "rows_before": 0,
        "rows_removed": 0,
        "trimmed_cells": 0,
        "numeric_columns_converted": []
    }

    if df is None or df.empty:
        return df, summary

    df = df.copy()
    summary["rows_before"] = len(df)

    # ---------- FIX COLUMN NAMES ----------
    df.columns = [
        f"Column_{i+1}" if pd.isna(col) or str(col).strip() == ""
        else str(col).strip()
        for i, col in enumerate(df.columns)
    ]

    # ---------- REMOVE FULLY EMPTY ROWS ----------
    before = len(df)
    df = df.dropna(how="all")
    summary["rows_removed"] = before - len(df)

    # ---------- TRIM TEXT COLUMNS ----------
    text_cols = df.select_dtypes(include=["object", "string"]).columns
    if len(text_cols) > 0:
        before_trim = df[text_cols].copy()

        for col in text_cols:
            df[col] = df[col].astype(str).str.strip()

        summary["trimmed_cells"] = (before_trim != df[text_cols]).sum().sum()

    # ---------- CLEAN CURRENCY COLUMNS ----------
    for col in text_cols:
        sample = df[col].dropna().astype(str).head(10)

        if sample.str.contains(r"[$€£₹]", regex=True).any():
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(r"[$€£₹,]", "", regex=True)
                .str.strip()
            )
            df[col] = pd.to_numeric(df[col], errors="coerce")
            summary["numeric_columns_converted"].append(col)

    # ---------- AUTO NUMERIC CAST ----------
    for col in df.columns:
        if df[col].dtype == "object":
            converted = pd.to_numeric(df[col], errors="ignore")
            if converted.dtype != "object":
                df[col] = converted
                summary["numeric_columns_converted"].append(col)

    summary["numeric_columns_converted"] = list(
        set(summary["numeric_columns_converted"])
    )

    return df, summary
