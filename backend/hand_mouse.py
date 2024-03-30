import cv2
import mediapipe as mp
import pyautogui

# Initialize mediapipe hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)

# Initialize screen size
screen_width, screen_height = pyautogui.size()

def hand_mouse(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    #process to detect hands in frame
    results = hands.process(rgb_frame)
    mouse_posi = "up"

    #check if hands are detected
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            palm = (hand_landmarks.landmark[0].x, hand_landmarks.landmark[0].y)
            index_tip = (hand_landmarks.landmark[8].x, hand_landmarks.landmark[8].y)
            thumb_tip = (hand_landmarks.landmark[4].x, hand_landmarks.landmark[4].y)
            tip_distance = ((index_tip[0] - thumb_tip[0]) ** 2) - ((index_tip[1] - thumb_tip[1]) ** 2)
            print(tip_distance)
            try:
                pyautogui.dragTo(palm[0]*screen_width, palm[1]*screen_height)
                if(abs(tip_distance)<0.005 and mouse_posi != "down"):
                    print("down")
                    pyautogui.mouseDown()
                    mouse_posi = "down"
                else:
                    print("up")
                    pyautogui.mouseUp()
                    mouse_posi = "up"
            except:
                print("failed")
            