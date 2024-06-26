import re

def validate_email(email):
    # Define regex for a valid email
    email_regex = re.compile(
        r"^(?!.*\.\.)(?!.*\.\.@)(?!.*@\.)(?!.*\.@)(?!.*\.$)[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    )
    
    # Check if email matches the regex
    if not email_regex.match(email):
        # Identify specific issues
        issues = []
        
        # Check for double dots
        if ".." in email:
            issues.append("Email contains consecutive dots (..).")
        
        # Check for leading or trailing dots
        if email.startswith(".") or email.endswith("."):
            issues.append("Email contains leading or trailing dots.")
        
        # Check for dots around @
        if ".@" in email or "@." in email:
            issues.append("Email contains dots just before or after '@'.")
        
        # Check if @ is present
        if "@" not in email:
            issues.append("Email does not contain '@'.")
        
        # Check for proper domain and TLD
        parts = email.split("@")
        if len(parts) != 2:
            issues.append("Email should contain exactly one '@'.")
        else:
            local_part, domain_part = parts
            domain_parts = domain_part.split(".")
            if len(domain_parts) < 2:
                issues.append("Domain part should contain at least one dot.")
            elif any(not part for part in domain_parts):
                issues.append("Domain part should not have empty labels (e.g., '..')")
            else:
                tld = domain_parts[-1]
                if len(tld) < 2:
                    issues.append("Top-level domain (TLD) should be at least 2 characters long.")
        
        # Provide recommendations
        recommendations = "Please ensure the email has:\n"
        recommendations += "- No consecutive dots.\n"
        recommendations += "- No leading or trailing dots.\n"
        recommendations += "- No dots just before or after '@'.\n"
        recommendations += "- Exactly one '@'.\n"
        recommendations += "- A proper domain and TLD (e.g., example.com)."
        
        return "Invalid", issues, recommendations
    
    return "Valid", [], "The email is valid."

# Test the function
emails = [
    "test..email@example.com",
    ".testemail@example.com",
    "testemail.@example.com",
    "testemail@.example.com",
    "testemail@example..com",
    "testemail@examplecom",
    "testemail@com",
    "testemail@example.com"
    "test..aijs@email.com",
    ".test@gmail.com",
    "tess@_@gmail.com"
]

for email in emails:
    status, issues, recommendations = validate_email(email)
    print(f"Email: {email}")
    print(f"Status: {status}")
    if status == "Invalid":
        print("Issues:")
        for issue in issues:
            print(f"- {issue}")
        print("Recommendations:")
        print(recommendations)
    print()
