import pytesseract
import logging

logger = logging.getLogger(__name__)


def get_p_id_text(img):
    logger.info("Formatting id data...")
    text1 = []
    from PIL import Image

    # Load an image using PIL
    image = Image.open(img)

    custom_config = r'--psm 11'

    # Perform OCR on the image using the configured settings
    text = pytesseract.image_to_string(image, config=custom_config)


    lines = text.split('\n')
    for lin in lines:
        s = lin.strip()
        s = lin.replace('\n', '')
        s = s.rstrip()
        s = s.lstrip()
        text1.append(s)
    text1 = list(filter(None, text1))
    text0 = text1[:]
    return text0
