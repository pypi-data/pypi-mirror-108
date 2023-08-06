from typing import Dict, Any
from datetime import datetime
from camai_utils.processing.pdfs.pdf_extractor import PDFExtractor


def extract(pdf_bytes: bytes) -> Dict[str, Any]:
    pdf = PDFExtractor(pdf_file=pdf_bytes)
    data =  pdf.extract([
        'first_name', 
        'gender', 
        'ssn', 
        'race_ethnicity', 
        'home_phone', 
        'cell_phone', 
        'local_phone', 
        'email', 
        'release_test_results_to', 
        'last_name', 
        'patient_id', 
        'collection_month', 
        'collection_day', 
        'collection_year', 
        'fishery_name', 
        'hispanic', 
        'sars_cov2_result', 
        'street_physical_address',
        'city_physical_address',
        'state_physical_address',
        'zip_physical_address'
    ])
    dob_data = pdf.extract(['dob_month','dob_day', 'dob_year'])
    dob = datetime(int(dob_data['dob_year']), int(dob_data['dob_month']), int(dob_data['dob_day']))
    data.update({
        'dob': dob.isoformat(),
    })
    return data
