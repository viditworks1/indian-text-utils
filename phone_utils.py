def clean_indian_phone(phone_input):
    """
    Clean and standardize Indian phone numbers to +91XXXXXXXXXX format
    
    Examples:
    clean_indian_phone("9876543210") → "+919876543210"
    clean_indian_phone("91-9876543210") → "+919876543210" 
    clean_indian_phone("+91 98765 43210") → "+919876543210"
    """
    
    if not phone_input:
        return None
    
    # Convert to string and remove all spaces, dashes, parentheses
    phone = str(phone_input).strip()
    phone = phone.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    
    # Remove leading + if present
    if phone.startswith("+"):
        phone = phone[1:]
    
    # Remove leading 0 if present (Indian format)
    if phone.startswith("0"):
        phone = phone[1:]
    
    # Add country code if missing
    if len(phone) == 10 and phone[0] in "6789":  # Valid Indian mobile starts with 6,7,8,9
        phone = "91" + phone
    
    # Validate: should be 12 digits starting with 91
    if len(phone) == 12 and phone.startswith("91") and phone[2:].isdigit():
        return "+" + phone
    else:
        return None  # Invalid number


# Test function
if __name__ == "__main__":
    test_cases = [
        "9876543210",
        "+91 98765 43210", 
        "91-9876543210",
        "098765-43210",
        "(+91) 9876543210",
        "invalid123"
    ]
    
    print("Testing phone number cleaner:")
    for test in test_cases:
        result = clean_indian_phone(test)
        print(f"'{test}' → '{result}'")