import face_recognition
import json
import cv2
import requests
from dotenv import load_dotenv, find_dotenv
import os
dotenv_path = find_dotenv('../.env')
load_dotenv(dotenv_path)

webAppIP = os.getenv('WEBAPP_IP')
webAppPort = os.getenv("WEBAPP_PORT")

def user_recognition(image_cv2):
    return_val = {
        "success": -1
    }
    
    people = requests.get("http://" + webAppIP + ":" + webAppPort + "/get_face_patterns_api/2")
    people_json = people.json()["data"]
    
    # Convert BGR image to RGB
    rgb_image = cv2.cvtColor(image_cv2, cv2.COLOR_BGR2RGB)
    
    cpm_img_encodings = face_recognition.face_encodings(rgb_image)
    for encoding in cpm_img_encodings:
        for person in people_json:
            if face_recognition.compare_faces([json.loads(person["face_pattern"])], encoding)[0]:
                return_val["success"] = 1
                return_val["username"] = person["username"]
                return_val["uid"] = person["userid"]
                return return_val
    
    return return_val
