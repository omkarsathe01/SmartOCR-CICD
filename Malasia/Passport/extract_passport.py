import pytesseract
import cv2


def get_passport_text(image):
    # text1 = []
    # Load the Aadhar card image
    image = cv2.imread(image)
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Increase contrast using histogram equalization
    clahe = cv2.createCLAHE(clipLimit=1.0, tileGridSize=(16, 16))
    enhanced_gray = clahe.apply(gray)
    custom_config = r'--psm 3'
    # Read the image
    text = pytesseract.image_to_string(enhanced_gray, config=custom_config)


    lines = text.split('\n')
    text1 = []
    for lin in lines:
        s = lin.strip()
        s = lin.replace('\n', '')
        s = s.rstrip()
        s = s.lstrip()
        text1.append(s)
    text1 = list(filter(None, text1))
    text0 = text1[:]
    print(text0)
    # return text0

