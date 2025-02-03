import re
import warnings
import pandas as pd
from pathlib import Path
from skip_junk_rows import find_header_row
from rename_or_drop_columns import process_dataframe, column_mapping


from term_session_dates import TERM_SESSION_DATES, get_dates
import logging


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    # Strip whitespace from column names
    df.columns = df.columns.str.strip()

    # Strip whitespace from string columns
    for col in df.select_dtypes(include=["object"]):
        df[col] = df[col].str.strip()

    return df


def process_room_number(room: str | float | int) -> int | None:
    """
    This function does two things: it ensures that a string or float is converted to an integer, and it removes the final digit if it is 0.

    All the room numbers from CID are padded with a final 0, which we want to remove.

    Args:
        room: str | float | int: The input room number, which can be a string, float, or integer.

    Returns:
        int | None: The processed room number as an integer, or None if the input is invalid or cannot be processed.

    Examples:
        >>> process_room_number("103")
        103
        >>> process_room_number(10.0)
        1
        >>> process_room_number("invalid")
        None
    """
    if pd.isna(room):
        return None
    try:
        room_float = float(room)
        room_int = int(room_float)
        if room_int % 10 == 0 and room_int != 0:
            return room_int // 10
        else:
            return room_int
    except ValueError:
        return None


def transform_xlsx_to_csv(input_file: str | Path, output_file: str | Path) -> None:
    # Get the expected column names directly from the imported mapping
    expected_columns = list(column_mapping.keys())
    
    # Find the actual header row
    header_row = find_header_row(input_file, expected_columns)
    
    # Read the Excel file starting from the identified header row
    df = pd.read_excel(input_file, header=header_row)
    logging.debug(f"After initial read: {df.shape}")

    # Debug: Print actual columns
    print("\nActual columns in Excel file:")
    for col in df.columns:
        print(f"  '{col}'")
    print("\n")

    # Process the DataFrame (rename/drop columns)
    df = process_dataframe(df)
    logging.debug(f"After process_dataframe: {df.shape}")

    def process_column(col: str, processor: callable, error_msg: str = None) -> None:
        if col in df.columns:
            df[col] = processor(df[col])
        else:
            print(error_msg or f"Column '{col}' not found in the DataFrame")

    # Process integer columns
    for col in ["reference_number", "room_cap", "session", "term"]:
        process_column(col, lambda x: pd.to_numeric(x, errors="coerce").fillna(0).astype(int))

    # Process text columns with regex
    for col in ["campus", "department", "division"]:
        process_column(col, lambda x: x.apply(lambda y: re.sub(r"\s.*$", "", str(y))))

    # Process room number
    process_column(
        "room_number",
        lambda x: pd.to_numeric(x.apply(process_room_number), errors="coerce").astype("Int64"),
        "Warning: 'room_number' column not found in DataFrame"
    )

    # Process time columns
    def format_time(x):
        if pd.isna(x) or x == "TBA":
            return x
        try:
            return pd.to_datetime(x).strftime("%H:%M")
        except:
            return x

    for col in ["start_time", "end_time"]:
        process_column(col, lambda x: x.apply(format_time))

    # Process dates
    date_pairs = df.apply(lambda row: get_dates(row["term"], row["session"]), axis=1)
    # print("Debug: date_pairs =", date_pairs)
    if not date_pairs.empty:
        df["start_date"], df["end_date"] = zip(
            *[(pair if pair is not None else (None, None)) for pair in date_pairs]
        )
    else:
        print("Warning: date_pairs is empty")
        df["start_date"] = None
        df["end_date"] = None

    # Sort the columns alphabetically
    # this puts start_date and end_date in the right place; the list was already sorted in rename_or_drop_columns.py
    df = df.reindex(sorted(df.columns), axis=1)

    # Write the transformed data to a CSV file
    df.to_csv(output_file, index=False)


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
