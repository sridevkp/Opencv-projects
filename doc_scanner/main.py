import cv2 as cv
import numpy as np

# img = cv.imread('sample_images/green.jpg')
w, h = 640, 480
thres1 , thres2 = 0, 100 

cv.namedWindow("main")
# nothing = lambda a : a
# cv.createTrackbar( "thres1", "main", 0 , 255, nothing )
# cv.createTrackbar( "thres2", "main", 100, 255, nothing )
cap = cv.VideoCapture(0)
cap.set( cv.CAP_PROP_FRAME_WIDTH , w )
cap.set( cv.CAP_PROP_FRAME_HEIGHT, h )



def get_doc_contour( contours ):
    largest = None
    largest_area = 0 
    for contour in contours :
        area = cv.contourArea( contour )
        if area > 3500 and area > largest_area  :
            pm = cv.arcLength( contour, True )
            approx_contour = cv.approxPolyDP( contour, pm * 0.02, True )
            if len(approx_contour) == 4 :
                largest = approx_contour
                largest_area = area
    return largest

def reshape( contour ):
    contour = contour.reshape((4,2))
    points = np.zeros(( 4, 2 ), dtype="float32" )

    contour_sum = np.sum( contour, axis=1 )
    points[0] = contour[np.argmin(contour_sum)]
    points[3] = contour[np.argmax(contour_sum)]

    contour_diff = np.diff( contour, axis=1 )
    points[1] = contour[np.argmin(contour_diff)]
    points[2] = contour[np.argmax(contour_diff)]

    return points


def scan( im ):
    img = im.copy()
    imGray = cv.cvtColor( img, cv.COLOR_BGR2GRAY )
    imgBlur = cv.GaussianBlur( imGray, (5,5), 10 )
    _, thresh = cv.threshold(imgBlur, 127, 255, 0)
    canny = cv.Canny( imgBlur, thres1, thres2 )

    imgDial = cv.dilate( canny, np.ones((5,5)), iterations=2 )
    imgErode = cv.erode( imgDial, np.ones((5,5)), iterations=2 )

    contours, hierarchy = cv.findContours(imgErode, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    doc_contour = get_doc_contour( contours )
    if not doc_contour is None : 
        width, height = 400, int(400 * 1.41)

        points1 = np.float32( reshape(doc_contour) )
        doc_output = np.float32([[ 0, 0], [ width, 0 ], [ 0, height ], [ width, height ] ])
        matrix = cv.getPerspectiveTransform( points1, doc_output )
        warped_img = cv.warpPerspective( img, matrix, ( width, height ))

        cv.drawContours( img, [doc_contour], -1, (0,0,255), 2 )
        cv.imshow( "scanned", warped_img )

    cv.putText( img, "scanning", (20,h-20), cv.FONT_HERSHEY_COMPLEX, 1, 255, 2 )
    return img



while True:
    _, frame = cap.read()
    try:
        thres1 = cv.getTrackbarPos("thres1", "main" )
        thres2 = cv.getTrackbarPos("thres2", "main" )
    except :
        pass
    
    blur = cv.Laplacian( frame, cv.CV_64F ).var()
    
    if 80 < blur < 500 : frame = scan( frame )
    cv.imshow("main", frame )

    if  cv.waitKey(1) == ord('q'):
        break


cap.release()
cv.destroyAllWindows()