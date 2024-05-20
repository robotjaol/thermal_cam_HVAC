import socket
import time
import threading
from flask import Flask, render_template, Response
import cv2

# server_ip = "192.168.1.100"   #connect with router
server_ip = "127.0.0.1"         #connect with IP computer
server_port = 8899

app = Flask(__name__)

video_capture = cv2.VideoCapture(0)

def detect_faces(frame):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.putText(frame, f'Wajah yang terdeteksi: {len(faces)}', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    return frame, len(faces)

def generate_frames():
    while True:
        success, frame = video_capture.read()
        if not success:
            break
        frame_with_faces, num_faces = detect_faces(frame)
        ret, buffer = cv2.imencode('.jpg', frame_with_faces)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        yield str(num_faces).encode() + b'\n'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def run_flask_app():
    app.run(host='0.0.0.0', port=5000)

# Fungsi untuk mengirim perintah IR ke klien
def transmit_ir(client_socket):
    for ir_command in range(1, 5):
        command_str = str(ir_command)
        client_socket.sendall(command_str.encode())
        print(f"IR command {ir_command} terkirim")
        time.sleep(2)

# Fungsi untuk mengirim perintah kontrol LED ke klien
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
            print(f"Connection from address {client_address} successfully established")

            try:
                while True:
                    success, frame = video_capture.read()
                    if not success:
                        break
                    _, num_faces = detect_faces(frame)
                    client_socket.sendall(str(num_faces).encode() + b'\n')
                    time.sleep(1)
                    
                    # Tunggu respons dari klien
                    response = client_socket.recv(1024).decode()
                    if response == "jon":
                        print("Data Transmission Success")

                    # Uncomment the following lines to enable IR and LED commands
                    # transmit_ir(client_socket)
                    # server_led(client_socket)
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


