import cv2
import mediapipe as mp
import pyautogui

# Initialize mediapipe hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)

# Initialize screen size
screen_width, screen_height = pyautogui.size()

def hand_mouse(frame):
    # Convert the image from BGR to GREYSCALE for faster processing
    grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    #process to detect hands in frame
    results = hands.process(grey_frame)

    #check if hands are detected
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            palm = (hand_landmarks.landmark[0].x, hand_landmarks.landmark[0].y)
            print("palm")
            print(palm)
            try:
                pyautogui.moveTo(palm[0]*screen_width, palm[1]*screen_height)
            except:
                print("failed")
            