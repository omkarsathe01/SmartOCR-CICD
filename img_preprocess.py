import cv2
#=========================================MAIN FUNCTION(s)====================================================
#using for salaryslips
def process_from_path(path):
    print("path", path)
    input_image = cv2.imread(path)
    grayscale_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
    moments = cv2.moments(grayscale_image)
    skew_angle = moments['mu11'] / moments['mu02'] if moments['mu02'] != 0 else 0
    rotation_matrix = cv2.getRotationMatrix2D((input_image.shape[1] / 2, input_image.shape[0] / 2), skew_angle, 1)
    deskewed_image = cv2.warpAffine(input_image, rotation_matrix, (input_image.shape[1], input_image.shape[0]),
                                    flags=cv2.INTER_LINEAR,
                                    borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255))
    temp_img = path.split('.')[0] + '.tif'
    cv2.imwrite(temp_img, deskewed_image)
    print("temp img: ", temp_img)
    return temp_img
