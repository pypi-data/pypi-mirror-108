from fastapi import UploadFile

from camai_utils.processing.images import image_processing
from camai_utils.processing.text import result_text_parsing
from camai_utils.processing.pdfs import (lab_pdf_extraction)



async def process_lab_file(file_bytes, process_mode:str):
    if process_mode == 'ocr':
        text = await image_processing.process_pdf(file_bytes)
        #TODO: parse patient_data data. Likely deprecate this mode.
    elif process_mode == 'pdf':
        #TODO: implement pdf parsing of data.
        data = lab_pdf_extraction.extract(file_bytes)
        return data

async def process_results_file(file_bytes, process_mode:str):
    if process_mode == 'ocr':
        text = await image_processing.process_pdf(file_bytes)
        patient_data = result_text_parsing.scrape_patient_data(text)
        return patient_data
    elif process_mode == 'pdf':
        #TODO: handle pdf extraction OR return deprecation/not supported warning
        pass