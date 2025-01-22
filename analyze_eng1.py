import pandas as pd

# Read the CSV file
df = pd.read_csv('data/2024-12-13 data.csv')

# Filter for ENG1 division
eng1_df = df[df['division'] == 'Eng1']

print(f"Total number of ENG1 sections found: {len(eng1_df)}")

# Group by instructor, days, start_time, and end_time
conflicts = eng1_df.groupby(['instructor_name', 'days', 'start_time', 'end_time']).size().reset_index(name='count')

# Filter for cases where an instructor has multiple sections at the same time
conflicts = conflicts[conflicts['count'] > 1]

if len(conflicts) > 0:
    print('\nAnalyzing concurrent sections:')
    
    # Show the actual course details for these cases
    for _, row in conflicts.iterrows():
        concurrent_sections = eng1_df[
            (eng1_df['instructor_name'] == row['instructor_name']) &
            (eng1_df['days'] == row['days']) &
            (eng1_df['start_time'] == row['start_time']) &
            (eng1_df['end_time'] == row['end_time'])
        ][['course_id', 'reference_number', 'room_number', 'building', 'session']]
        
        # Get unique session numbers for these concurrent sections
        sessions = sorted(concurrent_sections['session'].unique())
        
        # Check if this is a problematic case (not a session 2 and 4 pair)
        is_problematic = not (len(sessions) == 2 and set(sessions) == {2, 4})
        
        if is_problematic:
            print(f"\n⚠️ PROBLEMATIC: {row['instructor_name']} on {row['days']} at {row['start_time']}-{row['end_time']}")
            print("Sessions:", sessions)
            print(concurrent_sections)
        else:
            print(f"\n✓ OK: {row['instructor_name']} on {row['days']} at {row['start_time']}-{row['end_time']} (Sessions 2 & 4)")
else:
    print('\nNo instructors are teaching multiple ENG1 sections at the same days/times.') 