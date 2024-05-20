import requests

def main():
    server_url = 'http://localhost:5000'  # Ganti dengan URL server Anda
    response = requests.get(f'{server_url}/video_feed')
    if response.status_code == 200:
        # Menggunakan EventSource untuk menerima data secara streaming dari server
        for line in response.iter_lines():
            if line:
                num_people = line.decode('utf-8').split(': ')[1]
                print("Jumlah orang:", num_people)
    else:
        print("Gagal terhubung ke server")

if __name__ == '__main__':
    main()
