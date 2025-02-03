import pandas as pd
import logging
from pathlib import Path
from typing import List, Union

def find_header_row(excel_file: Union[str, Path], expected_columns: List[str]) -> int:
    """
    Find the actual header row in an Excel file by looking for expected column names.
    
    Args:
        excel_file: Path or string pointing to the Excel file to read
        expected_columns: List of column names to look for in the header row
        
    Returns:
        int: The index of the header row
        
    Raises:
        ValueError: If no header row is found containing at least 50% of expected columns
    """
    logging.debug(f"Looking for header row with expected columns: {expected_columns}")
    
    # Read first 20 rows
    preview_df = pd.read_excel(excel_file, nrows=20)
    expected_columns_lower = set(col.lower() for col in expected_columns)
    
    # Check each row for matches
    for idx in range(len(preview_df)):
        row_values = preview_df.iloc[idx].astype(str).str.strip().str.lower()
        matches = expected_columns_lower.intersection(row_values)
        
        logging.debug(f"Row {idx}: found {len(matches)} matches")
        if matches:
            logging.debug(f"Matched columns: {matches}")
        
        if len(matches) >= len(expected_columns) * 0.5:
            logging.info(f"Found header row at index {idx}")
            return idx
    
    raise ValueError(f"No header row found with expected columns: {expected_columns}")