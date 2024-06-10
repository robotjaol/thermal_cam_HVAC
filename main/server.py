import socket
import time
import threading
from flask import Flask, render_template, Response, request, jsonify
import cv2
import torch
import numpy as np

# Server Configuration
# server_ip = "192.168.1.100"  # Connect with IP router
server_ip = "127.0.0.1"    # Connect with IP computer
server_port = 8899           # PORT TRANSMISSION

app = Flask(__name__)

# Path to thermal video
thermal_video_path = '/home/robotjaol/project/cctv_thermal_hvac/main/sample/thermal.mp4'

# Load the YOLO model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# Initial calibration offset manual
calibration_offset = -75

# Function to detect people and temperature
def detect_people_and_temperature(frame):
    global calibration_offset
    results = model(frame)
    detections = results.xyxy[0].cpu().numpy()
    person_count = 0
    temperatures = []

    for x1, y1, x2, y2, conf, cls in detections:
        if int(cls) == 0:  # setup 0 for person
            person_count += 1
            person_region = frame[int(y1):int(y2), int(x1):int(x2)]
            temperature = np.mean(person_region) + calibration_offset
            temperatures.append(temperature)
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(frame, f'{temperature:.2f}C', (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2, cv2.LINE_AA)

    average_temperature = np.mean(temperatures) if temperatures else 0
    cv2.putText(frame, f'Orang yang terdeteksi: {person_count}', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, f'Rata-rata Suhu: {average_temperature:.2f}C', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    return frame, person_count, average_temperature

# Function to generate frames for video feed
def generate_frames():
    thermal_video_capture = cv2.VideoCapture(thermal_video_path)
    while True:
        success, frame = thermal_video_capture.read()
        if not success:
            thermal_video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        frame_with_people, num_people, avg_temp = detect_people_and_temperature(frame)
        ret, buffer = cv2.imencode('.jpg', frame_with_people)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    thermal_video_capture.release()

# Flask route to render index.html
@app.route('/')
def index():
    return render_template('index.html')

# Flask route for video feed
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Flask route for calibration
@app.route('/calibrate', methods=['POST'])
def calibrate():
    global calibration_offset
    data = request.get_json()
    calibration_offset = data.get('offset', 0.0)
    return jsonify({"message": "Calibration Updated", "offset": calibration_offset})

# Flask route to toggle off
@app.route('/toggle_off', methods=['POST'])
def toggle_off():
    global thermal_video_capture
    thermal_video_capture.release()
    return '', 204

# Function to run Flask app
def run_flask_app():
    app.run(host='0.0.0.0', port=5000)

# Function to send people count and average temperature via socket
def send_people_count(client_socket, num_people, avg_temp):
    message = f'{num_people},{avg_temp:.2f}'
    client_socket.sendall(message.encode())
    print(f"Number of people {num_people} and average temperature {avg_temp:.2f} sent")

# Function to run socket server
def run_socket_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((server_ip, server_port))
    server.listen(5)
    print(f"Running server at: {server_ip}:{server_port}")

    while True:
        client_socket, client_address = server.accept()
        print(f"Connect with {client_address} success")
        try:
            while True:
                thermal_video_capture = cv2.VideoCapture(thermal_video_path)
                success, frame = thermal_video_capture.read()
                if not success:
                    thermal_video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    continue
                _, num_people, avg_temp = detect_people_and_temperature(frame)
                send_people_count(client_socket, num_people, avg_temp)
                time.sleep(1)
                try:
                    response = client_socket.recv(1024).decode()
                    if response == "jon":
                        print("Data Transmission Success")
                except socket.error as e:
                    print(f"Error receiving data: {e}")
                    break
                finally:
                    thermal_video_capture.release()

        except Exception as e:
            print(f"Error during communication: {e}")
        finally:
            client_socket.close()
            print("Data transmission completed")

    server.close()

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.daemon = True  # Ensures the thread will close when the main thread ends
    flask_thread.start()
    run_socket_server()


# import socket
# import time
# import threading
# from flask import Flask, render_template, Response, request, jsonify
# import cv2
# import torch
# import numpy as np

# server_ip = "192.168.1.100"   #connect with IP router
# # server_ip = "127.0.0.1"     # Connect with IP computer
# server_port = 8899          # PORT TRANSMISI

# app = Flask(__name__)

# thermal_video_path = '/home/robotjaol/project/cctv_thermal_hvac/main/sample/thermal.mp4'
# thermal_video_capture = cv2.VideoCapture(thermal_video_path)

# model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# # Initial calibration offset manual
# calibration_offset = -75

# #FUNCTION START
# def detect_people_and_temperature(frame):
#     global calibration_offset
#     results = model(frame)
#     detections = results.xyxy[0].cpu().numpy()
#     person_count = 0
#     temperatures = []

#     for x1, y1, x2, y2, conf, cls in detections:
#         if int(cls) == 0:  #setup 0 for person
#             person_count += 1
#             person_region = frame[int(y1):int(y2), int(x1):int(x2)]
#             temperature = np.mean(person_region) + calibration_offset
#             temperatures.append(temperature)
#             # color = colormap[0, int((temperature - 20) * 100)][::-1]
#             cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
#             cv2.putText(frame, f'{temperature:.2f}C', (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2, cv2.LINE_AA)

#     average_temperature = np.mean(temperatures) if temperatures else 0
#     cv2.putText(frame, f'Orang yang terdeteksi: {person_count}', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
#     cv2.putText(frame, f'Rata-rata Suhu: {average_temperature:.2f}C', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

#     return frame, person_count, average_temperature

# def generate_frames():
#     while True:
#         success, frame = thermal_video_capture.read()
#         if not success:
#             thermal_video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
#             continue

#         frame_with_people, num_people, avg_temp = detect_people_and_temperature(frame)
#         ret, buffer = cv2.imencode('.jpg', frame_with_people)
#         frame = buffer.tobytes()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/calibrate', methods=['POST'])
# def calibrate():
#     global calibration_offset
#     data = request.get_json()
#     calibration_offset = data.get('offset', 0.0)
#     return jsonify({"message": "Calibration Updated", "offset": calibration_offset})

# @app.route('/toggle_off', methods=['POST'])
# def toggle_off():
#     global thermal_video_capture
#     thermal_video_capture.release()
#     return '', 204

# def run_flask_app():
#     app.run(host='0.0.0.0', port=5000)

# def send_people_count(client_socket, num_people, avg_temp):
#     message = f'{num_people},{avg_temp:.2f}'
#     client_socket.sendall(message.encode())
#     print(f"Number of people {num_people} and average temperature {avg_temp:.2f} sent")

# def run_socket_server():
#     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server.bind((server_ip, server_port))
#     server.listen(5)
#     print(f"Running server at: {server_ip}:{server_port}")

#     try:
#         while True:
#             client_socket, client_address = server.accept()
#             print(f"connect with {client_address} success")

#             try:
#                 while True:
#                     success, frame = thermal_video_capture.read()
#                     if not success:
#                         thermal_video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
#                         continue
#                     _, num_people, avg_temp = detect_people_and_temperature(frame)
#                     send_people_count(client_socket, num_people, avg_temp)
#                     time.sleep(1)
#                     try:
#                         response = client_socket.recv(1024).decode()
#                         if response == "jon":
#                             print("Data Transmission Success")
#                     except socket.error as e:
#                         print(f"Error receiving data: {e}")
#                         break

#             except Exception as e:
#                 print(f"Error during communication: {e}")
#             finally:
#                 client_socket.close()
#                 print("Data transmission completed")

#     finally:
#         server.close()

# if __name__ == '__main__':
#     flask_thread = threading.Thread(target=run_flask_app)
#     flask_thread.start()
#     run_socket_server()






