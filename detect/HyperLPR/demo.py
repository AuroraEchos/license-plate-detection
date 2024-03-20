import importlib.util
import subprocess
import sys
import cv2
import numpy as np
from PIL import ImageFont, Image, ImageDraw
import hyperlpr3 as lpr3


class DependenciesInstaller:
    def __init__(self):
        missing_dependencies = self.check_dependencies()
        if missing_dependencies:
            print("发现缺失的库，正在安装...")
            self.install_dependencies(missing_dependencies)
            print("库安装完成。")
        else:
            print("所有依赖库已安装。")

    def install_dependencies(self, dependencies):
        print("开始安装依赖库...")
        total_dependencies = len(dependencies)
        progress = 0
        
        for dependency in dependencies:
            process = subprocess.Popen([sys.executable, "-m", "pip", "install", dependency], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            while True:
                output = process.stderr.readline().decode().strip()
                if output == '' and process.poll() is not None: 
                    break
                if output:
                    print(output)
                    progress += 1
                    install_progress = progress / total_dependencies * 100
                    progress_bar = int(install_progress / 2) * "#" 
                    print(f"\r[{'#' * 50}] {install_progress:.2f}%", end="", flush=True)

    def check_dependencies(self):
        print("开始检测项目所需依赖库...")
        dependencies = ['cv2', 'hyperlpr3']
        total_dependencies = len(dependencies)
        missing_dependencies = []
        
        for index, dependency in enumerate(dependencies, start=1):
            spec = importlib.util.find_spec(dependency)
            if spec is None:
                missing_dependencies.append(dependency)
            progress = index / total_dependencies * 100
            progress_bar = int(progress / 2) * "#"  
            print(f"\r[{'#' * 50}] {progress:.2f}%", end="", flush=True)
        
        print("\n检测完成。")
        return missing_dependencies

class PlateDetector:
    def __init__(self):
        self.catcher = lpr3.LicensePlateCatcher(detect_level=lpr3.DETECT_LEVEL_HIGH)

    def draw_plate(self, img, box, text):
        x1, y1, x2, y2 = box
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 200), 2, cv2.LINE_AA)
        data = Image.fromarray(img)
        draw = ImageDraw.Draw(data)
        font = ImageFont.truetype("HyperLPR\\resource\\font\\STFANGSO.TTF", 30, 0)
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
            text = f"{code} - {confidence:.2f}"
            img = self.draw_plate(img, box, text)

        cv2.imshow("w", img)
        cv2.waitKey(0)
    
    def detect_plate(self, input_source):
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
                cv2.waitKey(1)
                continue

            for code, confidence, type_idx, box in results:
                print(f"{code} - {confidence:.4f} - {type_idx} - {box}")
                text = f"{code} - {confidence:.2f}"
                frame = self.draw_plate(frame, box, text)
            
            cv2.imshow("video", frame)

            if cv2.waitKey(1) & 0xFF == 27:
                break
        
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    installer = DependenciesInstaller()
    detector = PlateDetector()

    while True:
        print("Options:")
        print("1. Image detection")
        print("2. Video detection")
        print("3. Camera detection")
        print("4. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            image_path = input("Enter image path: ")
            detector.detect_plate(image_path)
        elif choice == "2":
            video_path = input("Enter video path: ")
            detector.detect_plate(video_path)
        elif choice == "3":
            camera_id = int(input("Enter camera id (0 or 1): "))
            detector.detect_plate(camera_id)
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice.")

