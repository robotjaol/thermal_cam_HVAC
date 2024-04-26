# Testing pertama

# import streamlit as st
# import cv2

# def main():
#     st.set_page_config(page_title="Streamlit WebCam App")
#     st.title("Webcam Display Steamlit App")
#     st.caption("Powered by OpenCV, Streamlit")
#     cap = cv2.VideoCapture(0)
#     frame_placeholder = st.empty()
#     stop_button_pressed = st.button("Stop")
#     while cap.isOpened() and not stop_button_pressed:
#         ret, frame = cap.read()
#         if not ret:
#             st.write("Video Capture Ended")
#             break
#         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         frame_placeholder.image(frame,channels="RGB")
#         if cv2.waitKey(1) & 0xFF == ord("q") or stop_button_pressed:
#             break
#     cap.release()
#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     main()

# Testing Kedua
import streamlit as st
import cv2
import time


def main():
    st.set_page_config(page_title="Streamlit WebCam App")
    st.title("Webcam Display Streamlit App")
    st.caption("Powered by OpenCV and Streamlit")

    cap = cv2.VideoCapture(0)
    frame_placeholder = st.empty()
    stop_button_pressed = st.button("Stop")

    while cap.isOpened() and not stop_button_pressed:
        ret, frame = cap.read()
        if not ret:
            st.write("Video Capture Ended")
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_placeholder.image(frame_rgb, channels="RGB")
        time.sleep(0.01)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
