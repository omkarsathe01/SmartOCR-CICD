import cv2
import matplotlib.pyplot as plt
# import pytesseract
import img_preprocess

def display(im_path):
    dpi = 80
    im_data = plt.imread(im_path)
    # print(im_data)
    # print(type(im_data))
    # print(im_data.shape)


    height, width  = im_data.shape[:2]
    
    figsize = width / float(dpi), height / float(dpi)

    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([0, 0, 1, 1])

    ax.axis('off')

    ax.imshow(im_data, cmap='gray')

    plt.show()
    pass

def show_img(txt, img):
    cv2.imshow(txt, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def box_generate(path, ww=150):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    show_img("gray",gray)
    blur = cv2.GaussianBlur(gray, (7,7), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    show_img("thresh", thresh)
    kernal = cv2.getStructuringElement(cv2.MORPH_RECT, (3,13))
    dilate = cv2.dilate(thresh, kernal, iterations=1)
    show_img("dilate", dilate)
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    cnts = sorted(cnts, key=lambda x: cv2.boundingRect(x)[0])
    i=0
    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)
        
        if w>ww:
            roi = img[y:y+h, x:x+w]
            # cv2.imshow(f"{i}", roi)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            print(i)
            cv2.imwrite(f"temp/bounding/bounding_roi_{i}.png", roi)
            display(f"temp/bounding/bounding_roi_{i}.png")
            i+=1
            cv2.rectangle(img, (x,y), (x+w, y+h), (0,0,255), 2)
    cv2.imwrite("temp/bounding_bbox.png", img)
    display("temp/bounding_bbox.png")
    return img

def split(img):
    # img = cv2.imread("Images/1.png")
    # h, w, ch = img.shape
    # img = cv2.resize(img, (w//2, h//2))

    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.imwrite("temp/bounding_gray.png", gray)
    blur = cv2.GaussianBlur(img, (7,7), 0)
    # cv2.imwrite("temp/bounding_blur.png", blur)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    kernal = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 5e))
    print(kernal)
    dilate = cv2.dilate(thresh, kernal, iterations=10)
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    cnts = sorted(cnts, key=lambda x: cv2.boundingRect(x)[0])
    i=0
    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)
        # print(f"x: {x}--> y: {y}--> w: {w}--> h: {h}")
        
        if w>0:
            roi = img[y:y+h, x:x+w]
            # cv2.imshow(f"{i}", roi)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            print(i)
            # cv2.imwrite(f"temp/bounding/bounding_roi_{i}.png", roi)
            # display(f"temp/bounding/bounding_roi_{i}.png")
            i+=1
            cv2.rectangle(img, (x,y), (x+w, y+h), (0,0,255), 2)
    cv2.imwrite("temp/bounding_bbox.png", img)
    display("temp/bounding_bbox.png")
    pass


print("Begin")
img = cv2.imread("Images/1.png")
img = img_preprocess.process_from_img(img)
# show_img("", img)
split(img)
print("Done and dusted!!")