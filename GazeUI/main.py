import cv2
import os
import mediapipe as mp
import argparse
import time
from user_face_recognition import user_recognition
import subprocess
import multiprocessing
import pyautogui
from datetime import datetime, timezone
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import json
import pygame
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import requests
import RPi.GPIO as GPIO
from dotenv import load_dotenv, find_dotenv

dotenv_path = find_dotenv('../.env')
load_dotenv(dotenv_path)

webAppIP = os.getenv('WEBAPP_IP')
webAppPort = os.getenv('WEBAPP_PORT')

time_interval = 600

#setup GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(11, GPIO.IN)
GPIO.setup(9, GPIO.OUT)

# mirror api call

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pyautogui.FAILSAFE = False
authenticated = False
BOX_SIZE_RATIO = 0.3 
screen_width, screen_height = pyautogui.size()

#open frontend

http_server_process = subprocess.Popen('serve -s build', shell=True)
time.sleep(5)

chrome_options = Options()
ser = Service("/usr/lib/chromium-browser/chromedriver")
chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
driver = webdriver.Chrome(service = ser, options = chrome_options)
driver.maximize_window()
driver.get('http://localhost:3000/')
driver.fullscreen_window()
time.sleep(2)

#set alarms
def alarms_thread(alarms, queue):
  pygame.init()
  print("alarm")
  alarm_sound = "alarm.MP3"
  pygame.mixer.music.load(alarm_sound)
  for alarm in alarms:
    alarm_datetime = (datetime.strptime(f"{alarm['alarm_date']} {alarm['alarm_time']}", "%Y-%m-%d %H:%M:%S").astimezone().timestamp())
    time_to_wait = alarm_datetime - datetime.now(timezone.utc).timestamp()
    if(time_to_wait > 0):
      print(alarm_datetime)
      print(datetime.now(timezone.utc).timestamp())
      print(time_to_wait)
      print(alarm['alarm_time'])
      time.sleep(int(time_to_wait))
      print("alarm_time")
      pygame.mixer.music.play()
      while pygame.mixer.music.get_busy():
        authenticated = queue.get()
        if(authenticated == True):
          print("auth")
          pygame.mixer.music.stop()

