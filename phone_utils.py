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
import re


import re

def clean_indian_phone(phone_input):
    """
    Clean and standardize Indian phone numbers to +91XXXXXXXXXX format
    Handles messy real-world input with prefixes, suffixes, and extra text
    """
    
    if not phone_input:
        return None
    
    # Convert to string
    phone = str(phone_input).strip()
    
    # Remove all non-digits except +
    digits_only = re.sub(r'[^\d+]', '', phone)
    
    # Handle different patterns
    if digits_only.startswith('+91'):
        number = digits_only[3:]  # Remove +91
    elif digits_only.startswith('91'):
        number = digits_only[2:]  # Remove 91
    else:
        number = digits_only
    
    # Remove leading zeros
    number = number.lstrip('0')
    
    # Validate: exactly 10 digits starting with 6-9
    if len(number) == 10 and number[0] in '6789' and number.isdigit():
        return f"+91{number}"
    
    return None


# Enhanced test function
def test_phone_cleaner():
    test_cases = [
        # Original cases
        ("9876543210", "+919876543210"),
        ("+91 98765 43210", "+919876543210"),
        ("91-9876543210", "+919876543210"),
        ("098765-43210", "+919876543210"),
        ("(+91) 9876543210", "+919876543210"),
        ("invalid123", None),
        
        # Messy real-world cases
        ("tel: +91-9876543210", "+919876543210"),
        ("9876543210 (Vidit)", "+919876543210"),
        ("91 9876 543 210 ext 123", "+919876543210"),
        ("WhatsApp: 919876543210", "+919876543210"),
        ("Call me at 09876543210", "+919876543210"),
        ("+919876543210#123", "+919876543210"),
        ("Mobile - 98765-43210", "+919876543210"),
        ("   +91  9876  543210   ", "+919876543210"),
        ("7876543210", "+917876543210"),
        ("5876543210", None),  # Invalid start digit
        ("", None)
    ]
    
    passed = 0
    total = len(test_cases)
    
    print("Testing enhanced phone cleaner:")
    for input_val, expected in test_cases:
        result = clean_indian_phone(input_val)
        status = "✅" if result == expected else "❌"
        print(f"{status} '{input_val}' → '{result}' (expected: '{expected}')")
        if result == expected:
            passed += 1
    
    print(f"\nSuccess Rate: {passed}/{total} ({passed/total*100:.1f}%)")
    return passed == total

if __name__ == "__main__":
    test_phone_cleaner()