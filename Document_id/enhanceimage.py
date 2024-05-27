import cv2


def enhance_image(image):
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Increase contrast using histogram equalization
    clahe = cv2.createCLAHE(clipLimit=1.0, tileGridSize=(16, 16))
    enhanced_gray = clahe.apply(gray)

    cv2.imwrite(image, enhanced_gray)
    return image