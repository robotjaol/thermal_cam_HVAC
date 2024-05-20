#-----------------------------------------------------------
#-------------------TESTING PROGRAM PROGRESS----------------
#-----------WEB OPENCV AS SERVER AND ESP32 AS CLIENT ------- 
#-----------------------------------------------------------

import socket
import time
from flask import Flask, request, render_template
import threading

server_ip = "192.168.1.100"
server_port = 8899
data_count = 0

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('/web/index.html')

@app.route('/data', methods=['POST'])
def receive_data():
    global data_count
    data_count = request.json['count']
    return 'Data received', 200

def run_flask_app():
    app.run(host='0.0.0.0', port=5000)

def run_socket_server():
    global data_count
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((server_ip, server_port))
    server.listen(5)

    print(f"Running server at: {server_ip}:{server_port}")

    try:
        while True:
            client_socket, client_address = server.accept()
            print(f"Connection from address {client_address} successfully established")

            try:
                send_people_count(client_socket)# Send the number of people detected
                # transmit_ir(client_socket)
                # server_led(client_socket)
                response = client_socket.recv(1024).decode()
                print(f"Response from client: {response}")
                time.sleep(2)
            except Exception as e:
                print(f"Error during communication: {e}")
            finally:
                client_socket.close()
                print("Data transmission completed")

    finally:
        server.close()

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

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.start()

    run_socket_server()


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


