import re
import pandas as pd

# Move column_mapping outside the function
column_mapping = { 
    "Bldg": "building",
    "Campus": "campus",
    "Course ID": "course_id",
    "Days": "days",
    "Department": "department",
    "Designators": "designators",
    "Division": "division",
    "End": "end_time",
    "Instructor Name": "instructor_name",
    "RefNum": "reference_number",
    "Rm #": "room_number",
    "Rm Cap": "room_cap",
    "Sess": "session",
    "Start": "start_time",
    "Term": "term"
}

def process_dataframe(df):

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
