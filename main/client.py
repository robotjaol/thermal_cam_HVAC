import socket
import time

server_ip = "127.0.0.1"
server_port = 8899

def run_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((server_ip, server_port))
        print("Connected to server")

        while True:
            data = client.recv(1024).decode()
            if not data:
                break

            try:
                num_people, avg_temp = map(float, data.split(','))
                print(f"Number of People: {int(num_people)}")
                print(f"Average Temperature: {avg_temp:.2f}°C")

                # Send acknowledgment to server
                client.sendall("ACK".encode())
            except ValueError as ve:
                print(f"Error: Received invalid data format - {ve}")
            except Exception as e:
                print(f"Error: {e}")

            time.sleep(1)
    except ConnectionError as ce:
        print(f"Connection error: {ce}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == '__main__':
    run_client()






# import socket
# import time

# # server_ip = "192.168.1.100"   #connect with router/etherner/W5500
# server_ip = "127.0.0.1"         #connect with IP computer 
# server_port = 8899

# def run_client():
#     client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client.connect((server_ip, server_port))

#     try:
#         while True:
#             data = client.recv(1024).decode()
#             if data.startswith('--frame'):
#                 continue
#             else:
#                 try:
#                     num_faces = int(data.strip())
#                     print(f"Number of faces detected: {num_faces}")
#                 except ValueError:
#                     print(f"Received invalid data: {data}")
#             time.sleep(1)  # Menambahkan jeda selama 1 detik
#     except Exception as e:
#         print(f"Error receiving data: {e}")
#     finally:
#         client.close()

# if __name__ == '__main__':
#     run_client()



# import socket

# # server_ip = "192.168.1.100"   #connect with router/etherner/W5500
# server_ip = "127.0.0.1"         #connect with IP computer 
# server_port = 8899

# def run_client():
#     client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client.connect((server_ip, server_port))

#     try:
#         buffer = b""  # Buffer untuk menyimpan data yang belum lengkap
#         while True:
#             data = client.recv(1024)
#             if not data:
#                 break
#             buffer += data
#             while b'\n' in buffer:
#                 idx = buffer.index(b'\n')
#                 data_piece = buffer[:idx]
#                 buffer = buffer[idx + 1:]
#                 if data_piece.startswith(b'--frame'):
#                     # Jika ini adalah bagian frame, lanjutkan ke iterasi berikutnya
#                     continue
#                 else:
#                     # Ini adalah data jumlah wajah, cetak jika valid
#                     try:
#                         num_faces = int(data_piece.decode())
#                         print(f"Number of faces detected: {num_faces}")
#                     except ValueError:
#                         print(f"Received invalid data: {data_piece}")
#     except Exception as e:
#         print(f"Error receiving data: {e}")
#     finally:
#         client.close()

# if __name__ == '__main__':
#     run_client()

