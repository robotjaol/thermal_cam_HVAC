import socket
import time
import threading
from flask import Flask, render_template, Response, request, jsonify
import cv2
import torch
import numpy as np

server_ip = "192.168.1.100"   #connect with IP router
# server_ip = "127.0.0.1"     # Connect with IP computer
server_port = 8899          # PORT TRANSMISI

app = Flask(__name__)

thermal_video_path = '/home/robotjaol/project/cctv_thermal_hvac/main/sample/thermal.mp4'
thermal_video_capture = cv2.VideoCapture(thermal_video_path)

model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# Initial calibration offset manual
calibration_offset = -77

#FUNCTION START
def detect_people_and_temperature(frame):
    global calibration_offset
    results = model(frame)
    detections = results.xyxy[0].cpu().numpy()
    person_count = 0
    temperatures = []

    for x1, y1, x2, y2, conf, cls in detections:
        if int(cls) == 0:  #setup 0 for person
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

def generate_frames():
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/calibrate', methods=['POST'])
def calibrate():
    global calibration_offset
    data = request.get_json()
    calibration_offset = data.get('offset', 0.0)
    return jsonify({"message": "Calibration Updated", "offset": calibration_offset})

@app.route('/toggle_off', methods=['POST'])
def toggle_off():
    global thermal_video_capture
    thermal_video_capture.release()
    return '', 204

def run_flask_app():
    app.run(host='0.0.0.0', port=5000)

def send_people_count(client_socket, num_people, avg_temp):
    message = f'{num_people},{avg_temp:.2f}'
    client_socket.sendall(message.encode())
    print(f"Number of people {num_people} and average temperature {avg_temp:.2f} sent")

def run_socket_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((server_ip, server_port))
    server.listen(5)
    print(f"Running server at: {server_ip}:{server_port}")

    try:
        while True:
            client_socket, client_address = server.accept()
            print(f"connect with {client_address} success")

            try:
                while True:
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

            except Exception as e:
                print(f"Error during communication: {e}")
            finally:
                client_socket.close()
                print("Data transmission completed")

    finally:
        server.close()

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.start()
    run_socket_server()




# #-----------------------------------------------------------
# #-------------------TESTING PROGRAM PROGRESS----------------
# #-----------WEB YOLOv5 AS SERVER AND ESP32 AS CLIENT -------
# #---------------THERMAL VIDEO LOAD MIX WEBCAM ONLY----------
# #---------------------------PART 5--------------------------

# import socket
# import time
# import threading
# from flask import Flask, render_template, Response, request
# import cv2
# import torch
# import numpy as np

# # server_ip = "192.168.1.100"   #connect with IP router
# server_ip = "127.0.0.1"     #connect with IP computer
# server_port = 8899

# app = Flask(__name__)

# thermal_video_path = '/home/robotjaol/pbl/thermal_CCTV_HVAC/main/sample/thermal.mp4'
# thermal_video_capture = cv2.VideoCapture(thermal_video_path)

# webcam_video_capture = cv2.VideoCapture(0)
# use_webcam = False

# model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# #FUNCTION START
# def detect_people_and_temperature(frame):
#     results = model(frame)
#     detections = results.xyxy[0].cpu().numpy()
#     person_count = 0
#     temperatures = []

#     for x1, y1, x2, y2, conf, cls in detections:
#         if int(cls) == 0:  #setup 0 for person
#             person_count += 1
#             person_region = frame[int(y1):int(y2), int(x1):int(x2)]
#             temperature = np.mean(person_region)
#             temperatures.append(temperature)
#             cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
#             cv2.putText(frame, f'{temperature:.2f}C', (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2, cv2.LINE_AA)

#     average_temperature = np.mean(temperatures) if temperatures else 0
#     cv2.putText(frame, f'Orang yang terdeteksi: {person_count}', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
#     cv2.putText(frame, f'Rata-rata Suhu: {average_temperature:.2f}C', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

#     return frame, person_count, average_temperature

# def generate_frames():
#     global use_webcam
#     while True:
#         if use_webcam:
#             success, frame = webcam_video_capture.read()
#         else:
#             success, frame = thermal_video_capture.read()
#             if not success:
#                 thermal_video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
#                 continue

#         if not success:
#             break

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

# @app.route('/toggle_video', methods=['POST'])
# def toggle_video():
#     global use_webcam
#     use_webcam = request.form.get('video_source') == 'webcam'
#     return '', 204

# @app.route('/toggle_off', methods=['POST'])
# def toggle_off():
#     global use_webcam
#     use_webcam = False
#     return '', 204

# def run_flask_app():
#     app.run(host='0.0.0.0', port=5000)

# def send_people_count(client_socket, num_people, avg_temp):
#     message = f'{num_people},{avg_temp:.2f}'
#     client_socket.sendall(message.encode())
#     print(f"Number of people {num_people} and average temperature {avg_temp:.2f} sent")

# # Fungsi untuk mengirim perintah IR ke klien
# def transmit_ir(client_socket):
#     for ir_command in range(1, 5):
#         command_str = str(ir_command)
#         client_socket.sendall(command_str.encode())
#         print(f"IR command {ir_command} terkirim")
#         time.sleep(2)

# # Fungsi untuk mengirim perintah kontrol LED ke klien
# def server_led(client_socket):
#     led_command = "LED_ON"
#     client_socket.sendall(led_command.encode())
#     print(f"LED command {led_command} sent")

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





