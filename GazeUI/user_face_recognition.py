import face_recognition
import json
import cv2
import requests
from dotenv import load_dotenv
import os
load_dotenv()

WebAppIP = os.getenv('WEBAPP_IP')

def user_recognition(image_cv2):
    #with open(file) as fp:
    #    people = json.load(fp)
    return_val = {
        "success": -1
    }
    
    people = requests.get("http://" + WebAppIP + "/get_face_patterns_api/2")
    people_json = people.json()["data"]
    #print(people_json)
    
    # Convert BGR image to RGB
    rgb_image = cv2.cvtColor(image_cv2, cv2.COLOR_BGR2RGB)
    
    cpm_img_encodings = face_recognition.face_encodings(rgb_image)
    for encoding in cpm_img_encodings:
        for person in people_json:
            #person_json = json.loads(person)
            if face_recognition.compare_faces([json.loads(person["face_pattern"])], encoding)[0]:
                return_val["success"] = 1
                return_val["username"] = person["username"]
                return_val["uid"] = person["userid"]
                return return_val
    
    return return_val
