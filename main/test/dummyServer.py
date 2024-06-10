import socket
import cv2
import time
import threading
import numpy as np
import torch

server_ip = "127.0.0.1"
server_port = 8899

thermal_video_path = '/home/robotjaol/project/cctv_thermal_hvac/main/sample/thermal.mp4'

model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

calibration_offset = -75

def detect_heads(frame):
    results = model(frame)
    detections = results.xyxy[0].cpu().numpy()
    head_count = 0
    temperatures = []

    for x1, y1, x2, y2, conf, cls in detections:
        if int(cls) == 0:  # Class index for head
            head_count += 1
            head_region = frame[int(y1):int(y2), int(x1):int(x2)]
            temperature = np.mean(head_region) + calibration_offset
            temperatures.append(temperature)
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)
            cv2.putText(frame, f'{temperature:.2f}C', (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2, cv2.LINE_AA)

    average_temperature = np.mean(temperatures) if temperatures else 0

    return head_count, average_temperature

def send_head_count(client_socket, head_count, avg_temp):
    message = f'{head_count},{avg_temp:.2f}'
    try:
        client_socket.sendall(message.encode())
        print(f"Number of heads detected: {head_count}, Average temperature: {avg_temp:.2f}°C")
    except socket.error as e:
        print(f"Error sending data: {e}")

def run_socket_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((server_ip, server_port))
    server.listen(5)
    print(f"Running server at: {server_ip}:{server_port}")

    thermal_video_capture = cv2.VideoCapture(thermal_video_path)

    try:
        while True:
            client_socket, client_address = server.accept()
            print(f"Connected with {client_address}")

            try:
                while True:
                    success, frame = thermal_video_capture.read()
                    if not success:
                        thermal_video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
                        continue
                    head_count, avg_temp = detect_heads(frame)
                    send_head_count(client_socket, head_count, avg_temp)
                    time.sleep(1)
                    try:
                        client_socket.fileno()
                    except socket.error:
                        print("Client disconnected")
                        break

            except Exception as e:
                print(f"Error during communication: {e}")
            finally:
                client_socket.close()
                print("Data transmission completed")

    finally:
        server.close()

if __name__ == '__main__':
    run_socket_server()



 

## SUKSESSSSSSS KIRIM GANTI VALUEE
# import socket
# import cv2
# import time
# import threading
# import numpy as np
# import torch

# server_ip = "127.0.0.1"     # Connect dengan IP komputer
# server_port = 8899          # PORT TRANSMISI

# thermal_video_path = '/home/robotjaol/project/cctv_thermal_hvac/main/sample/thermal.mp4'

# model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# # Initial calibration offset manual
# calibration_offset = -75

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
#             cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
#             cv2.putText(frame, f'{temperature:.2f}C', (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2, cv2.LINE_AA)

#     average_temperature = np.mean(temperatures) if temperatures else 0
#     cv2.putText(frame, f'Orang yang terdeteksi: {person_count}', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
#     cv2.putText(frame, f'Rata-rata Suhu: {average_temperature:.2f}C', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

#     return person_count, average_temperature

# def send_people_count(client_socket, num_people, avg_temp):
#     message = f'{num_people},{avg_temp:.2f}'
#     client_socket.sendall(message.encode())
#     print(f"Number of people {num_people} and average temperature {avg_temp:.2f} sent")

# def run_socket_server():
#     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server.bind((server_ip, server_port))
#     server.listen(5)
#     print(f"Running server at: {server_ip}:{server_port}")

#     thermal_video_capture = cv2.VideoCapture(thermal_video_path)

#     try:
#         while True:
#             client_socket, client_address = server.accept()
#             print(f"Connected with {client_address}")

#             try:
#                 while True:
#                     success, frame = thermal_video_capture.read()
#                     if not success:
#                         thermal_video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
#                         continue
#                     num_people, avg_temp = detect_people_and_temperature(frame)
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
#     run_socket_server()


# import socket
# import time
# import threading
# from flask import Flask, render_template, Response, request, jsonify
# import cv2
# import torch
# import numpy as np

# # Server Configuration
# # server_ip = "192.168.1.100"  # Connect with IP router
# server_ip = "127.0.0.1"    # Connect with IP computer
# server_port = 8899           # PORT TRANSMISSION

# app = Flask(__name__)

# # Path to thermal video
# thermal_video_path = '/home/robotjaol/project/cctv_thermal_hvac/main/sample/thermal.mp4'
# model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# # Initial calibration offset manual
# calibration_offset = -75

# # Function to detect people and temperature
# def detect_people_and_temperature(frame):
#     global calibration_offset
#     results = model(frame)
#     detections = results.xyxy[0].cpu().numpy()
#     person_count = 0
#     temperatures = []

#     for x1, y1, x2, y2, conf, cls in detections:
#         if int(cls) == 0:  # setup 0 for person
#             person_count += 1
#             person_region = frame[int(y1):int(y2), int(x1):int(x2)]
#             temperature = np.mean(person_region) + calibration_offset
#             temperatures.append(temperature)
#             cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
#             cv2.putText(frame, f'{temperature:.2f}C', (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2, cv2.LINE_AA)

#     average_temperature = np.mean(temperatures) if temperatures else 0
#     cv2.putText(frame, f'Orang yang terdeteksi: {person_count}', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
#     cv2.putText(frame, f'Rata-rata Suhu: {average_temperature:.2f}C', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

#     return frame, person_count, average_temperature

# # Function to generate frames for video feed
# def generate_frames():
#     thermal_video_capture = cv2.VideoCapture(thermal_video_path)
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
#     thermal_video_capture.release()

# # Flask route to render index.html
# @app.route('/')
# def index():
#     return render_template('index.html')

# # Flask route for video feed
# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# # Flask route for calibration
# @app.route('/calibrate', methods=['POST'])
# def calibrate():
#     global calibration_offset
#     data = request.get_json()
#     calibration_offset = data.get('offset', 0.0)
#     return jsonify({"message": "Calibration Updated", "offset": calibration_offset})

# # Flask route to toggle off
# @app.route('/toggle_off', methods=['POST'])
# def toggle_off():
#     global thermal_video_capture
#     thermal_video_capture.release()
#     return '', 204

# # Function to run Flask app
# def run_flask_app():
#     app.run(host='0.0.0.0', port=5000)

# # Function to send people count and average temperature via socket
# def send_people_count(client_socket, num_people, avg_temp):
#     message = f'{num_people},{avg_temp:.2f}'
#     client_socket.sendall(message.encode())
#     print(f"Number of people {num_people} and average temperature {avg_temp:.2f} sent")

# # Function to run socket server
# def run_socket_server():
#     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server.bind((server_ip, server_port))
#     server.listen(5)
#     print(f"Running server at: {server_ip}:{server_port}")

#     while True:
#         client_socket, client_address = server.accept()
#         print(f"Connect with {client_address} success")
#         try:
#             while True:
#                 thermal_video_capture = cv2.VideoCapture(thermal_video_path)
#                 success, frame = thermal_video_capture.read()
#                 if not success:
#                     thermal_video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
#                     continue
#                 _, num_people, avg_temp = detect_people_and_temperature(frame)
#                 send_people_count(client_socket, num_people, avg_temp)
#                 time.sleep(1)
#                 try:
#                     response = client_socket.recv(1024).decode()
#                     if response == "jon":
#                         print("Data Transmission Success")
#                 except socket.error as e:
#                     print(f"Error receiving data: {e}")
#                     break
#                 finally:
#                     thermal_video_capture.release()

#         except Exception as e:
#             print(f"Error during communication: {e}")
#         finally:
#             client_socket.close()
#             print("Data transmission completed")

#     server.close()

# if __name__ == '__main__':
#     flask_thread = threading.Thread(target=run_flask_app)
#     flask_thread.daemon = True  # Ensures the thread will close when the main thread ends
#     flask_thread.start()
#     run_socket_server()


# import socket
# import time
# import threading
# from flask import Flask, render_template, Response, request, jsonify
# import cv2
# import torch
# import numpy as np

# # server_ip = "192.168.1.100"   #connect with IP router
# server_ip = "127.0.0.1"     # Connect with IP komputer
# server_port = 8899          # PORT TRANSMISI

# app = Flask(__name__)

# thermal_video_path = '/home/robotjaol/project/cctv_thermal_hvac/main/sample/thermal.mp4'

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
#     thermal_video_capture = cv2.VideoCapture(thermal_video_path)
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

# def send_people_count(client_socket, num_people, avg_temp):
#     message = f'{num_people},{avg_temp:.2f}'
#     client_socket.sendall(message.encode())
#     print(f"Number of people {num_people} and average temperature {avg_temp:.2f} sent")

# def run_flask_app():
#     app.run(host='0.0.0.0', port=5000)

# def run_socket_server():
#     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server.bind((server_ip, server_port))
#     server.listen(5)
#     print(f"Running server at: {server_ip}:{server_port}")

#     try:
#         while True:
#             client_socket, client_address = server.accept()
#             print(f"Connected with {client_address}")

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


# ---------------------------------------------------------------------------
# import socket
# import time
# import threading
# from flask import Flask, render_template, Response
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
# calibration_offset = -10

# #FUNCTION START
# def detect_people_and_temperature(frame):
#     global calibration_offset
#     results = model(frame)
#     detections = results.xyxy[0].cpu().numpy()
#     person_count = 0
#     temperatures = []

#     colormap = cv2.applyColorMap(np.arange(20, 42, 0.01).reshape(1, -1), cv2.COLORMAP_JET)

#     for x1, y1, x2, y2, conf, cls in detections:
#         if int(cls) == 0:  #setup 0 for person
#             person_count += 1
#             person_region = frame[int(y1):int(y2), int(x1):int(x2)]
#             temperature = np.mean(person_region) + calibration_offset
#             temperatures.append(temperature)
#             color = colormap[0, int((temperature - 20) * 100)][::-1] #COLOR MAP

#             cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
#             cv2.putText(frame, f'{temperature:.2f}C', (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2, cv2.LINE_AA)

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
#     flask_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False))
#     flask_thread.start()
#     run_socket_server()
#  ----------------------------------------------------------------------------



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

#-----------------------------------------------------------
#-------------------TESTING PROGRAM PROGRESS----------------
#-----------WEB YOLOv5 AS SERVER AND ESP32 AS CLIENT -------
#-------------------- THERMAL VIDEO LOAD -------------------
#---------------------------PART 5--------------------------

# import socket
# import time
# import threading
# from flask import Flask, render_template, Response
# import cv2
# import torch
# import numpy as np

# # server_ip = "192.168.1.100"   #connect with IP router
# server_ip = "127.0.0.1"     #connect with IP computer
# server_port = 8899

# app = Flask(__name__)

# # Path to the thermal video file
# video_capture = cv2.VideoCapture('/home/robotjaol/pbl/thermal_CCTV_HVAC/main/sample/thermal.mp4')

# # Load YOLOv5 model
# model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# def detect_people_and_temperature(frame):
#     results = model(frame)
#     detections = results.xyxy[0].cpu().numpy()
#     person_count = 0
#     temperatures = []

#     for x1, y1, x2, y2, conf, cls in detections:
#         if int(cls) == 0:  # Class 0 is 'person'
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
#     while True:
#         success, frame = video_capture.read()
#         if not success:
#             video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
#             continue
#         frame_with_people, num_people, avg_temp = detect_people_and_temperature(frame)
#         ret, buffer = cv2.imencode('.jpg', frame_with_people)
#         frame = buffer.tobytes()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

#         # Send data for client
#         yield f'{num_people},{avg_temp:.2f}\n'.encode()

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

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
#                     success, frame = video_capture.read()
#                     if not success:
#                         video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
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



# #-----------------------------------------------------------
# #-------------------TESTING PROGRAM PROGRESS----------------
# #-----------WEB YOLOv5 AS SERVER AND ESP32 AS CLIENT -------
# #---------------------------PART 5--------------------------

# import socket
# import time
# import threading
# from flask import Flask, render_template, Response
# import cv2
# import torch

# # server_ip = "192.168.1.100"   #connect with IP router
# server_ip = "127.0.0.1"     #connect with IP computer
# server_port = 8899

# app = Flask(__name__)

# video_capture = cv2.VideoCapture(0)

# # Load YOLOv5 model
# model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# def detect_people(frame):
#     results = model(frame)
#     detections = results.xyxy[0].cpu().numpy()
#     person_count = 0
#     for x1, y1, x2, y2, conf, cls in detections:
#         if int(cls) == 0:
#             person_count += 1
#             cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
#     cv2.putText(frame, f'Orang yang terdeteksi: {person_count}', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
#     return frame, person_count

# def generate_frames():
#     while True:
#         success, frame = video_capture.read()
#         if not success:
#             break
#         frame_with_people, num_people = detect_people(frame)
#         ret, buffer = cv2.imencode('.jpg', frame_with_people)
#         frame = buffer.tobytes()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

#         yield str(num_people).encode() + b'\n'

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# def run_flask_app():
#     app.run(host='0.0.0.0', port=5000)

# def send_people_count(client_socket):
#     global data_count
#     client_socket.sendall(str(data_count).encode())
#     print(f"Number of people {data_count} sent")

# # Send IR command to the client
# def transmit_ir(client_socket):
#     for ir_command in range (1,5):
#         command_str = str(ir_command)
#         client_socket.sendall(command_str.encode())
#         print(f"IR command {ir_command} terkirim")
#         time.sleep(2)
# # Send LED control command to the client
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
#                     success, frame = video_capture.read()
#                     if not success:
#                         break
#                     _, num_people = detect_people(frame)
#                     client_socket.sendall(str(num_people).encode() + b'\n')
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


#-----------------------------------------------------------
#-------------------TESTING PROGRAM PROGRESS----------------
#-----------WEB OPENCV AS SERVER AND ESP32 AS CLIENT -------
#---------------------------PART 4--------------------------

# import socket
# import time
# import threading
# from flask import Flask, render_template, Response
# import cv2

# server_ip = "192.168.1.100"   #connect with router
# # server_ip = "127.0.0.1"
# server_port = 8899

# app = Flask(__name__)

# video_capture = cv2.VideoCapture(0)

# def detect_faces(frame):
#     face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
#     for (x, y, w, h) in faces:
#         cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
#     cv2.putText(frame, f'Wajah yang terdeteksi: {len(faces)}', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
#     return frame, len(faces)

# def generate_frames():
#     while True:
#         success, frame = video_capture.read()
#         if not success:
#             break
#         frame_with_faces, num_faces = detect_faces(frame)
#         ret, buffer = cv2.imencode('.jpg', frame_with_faces)
#         frame = buffer.tobytes()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

#         yield str(num_faces).encode() + b'\n'

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# def run_flask_app():
#     app.run(host='0.0.0.0', port=5000)

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
#                     success, frame = video_capture.read()
#                     if not success:
#                         break
#                     _, num_faces = detect_faces(frame)
#                     client_socket.sendall(str(num_faces).encode() + b'\n')
#                     time.sleep(1)
#                     # read data client
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


#-----------------------------------------------------------
#-------------------TESTING PROGRAM PROGRESS----------------
#-----------WEB OPENCV AS SERVER AND ESP32 AS CLIENT -------
#---------------------------PART 3--------------------------

# import socket
# import time
# import threading
# from flask import Flask, render_template, Response
# import cv2

# server_ip = "192.168.1.100"   #connect with router
# # server_ip = "127.0.0.1"     #connect with IP computer
# server_port = 8899

# app = Flask(__name__)

# video_capture = cv2.VideoCapture(0)

# def detect_faces(frame):
#     face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
#     for (x, y, w, h) in faces:
#         cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
#     cv2.putText(frame, f'Wajah yang terdeteksi: {len(faces)}', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
#     return frame, len(faces)

# def generate_frames():
#     while True:
#         success, frame = video_capture.read()
#         if not success:
#             break
#         frame_with_faces, num_faces = detect_faces(frame)
#         ret, buffer = cv2.imencode('.jpg', frame_with_faces)
#         frame = buffer.tobytes()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

#         yield str(num_faces).encode() + b'\n'

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# def run_flask_app():
#     app.run(host='0.0.0.0', port=5000)

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
#                     success, frame = video_capture.read()
#                     if not success:
#                         break
#                     _, num_faces = detect_faces(frame)
#                     client_socket.sendall(str(num_faces).encode() + b'\n')
#                     time.sleep(1)
#                     # Tunggu respons dari klien
#                     response = client_socket.recv(1024).decode()
#                     if response == "jon":
#                         print("Data Transmission Success")

#                     # Uncomment the following lines to enable IR and LED commands
#                     # transmit_ir(client_socket)
#                     # server_led(client_socket)
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



#-----------------------------------------------------------
#-------------------TESTING PROGRAM PROGRESS----------------
#-----------WEB OPENCV AS SERVER AND ESP32 AS CLIENT -------
#---------------------------PART 3--------------------------

# import socket
# import time
# import threading
# from flask import Flask, render_template, Response
# import cv2

# # server_ip = "192.168.1.100"   #connect with router
# server_ip = "127.0.0.1"         #connect with ip computer
# server_port = 8899

# app = Flask(__name__)

# video_capture = cv2.VideoCapture(0)

# def detect_faces(frame):
#     face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
#     for (x, y, w, h) in faces:
#         cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
#     cv2.putText(frame, f'Wajah yang terdeteksi: {len(faces)}', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
#     return frame, len(faces)

# def generate_frames():
#     while True:
#         success, frame = video_capture.read()
#         if not success:
#             break
#         frame_with_faces, _ = detect_faces(frame)
#         ret, buffer = cv2.imencode('.jpg', frame_with_faces)
#         frame_bytes = buffer.tobytes()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# def generate_face_count():
#     while True:
#         _, num_faces = detect_faces(video_capture.read()[1])
#         yield str(num_faces).encode() + b'\n'

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# def run_flask_app():
#     app.run(host='0.0.0.0', port=5000)

# def run_socket_server():
#     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server.bind((server_ip, server_port))
#     server.listen(5)
#     print(f"Running server at: {server_ip}:{server_port}")

#     try:
#         while True:
#             client_socket, client_address = server.accept()
#             print(f"Connection from address {client_address} successfully established")

#             try:
#                 while True:
#                     client_socket.sendall(next(generate_face_count()))
#                     response = client_socket.recv(1024).decode()
#                     time.sleep(2)
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

#-----------------------------------------------------------
#-------------------TESTING PROGRAM PROGRESS----------------
#-----------WEB OPENCV AS SERVER AND ESP32 AS CLIENT ------- 
#---------------------------PART 2--------------------------

# import socket
# import time
# import threading
# from flask import Flask, render_template, Response
# import cv2

# server_ip = "192.168.1.100"
# server_port = 8899

# app = Flask(__name__)

# video_capture = cv2.VideoCapture(0)

# def detect_faces(frame):
#     face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
#     for (x, y, w, h) in faces:
#         cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
#     cv2.putText(frame, f'Wajah yang terdeteksi: {len(faces)}', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
#     return frame

# def generate_frames():
#     while True:
#         success, frame = video_capture.read()
#         if not success:
#             break
#         frame_with_faces = detect_faces(frame)
#         ret, buffer = cv2.imencode('.jpg', frame_with_faces)
#         frame = buffer.tobytes()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# def run_flask_app():
#     app.run(host='0.0.0.0', port=5000)

# def run_socket_server():
#     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server.bind((server_ip, server_port))
#     server.listen(5)
#     print(f"Running server at: {server_ip}:{server_port}")

#     try:
#         while True:
#             client_socket, client_address = server.accept()
#             print(f"Connection from address {client_address} successfully established")

#             try:
#                 num_faces = len(detect_faces(video_capture.read()[1]))
#                 client_socket.sendall(str(num_faces).encode())
#                 response = client_socket.recv(1024).decode()
#                 time.sleep(2)
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




#-----------------------------------------------------------
#-------------------TESTING PROGRAM PROGRESS----------------
#-----------WEB OPENCV AS SERVER AND ESP32 AS CLIENT ------- 
#---------------------------PART 1--------------------------

# import socket
# import time
# from flask import Flask, request, render_template
# import threading

# server_ip = "192.168.1.100"
# server_port = 8899
# data_count = 0

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('/web/index.html')

# @app.route('/data', methods=['POST'])
# def receive_data():
#     global data_count
#     data_count = request.json['count']
#     return 'Data received', 200

# def run_flask_app():
#     app.run(host='0.0.0.0', port=5000)

# def run_socket_server():
#     global data_count
#     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server.bind((server_ip, server_port))
#     server.listen(5)

#     print(f"Running server at: {server_ip}:{server_port}")

#     try:
#         while True:
#             client_socket, client_address = server.accept()
#             print(f"Connection from address {client_address} successfully established")

#             try:
#                 # send_people_count(client_socket)# Send the number of people detected
#                 # transmit_ir(client_socket)
#                 # server_led(client_socket)
#                 response = client_socket.recv(1024).decode()
#                 print(f"Response from client: {response}")
#                 time.sleep(2)
#             except Exception as e:
#                 print(f"Error during communication: {e}")
#             finally:
#                 client_socket.close()
#                 print("Data transmission completed")

#     finally:
#         server.close()

# def send_people_count(client_socket):
#     global data_count
#     client_socket.sendall(str(data_count).encode())
#     print(f"Number of people {data_count} sent")

# # Send IR command to the client
# def transmit_ir(client_socket):
#     for ir_command in range (1,5):
#         command_str = str(ir_command)
#         client_socket.sendall(command_str.encode())
#         print(f"IR command {ir_command} terkirim")
#         time.sleep(2)
# # Send LED control command to the client
# def server_led(client_socket):
#     led_command = "LED_ON"
#     client_socket.sendall(led_command.encode())
#     print(f"LED command {led_command} sent")

# if __name__ == '__main__':
#     flask_thread = threading.Thread(target=run_flask_app)
#     flask_thread.start()

#     run_socket_server()


#-----------------------------------------------------------
#-------------------TESTING PROGRAM DONE--------------------
#-----------CONTROLLING COMMMUNICATION USING 4 COMMANDS----- 
#-----------------------------------------------------------

# import socket
# import time

# server_ip = "192.168.1.100"
# server_port = 8899

# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind((server_ip, server_port))
# server.listen(5)

# print(f"Running server :{server_ip}:{server_port}")

# try:
#     while True:
#         client_socket, client_address = server.accept()
#         print(f"Koneksi address {client_address} Alhamdullilah wis Connect Bos")

#         try:
#             for command in ["1\n", "2\n", "3\n", "4\n"]:
#                 client_socket.sendall(command.encode())
#                 response = client_socket.recv(1024).decode()
#                 print(f"Respons dari klien: {response}")
#                 time.sleep(2)  

#         except Exception as e:
#             print(f"Error selama komunikasi: {e}")
#         finally:
#             client_socket.close()
#             print("Data telah ditransmisikan")

# finally:
#     server.close()


#-----------------------------------------------------------
#-------------------TESTING PROGRAM DONE--------------------
#-------------------BASIC COMMUNICATION--------------------- 
#-----------------------------------------------------------

# import socket

# server_ip = "192.168.1.100"
# server_port = 8899

# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind((server_ip, server_port))
# server.listen(5)

# print(f"Running server :{server_ip}:{server_port}")

# try:
#     while True:
#         client_socket, client_address = server.accept()
#         print(f"Koneksi address {client_address} Alhamdullilah wis Connect Bos")

#         try:
#             command = "LED_ON\n"
#             client_socket.sendall(command.encode())
#             response = client_socket.recv(1024).decode()
#             print(f"Respons dari klien: {response}")

#         except Exception as e:
#             print(f"Error selama komunikasi: {e}")
#         finally:
#             client_socket.close()
#             print("Koneksi ditutup")

# finally:
#     server.close()


# TES KIRIM SESUAL PBL 
# import socket
# import time

# server_ip = "192.168.1.100"
# server_port = 8899

# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind((server_ip, server_port))
# server.listen(5)

# print(f"Running server :{server_ip}:{server_port}")

# try:
#     while True:
#         client_socket, client_address = server.accept()
#         print(f"Koneksi address {client_address} Alhamdullilah wis Connect Bos")

#         try:
#             command = "1\n"
#             client_socket.sendall(command.encode())
#             response = client_socket.recv(1024).decode()
#             print(f"Respons dari klien: {response}")

#             time.sleep(2)

#             command = "2\n"
#             client_socket.sendall(command.encode())
#             response = client_socket.recv(1024).decode()
#             print(f"Respons dari klien: {response}")

#             command = "3\n"
#             client_socket.sendall(command.encode())
#             response = client_socket.recv(1024).decode()
#             print(f"Respons dari klien: {response}")

#             time.sleep(2)

#             command = "4\n"
#             client_socket.sendall(command.encode())
#             response = client_socket.recv(1024).decode()
#             print(f"Respons dari klien: {response}")

#         except Exception as e:
#             print(f"Error selama komunikasi: {e}")
#         # finally:
#         #     client_socket.close()
#         #     print("Koneksi ditutup")

# finally:
#     server.close()