def run(model: str, num_hands: int,
        min_hand_detection_confidence: float,
        min_hand_presence_confidence: float, min_tracking_confidence: float,
        camera_id: int, width: int, height: int) -> None:
    
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    
    queue = multiprocessing.Queue()
    
    #send get_alarms request to server

    alarm_times = [time.time() + 15]
    
    alarms_api = requests.get("http://" + webAppIP + ":" + webAppPort + "/alarm_api/2")
    alarms = alarms_api.json()["data"]
    print(alarms)
    alarm_thread_instance = multiprocessing.Process(target=alarms_thread, args=(alarms, queue))
    alarm_thread_instance.start()
    
    current_frontend_state = "home"
    spotify_delay = 0
    snapshot_write_delay = 0
    snapshot_read_delay = 0

    authenticated = False
    spotify_playing = False

    base_options = python.BaseOptions(model_asset_path=model)
    options = vision.GestureRecognizerOptions(base_options=base_options)
    recognizer = vision.GestureRecognizer.create_from_options(options)

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=min_tracking_confidence) as pose_model:
      
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture frame.")
                break

            image = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            queue.put(authenticated)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
            results_pose = pose_model.process(rgb_frame)

            if results_pose.pose_landmarks:
                ih, iw, _ = frame.shape
                box_size = int(min(iw, ih) * BOX_SIZE_RATIO)

                nose_landmark = results_pose.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE.value]
                if nose_landmark.visibility > 0.5:
                    nose_x = int(nose_landmark.x * iw)
                    nose_y = int(nose_landmark.y * ih)
                    face_box = (nose_x - box_size, nose_y - box_size, nose_x + box_size, nose_y + box_size)

                left_hand_box = (int(results_pose.pose_landmarks.landmark[19].x * iw) - box_size, int(results_pose.pose_landmarks.landmark[19].y * ih) - box_size,int(results_pose.pose_landmarks.landmark[19].x * iw) + box_size, int(results_pose.pose_landmarks.landmark[19].y * ih) + box_size)
                right_hand_box = (int(results_pose.pose_landmarks.landmark[20].x * iw) - box_size, int(results_pose.pose_landmarks.landmark[20].y * ih) - box_size,int(results_pose.pose_landmarks.landmark[20].x * iw) + box_size, int(results_pose.pose_landmarks.landmark[20].y * ih) + box_size)
                
                left_hand_roi = rgb_frame[max(0, left_hand_box[1]):min(ih, left_hand_box[3]), max(0, left_hand_box[0]):min(iw, left_hand_box[2])]
                right_hand_roi = rgb_frame[max(0, right_hand_box[1]):min(ih, right_hand_box[3]), max(0, right_hand_box[0]):min(iw, right_hand_box[2])]
                
                if(face_box != None):
                  face_roi = rgb_frame[max(0, face_box[1]):min(ih, face_box[3]), max(0, face_box[0]):min(iw, face_box[2])]
                  if(face_roi.shape[0]> 0 and authenticated != True):
                    auth = user_recognition(face_roi)
                    if(auth["success"] == 1):
                        person = auth["username"]
                        uid = auth["uid"] 
                        if(current_frontend_state == "home"):
                          #call get all API
                          api_data = requests.get("http://"+ webAppIP + ":" + webAppPort +"/get_everything_api/" + str(uid))
                          data = api_data.json()
                          print(data)
                          data["layout"] = json.loads(data["layout"])
                          #data = '{"alarm_time": "07:00:00", "alarm_date": "2024-05-15", "layout": [{"i": "widget1", "x": 0, "y": 0, "w": 1, "h": 1}, {"i": "widget2", "x": 0, "y": 1, "w": 1, "h": 3}, {"i": "widget3", "x": 1, "y": 0, "w": 1, "h": 1}, {"i": "widget4", "x": 2, "y": 0, "w": 1, "h": 1}, {"i": "widget5", "x": 2, "y": 1, "w": 1, "h": 1}], "user_data": {"id": 2, "username": "siddramu", "spotify_access_token": "BQAgHsAY0vFDmzsXlHAIh43plbiedCZbBnEbFIfNoAVudfs1WaBqa89QiOGcvMHlvNM9MCA4YesQNeyt0OgvgZ3a0Gf1Du6Pn2Wktrb8iGBpqJuzlvhq1e244MZpMxfLBvy-Zyb2Ub5DhdJ49aqCu4MnrPepeanw_7t4lPpyLHdhyKx2DNunzyAMz4Yc7fh9Iy5y_kWNOOWor7Rkp0UpEZRzcivf", "spotify_refresh_token": "AQD8e2uO6XiTtJCtbwXqqNaupcC1Nl2YYQVX7gZ-ifrO7attvQUdzlkzu28ki0P-gMI3Sz9SYYzwQNPszZ_HxjOhQ2eCEZjrRA87Adq528Bv4gpXLP9NkKq9dgU9Oxgc5Y8"}, "top_10_todo": [{"title": "Running", "due_date": "2024-05-15T07:25:00Z", "task_status": "Pending"}, {"title": "PPT", "due_date": "2024-05-15T23:46:00Z", "task_status": "Pending"}]}'
                          driver.maximize_window()
                          driver.get('http://localhost:3000/users/' + json.dumps(data))
                          driver.fullscreen_window()
                          current_frontend_state = "user"
                          authenticated = True
                          queue.put(authenticated)
                          GPIO.output(9, GPIO.HIGH)
                          auth_time = int(time.time())
                    else:
                        authenticated = False
                        queue.put(authenticated)
                        GPIO.output(9, GPIO.LOW)
                        if(current_frontend_state == "user"):
                          driver.maximize_window()
                          driver.get('http://localhost:3000/')
                          driver.fullscreen_window()
                          current_frontend_state = "home"
                          break
        
                if(authenticated and results_pose.pose_landmarks and results_pose.pose_landmarks.landmark[16] != None):
                    if(int(time.time()) - auth_time > time_interval):
                      authenticated = False
                      GPIO.output(9, GPIO.LOW)
                      queue.put(authenticated)
                      continue
                    pyautogui.moveTo(int((results_pose.pose_landmarks.landmark[16].x) * screen_width), int(results_pose.pose_landmarks.landmark[16].y * screen_height))
                    #mp_right_hand = mp.Image(image_format=mp.ImageFormat.SRGB, data=right_hand_roi)
                    if(right_hand_roi.shape[0]>0):
                          gesture = recognizer.recognize(mp_image).gestures
                          if(len(gesture) > 0):
                            hand_gesture = gesture[0][0].category_name
                            if(hand_gesture ==  "Open_Palm"):
                                pyautogui.mouseUp()
                            elif(hand_gesture == "Closed_Fist"):
                                pyautogui.mouseDown()
                            elif(hand_gesture == "Victory"):
                                if(int(time.time()) - spotify_delay > 5):
                                  pyautogui.press("k")
                                  spotify_playing = not spotify_playing
                                  print(spotify_playing)
                                  spotify_delay = int(time.time())
                            elif(hand_gesture == "Thumb_Up"):
                                if(int(time.time()) - snapshot_write_delay > 5):
                                  print("snapshot")
                                  cv2.imwrite("snapshots/" + str(time.time()) + ".jpg", image)
                                  pyautogui.press("f")
                                  snapshot_write_delay = int(time.time())
                            elif(hand_gesture == "Thumb_Down"):
                                if(int(time.time()) - snapshot_read_delay > 5):
                                  for filename in reversed(os.listdir("snapshots")):
                                    filepath = os.path.join("snapshots", filename)
                                    image = cv2.imread(filepath)
                                    cv2.namedWindow("Image", cv2.WND_PROP_FULLSCREEN)
                                    cv2.setWindowProperty("Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                                    if image is not None:
                                      print("snapshot_show")
                                      cv2.imshow("Image", image)
                                      cv2.waitKey(1000)
                                      time.sleep(2)
                                  cv2.destroyAllWindows()
                                  snapshot_read_delay = int(time.time())
                            elif(hand_gesture == "Pointing_Up" and spotify_playing):
                              if(int(time.time()) - spotify_delay > 5):
                                pyautogui.press("l")
                                spotify_delay = int(time.time())
            else:
              if(current_frontend_state == "user"):
                driver.maximize_window()
                driver.get('http://localhost:3000/')
                driver.fullscreen_window()
                current_frontend_state = "home"
                GPIO.output(9, GPIO.LOW)
                authenticated = False

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    recognizer.close()      
    cap.release()
    cv2.destroyAllWindows()

def main():
  parser = argparse.ArgumentParser(
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument(
      '--model',
      help='Name of gesture recognition model.',
      required=False,
      default='gesture_recognizer.task')
  parser.add_argument(
      '--numHands',
      help='Max number of hands that can be detected by the recognizer.',
      required=False,
      default=1)
  parser.add_argument(
      '--minHandDetectionConfidence',
      help='The minimum confidence score for hand detection to be considered '
           'successful.',
      required=False,
      default=0.5)
  parser.add_argument(
      '--minHandPresenceConfidence',
      help='The minimum confidence score of hand presence score in the hand '
           'landmark detection.',
      required=False,
      default=0.5)
  parser.add_argument(
      '--minTrackingConfidence',
      help='The minimum confidence score for the hand tracking to be '
           'considered successful.',
      required=False,
      default=0.5)
  # Finding the camera ID can be very reliant on platform-dependent methods.
  # One common approach is to use the fact that camera IDs are usually indexed sequentially by the OS, starting from 0.
  # Here, we use OpenCV and create a VideoCapture object for each potential ID with 'cap = cv2.VideoCapture(i)'.
  # If 'cap' is None or not 'cap.isOpened()', it indicates the camera ID is not available.
  parser.add_argument(
      '--cameraId', help='Id of camera.', required=False, default=0)
  parser.add_argument(
      '--frameWidth',
      help='Width of frame to capture from camera.',
      required=False,
      default=640)
  parser.add_argument(
      '--frameHeight',
      help='Height of frame to capture from camera.',
      required=False,
      default=480)
  args = parser.parse_args()
  while True:
    PIR = GPIO.input(11)
    if PIR == 1:
      run(args.model, int(args.numHands), args.minHandDetectionConfidence, args.minHandPresenceConfidence, args.minTrackingConfidence, int(args.cameraId), args.frameWidth, args.frameHeight)


if __name__ == '__main__':
  main()
