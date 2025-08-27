import unittest
import os
import sys

# Add parent directory to path for module import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from indian_text_utils.address_parser_utils import EnhancedIndianAddressParser

class TestAddressParser(unittest.TestCase):
    def setUp(self):
        self.parser = EnhancedIndianAddressParser()

    def test_flat_number_with_hyphen(self):
        address = "B-177 ; Green Heights ; MG Extn ; Nagar 84 ; B/H Hospital ; Mangaluru ; Karnataka ; 575073"
        result = self.parser.parse_address(address)
        self.assertEqual(result['address_line_1'], "B-177")
        self.assertIn("Green Heights", result['address_line_2'])
        self.assertEqual(result['city'], "Mangaluru")
        self.assertEqual(result['state'], "Karnataka")
        self.assertEqual(result['pincode'], "575073")

    def test_landmark_and_city(self):
        address = "Flat 754 - Orchid Plaza - College Road - Colony 37 - Near Metro Stn - Ahmedabad - Gujarat - 380012"
        result = self.parser.parse_address(address)
        self.assertEqual(result['landmark'], "Near Metro Stn")
        self.assertEqual(result['city'], "Ahmedabad")
        self.assertEqual(result['state'], "Gujarat")
        self.assertEqual(result['pincode'], "380012")
        self.assertTrue(result['address_line_1'].startswith("Flat 754"))

    def test_simple_address_parsing(self):
        address = "8/4 ; Silver CHS ; Enclave 92 ; Ranchi ; 834086"
        result = self.parser.parse_address(address)
        self.assertEqual(result['city'], "Ranchi")
        self.assertEqual(result['pincode'], "834086")

if __name__ == "__main__":
    unittest.main()
