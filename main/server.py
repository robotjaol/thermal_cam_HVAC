import socket
import cv2
import threading
import numpy as np
import torch
from flask import Flask, render_template, Response, jsonify, request
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
        if int(cls) == 0.5:   # Class index for head
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

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/data')
def get_data():
    head_count, avg_temp = detect_heads_from_video()
    data = {'num_heads': int(head_count), 'avg_temp': round(avg_temp, 2), 'tcp_status': True, 'microcontroller_status': False}
    return jsonify(data)

@app.route('/toggle_tcp', methods=['POST'])
def toggle_tcp():
    data = request.get_json()
    new_status = data['tcp_status']
    # Code to handle TCP status toggle
    return jsonify({'success': True})

@app.route('/toggle_microcontroller', methods=['POST'])
def toggle_microcontroller():
    data = request.get_json()
    new_status = data['microcontroller_status']
    # Code to handle microcontroller status toggle
    return jsonify({'success': True})

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
        if len(head_counts) >= 10:
            break

    avg_head_count = sum(head_counts) / len(head_counts)
    avg_temperature = sum(temperatures) / len(temperatures)
    return avg_head_count, avg_temperature

def send_data_to_clients():
    while True:
        head_count, avg_temp = detect_heads_from_video()
        data = {'num_heads': int(head_count), 'avg_temp': int(round(avg_temp)), 'tcp_status': True, 'microcontroller_status': False}
        json_data = json.dumps(data)
        
        try:
            # Connect to ESP32 and send data
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as esp32_socket:
                esp32_socket.connect((esp32_ip, esp32_port))
                esp32_socket.sendall(json_data.encode())
                print("Data sent to ESP32")
        except Exception as e:
            print(f"Error sending data to ESP32: {e}")

        try:
            # Send data to website client
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as website_socket:
                website_socket.connect(('127.0.0.1', server_port))
                website_socket.sendall(json_data.encode())
                print("Data sent to website client")
        except Exception as e:
            print(f"Error sending data to website client: {e}")

        time.sleep(1)  # Adjust the frequency of data transmission as needed

if __name__ == '__main__':
    sender_thread = threading.Thread(target=send_data_to_clients)
    sender_thread.start()

    app.run(host='0.0.0.0', port=server_port, threaded=True)
