from datetime import datetime
from dateparser import parse

# ONLY MAP FIELDS THAT AREN'T IDENTICAL!
patient_pdf_to_schema = {
    'email': 'email_address',
}

address_pdf_to_schema = {
    'street_physical_address': 'street',
    'city_physical_address': 'city',
    'state_physical_address': 'state',
    'zip_physical_address': 'zip'
}


def make_date(month, day, year):
    return datetime.strptime(f'{month}/{day}/{year}', '%m/%d/%Y')


def make_test_datetime(month, day, year, time):
    return {'lab_slip_colletion_datetime': None}
