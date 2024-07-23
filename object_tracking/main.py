import cv2 as cv
import time 
from tracker import *

cap = cv.VideoCapture("sample/sample2.mp4")

detections = []
detector = cv.createBackgroundSubtractorMOG2( history=100, varThreshold=40 )

tracker = EuclideanDistTracker()

while True:
    ret , frame = cap.read()
    if not ret: continue
    
    frame = cv.flip( frame, 1 )              
    frame = cv.resize( frame, ( 640, 320 ))   
    mask = detector.apply( frame )                      
    _, thresh = cv.threshold( mask, 254, 255, cv.THRESH_BINARY )
    
    contours, _ = cv.findContours( thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE )
    detections = []
    for cnt in contours:
        area = cv.contourArea( cnt )
        if area < 500 : continue
        x, y, w, h = cv.boundingRect( cnt )
        detections.append([ x, y, w, h ])
        cv.rectangle( frame, ( x, y ), ( x +w, y +h ), ( 0, 0, 255 ), 2 )
        cv.drawContours( frame, [cnt], -1, ( 0, 255, 0 ), 1)

    trackings = tracker.update( detections )
    for x, y, id, speed in trackings :
        cv.putText( frame , str(id), (x,y), cv.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, ( 255, 0, 0 ), 2)


    cv.imshow( "win", frame )
    time.sleep(0.02)
    if cv.waitKey(1) == ord("q") : break

cap.release()
cv.destroyAllWindows()
exit()