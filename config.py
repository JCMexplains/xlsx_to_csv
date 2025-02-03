# Configuration for column mapping and data processing
COLUMN_MAPPING = {
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

# Column type configurations
INTEGER_COLUMNS = ["reference_number", "room_cap", "session", "term"]
TEXT_COLUMNS = ["campus", "department", "division"]
TIME_COLUMNS = ["start_time", "end_time"]

# File patterns
EXCEL_PATTERN = "data*.xlsx" 