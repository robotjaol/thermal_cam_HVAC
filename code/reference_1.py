import cv2
import numpy as np

thermal_camera = cv2.VideoCapture(0)

thermal_camera.set(cv2.CAP_PROP_FRAME_WIDTH, 160)
thermal_camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 120)

thermal_camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('Y','1','6',' '))
thermal_camera.set(cv2.CAP_PROP_CONVERT_RGB, 0)



# cv2.imshow("Tes", thermal_camera)
# cv2.waitKey(0)