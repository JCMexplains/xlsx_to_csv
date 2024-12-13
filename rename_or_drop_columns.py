import re

import pandas as pd

def process_dataframe(df):


    column_mapping = { 
        "Course ID": "course_id",
        "RefNum": "reference_number",
        "F/P/E": None,
        "Pay": None,
        "Instructor Name": "instructor_name",
        "Sess": "session",
        "Start": "start_time",
        "End": "end_time",
        "Days": "days",
        "Bldg": "building",
        "Rm #": "room_number",
        "Rm Cap": "room_cap",
        "Cls Max": None,
        "Enrolled": None,
        "Paid": None,
        "Outlier": None,
        "Class Title": None,
        "Delivery Method": None,
        "Designators": None,
        "ZT": None,
        "Fees": None,
        "FTE": None,
        "Paid FTE": None,
        "Credit Hrs": None,
        "Act Cntct Hrs": None,
        "Std Cntct Hrs": None,
        "Campus": "campus",
        "Campus Code": None,
        "Division": "division",
        "Department": "department",
        "Cost Center": None,
        "Credit Type": None,
        "Term": "term",
        "Schedule Notes": None,
        "Course Description": None,
        "Curriculum.Primary Instructor Type": None,
        "Curriculum.Campus": None,
        "Curriculum.Course Pathway": None,
        "Curriculum.Division Department": None,
        "Curriculum.ICS Code": None,
        "Curriculum.Class Status": None,
        "Gen Ed": None,
        "SummaryKey": None,
        "Curriculum.Course Id Prefix": None,
        "Curriculum.Primary Instructor Id": None,
        "Curriculum.BC Course Discipline": None,
        "FPE": None,
        "CourseTermKey": None,
        "Random": None,
        "Sort": None,
        "Curriculum.Primary Instructor Job Profile": None,
        "ClassFilter": None,
        "Curriculum.Credit Non Credit Vocational": None,
        "Curriculum.Internal Job Classification": None
    }

    # Rename columns (only for existing columns)
    df = df.rename(
        columns={
            col: new_name
            for col, new_name in column_mapping.items()
            if col in df.columns and new_name is not None
        }
    )

    # Drop columns (only existing columns that are mapped to None)
    columns_to_drop = [
        col
        for col in df.columns
        if col in column_mapping and column_mapping[col] is None
    ]
    df = df.drop(columns=columns_to_drop)

    # Sort the columns alphabetically
    df = df.reindex(sorted(df.columns), axis=1)

    # Modify the string stripping part to handle non-string columns
    for col in df.columns:
        if df[col].dtype == 'object':  # only process string/object columns
            df[col] = df[col].astype(str).str.strip()

    return df
