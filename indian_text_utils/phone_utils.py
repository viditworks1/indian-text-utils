import re

def clean_indian_phone(phone_input):
    """
    Clean and standardize Indian mobile numbers to +91XXXXXXXXXX format
    
    Based on TRAI National Numbering Plan (verified Aug 2024):
    - Indian mobile numbers start with 6, 7, 8, or 9
    - Source: Wikipedia, TRAI documentation
    - Note: TRAI is updating numbering plan in 2024, may change
    
    Args:
        phone_input: String containing phone number in any format
        
    Returns:
        str: Standardized phone number (+91XXXXXXXXXX) or None if invalid
    """
    
    if not phone_input:
        return None
    
    # Convert to string and remove all non-digits except +
    phone = str(phone_input).strip()
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
    
    # Validate: exactly 10 digits starting with 6-9 (per TRAI numbering plan)
    VALID_INDIAN_MOBILE_PREFIXES = ['6', '7', '8', '9']  # Source: TRAI/Wikipedia 2024
    
    if (len(number) == 10 and 
        number[0] in VALID_INDIAN_MOBILE_PREFIXES and 
        number.isdigit()):
        return f"+91{number}"
    
    return None

def interactive_test():
    """Interactive testing function - great for GitHub demos"""
    print("🔧 Indian Mobile Number Cleaner")
    print("=" * 40)
    print("✨ Based on TRAI numbering plan (verified Aug 2025)")
    print("📱 Supports Indian mobile numbers starting with 6, 7, 8, 9")
    print()
    print("Enter numbers to test (type 'quit' to exit):")
    print("Examples: 9876543210, +91-98765-43210, WhatsApp: 9876543210")
    print()
    
    while True:
        user_input = input("📞 Enter phone: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("👋 Thanks for testing!")
            break
            
        if not user_input:
            continue
            
        result = clean_indian_phone(user_input)
        
        if result:
            print(f"✅ Cleaned: {result}")
        else:
            print(f"❌ Invalid (not Indian mobile format)")
        print("-" * 30)


if __name__ == "__main__":
    interactive_test()