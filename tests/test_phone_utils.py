"""
Tests for phone_utils module
"""

import pytest
from indian_text_utils.phone_utils import clean_indian_phone

class TestPhoneUtils:
    """Test cases for Indian phone number cleaning"""
    
    def test_basic_ten_digit_number(self):
        """Test basic 10-digit Indian mobile number"""
        assert clean_indian_phone("9876543210") == "+919876543210"
        assert clean_indian_phone("7876543210") == "+917876543210"
    
    def test_formatted_numbers(self):
        """Test various formatted numbers"""
        assert clean_indian_phone("+91 98765 43210") == "+919876543210"
        assert clean_indian_phone("91-9876543210") == "+919876543210"
        assert clean_indian_phone("(+91) 9876543210") == "+919876543210"
    
    def test_numbers_with_text(self):
        """Test numbers embedded in text"""
        assert clean_indian_phone("WhatsApp: 919876543210") == "+919876543210"
        assert clean_indian_phone("Call me at 09876543210") == "+919876543210"
    
    def test_invalid_numbers(self):
        """Test invalid inputs"""
        assert clean_indian_phone("5876543210") is None  # Invalid prefix
        assert clean_indian_phone("invalid123") is None
        assert clean_indian_phone("") is None
        assert clean_indian_phone(None) is None
    
    def test_edge_cases(self):
        """Test edge cases"""
        assert clean_indian_phone("098765-43210") == "+919876543210"
        assert clean_indian_phone("Mobile - 98765-43210") == "+919876543210"