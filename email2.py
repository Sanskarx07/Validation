import re

def validate_email(email):
    # Regular expression for basic email validation
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    # Initialize validation result
    result = {
        "Email": email,
        "Is Valid": True,
        "Reason": "Email is valid.",
        "Suggestion": "No action needed."
    }

    # Check if email matches the basic regex
    if not re.match(regex, email):
        result["Is Valid"] = False
        result["Reason"] = "Email does not match the basic format."
        result["Suggestion"] = "Ensure the email follows the format localpart@domain.tld"
        return result

    # Additional checks
    local_part, domain_part = email.rsplit('@', 1)

    # Check for double dots in the email
    if '..' in email:
        result["Is Valid"] = False
        result["Reason"] = "Email contains double dots."
        result["Suggestion"] = "Remove any consecutive dots."
        return result

    # Check for leading and trailing dots in local part
    if local_part.startswith('.') or local_part.endswith('.'):
        result["Is Valid"] = False
        result["Reason"] = "Email has leading or trailing dots in the local part."
        result["Suggestion"] = "Remove dots at the start or end of the local part."
        return result

    # Check for dots just before and after @
    if local_part.endswith('.') or domain_part.startswith('.'):
        result["Is Valid"] = False
        result["Reason"] = "Email has dots just before or after @."
        result["Suggestion"] = "Ensure there are no dots immediately before or after @."
        return result

    # Check for proper domain part and TLD
    domain_parts = domain_part.split('.')
    if len(domain_parts) < 2:
        result["Is Valid"] = False
        result["Reason"] = "Domain part is incomplete."
        result["Suggestion"] = "Ensure the domain part has at least one dot separating the domain and the TLD."
        return result

    # Check for valid TLD length
    tld = domain_parts[-1]
    if len(tld) < 2:
        result["Is Valid"] = False
        result["Reason"] = "Top-level domain (TLD) is too short."
        result["Suggestion"] = "Ensure the TLD is at least 2 characters long."
        return result
    
    
            
    # If all checks pass, the email is valid
    result["Is Valid"] = True
    result["Reason"] = "Email is valid."
    result["Suggestion"] = "No action needed."

    return result

def print_validation_result(result):
    print("------------------------")
    print(f"Email:      {result['Email']}")
    print(f"Is Valid:   {result['Is Valid']}")
    print(f"Reason:     {result['Reason']}")
    print(f"Suggestion: {result['Suggestion']}")



def improve_email(email):
    

    # Apply corrections based on the suggested improvements
    corrected_email = email
    
    if "double dots" in validation_result["Reason"].lower():
        corrected_email = corrected_email.replace('..', '.')

    if "leading or trailing dots" in validation_result["Reason"].lower():
        corrected_email = corrected_email.strip('.')

    if "dots just before or after @" in validation_result["Reason"].lower():
        corrected_email = corrected_email.replace('.@', '@').replace('@.', '@')

    if "domain part is incomplete" in validation_result["Reason"].lower():
        local_part, domain_part = corrected_email.rsplit('@', 1)
        if '.' not in domain_part:
            corrected_email = f"{local_part}@{domain_part}.com"  # Assuming .com as default TLD

    if "top-level domain (tld) is too short" in validation_result["Reason"].lower():
        local_part, domain_part = corrected_email.rsplit('@', 1)
        domain_parts = domain_part.split('.')
        if len(domain_parts[-1]) < 2:
            domain_parts[-1] = "com"  # Assuming .com as default TLD
            corrected_email = f"{local_part}@{'.'.join(domain_parts)}"
    
    # Remove trailing dots before @
    local_part, domain_part = corrected_email.rsplit('@', 1)
    corrected_local_part = local_part.rstrip('.')
    corrected_email = f"{corrected_local_part}@{domain_part}"

    # Remove extra @ in local part
    if corrected_email.count('@') > 1:
        corrected_email = corrected_email.replace('@', '', 1)

    return corrected_email
   

# Example usage:
emails = [
    "test..email@example.com",
    ".testemail@example.com",
    "testemail.@example.com",
    "testemail@.example.com",
    "testemail@example..com",
    "testemail@examplecom",
    "testemail@com",
    "testemail@example.com",
    "test..aijs@email.com",
    ".test@gmail.com",
    "tess@_@gmail.com",
    "sanskar.ojha@gmailcom"
]

for i in emails:
   validation_result = validate_email(i)
   if(validation_result["Is Valid"]==False):
     print_validation_result(validation_result)
     improved_email = improve_email(i)
     print(f"\nOriginal Email:   {i}")
     print(f"Improved Email:   {improved_email}\n")
   else:
       print_validation_result(validation_result)

   

