# Configuration for column mapping and data processing
COLUMN_MAPPING = {
    "Bldg": "building",
    "Campus": "campus",
    "Class Title": "class_title",
    "Cls Max": "class_max",
    "Course ID": "course_id",
    "Days": "days",
    "Delivery Method": "delivery_method",
    "Department": "department",
    "Designators": "designators",
    "Division": "division",
    "End": "end_time",
    "Enrolled": "students_enrolled",
    "Instructor Name": "instructor_name",
    "Paid": "students_paid",
    "Pay": "pay_method",
    "RefNum": "reference_number",
    "Rm #": "room_number",
    "Rm Cap": "room_cap",
    "Schedule Notes": "schedule_notes",
    "Sess": "session",
    "Start": "start_time",
    "Term": "term",
}

# Column type configurations
INTEGER_COLUMNS = ["reference_number", "room_cap", "session", "term"]
TEXT_COLUMNS = ["campus", "department", "division"]
TIME_COLUMNS = ["start_time", "end_time"]

# File patterns
EXCEL_PATTERN = "data*.xlsx"
