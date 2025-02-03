import re
import warnings
import pandas as pd
from pathlib import Path
from typing import Tuple, Optional

from config import COLUMN_MAPPING, INTEGER_COLUMNS, TEXT_COLUMNS, TIME_COLUMNS
from skip_junk_rows import find_header_row

from term_session_dates import TERM_SESSION_DATES, get_dates
import logging


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    # Strip whitespace from column names
    df.columns = df.columns.str.strip()

    # Strip whitespace from string columns
    for col in df.select_dtypes(include=["object"]):
        df[col] = df[col].str.strip()

    return df


def process_integer_column(series: pd.Series) -> pd.Series:
    """Convert a series to integers, handling errors gracefully"""
    return pd.to_numeric(series, errors="coerce").fillna(0).astype(int)


def process_text_column(series: pd.Series) -> pd.Series:
    """Clean text columns by removing trailing text after spaces"""
    return series.apply(lambda x: re.sub(r"\s.*$", "", str(x)))


def process_time_column(series: pd.Series) -> pd.Series:
    """Format time columns consistently"""
    def format_time(x):
        if pd.isna(x) or x == "TBA":
            return x
        try:
            return pd.to_datetime(x).strftime("%H:%M")
        except:
            return x
    return series.apply(format_time)


def process_room_number(room: str | float | int) -> Optional[int]:
    """Process room numbers, removing trailing zeros"""
    if pd.isna(room):
        return None
    try:
        room_int = int(float(room))
        return room_int // 10 if room_int % 10 == 0 and room_int != 0 else room_int
    except ValueError:
        return None


def process_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Process the dataframe by applying all necessary transformations"""
    # Drop and rename columns
    df = df.drop(columns=[col for col in df.columns if col not in COLUMN_MAPPING])
    df = df.rename(columns={col: new_name for col, new_name in COLUMN_MAPPING.items() 
                          if col in df.columns})

    # Process different column types
    for col in INTEGER_COLUMNS:
        if col in df.columns:
            df[col] = process_integer_column(df[col])

    for col in TEXT_COLUMNS:
        if col in df.columns:
            df[col] = process_text_column(df[col])

    for col in TIME_COLUMNS:
        if col in df.columns:
            df[col] = process_time_column(df[col])

    if "room_number" in df.columns:
        df["room_number"] = pd.to_numeric(
            df["room_number"].apply(process_room_number), 
            errors="coerce"
        ).astype("Int64")

    # Add date columns
    date_pairs = df.apply(lambda row: get_dates(row["term"], row["session"]), axis=1)
    if not date_pairs.empty:
        df["start_date"], df["end_date"] = zip(*[
            pair if pair is not None else (None, None) for pair in date_pairs
        ])

    return df.reindex(sorted(df.columns), axis=1)


def transform_xlsx_to_csv(input_file: str | Path, output_file: str | Path) -> None:
    """Transform Excel file to CSV with data cleaning"""
    # Find header row and read data
    header_row = find_header_row(input_file, list(COLUMN_MAPPING.keys()))
    df = pd.read_excel(input_file, header=header_row)
    
    logging.debug(f"Initial dataframe shape: {df.shape}")
    logging.debug(f"Columns found: {df.columns.tolist()}")
    
    # Process and save
    df = process_dataframe(df)
    df.to_csv(output_file, index=False)
    logging.info(f"Successfully transformed {input_file} to {output_file}")


if __name__ == "__main__":
    current_dir = Path(__file__).parent
    data_dir = current_dir / "data"

    # Check if data directory exists, fail if it doesn't
    if not data_dir.exists():
        raise FileNotFoundError(f"Data directory not found: {data_dir}")

    print(f"Looking for Excel files in: {data_dir}")

    # Find all xlsx files that start with "data"
    xlsx_files = list(data_dir.glob("data*.xlsx"))

    if not xlsx_files:
        print("No data*.xlsx files found!")
        print(
            "Please place your Excel file (named 'data.xlsx' or similar) in the following directory:"
        )
        print(f"  {data_dir}")
        exit(1)

    # Take the first matching file
    input_xlsx = xlsx_files[0]
    output_csv = data_dir / "data.csv"

    print(f"Found Excel file: {input_xlsx}")
    print(f"Will save CSV to: {output_csv}")

    transform_xlsx_to_csv(input_xlsx, output_csv)
    print("Conversion completed successfully!")
