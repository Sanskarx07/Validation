import re
from datetime import datetime

def validate_and_correct_date(date_str):
    # Define the valid date formats with different separators
    date_formats = [
        '%m-%d-%Y', '%d-%m-%Y', '%Y-%m-%d',
        '%b-%d-%Y', '%d-%b-%Y', '%Y-%b-%d',
        '%m/%d/%Y', '%d/%m/%Y', '%Y/%m/%d',
        '%b/%d/%Y', '%d/%b/%Y', '%Y/%b/%d'
    ]
    
    # Define month names to convert to numeric
    month_name_to_number = {month: index for index, month in enumerate(["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], start=1)}

    def correct_month_name(date_str):
        # Convert month names to numeric
        for month_name, month_number in month_name_to_number.items():
            if month_name in date_str.lower():
                return date_str.lower().replace(month_name, str(month_number).zfill(2))
        return date_str

    def replace_separators(date_str):
        return re.sub(r'[-/]', '-', date_str)
    
    # Correct the month names and replace separators in the input date string
    date_str_corrected = correct_month_name(date_str)
    date_str_corrected = replace_separators(date_str_corrected)
    
    for date_format in date_formats:
        try:
            # Try to parse the date
            parsed_date = datetime.strptime(date_str_corrected, date_format)
            
            # Check if the date is within the valid range
            if 1900 <= parsed_date.year <= 2024 and 1 <= parsed_date.month <= 12 and 1 <= parsed_date.day <= 31:
                # Return valid date in the correct format
                return "valid", parsed_date.strftime('%m-%d-%Y')
        except ValueError:
            # Continue if the current format does not match
            continue

    # If no valid date format was found, check if the format is correct but date itself is invalid
    for date_format in date_formats:
        try:
            # Extract the parts of the date
            parsed_date = datetime.strptime(date_str_corrected, date_format)
            # If we can parse the date, format it correctly
            return "valid", parsed_date.strftime('%m-%d-%Y')
        except ValueError:
            continue

    return "invalid", date_str

# Test cases
dates = [
    "01-15-2022", "15-01-2022", "2022-01-15", 
    "jan-15-2022", "15-jan-2022", "2022-jan-15", 
    "01/15/2022", "15/01/2022", "2022/01/15", 
    "jan/15/2022", "15/jan/2022", "2022/jan/15", 
    "31-02-2020", "15-13-2022", "2022-15-01",
    "31/02/2020", "15/13/2022", "2022/15/01",
    "26/10/2023", "2023/10/26"
]

for date in dates:
    status, corrected_date = validate_and_correct_date(date)
    if(status=="invalid"):
      print(f"Input: {date}, Status: {status}, Output: Wrong date")
    else :
      print(f"Input: {date}, Status: {status}, Output: {corrected_date}")
