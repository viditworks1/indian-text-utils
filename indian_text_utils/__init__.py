"""
Indian Text Utils - Utility functions for processing Indian text data

A collection of tools for handling Indian phone numbers, addresses, names, 
and other text processing tasks common in Indian applications.
"""

__version__ = "0.1.0"
__author__ = "Vidit"

# Import main functions for easy access
from .phone_utils import clean_indian_phone

# Make functions available when importing the package
__all__ = ['clean_indian_phone']