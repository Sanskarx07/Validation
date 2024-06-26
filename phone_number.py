import re

def validate_and_correct_phone_number(phone_number):
    pattern = r'^(?!0{3}-|1{3}-)(?!(\d)\1{2}-\1{3}-\1{4}$)\d{3}-\d{3}-\d{4}$'
    
    # Check if the phone number matches the pattern
    if re.match(pattern, phone_number):
        return "Valid format: {}".format(phone_number)
    else:
        # Remove any non-digit characters
        digits_only = re.sub(r'\D', '', phone_number)
        
        # Correct format xxx-xxx-xxxx
        formatted_number = '{}-{}-{}'.format(digits_only[:3], digits_only[3:6], digits_only[6:])
        return "Invalid format. Corrected to: {}".format(formatted_number)

# Example usage:
phone1 = "1234727890"
phone2 = "111-111-1111"
phone3 = "999-999-9999"
phone4 = "012-345-6789"
phone5 = "112-345-6789"

print(validate_and_correct_phone_number(phone1))
print(validate_and_correct_phone_number(phone2))
print(validate_and_correct_phone_number(phone3))
print(validate_and_correct_phone_number(phone4))
print(validate_and_correct_phone_number(phone5))
