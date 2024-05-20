from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)
camera = cv2.VideoCapture(0)  # Gunakan webcam utama (0)

def detect_people(frame):
    # Implementasi deteksi orang di sini, contoh menggunakan Haar Cascade
    # Ubah logika ini sesuai kebutuhan Anda
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier('/home/robotjaol/pbl/thermal_CCTV_HVAC/main/test/haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    return len(faces)

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            num_people = detect_people(frame)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # Menambahkan frame ke Response
            # Kirim jumlah orang yang terdeteksi ke klien Python
            yield f"data:{num_people}\n\n"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
