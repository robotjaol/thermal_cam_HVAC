#-----------------------------------------------------------
#-------------------TESTING PROGRAM PROGRESS----------------
#-----------WEB YOLOv5 AS SERVER AND ESP32 AS CLIENT -------
#---------------------------PART 5--------------------------

import socket
import time
import threading
from flask import Flask, render_template, Response
import cv2
import torch

# server_ip = "192.168.1.100"   #connect with IP router
server_ip = "127.0.0.1"     #connect with IP computer
server_port = 8899

app = Flask(__name__)

video_capture = cv2.VideoCapture(0)

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

def detect_people(frame):
    results = model(frame)
    detections = results.xyxy[0].cpu().numpy()
    person_count = 0
    for x1, y1, x2, y2, conf, cls in detections:
        if int(cls) == 0:
            person_count += 1
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
    cv2.putText(frame, f'Orang yang terdeteksi: {person_count}', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    return frame, person_count

def generate_frames():
    while True:
        success, frame = video_capture.read()
        if not success:
            break
        frame_with_people, num_people = detect_people(frame)
        ret, buffer = cv2.imencode('.jpg', frame_with_people)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        yield str(num_people).encode() + b'\n'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def run_flask_app():
    app.run(host='0.0.0.0', port=5000)

def send_people_count(client_socket):
    global data_count
    client_socket.sendall(str(data_count).encode())
    print(f"Number of people {data_count} sent")

# Send IR command to the client
def transmit_ir(client_socket):
    for ir_command in range (1,5):
        command_str = str(ir_command)
        client_socket.sendall(command_str.encode())
        print(f"IR command {ir_command} terkirim")
        time.sleep(2)
# Send LED control command to the client
def server_led(client_socket):
    led_command = "LED_ON"
    client_socket.sendall(led_command.encode())
    print(f"LED command {led_command} sent")

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
                    success, frame = video_capture.read()
                    if not success:
                        break
                    _, num_people = detect_people(frame)
                    client_socket.sendall(str(num_people).encode() + b'\n')
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



