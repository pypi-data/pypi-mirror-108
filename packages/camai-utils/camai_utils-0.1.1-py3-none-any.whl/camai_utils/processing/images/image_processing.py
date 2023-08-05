import pdf2image
import pytesseract
from PIL import ImageEnhance



def pdf_to_image(file, dpi):
    print(f'Reading from {file.filename}')
    pages = pdf2image.convert_from_bytes(file_bytes, dpi=dpi)
    return pages


def sharpen_image(image, factor):
    enhancer = ImageEnhance.Sharpness(image)
    enhanced_image = enhancer.enhance(factor)
    return enhanced_image


def image_to_text(image):
    return pytesseract.image_to_string(image)


def process_pdf(file, dpi=300, enhancement_factor=3):
    imgs = pdf_to_image(file, dpi=dpi)
    assert len(imgs) == 1, 'Uploaded file is multipage - this is not expected.'
    img = imgs[0]
    sharp_img = sharpen_image(img, factor=enhancement_factor)
    text = image_to_text(sharp_img)
    return text
