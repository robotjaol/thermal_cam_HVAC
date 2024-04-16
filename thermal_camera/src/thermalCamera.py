import os
import numpy as np
import cv2


class ThermalScreening:
    def __init__(self):
        self.base_dir = '3_thermal_screening/sample videos'
        self.threshold = 200
        self.area_of_box = 700        # 3000 for img input
        self.min_temp = 102           # in fahrenheit
        self.font_scale_caution = 1   # 2 for img input
        self.font_scale_temp = 0.7    # 1 for img input

    def convert_to_temperature(self, pixel_avg):
        return pixel_avg / 2.25

    def process_frame(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        heatmap_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        heatmap = cv2.applyColorMap(heatmap_gray, cv2.COLORMAP_HOT)

        _, binary_thresh = cv2.threshold(
            heatmap_gray, self.threshold, 255, cv2.THRESH_BINARY)

        kernel = np.ones((3, 3), np.uint8)
        image_erosion = cv2.erode(binary_thresh, kernel, iterations=1)
        image_opening = cv2.dilate(image_erosion, kernel, iterations=1)

        contours, _ = cv2.findContours(image_opening, 1, 2)

        image_with_rectangles = np.copy(heatmap)

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)

            if (w) * (h) < self.area_of_box:
                continue

            mask = np.zeros_like(heatmap_gray)
            cv2.drawContours(mask, contour, -1, 255, -1)

            mean = self.convert_to_temperature(
                cv2.mean(heatmap_gray, mask=mask)[0])

            temperature = round(mean, 2)
            color = (0, 255, 0) if temperature < self.min_temp else (
                255, 255, 127)

            if temperature >= self.min_temp:
                cv2.putText(image_with_rectangles, "Suhu tinggi terdeteksi !!!", (35, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, self.font_scale_caution, color, 2, cv2.LINE_AA)

            image_with_rectangles = cv2.rectangle(
                image_with_rectangles, (x, y), (x+w, y+h), color, 2)

            cv2.putText(image_with_rectangles, "{} F".format(temperature), (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, self.font_scale_temp, color, 2, cv2.LINE_AA)

        return image_with_rectangles

    def process_video(self):
        video = cv2.VideoCapture(str(self.base_dir+'video_input.mp4'))
        video_frames = []
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

        while True:
            ret, frame = video.read()

            if not ret:
                break

            frame = self.process_frame(frame)
            video_frames.append(frame)

            cv2.imshow('frame', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        video.release()
        cv2.destroyAllWindows()

        size = (width, height)
        out = cv2.VideoWriter(str(self.base_dir+'output.avi'),
                              cv2.VideoWriter_fourcc(*'MJPG'), 100, size)

        for i in range(len(video_frames)):
            out.write(video_frames[i])
        out.release()

    def run(self):
        self.process_video()


if __name__ == "__main__":
    thermal_screening = ThermalScreening()
    thermal_screening.run()
