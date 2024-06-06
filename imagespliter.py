import cv2
import numpy as np


def split_image(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply adaptive thresholding to extract horizontal lines
    _, thresholded = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (image.shape[1] // 20, 1))
    horizontal_lines = cv2.morphologyEx(thresholded, cv2.MORPH_OPEN, kernel)

    # Find the contours of the horizontal lines
    contours, _ = cv2.findContours(horizontal_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Extract the y-coordinates and lengths of the horizontal lines
    line_y_coordinates = []
    line_lengths = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w > (2 / 3) * image.shape[1]:
            line_y_coordinates.append(y)
            line_lengths.append(w)

    # Sort the y-coordinates in ascending order
    sorted_indices = np.argsort(line_y_coordinates)
    line_y_coordinates = np.array(line_y_coordinates)[sorted_indices]
    line_lengths = np.array(line_lengths)[sorted_indices]

    # Calculate the splitting points based on the horizontal lines
    split_points = [0]
    prev_line_y = 0
    for i in range(len(line_y_coordinates)):
        if line_y_coordinates[i] - prev_line_y >= (1 / 3) * image.shape[0]:
            split_points.append(line_y_coordinates[i])
            prev_line_y = line_y_coordinates[i]

    split_points.append(image.shape[0])

    # Split the image into parts
    parts = []
    for i in range(len(split_points) - 1):
        start_y = split_points[i]
        end_y = split_points[i + 1]

        # Extract the part from the original image
        part = image[start_y:end_y, :]
        parts.append(part)

    return parts