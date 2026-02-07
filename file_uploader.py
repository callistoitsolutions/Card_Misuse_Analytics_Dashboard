import pandas as pd
from processing.standardizer import standardize_columns
from processing.cleaner import clean_data


def load_file(file_input):
    """
    Supports:
    1. Streamlit UploadedFile object
    2. Normal file path (string)
    """

    # ---- Streamlit UploadedFile ----
    if hasattr(file_input, "name"):
        file_name = file_input.name.lower()

        if file_name.endswith(".csv"):
            df = pd.read_csv(file_input)
        elif file_name.endswith((".xlsx", ".xls")):
            df = pd.read_excel(file_input)
        else:
            raise ValueError("Unsupported file format")

    # ---- Normal file path ----
    else:
        file_name = file_input.lower()

        if file_name.endswith(".csv"):
            df = pd.read_csv(file_input)
        elif file_name.endswith((".xlsx", ".xls")):
            df = pd.read_excel(file_input)
        else:
            raise ValueError("Unsupported file format")

    # ---- Standardize & Clean ----
    df = standardize_columns(df)
    df = clean_data(df)

    return df
