from solver import solved
import pytesseract
import numpy as np
import cv2 as cv
import sys

size = 9*56
image = np.zeros(( size, size, 3 ))

def preprocess( image ):
    blurred = cv.medianBlur( image, 5)
    gray = cv.cvtColor( image, cv.COLOR_BGR2GRAY)
    edge = cv.adaptiveThreshold( gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 21, 10)
    return edge

def reorder( contour ):
    contour = contour[:4].reshape((4,2))
    points = np.zeros(( 4, 2 ), dtype="float32" )

    contour_sum = np.sum( contour, axis=1 )
    points[0] = contour[np.argmin(contour_sum)] # top left
    points[3] = contour[np.argmax(contour_sum)] # bottom left

    contour_diff = np.diff( contour, axis=1 )
    points[2] = contour[np.argmin(contour_diff)] # top right
    points[1] = contour[np.argmax(contour_diff)] # bottom right

    return points

def largest_countour( contours ):
    largest = None
    largest_area = 0 
    for contour in contours:
        area = cv.contourArea( contour )
        if area > 50 and area > largest_area:
            pm = cv.arcLength( contour, True )
            approx = cv.approxPolyDP( contour, .04*pm, True)
            largest_area = area
            largest = approx

    return largest

def split_image( image, grid ):
    x, y = grid
    rows = np.vsplit( image, x )
    boxes = []
    for row in rows:
        columns = np.hsplit( row, y )
        for box in columns:
            boxes.append( box )

    return boxes

def read_values( boxes ):
    vals = []
    for box in boxes:
        val = ocr( box )
        vals.append( val )

    return vals

def ocr( box ):
    # box = cv.cvtColor( box, cv.COLOR_BGR2GRAY )
    # box = cv.threshold(box, 0, 255, cv.THRESH_OTSU + cv.THRESH_BINARY_INV)[1]

    # text = pytesseract.image_to_string(box, config='--psm 10')
    # text = text.replace('\n', '').replace('\f', '')
    # if text != "" : 
    #     cv.imshow( text, box )
    #     return text
    return 0

def main( image ):
    # preprocess
    processed = preprocess( image )
    # finding countour
    contours, hierarchy = cv.findContours(processed, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE) 

    # finding largest contour
    puzzle_contour = largest_countour( contours ) 

    # preview
    contour_preview = image.copy()

    if puzzle_contour is not None:
        cv.drawContours(contour_preview, [puzzle_contour], -1, (0, 255, 0), 2)
    else :
        print("Couldn't find puzzle")
        cv.drawContours(contour_preview, contours, -1, (0, 255, 0), 1)

    ordered = reorder( puzzle_contour )

    src = np.float32( ordered )
    dest = np.float32([[0,0], [0,size], [size,0], [size,size]])

    mat = cv.getPerspectiveTransform( src, dest )
    warped = cv.warpPerspective( image, mat, (size,size))

    splitted = split_image( warped, (9, 9) )
    puzzle = read_values( splitted )

    ret, solved_puzzle = solved( puzzle ) 

    print( puzzle )
    if ret : print( solved )

    cv.imshow("preview", contour_preview)
    cv.imshow("waped", warped)
    cv.waitKey(0)


try:
    [ _, file ] = sys.argv
    image = cv.imread( file )
    main( image )

except ValueError as e :
    print( e )
    print("please specify a image file")
    exit()
    
except Exception as e :
    print(e)
    print("File doesnt exist")
    exit() 



