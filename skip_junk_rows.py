import pandas as pd
import logging

def find_header_row(excel_file, expected_columns):
    """
    Find the actual header row in an Excel file by looking for expected column names.
    Returns the index of the header row.
    """
    logging.debug(f"Expected columns: {expected_columns}")
    
    # Read the first several rows of the Excel file
    preview_df = pd.read_excel(excel_file, nrows=20)
    
    # Try each row as a potential header
    for idx in range(len(preview_df)):
        # Get the row values as potential headers
        potential_headers = preview_df.iloc[idx].values
        # Convert to strings and clean whitespace
        potential_headers = [str(h).strip() if pd.notna(h) else "" for h in potential_headers]
        
        logging.debug(f"\nChecking row {idx}:")
        logging.debug(f"Potential headers: {potential_headers}")
        
        # Check if any of our expected columns are in this row
        matches = []
        for col in expected_columns:
            if col in potential_headers:
                matches.append(col)
        
        match_count = len(matches)
        logging.debug(f"Found {match_count} matches out of {len(expected_columns)} expected columns")
        if matches:
            logging.debug(f"Matched columns: {matches}")
        
        # If we find most of our expected columns, this is likely the header row
        if match_count >= len(expected_columns) * 0.5:  # At least 50% match
            logging.info(f"Found header row at index {idx} with {match_count} matching columns")
            return idx
    
    error_msg = f"Could not find header row containing at least 50% of expected columns: {expected_columns}"
    logging.error(error_msg)
    raise ValueError(error_msg) 