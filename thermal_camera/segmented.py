import cv2
import numpy as np
import matplotlib as plt

thermalVideo = cv2.VideoCapture('dataset/dataset_2.mp4')

if not thermalVideo.isOpened():
    print("Error: Could not open video file.")
    exit()

def preprocess_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    normalized = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)
    return normalized

def segment_frame(frame):
    _, thresholded = cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

while thermalVideo.isOpened():
    ret, frame = thermalVideo.read()

    if not ret:
        break

    preprocessed_frame = preprocess_frame(frame)
    contours = segment_frame(preprocessed_frame)
    cv2.drawContours(frame, contours, -1, (0, 0, 255), 2)
    cv2.imshow('Segmented Thermal Video', frame)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

thermalVideo.release()
cv2.destroyAllWindows()
