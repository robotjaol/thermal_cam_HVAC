import socket

server_ip = "192.168.1.100"
server_port = 8899

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((server_ip, server_port))
server.listen(5)

print(f"Running server :{server_ip}:{server_port}")

try:
    while True:
        client_socket, client_address = server.accept()
        print(f"Koneksi address {client_address} Alhamdullilah wis Connect Bos")

        try:
            command = "LED_ON\n"
            client_socket.sendall(command.encode())
            response = client_socket.recv(1024).decode()
            print(f"Respons dari klien: {response}")

        except Exception as e:
            print(f"Error selama komunikasi: {e}")
        finally:
            client_socket.close()
            print("Koneksi ditutup")

finally:
    server.close()


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
#             command = "ON_AC1\n"
#             client_socket.sendall(command.encode())
#             response = client_socket.recv(1024).decode()
#             print(f"Respons dari klien: {response}")

#             time.sleep(2)

#             command = "OFF_AC1\n"
#             client_socket.sendall(command.encode())
#             response = client_socket.recv(1024).decode()
#             print(f"Respons dari klien: {response}")

#             command = "ON_AC2\n"
#             client_socket.sendall(command.encode())
#             response = client_socket.recv(1024).decode()
#             print(f"Respons dari klien: {response}")

#             time.sleep(2)

#             command = "OFF_AC2\n"
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
