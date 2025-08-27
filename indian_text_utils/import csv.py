import csv

def load_pincode_csv(pincode):
    pincode_dict = {}
    with open(pincode, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            pincode = row['pincode'].strip()
            city = row['regionname'].strip()
            state = row['statename'].strip()
            district = row['districtname'].strip()
            pincode_dict[pincode] = {'city': city, 'state': state, 'district':district}
    return pincode_dict
