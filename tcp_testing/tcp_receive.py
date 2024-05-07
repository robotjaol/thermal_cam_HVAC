import socket

# Set the IP address and port to listen on
host = '192.168.1.100'  # Change to your mini PC's IP address
port = 1234             # Port yang dipakai

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))

server_socket.listen(5)

print(f"Listening for connections on {host}:{port}")

while True:
    client_socket, address = server_socket.accept()
    print(f"Connection from {address}")

    data = client_socket.recv(1024).decode('utf-8')
    if data:
        print(f"Received data: {data}")
    client_socket.close()
