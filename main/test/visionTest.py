import cv2

def main():
    camera = cv2.VideoCapture(0)  # Gunakan webcam utama (0)

    while True:
        ret, frame = camera.read()
        if not ret:
            print("Gagal mengambil frame dari kamera")
            break

        # Tampilkan frame video
        cv2.imshow('Webcam', frame)

        # Tunggu 1 milidetik dan periksa apakah pengguna menekan tombol 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Bebaskan sumber daya
    camera.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
