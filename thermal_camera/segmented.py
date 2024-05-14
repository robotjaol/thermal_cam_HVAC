import cv2
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

thermalVideo = cv2.VideoCapture('dataset/dataset_2.mp4')

if not thermalVideo.isOpened():
    print("Error: Could not open video file.")
    exit()

# Function untuk mengembalikan value thermal
def preprocess_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    normalized = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)
    return normalized

# Function untuk mencari kontur dari biner image
def segment_frame(frame):
    _, thresholded = cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

# def resize_frame(frame, width, height):
#     return cv2.resize(frame, (width, height))

# # Ukuran gambar yang diinginkan
# desired_width = 640
# desired_height = 480

# Testing run di streamlit 
# st.title("Thermal Video Segmentation")
# frame_placeholder = st.empty()

while thermalVideo.isOpened():
    ret, frame = thermalVideo.read()

    if not ret:
        break

    # resized_frame = resize_frame(frame, desired_width, desired_height)
    preprocessed_frame = preprocess_frame(frame)
    contours = segment_frame(preprocessed_frame)
    cv2.drawContours(frame, contours, -1, (0, 255, 0), 2) # Display contour dengan warna hijau
    cv2.imshow('Segmented Thermal Video', frame)

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

thermalVideo.release()
# cv2.destroyAllWindows()
