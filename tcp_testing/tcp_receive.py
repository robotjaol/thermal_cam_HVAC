import socket

# Set the IP address and port to listen on
host = '192.168.1.100'  # Change to your mini PC's IP address
port = 1234             # Change to the port number your mini PC is listening on

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the host and port
server_socket.bind((host, port))

# Start listening for incoming connections
server_socket.listen(5)

print(f"Listening for connections on {host}:{port}")

while True:
    # Accept a connection
    client_socket, address = server_socket.accept()
    print(f"Connection from {address}")

    # Receive data from the client
    data = client_socket.recv(1024).decode('utf-8')
    if data:
        print(f"Received data: {data}")

    # Close the client socket
    client_socket.close()
