import csv
import re
import argparse
import os


class EnhancedIndianAddressParser:
    def __init__(self):
        self.indian_cities = {
            'ranchi', 'ahmedabad', 'vijayawada', 'visakhapatnam', 'mangaluru', 'mysuru',
            'ghaziabad', 'chandigarh', 'varanasi', 'jaipur', 'lucknow', 'meerut', 'bengaluru',
            'mumbai', 'delhi', 'kolkata', 'chennai', 'hyderabad', 'pune', 'surat', 'kanpur',
            'nagpur', 'patna', 'indore', 'thane', 'bhopal', 'ludhiana', 'agra', 'vadodara',
            'coimbatore', 'kochi', 'thiruvananthapuram', 'madurai', 'nashik', 'faridabad',
            'rajkot', 'vasai', 'jodhpur', 'guwahati', 'dhanbad', 'amritsar', 'allahabad',
            'jabalpur', 'haora', 'aurangabad', 'solapur', 'jammu', 'gwalior', 'tiruchirappalli',
            'salem', 'tirunelveli', 'bangalore'
        }

        self.indian_states = {
            'andhra pradesh', 'arunachal pradesh', 'assam', 'bihar', 'chhattisgarh', 'goa',
            'gujarat', 'haryana', 'himachal pradesh', 'jharkhand', 'karnataka', 'kerala',
            'madhya pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram', 'nagaland',
            'odisha', 'punjab', 'rajasthan', 'sikkim', 'tamil nadu', 'telangana', 'tripura',
            'uttar pradesh', 'uttarakhand', 'west bengal', 'delhi'
        }

        self.pincode_pattern = re.compile(r'\b[1-9][0-9]{5}\b')
        self.landmark_keywords = ['near', 'nr', 'next to', 'opp', 'opposite', 'behind', 'adj', 'beside']

        # Detect flat number with hyphen at start within first ~5 chars, e.g. B-98, D-198
        self.flat_number_pattern = re.compile(r'^([A-Za-z]-\d{1,3})(?=\s|;|,|$)')

        self.pincode_dict = {}

    def load_pincode_dict(self, filename):
        if os.path.exists(filename):
            with open(filename, encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    pincode = row['pincode'].strip()
                    self.pincode_dict[pincode] = {
                        'state': row.get('statename', '').strip()
                    }

    def load_cities_states(self, filename):
        if os.path.exists(filename):
            with open(filename, encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    city = row.get('city', '').strip().lower()
                    state = row.get('state', '').strip().lower()
                    if city:
                        self.indian_cities.add(city)
                    if state:
                        self.indian_states.add(state)

    def extract_pincode(self, address):
        match = self.pincode_pattern.search(address)
        return match.group() if match else ''

    def extract_landmark(self, address):
        address_lower = address.lower()
        for kw in self.landmark_keywords:
            pattern = rf'\b{kw}\b[^,;|\-]*'
            match = re.search(pattern, address_lower)
            if match:
                landmark = match.group().strip()
                if len(landmark) > len(kw) + 2:
                    return landmark.title()
        return ''

    def find_city_state_from_text(self, address):
        address_lower = address.lower()
        found_city = ''
        found_state = ''

        words = address_lower.split()
        phrases_to_check = []
        phrases_to_check.extend(words)
        for i in range(len(words) - 1):
            phrases_to_check.append(f"{words[i]} {words[i+1]}")
        for i in range(len(words) - 2):
            phrases_to_check.append(f"{words[i]} {words[i+1]} {words[i+2]}")

        for phrase in phrases_to_check:
            if phrase in self.indian_cities:
                found_city = phrase.title()
                break
        for phrase in phrases_to_check:
            if phrase in self.indian_states:
                found_state = phrase.title()
                break

        return found_city, found_state

    def normalize_part(self, part):
        return part.title().strip() if part else ''

    def join_if_short(self, parts, max_length=3):
        merged = []
        buffer = ''
        for p in parts:
            if len(p) <= max_length:
                buffer += (p + ' ')
            else:
                if buffer:
                    merged.append(buffer.strip())
                    buffer = ''
                merged.append(p)
        if buffer:
            merged.append(buffer.strip())
        return merged

    def parse_address(self, address):
        original_address = address.strip()

        pincode = self.extract_pincode(original_address)
        landmark = self.extract_landmark(original_address)
        city, state = self.find_city_state_from_text(original_address)

        enrichment = self.pincode_dict.get(pincode, {})
        if not state and enrichment.get('state'):
            state = enrichment.get('state').title()

        # Remove city, state, pincode and landmark strings from address before splitting
        addr_line_raw = original_address
        for part in [pincode, landmark, city, state]:
            if part:
                addr_line_raw = re.sub(re.escape(part), '', addr_line_raw, flags=re.IGNORECASE).strip()

        # Detect flat number pattern like 'B-98' at start and extract it
        flat_number_match = self.flat_number_pattern.match(addr_line_raw)
        flat_number = ''
        if flat_number_match:
            flat_number = flat_number_match.group(1)
            addr_line_raw = addr_line_raw[len(flat_number):].strip()

        # Split remaining address on delimiters
        parts = [p.strip() for p in re.split(r'[;|,\\-]+', addr_line_raw) if p.strip()]

        # Build address lines, prefixing with flat number if present
        if flat_number:
            address_line_1 = flat_number
            address_line_2 = self.normalize_part(parts[0]) if parts else ''
            address_line_3 = self.normalize_part(' '.join(parts[1:])) if len(parts) > 1 else ''
        else:
            if len(parts) >= 3:
                address_line_1 = self.normalize_part(parts[0])
                address_line_2 = self.normalize_part(parts[1])
                address_line_3 = self.normalize_part(' '.join(parts[2:]))
            elif len(parts) == 2:
                address_line_1 = self.normalize_part(parts[0])
                address_line_2 = self.normalize_part(parts[1])
                address_line_3 = ''
            elif len(parts) == 1:
                address_line_1 = self.normalize_part(parts[0])
                address_line_2 = ''
                address_line_3 = ''
            else:
                address_line_1 = ''
                address_line_2 = ''
                address_line_3 = ''

        return {
            'address_line_1': address_line_1,
            'address_line_2': address_line_2,
            'address_line_3': address_line_3,
            'landmark': landmark,
            'city': city,
            'state': state,
            'pincode': pincode
        }


def bulk_parse(input_path, output_path, pincode_csv=None, cities_states_csv=None):
    parser = EnhancedIndianAddressParser()
    if pincode_csv:
        parser.load_pincode_dict(pincode_csv)
    if cities_states_csv:
        parser.load_cities_states(cities_states_csv)

    if not os.path.exists(input_path):
        print(f"Input file not found: {input_path}")
        return

    with open(input_path, encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        if 'address' not in reader.fieldnames:
            print("Input CSV must contain an 'address' column for bulk parsing.")
            return
        rows = list(reader)

    out_fieldnames = reader.fieldnames + [
        'address_line_1', 'address_line_2', 'address_line_3', 'landmark', 'city', 'state', 'pincode'
    ]

    with open(output_path, 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=out_fieldnames)
        writer.writeheader()
        for row in rows:
            parsed = parser.parse_address(row['address'])
            row.update(parsed)
            writer.writerow(row)
    print(f"Output saved to {output_path}")


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="Enhanced Indian Address Parser")
    arg_parser.add_argument("--bulk", action="store_true", help="Bulk parse mode")
    arg_parser.add_argument("--input", type=str, help="Input CSV file path")
    arg_parser.add_argument("--output", type=str, help="Output CSV file path")
    arg_parser.add_argument("--pincodecsv", type=str, help="Pincode metadata CSV file path (optional)")
    arg_parser.add_argument("--citiescsv", type=str, help="City and State list CSV file path (optional)")
    args = arg_parser.parse_args()

    if args.bulk:
        if not args.input or not args.output:
            print("Please specify --input and --output for bulk mode")
        else:
            bulk_parse(args.input, args.output, args.pincodecsv, args.citiescsv)
    else:
        print("Please specify --bulk mode")
