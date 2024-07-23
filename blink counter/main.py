import cv2 as cv
import mediapipe as mp
import math

mp_holistic = mp.solutions.holistic

BG_COLOR = (192, 192, 192)


def dist( a, b ):
    dx = a.x - b.x
    dy = a.y - b.y 
    return math.sqrt( dx*dx + dy*dy )

cap = cv.VideoCapture(0)

blink_Count = 0
eye_open = True

frame_count = 0
with mp_holistic.Holistic(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as holistic:
    while True:
        ret, frame = cap.read()
        if not ret : continue
        frame_count += 1

        h, w, _ = frame.shape

        img = cv.cvtColor( frame, cv.COLOR_BGR2RGB )

        results = holistic.process( img )
        if results.face_landmarks:

            right_top = results.face_landmarks.landmark[159]
            right_bottom = results.face_landmarks.landmark[145]

            right_left = results.face_landmarks.landmark[33]
            right_right = results.face_landmarks.landmark[133]
            
            left_top = results.face_landmarks.landmark[386]
            left_bottom = results.face_landmarks.landmark[374]

            left_right = results.face_landmarks.landmark[263]
            left_left = results.face_landmarks.landmark[362]

            vdist = dist( right_bottom, right_top )
            hdist = dist( right_left, right_right )

            ratio = vdist / hdist * 100
            if ratio > 28 :
                eye_open = True 
            elif eye_open :
                print(ratio)
                eye_open = False
                blink_Count += 1

            for pos in [ right_top, right_bottom, right_left, right_right, left_bottom, left_top, left_left, left_right]: cv.circle( frame, ( int(pos.x *w), int(pos.y *h) ), 1, (0,0,255), 1 )
                 
        cv.putText( frame, str(blink_Count), (int(w/2),h-40), cv.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, 255, 2 )

        cv.imshow( "main", frame )
        if cv.waitKey(1) == ord("q"): break 

cap.release()
cv.destroyAllWindows()