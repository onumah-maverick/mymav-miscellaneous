import pandas as pd
from datetime import datetime, timedelta
from collections import defaultdict

# Define Public Holiday Map
GHANA_HOLIDAYS = ['01/01/2026', '09/01/2026', '06/03/2026', '20/03/2026', '21/03/2026', 
                  '03/04/2026', '06/04/2026', '01/05/2026', '25/05/2026', '28/05/2026', 
                  '01/07/2026', '21/09/2026', '04/12/2026', '25/12/2026', '26/12/2026']
CIV_HOLIDAYS = ['01/01/2026', '17/03/2026', '20/03/2026', '06/04/2026', '01/05/2026', 
                '14/05/2026', '25/05/2026', '28/05/2026', '07/08/2026', '15/08/2026', 
                '25/08/2026', '01/11/2026', '15/11/2026', '25/12/2026']
CAM_HOLIDAYS = ['01/01/2026', '11/02/2026', '20/03/2026', '03/04/2026', '01/05/2026', '14/05/2026',
                '20/05/2026', '28/05/2026', '15/08/2026', '25/08/2026', '25/12/2026']

# Mapping of outlet codes to their public holidays
outlet_country_map = {
    'GHANA': GHANA_HOLIDAYS,
    "COTE D’IVOIRE": CIV_HOLIDAYS,
    'CAMEROON': CAM_HOLIDAYS,
}


# Function to check if the date is a public holiday
def is_public_holiday(date, country):
    if pd.isnull(date):
        return False
    holiday_list = outlet_country_map.get(country, [])
    date_str = date.strftime('%d/%m/%Y')

    # print(f"DEBUG: '{date_str}' in {holiday_list[:2]}...? {date_str in holiday_list}")  # SEE THE TRUTH
    return date_str in holiday_list

# Function to get a valid weekday (not a weekend or public holiday)
def get_valid_weekday(date, country):
    while date.weekday() >= 5 or is_public_holiday(date, country):
        date += timedelta(days=1)
    return date


# Function to get candidate dates for next visit within the specified date range (x month to y month)
def get_candidate_dates(last_visit_date, country):
    candidates = []
    # The valid date range: from x month to y month
    target_date_start = datetime(2026, 5, 5)
    target_date_end = datetime(2026, 5, 25)


    # Gather all valid weekdays and Saturdays in the window
    current_date = target_date_start
    while current_date <= target_date_end:
        is_holiday = is_public_holiday(current_date, country)
        date_str = current_date.strftime('%d/%m/%Y')
        print(f"Checking {date_str}, country {country}: holiday={is_holiday}")
        if current_date.weekday() < 4 and not is_holiday:  # Weekdays (Mon-Fri)
            candidates.append(current_date)
        elif current_date.weekday() == 4 and not is_holiday:  # Saturdays
            candidates.append(current_date)
        current_date += timedelta(days=1)
        # print(f"{current_date.strftime('%d/%m/%Y')} is_holiday={is_public_holiday(current_date, country)}")

    return candidates


# Function to assign visits to surveyors, ensuring no more than 4 visits per day and visits on all valid dates
def distribute_visits_evenly(df):
    surveyor_visit_counts = defaultdict(lambda: defaultdict(int))  # surveyor -> {date: count}
    next_visit_dates = []

    # Iterate through each row in the DataFrame
    for idx, row in df.iterrows():
        country = row['Country']
        last_visit_date = row['Date']
        surveyor = row['Surveyor']

        # Get all candidate dates within the specified range
        candidates = get_candidate_dates(last_visit_date, country)

        assigned_date = None
        # Check if a valid date exists within candidate dates
        for candidate in candidates:
            if surveyor_visit_counts[surveyor][candidate] < 4:
                assigned_date = candidate
                surveyor_visit_counts[surveyor][candidate] += 1
                break

        if assigned_date is None:
            # If no valid date found, assign a fallback date by checking other dates in the 30-day window
            fallback_start = last_visit_date + timedelta(days=29)
            fallback_end = last_visit_date + timedelta(days=33)
            candidate_date = get_valid_weekday(fallback_start, country)
            assigned_date = candidate_date
            surveyor_visit_counts[surveyor][assigned_date] += 1

        # Add the assigned date for the next visit
        next_visit_dates.append(assigned_date)

    df['Next_Visit_Date'] = next_visit_dates
    return df


# Main function to calculate the next visit dates
def calculate_next_visit_date(df):
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
    df = distribute_visits_evenly(df)
    return df


# input data (replace "TimePlanTest.csv" with your actual CSV file) - Delete previous visit column and rename current visit as date.
data = pd.read_excel(r"C:\Users\Andrew\OneDrive\retail audit\profile files\for may 2026\fieldwork_profile_apr26.xlsx", sheet_name="for_visitplan")
df = pd.DataFrame(data)

# Calculate next visit dates
df1 = calculate_next_visit_date(df)

# Debugging: Check if 'Next_Visit_Date' exists
print("Columns in df1 before export:", df1.columns.tolist())

# Export output(replace insert name with output file name)
df.to_excel(r'C:\Users\Andrew\OneDrive\retail audit\audit plan for DA\visitplan_may26.xlsx', index=False)
