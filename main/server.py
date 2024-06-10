import socket
import cv2
import threading
import numpy as np
import torch
from flask import Flask, render_template, Response, jsonify
import json
import time

esp32_ip = "192.168.1.100"
esp32_port = 8899
server_port = 5000

thermal_video_path = '/home/robotjaol/project/cctv_thermal_hvac/main/sample/thermal.mp4'

model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

calibration_offset = -75

app = Flask(__name__)

def detect_heads(frame):
    results = model(frame)
    detections = results.xyxy[0].cpu().numpy()
    head_count = 0
    temperatures = []

    for x1, y1, x2, y2, conf, cls in detections:
        if int(cls) == 0 and conf > 0.5:  # Class index for head and confidence threshold
            head_count += 1
            head_region = frame[int(y1):int(y2), int(x1):int(x2)]
            temperature = np.mean(head_region) + calibration_offset
            temperatures.append(temperature)
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)  
            cv2.putText(frame, f'{temperature:.2f}C', (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2, cv2.LINE_AA)

    average_temperature = np.mean(temperatures) if temperatures else 0

    return head_count, average_temperature


def generate_frames():
    thermal_video_capture = cv2.VideoCapture(thermal_video_path)
    while True:
        success, frame = thermal_video_capture.read()
        if not success:
            thermal_video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        head_count, avg_temp = detect_heads(frame)
        cv2.putText(frame, f'People: {head_count}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)  
        cv2.putText(frame, f'Avg Temp: {avg_temp:.2f}C', (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA) 

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def get_data():
    head_count, avg_temp = detect_heads_from_video()
    data = {'num_heads': int(head_count), 'avg_temp': round(avg_temp, 2)}
    return jsonify(data)

def send_data_to_clients():
    while True:
        head_count, avg_temp = detect_heads_from_video()
        data = {'num_heads': int(head_count), 'avg_temp': round(avg_temp, 2), 'tcp_status': True, 'microcontroller_status': False}
        json_data = json.dumps(data)
        
        try:
            # Connect to ESP32 and send data
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as esp32_socket:
                esp32_socket.connect((esp32_ip, esp32_port))
                esp32_socket.sendall(json_data.encode())
                print("Data sent to ESP32")
        except Exception as e:
            print(f"Error sending data to ESP32: {e}")

        time.sleep(1)  # Adjust the frequency of data transmission as needed

def detect_heads_from_video():
    thermal_video_capture = cv2.VideoCapture(thermal_video_path)
    head_counts = []
    temperatures = []

    while True:
        success, frame = thermal_video_capture.read()
        if not success:
            thermal_video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        head_count, avg_temp = detect_heads(frame)  
        head_counts.append(head_count)
        temperatures.append(avg_temp)

        # Break the loop after processing a few frames (adjust as needed)
        if len(head_counts) >= 10:
            break

    avg_head_count = sum(head_counts) / len(head_counts)
    avg_temperature = sum(temperatures) / len(temperatures)
    return avg_head_count, avg_temperature

if __name__ == '__main__':
    sender_thread = threading.Thread(target=send_data_to_clients)
    sender_thread.start()

    app.run(host='0.0.0.0', port=server_port, threaded=True)


# import socket
# import cv2
# import threading
# import numpy as np
# import torch
# from flask import Flask, render_template, Response, jsonify
# import json
# import time

# # server_ip = "192.168.1.100"
# server_ip = "127.0.0.1"
# server_port = 8899

# thermal_video_path = '/home/robotjaol/project/cctv_thermal_hvac/main/sample/thermal.mp4'

# model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# calibration_offset = -75

# app = Flask(__name__)

# def detect_heads(frame):
#     results = model(frame)
#     detections = results.xyxy[0].cpu().numpy()
#     head_count = 0
#     temperatures = []

#     for x1, y1, x2, y2, conf, cls in detections:
#         if int(cls) == 0:  # Class index for head
#             head_count += 1
#             head_region = frame[int(y1):int(y2), int(x1):int(x2)]
#             temperature = np.mean(head_region) + calibration_offset
#             temperatures.append(temperature)
#             cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)  # Green rectangle
#             cv2.putText(frame, f'{temperature:.2f}C', (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2, cv2.LINE_AA)

#     average_temperature = np.mean(temperatures) if temperatures else 0

#     return head_count, average_temperature

# def generate_frames():
#     thermal_video_capture = cv2.VideoCapture(thermal_video_path)
#     while True:
#         success, frame = thermal_video_capture.read()
#         if not success:
#             thermal_video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
#             continue

#         head_count, avg_temp = detect_heads(frame)
#         cv2.putText(frame, f'People: {head_count}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)  # Add number of people text
#         cv2.putText(frame, f'Avg Temp: {avg_temp:.2f}C', (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)  # Add average temperature text

#         ret, buffer = cv2.imencode('.jpg', frame)
#         frame = buffer.tobytes()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/data')
# def data():
#     head_count, avg_temp = detect_heads_from_video()
#     return jsonify(num_heads=head_count, avg_temp=avg_temp, tcp_status=True, microcontroller_status=False)

# def detect_heads_from_video():
#     thermal_video_capture = cv2.VideoCapture(thermal_video_path)
#     head_counts = []
#     temperatures = []

#     while True:
#         success, frame = thermal_video_capture.read()
#         if not success:
#             thermal_video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
#             continue

#         head_count, avg_temp = detect_heads(frame)
#         head_counts.append(head_count)
#         temperatures.append(avg_temp)

#         # Break the loop after processing a few frames (adjust as needed)
#         if len(head_counts) >= 10:
#             break

#     avg_head_count = sum(head_counts) / len(head_counts)
#     avg_temperature = sum(temperatures) / len(temperatures)
#     return avg_head_count, avg_temperature

# def handle_client(client_socket):
#     while True:
#         try:
#             head_count, avg_temp = detect_heads_from_video()
#             data = {'num_heads': int(head_count), 'avg_temp': avg_temp, 'tcp_status': True, 'microcontroller_status': False}
#             json_data = json.dumps(data)
#             client_socket.sendall(json_data.encode())
#             time.sleep(1)
#         except Exception as e:
#             print(f"Error sending data to client: {e}")
#             break

#     client_socket.close()


# def send_data_to_clients():
#     while True:
#         head_count, avg_temp = detect_heads_from_video()
#         data = {'num_heads': int(head_count), 'avg_temp': int(round(avg_temp)), 'tcp_status': True, 'microcontroller_status': False}
#         json_data = json.dumps(data)
#         for client in clients:
#             try:
#                 client.sendall(json_data.encode())
#             except Exception as e:
#                 print(f"Error sending data to client: {e}")
#                 clients.remove(client)

#         time.sleep(1)  # Adjust the frequency of data transmission as needed

# def accept_clients():
#     while True:
#         try:
#             client_socket, _ = server.accept()
#             print(f"Connected with {client_socket.getpeername()}")
#             clients.append(client_socket)
#             client_thread = threading.Thread(target=handle_client, args=(client_socket,))
#             client_thread.start()
#         except Exception as e:
#             print(f"Error accepting client connection: {e}")
#             break


# if __name__ == '__main__':
#     flask_thread = threading.Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 5000, 'threaded': True})
#     flask_thread.start()

#     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server.bind((server_ip, server_port))
#     server.listen(5)
#     print(f"Running server at: {server_ip}:{server_port}")

#     clients = []

#     server_thread = threading.Thread(target=accept_clients)
#     server_thread.start()

#     sender_thread = threading.Thread(target=send_data_to_clients)
#     sender_thread.start()




##----------------------------CLIENT SERVER SETTING DONE
# import socket
# import time
# import threading
# from flask import Flask, render_template, Response, request, jsonify
# import cv2
# import torch
# import numpy as np

# # server_ip = "192.168.1.100"
# server_ip = "127.0.0.1"
# server_port = 8899

# app = Flask(__name__)

# thermal_video_path = '/home/robotjaol/project/cctv_thermal_hvac/main/sample/thermal.mp4'
# model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# calibration_offset = -75

# def detect_heads_and_temperature(frame):
#     global calibration_offset
#     results = model(frame)
#     detections = results.xyxy[0].cpu().numpy()
#     head_count = 0
#     temperatures = []

#     for x1, y1, x2, y2, conf, cls in detections:
#         if int(cls) == 0:
#             head_region = frame[int(y1):int(y1 + (y2 - y1) / 3), int(x1):int(x2)]
#             head_count += 1
#             temperature = np.mean(head_region) + calibration_offset
#             temperatures.append(temperature)
#             cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y1 + (y2 - y1) // 3)), (0, 255, 0), 2)
#             cv2.putText(frame, f'{temperature:.2f}C', (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2, cv2.LINE_AA)

#     average_temperature = np.mean(temperatures) if temperatures else 0
#     cv2.putText(frame, f'People: {head_count}', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
#     cv2.putText(frame, f'Average Temp: {average_temperature:.2f}C', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

#     return head_count, average_temperature

# def get_data():
#     thermal_video_capture = cv2.VideoCapture(thermal_video_path)
#     success, frame = thermal_video_capture.read()
#     thermal_video_capture.release()
#     if success:
#         return detect_heads_and_temperature(frame)
#     else:
#         return 0, 0  # Default value during transmission

# def generate_frames():
#     thermal_video_capture = cv2.VideoCapture(thermal_video_path)
#     while True:
#         success, frame = thermal_video_capture.read()
#         if not success:
#             thermal_video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
#             continue

#         _, _ = detect_heads_and_temperature(frame)
#         ret, buffer = cv2.imencode('.jpg', frame)
#         frame = buffer.tobytes()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
#     thermal_video_capture.release()

# @app.route('/data', methods=['GET'])
# def data():
#     num_heads, avg_temp = get_data()
#     return jsonify({"num_heads": num_heads, "avg_temp": avg_temp})

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

# @app.route('/toggle_tcp', methods=['POST'])
# def toggle_tcp():
#     return '', 204

# @app.route('/adjust_temperature', methods=['POST'])
# def adjust_temperature():
#     return '', 204

# @app.route('/toggle_microcontroller', methods=['POST'])
# def toggle_microcontroller():
#     return '', 204

# def run_flask_app():
#     app.run(host='0.0.0.0', port=5000)

# def send_head_count(client_socket, num_heads, avg_temp):
#     message = f'{num_heads},{avg_temp:.2f}'
#     client_socket.sendall(message.encode())
#     print(f"Number of heads {num_heads} and average temperature {avg_temp:.2f} sent")

# def run_socket_server():
#     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server.bind((server_ip, server_port))
#     server.listen(5)
#     print(f"Running server at: {server_ip}:{server_port}")

#     while True:
#         client_socket, client_address = server.accept()
#         print(f"Connected with {client_address}")
#         try:
#             while True:
#                 num_heads, avg_temp = get_data()
#                 send_head_count(client_socket, num_heads, avg_temp)
#                 time.sleep(1)
#                 try:
#                     response = client_socket.recv(1024).decode()
#                     if response == "jon":
#                         print("Data Transmission Success")
#                 except socket.error as e:
#                     print(f"Error receiving data: {e}")
#                     break

#         except Exception as e:
#             print(f"Error during communication: {e}")
#         finally:
#             client_socket.close()
#             print("Data transmission completed")

#     server.close()

# if __name__ == '__main__':
#     flask_thread = threading.Thread(target=run_flask_app)
#     flask_thread.daemon = True
#     flask_thread.start()
#     run_socket_server()

## MAISH ERPROR DATA TIDAK UPDATE DARI SERVER
# import socket
# import time
# import threading
# from flask import Flask, render_template, Response, request, jsonify
# import cv2
# import torch
# import numpy as np

# # server_ip = "192.168.1.100"
# server_ip = "127.0.0.1"
# server_port = 8899

# app = Flask(__name__)

# thermal_video_path = '/home/robotjaol/project/cctv_thermal_hvac/main/sample/thermal.mp4'
# model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# calibration_offset = -75

# def detect_heads_and_temperature(frame):
#     global calibration_offset
#     results = model(frame)
#     detections = results.xyxy[0].cpu().numpy()
#     head_count = 0
#     temperatures = []

#     for x1, y1, x2, y2, conf, cls in detections:
#         if int(cls) == 0:
#             head_region = frame[int(y1):int(y1 + (y2 - y1) / 3), int(x1):int(x2)]
#             head_count += 1
#             temperature = np.mean(head_region) + calibration_offset
#             temperatures.append(temperature)
#             cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y1 + (y2 - y1) // 3)), (0, 255, 0), 2)
#             cv2.putText(frame, f'{temperature:.2f}C', (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2, cv2.LINE_AA)

#     average_temperature = np.mean(temperatures) if temperatures else 0
#     cv2.putText(frame, f'Orang yang terdeteksi: {head_count}', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
#     cv2.putText(frame, f'Rata-rata Suhu: {average_temperature:.2f}C', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

#     return head_count, average_temperature

# def get_data():
#     thermal_video_capture = cv2.VideoCapture(thermal_video_path)
#     success, frame = thermal_video_capture.read()
#     thermal_video_capture.release()
#     if success:
#         num_heads, avg_temp = detect_heads_and_temperature(frame)
#         return num_heads, avg_temp
#     else:
#         return 0, 0  # Default condition

# def generate_frames():
#     thermal_video_capture = cv2.VideoCapture(thermal_video_path)
#     while True:
#         success, frame = thermal_video_capture.read()
#         if not success:
#             thermal_video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
#             continue

#         _, _ = detect_heads_and_temperature(frame)
#         ret, buffer = cv2.imencode('.jpg', frame)
#         frame = buffer.tobytes()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
#     thermal_video_capture.release()

# @app.route('/data', methods=['GET'])
# def data():
#     num_heads, avg_temp = get_data()
#     return jsonify({"num_heads": num_heads, "avg_temp": avg_temp})

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

# @app.route('/toggle_tcp', methods=['POST'])
# def toggle_tcp():
#     return '', 204

# @app.route('/adjust_temperature', methods=['POST'])
# def adjust_temperature():
#     return '', 204

# @app.route('/toggle_microcontroller', methods=['POST'])
# def toggle_microcontroller():
#     return '', 204

# def run_flask_app():
#     app.run(host='0.0.0.0', port=5000)

# def send_head_count(client_socket, num_heads, avg_temp):
#     message = f'{num_heads},{avg_temp:.2f}'
#     client_socket.sendall(message.encode())
#     print(f"Number of heads {num_heads} and average temperature {avg_temp:.2f} sent")

# def run_socket_server():
#     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server.bind((server_ip, server_port))
#     server.listen(5)
#     print(f"Running server at: {server_ip}:{server_port}")

#     while True:
#         client_socket, client_address = server.accept()
#         print(f"Connected with {client_address}")
#         try:
#             while True:
#                 thermal_video_capture = cv2.VideoCapture(thermal_video_path)
#                 success, frame = thermal_video_capture.read()
#                 if not success:
#                     thermal_video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
#                     continue
#                 num_heads, avg_temp = detect_heads_and_temperature(frame)
#                 send_head_count(client_socket, num_heads, avg_temp)
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
#     flask_thread.daemon = True
#     flask_thread.start()
#     run_socket_server()

# import socket
# import time
# import threading
# from flask import Flask, render_template, Response, request, jsonify
# import cv2
# import torch
# import numpy as np

# # server_ip = "192.168.1.100"
# server_ip = "127.0.0.1"
# server_port = 8899

# app = Flask(__name__)

# thermal_video_path = '/home/robotjaol/project/cctv_thermal_hvac/main/sample/thermal.mp4'
# model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# calibration_offset = -75

# def detect_heads_and_temperature(frame):
#     global calibration_offset
#     results = model(frame)
#     detections = results.xyxy[0].cpu().numpy()
#     head_count = 0
#     temperatures = []

#     for x1, y1, x2, y2, conf, cls in detections:
#         if int(cls) == 0:
#             head_region = frame[int(y1):int(y1 + (y2 - y1) / 3), int(x1):int(x2)]
#             head_count += 1
#             temperature = np.mean(head_region) + calibration_offset
#             temperatures.append(temperature)
#             cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y1 + (y2 - y1) // 3)), (0, 255, 0), 2)
#             cv2.putText(frame, f'{temperature:.2f}C', (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2, cv2.LINE_AA)

#     average_temperature = np.mean(temperatures) if temperatures else 0
#     cv2.putText(frame, f'Orang yang terdeteksi: {head_count}', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
#     cv2.putText(frame, f'Rata-rata Suhu: {average_temperature:.2f}C', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

#     return head_count, average_temperature

# def get_data():
#     thermal_video_capture = cv2.VideoCapture(thermal_video_path)
#     success, frame = thermal_video_capture.read()
#     thermal_video_capture.release()
#     if success:
#         num_heads, avg_temp = detect_heads_and_temperature(frame)
#         return num_heads, avg_temp
#     else:
#         return 0, 0  # Kondisi Defalut

# def generate_frames():
#     thermal_video_capture = cv2.VideoCapture(thermal_video_path)
#     while True:
#         success, frame = thermal_video_capture.read()
#         if not success:
#             thermal_video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
#             continue

#         _, num_heads, avg_temp = detect_heads_and_temperature(frame)
#         ret, buffer = cv2.imencode('.jpg', frame)
#         frame = buffer.tobytes()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
#     thermal_video_capture.release()

# @app.route('/data', methods=['GET'])
# def data():
#     num_heads, avg_temp = get_data()
#     return jsonify({"num_heads": num_heads, "avg_temp": avg_temp})

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

# @app.route('/toggle_tcp', methods=['POST'])
# def toggle_tcp():
#     return '', 204

# @app.route('/adjust_temperature', methods=['POST'])
# def adjust_temperature():
#     return '', 204

# @app.route('/toggle_microcontroller', methods=['POST'])
# def toggle_microcontroller():
#     return '', 204

# def run_flask_app():
#     app.run(host='0.0.0.0', port=5000)

# def send_head_count(client_socket, num_heads, avg_temp):
#     message = f'{num_heads},{avg_temp:.2f}'
#     client_socket.sendall(message.encode())
#     print(f"Number of heads {num_heads} and average temperature {avg_temp:.2f} sent")

# def run_socket_server():
#     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server.bind((server_ip, server_port))
#     server.listen(5)
#     print(f"Running server at: {server_ip}:{server_port}")

#     while True:
#         client_socket, client_address = server.accept()
#         print(f"Connected with {client_address}")
#         try:
#             while True:
#                 thermal_video_capture = cv2.VideoCapture(thermal_video_path)
#                 success, frame = thermal_video_capture.read()
#                 if not success:
#                     thermal_video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
#                     continue
#                 num_heads, avg_temp = detect_heads_and_temperature(frame)
#                 send_head_count(client_socket, num_heads, avg_temp)
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
#     flask_thread.daemon = True
#     flask_thread.start()
#     run_socket_server()



# import socket
# import time
# import threading
# from flask import Flask, render_template, Response, request, jsonify
# import cv2
# import torch
# import numpy as np

# # server_ip = "192.168.1.100" # Server IP ROUTER
# server_ip = "127.0.0.1"    # Connect with IP computer
# server_port = 8899           # PORT TRANSMISSION

# app = Flask(__name__)

# # Path to thermal video
# thermal_video_path = '/home/robotjaol/proj@app.route('/data', methods=['GET'])
# def data():
#     num_heads, avg_temp = get_data()
#     return jsonify({"num_heads": num_heads, "avg_temp": avg_temp})ect/cctv_thermal_hvac/main/sample/thermal.mp4'
# model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# # Initial calibration offset manual
# calibration_offset = -75

# # Function to detect heads and temperature
# def detect_heads_and_temperature(frame):
#     global calibration_offset
#     results = model(frame)
#     detections = results.xyxy[0].cpu().numpy()
#     head_count = 0
#     temperatures = []

#     for x1, y1, x2, y2, conf, cls in detections:
#         if int(cls) == 0:  # setup 0 for person
#             # Focus on the upper part of the bounding box (head region)
#             head_region = frame[int(y1):int(y1 + (y2 - y1) / 3), int(x1):int(x2)]
#             head_count += 1
#             temperature = np.mean(head_region) + calibration_offset
#             temperatures.append(temperature)
#             cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y1 + (y2 - y1) // 3)), (0, 255, 0), 2)
#             cv2.putText(frame, f'{temperature:.2f}C', (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2, cv2.LINE_AA)

#     average_temperature = np.mean(temperatures) if temperatures else 0
#     cv2.putText(frame, f'Orang yang terdeteksi: {head_count}', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
#     cv2.putText(frame, f'Rata-rata Suhu: {average_temperature:.2f}C', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

#     return frame, head_count, average_temperature

# # Function to generate frames for video feed
# def generate_frames():
#     thermal_video_capture = cv2.VideoCapture(thermal_video_path)
#     while True:
#         success, frame = thermal_video_capture.read()
#         if not success:
#             thermal_video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
#             continue

#         frame_with_heads, num_heads, avg_temp = detect_heads_and_temperature(frame)
#         ret, buffer = cv2.imencode('.jpg', frame_with_heads)
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

# # Function to send head count and average temperature via socket
# def send_head_count(client_socket, num_heads, avg_temp):
#     message = f'{num_heads},{avg_temp:.2f}'
#     client_socket.sendall(message.encode())
#     print(f"Number of heads {num_heads} and average temperature {avg_temp:.2f} sent")

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
#                 _, num_heads, avg_temp = detect_heads_and_temperature(frame)
#                 send_head_count(client_socket, num_heads, avg_temp)
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








