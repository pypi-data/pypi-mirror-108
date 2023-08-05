from typing import Iterable, Dict, Any
import PyPDF2 as pypdf
import io

from camai_utils.processing.pdfs.field_mappings import (make_date, patient_pdf_to_schema, address_pdf_to_schema)


def apply_field_map(d, fmap):
    return {fmap.get(k, k): v for k, v in d.items()}


class PDFExtractor:
    def __init__(self, pdf_file: bytes):
        iostream = io.BytesIO(pdf_file)
        iostream.seek(0)
        self.pdf = pypdf.PdfFileReader(iostream)
        self.fields = self.pdf.getFields()

    def __getitem__(self, key):
        return self.fields.get(key, {None: None})

    def search(self, s):
        return [k for k in self.fields.keys() if s.upper() in k.upper()]

    def extract(self, fields=Iterable[str]) -> Dict[str, Any]:
        return {k: self[k].get('/V') for k in fields}

    def extract_patient(self):
        data = self.extract(
            fields=['first_name', 'last_name', 'patient_id', 'ssn', 'gender', 'race_ethnicity', 'hispanic',
                    'home_phone', 'cell_phone', 'local_phone', 'email',
                    'fishery_name'])
        fields_mapped = apply_field_map(data, patient_pdf_to_schema)
        dob_data = self.extract(fields=['dob_month', 'dob_day', 'dob_year'])
        fields_mapped['dob'] = make_date(dob_data['dob_month'], dob_data['dob_day'], dob_data['dob_year']).isoformat()

        return fields_mapped

    def extract_address(self):
        data = self.extract(fields=[
            'street_physical_address', 'city_physical_address', 'state_physical_address', 'zip_physical_address'
        ])
        fields_mapped = apply_field_map(data, address_pdf_to_schema)
        return fields_mapped


    def extract_test(self):
        data = self.extract(fields=[
            'collection_month', 'collection_day', 'collection_year'
        ])
        return {
            'specimen_type': 'NP-Nasopharyngeal swab',
            'lab_slip_colletion_datetime': make_date(data['collection_month'], data['collection_day'],
                                                     data['collection_year']).isoformat()
        }
