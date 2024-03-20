import cv2
import numpy as np
from PIL import ImageFont, Image, ImageDraw
import hyperlpr3 as lpr3
from ultralytics import YOLO

class PlateDetector:
    def __init__(self):
        self.catcher = lpr3.LicensePlateCatcher(detect_level=lpr3.DETECT_LEVEL_HIGH)
        self.model = YOLO('C:\\detect\\yolov8n.pt')

    def draw_plate(self, img, box, text):
        x1, y1, x2, y2 = box
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 200), 2, cv2.LINE_AA)
        data = Image.fromarray(img)
        draw = ImageDraw.Draw(data)
        font = ImageFont.truetype("C:\\Windows\\font\\STFANGSO.TTF", 30, 0)
        draw.text((x1 + 5, y1 - 40), text, (100, 200, 50), font=font)
        res = np.asarray(data)

        return res

    def image_detect(self, img_path):
        img = cv2.imread(img_path)
        results = self.catcher(img)
        
        if len(results) == 0:
            print("No license plate detected.")
            return

        for code, confidence, type_idx, box in results:
            print(f"{code} - {confidence:.4f} - {type_idx} - {box}")
            text = f"{code} - {confidence:.2f}"
            img = self.draw_plate(img, box, text)

        cv2.imshow("w", img)
        cv2.waitKey(0)

    def video_detect(self, video_path):
        video_capture = cv2.VideoCapture(video_path)

        width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        scale_factor = 640 / max(width, height)
        cv2.namedWindow('plate detect Videos', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('plate detect Videos', 1280, int(height * scale_factor))

        while True:
            ret, frame = video_capture.read()

            if not ret:
                break

            results_yolo = self.model(frame)
            annotated_frame = results_yolo[0].plot(conf=False, line_width=1, im_gpu=True, labels=False)

            results_hyperlpr = self.catcher(frame)
            if len(results_hyperlpr) == 0:
                print("No license plate detected.")
                cv2.imshow("plate detect Videos", frame)
                if cv2.waitKey(1) & 0xFF == 27:
                    break
                continue

            for code, confidence, type_idx, box in results_hyperlpr:
                text = f"{code} - {confidence:.2f}"
                frame = self.draw_plate(frame, box, text)

            annotated_frame_resized = cv2.resize(annotated_frame, None, fx=scale_factor, fy=scale_factor)
            frame_resized = cv2.resize(frame, None, fx=scale_factor, fy=scale_factor)

            combined_frame = cv2.hconcat([annotated_frame_resized, frame_resized])
            cv2.imshow('plate detect Videos', combined_frame)

            if cv2.waitKey(1) & 0xFF == 27:
                break

        video_capture.release()
        cv2.destroyAllWindows()
    
    def camera_detect(self, input_source):
        cap = cv2.VideoCapture(input_source)
        if not cap.isOpened():
            print("Error: Unable to open video file.")
            return
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame = cv2.flip(frame, 1)
            results = self.catcher(frame)

            if len(results) == 0:
                print("No license plate detected.")
                cv2.imshow("video", frame)
                if cv2.waitKey(1) & 0xFF == 27:
                    break
                continue

            for code, confidence, type_idx, box in results:
                text = f"{code} - {confidence:.2f}"
                frame = self.draw_plate(frame, box, text)
            
            cv2.imshow("video", frame)

            if cv2.waitKey(1) & 0xFF == 27:
                break
        
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    detector = PlateDetector()

    while True:
        print("  ")
        print("Options:")
        print("     1. Image detection")
        print("     2. Video detection")
        print("     3. Camera detection")
        print("     4. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            image_path = input("Enter image path: ")
            detector.image_detect(image_path)
        elif choice == "2":
            video_path = input("Enter video path: ")
            detector.video_detect(video_path)
        elif choice == "3":
            camera_id = int(input("Enter camera id (0 or 1): "))
            detector.camera_detect(camera_id)
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice.")

