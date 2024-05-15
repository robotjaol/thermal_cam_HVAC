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

import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # Inisialisasi protokol komunikasi TCP dengan IPv4
host = '192.168.1.100'  # Alamat IP statis untuk server
port = 12345  # Port custom

server_socket.bind((host, port))  # Binding host dan port agar dalam satu komunikasi
server_socket.listen(5)  # Listen server dengan 5 koneksi maksimum

print(f"Server running di {host} pada {port}")

while True:
    # Cetak indikator ketika koneksi dengan klien berhasil
    client_socket, address = server_socket.accept()
    print(f"Connection from {address} successful")

    message = "Uji coba TCP connection sukses"
    client_socket.send(message.encode('utf-8'))  # Transmisi data dengan utf-8

    client_socket.close()  # Tutup koneksi dengan client

