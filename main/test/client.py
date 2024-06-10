import socket
import time

server_ip = "127.0.0.1"
server_port = 8899

def run_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((server_ip, server_port))
        print("Connected to the server")

        while True:
            data = client.recv(1024).decode()
            if not data:
                break
            
            head_count, avg_temp = map(float, data.split(','))
            print(f"Number of heads: {int(head_count)}")
            print(f"Average temperature: {avg_temp:.2f}°C")

            client.sendall("jon".encode())
            
            time.sleep(1)
    except ConnectionError as ce:
        print(f"Connection error: {ce}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == '__main__':
    run_client()




# import requests

# def main():
#     server_url = 'http://localhost:5000'  # Ganti dengan URL server Anda
#     response = requests.get(f'{server_url}/video_feed')
#     if response.status_code == 200:
#         # Menggunakan EventSource untuk menerima data secara streaming dari server
#         for line in response.iter_lines():
#             if line:
#                 num_people = line.decode('utf-8').split(': ')[1]
#                 print("Jumlah orang:", num_people)
#     else:
#         print("Gagal terhubung ke server")

# if __name__ == '__main__':
#     main()
