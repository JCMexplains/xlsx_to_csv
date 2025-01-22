import re

import pandas as pd

def process_dataframe(df):


    column_mapping = { 
        "Course ID": "course_id",
        "RefNum": "reference_number",
        "Instructor Name": "instructor_name",
        "Sess": "session",
        "Start": "start_time",
        "End": "end_time",
        "Days": "days",
        "Bldg": "building",
        "Rm #": "room_number",
        "Rm Cap": "room_cap",
        "Campus": "campus",
        "Division": "division",
        "Department": "department",
        "Term": "term"
    }

    # Drop columns that aren't in our mapping dictionary
    columns_to_drop = [col for col in df.columns if col not in column_mapping]
    df = df.drop(columns=columns_to_drop)

    # Rename columns (only for existing columns that have a new name)
    df = df.rename(
        columns={
            col: new_name
            for col, new_name in column_mapping.items()
            if col in df.columns and new_name is not None
        }
    )

    # Sort the columns alphabetically
    df = df.reindex(sorted(df.columns), axis=1)

    # Modify the string stripping part to handle non-string columns
    for col in df.columns:
        if df[col].dtype == 'object':  # only process string/object columns
            df[col] = df[col].astype(str).str.strip()

    return df
