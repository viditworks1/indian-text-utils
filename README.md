# Indian Text Utils

Utility functions for processing Indian text data - phone numbers, addresses, names, and more.

## Features

### Phone Number Cleaner
```python
from phone_utils import clean_indian_phone

clean_indian_phone("9876543210")        # → "+919876543210"  
clean_indian_phone("+91 98765 43210")   # → "+919876543210"
clean_indian_phone("91-9876543210")     # → "+919876543210"