import PyPDF2 as pypdf
from pathlib import Path
from dateparser import parse
from app.processing.pdfs.extractor_utils import (handle_fishery_id, handle_phone_number)

class LabOrderPDFExtractor:
    def __init__(self, pdf_bytes):
        self.pdf = pypdf.PdfFileReader(pdf_bytes)
        self.fields = self.pdf.getFields()

    def __getitem__(self, key):
        return self.fields.get(key, {None: None})

    def search(self, s):
        return [k for k in self.fields.keys() if s.upper() in k.upper()]

    def _extract(self, fields=[]):
        return {k: self[k].get('/V') for k in fields}

    def extract_patient_data(self):
        data = self._extract(['FirstName',
                              'Last Name',
                              'MI',
                              'Date of Birth',
                              'Gender',
                              'Phone Number#2',
                              'Mailing Address#2',
                              'Patient ID Chart MR',
                              'Resp Viruses Specimen Type',
                              'Collection Date',
                              'Time'])
        return {
            'name': f"{data['FirstName']} {data['Last Name']}",
            'patient_id': f"{data['Patient ID Chart MR'].upper()}",
            'dob': parse(data['Date of Birth']).isoformat(),
            'gender': data['Gender'],
            'phone': handle_phone_number(data['Phone Number#2']),
            'address': data['Mailing Address#2'],
            'fishery_id': handle_fishery_id(data['Patient ID Chart MR'].upper()),
            'collection_type': data['Resp Viruses Specimen Type'],
            'specimen_collection_datetime': parse(data['Collection Date'] + ' ' + data['Time']).isoformat(),
        }
