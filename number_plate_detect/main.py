import cv2 as cv
import pytesseract
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from ultralytics import YOLO

plate_detector = YOLO("models/best.pt", task="detect")

WIDTH = 640
cv.namedWindow("image")

# select image files

def select_image():
    Tk().withdraw()
    file_path = askopenfilename(title="Select an image file",
                                filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")])
    
    if not file_path: return print("Failed to load")
    image = cv.imread(file_path)


    if image is not None:
        h, w, c = image.shape
        ratio = w / h
        new_w, new_h = WIDTH, int(WIDTH / ratio)
        image = cv.resize(image, (new_w, new_h))
        cv.imshow("image", image)

        detect_and_crop__plate(image)
    else:
        print("Error: Could not read the image file.")

def detect_and_crop__plate(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    image = cv.normalize(gray, None, alpha=0, beta=255, norm_type=cv.NORM_MINMAX)
    
    # alpha = 1.5 # Contrast control (1.0-3.0)
    # beta = 0    # Brightness control (0-100)
    # image = cv.convertScaleAbs(image, alpha=alpha, beta=beta)

    
    results = plate_detector(image, conf=.9)[0]
    results = results.boxes.data.tolist() # Get xyxy format and convert to numpy
    # results = results[results[:, 4] > 0.8]  # Apply confidence threshold

    # Visualize results
    plt.imshow(cv.cvtColor(image, cv.COLOR_BGR2RGB))
    for *box, conf, cls in results:
        plt.gca().add_patch(plt.Rectangle((box[0], box[1]), box[2] - box[0], box[3] - box[1], fill=False, color='red', linewidth=2))
    plt.show()
    
    return
    ocr(image)

def ocr(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    print(f"Detected text: {text}")
        

if __name__ == "__main__":
    select_image()
    
    cv.waitKey(0)
    cv.destroyAllWindows()
