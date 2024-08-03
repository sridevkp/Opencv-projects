cap = cv.VideoCapture(0)
# cap.set( cv.CAP_PROP_FRAME_WIDTH , 640 )
# cap.set( cv.CAP_PROP_FRAME_HEIGHT, 480 )
# cv.namedWindow('image')

# if not cap.isOpened():
#     print("Cannot open camera")
#     cap.open()


# while True:
#     ret, frame = cap.read()

#     if not ret : continue

#     cv.imshow("image", frame )
#     if cv.waitKey(1) == ord('q'):
#         break


# cap.release()
# cv.destroyAllWindows()
# exit()