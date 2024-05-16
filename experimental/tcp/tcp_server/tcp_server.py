
#SUKSES MENGIRIM DATA
# import socket

# # Set up server
# server_ip = "192.168.1.100"  # Replace with your server's IP address
# server_port = 8888  # Replace with your server's port

# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind((server_ip, server_port))
# server.listen(5)

# print(f"Server is listening on {server_ip}:{server_port}")

# try:
#     # Accept incoming connections
#     client_socket, client_address = server.accept()
#     print(f"Connection from {client_address} has been established")

#     # Send command to ESP32
#     command = "LED_ON\n"
#     client_socket.sendall(command.encode())

#     # Close connection
#     client_socket.close()
# finally:
#     server.close()

# ----------------------

# KODE SEND DATA LOOPING
import socket

# Set up server
server_ip = "192.168.1.100"  # Ganti dengan alamat IP server Anda
server_port = 8888  # Ganti dengan port server Anda

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((server_ip, server_port))
server.listen(5)

print(f"Running server :{server_ip}:{server_port}")

try:
    while True:
        # Menerima koneksi masuk
        client_socket, client_address = server.accept()
        print(f"Koneksi address {client_address} Alhamdullilah wis Connect Bos")

        try:
            # Kirim perintah ke ESP32
            command = "LED_ON\n"
            client_socket.sendall(command.encode())

            # Terima respons (opsional)
            response = client_socket.recv(1024).decode()
            print(f"Respons dari klien: {response}")

        except Exception as e:
            print(f"Error selama komunikasi: {e}")
        finally:
            client_socket.close()
            print("Koneksi ditutup")

finally:
    server.close()


# ------------------------------------


# import socket 

# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #inisialisasi protokol komunikasi TCP
# host = socket.gethostname()                                         #transmisi data menuju ke client dengan variabel host
# port = 12345                                                        #port custom

# server_socket.bind((host, port))                                    #binding host dan port agar dalam satu komunikasi
# server_socket.listen(5) #listen server 5 poin maksismum control HVAC

# print(f"Server running di {host} pada {port}")

# while True:
#     #cetak indikator ketika koneksi dengan klien berhasil
#     client_socket, address = server_socket.accept()
#     print(f"Connection from {address} successful")

#     message = "Uji coba TCP connection sukses"
#     client_socket.send(message.encode('utf-8')) # transmisi data dengan utf-8

#     client_socket.close() #tutup koneksi dengan client

# DEBUG THE CODE

# import socket

# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # Inisialisasi protokol komunikasi TCP dengan IPv4
# host = '192.168.1.100'  # Alamat IP statis untuk server
# port = 12345  # Port custom

# server_socket.bind((host, port))  # Binding host dan port agar dalam satu komunikasi
# server_socket.listen(5)  # Listen server dengan 5 koneksi maksimum

# print(f"Server running di {host} pada {port}")

# while True:
#     # Cetak indikator ketika koneksi dengan klien berhasil
#     client_socket, address = server_socket.accept()
#     print(f"Connection from {address} successful")

#     message = "Uji coba TCP connection sukses"
#     client_socket.send(message.encode('utf-8'))  # Transmisi data dengan utf-8

#     client_socket.close()  # Tutup koneksi dengan client


## DEBUG MAC ADDRESS

# import socket

# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Initialize TCP protocol
# host = '192.168.1.100'  # Server IP address
# port = 12345  # Custom port

# server_socket.bind((host, port))  # Bind host and port
# server_socket.listen(5)  # Maximum number of queued connections

# print(f"Server running on {host} at port {port}")

# while True:
#     client_socket, address = server_socket.accept()  # Accept client connection
#     print(f"Connection from {address} successful")

#     message = "Uji coba TCP connection sukses"
#     client_socket.send(message.encode('utf-8'))  # Send data to client

#     client_socket.close()  # Close client connection


# PORT 12345

# import socket 

# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # Initialize TCP protocol
# host = '192.168.1.100'  # Static IP address of the server
# port = 12345  # Custom port

# server_socket.bind((host, port))  # Bind the host and port for communication
# server_socket.listen(5)  # Listen for up to 5 connections

# print(f"Server running on {host} at port {port}")

# while True:
#     # Print indicator when a client connects successfully
#     client_socket, address = server_socket.accept()
#     print(f"Connection from {address} successful")

#     message = "Uji coba TCP connection sukses"
#     client_socket.send(message.encode('utf-8'))  # Transmit data in utf-8

#     client_socket.close()  # Close connection with the client



