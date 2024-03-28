import cv2
import os
import time

def read_images_from_directory(directory):
    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a valid directory.")
        return

    image_count = len([filename for filename in os.listdir(directory) if filename.endswith((".jpg", ".jpeg", ".png"))])
    images_displayed = 0

    while images_displayed < image_count:
        images_found = False
        for filename in os.listdir(directory):
            if filename.endswith((".jpg", ".jpeg", ".png")):
                filepath = os.path.join(directory, filename)
                image = cv2.imread(filepath)
                if image is not None:
                    cv2.imshow("Image", image)
                    cv2.waitKey(1000)
                    images_displayed += 1
                    images_found = True
                else:
                    print(f"Error: Unable to read image '{filepath}'")

        if not images_found:
            print("No images found in the directory.")
            break

        time.sleep(0.5)  # Adjust the delay (in seconds) between checking the directory for new images

    cv2.destroyAllWindows()   

directory = "C:\\Users\\mohit\\Desktop\\photos"
read_images_from_directory(directory)
