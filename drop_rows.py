import pandas as pd


def drop_rows(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove rows from the DataFrame based on specific conditions.

    This function filters out rows that don't meet certain criteria,
    such as empty 'days' fields, non-Central campus, TBA buildings or start times,
    and null room numbers.

    Args:
        df (pd.DataFrame): The input DataFrame to be filtered.

    Returns:
        pd.DataFrame: A new DataFrame with rows removed based on the specified conditions.

    Note:
        This function modifies the following columns if they exist:
        'days', 'campus', 'building', 'start_time', and 'room_number'.
        It prints warnings if any of these columns are missing.
    """

    # Check if 'days' column exists
    if "days" in df.columns:
        # Drop rows where 'days' is empty or equals ONLINE
        df = df.dropna(subset=["days"])
        df = df[(df["days"] != "") & (df["days"] != "ONLINE")]
    else:
        print("Warning: 'days' column not found in DataFrame")

    # Check if 'campus' column exists
    if "campus" in df.columns:
        # Drop rows where 'campus' is not 'Central'
        df = df[df["campus"] == "Central"]
    else:
        print("Warning: 'campus' column not found in DataFrame")

    # Check if 'building' column exists
    if "building" in df.columns:
        # Drop rows where 'building' is 'TBA'
        df = df[df["building"] != "TBA"]
    else:
        print("Warning: 'building' column not found in DataFrame")

    # Check if 'start_time' column exists
    if "start_time" in df.columns:
        # Drop rows where 'start_time' is 'TBA'
        df = df[df["start_time"] != "TBA"]
    else:
        print("Warning: 'start_time' column not found in DataFrame")

    # Check if 'room_number' column exists
    if "room_number" in df.columns:
        # Convert room_number to numeric, coerce errors to NaN
        df["room_number"] = pd.to_numeric(df["room_number"], errors="coerce")
        # Drop rows where 'room_number' is null after processing
        df = df.dropna(subset=["room_number"])
    else:
        print("Warning: 'room_number' column not found in DataFrame")

    return df
