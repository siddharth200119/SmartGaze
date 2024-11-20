# Smart Gaze
This project is about creating a Smart Mirror to add functionality to an everyday mirror by adding useful widgets such as Calender, News, To-Do List, Weather and Time along with a smart alarm system and Spotify Integration.


## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Hardware Requirements](#hardware-requirements)
4. [Software Requirements](#software-requirements)
5. [Setup Instructions](#setup-instructions)
6. [Configuration](#configuration)
7. [Usage](#usage)
8. [Troubleshooting](#troubleshooting)
9. [Contributing](#contributing)
10. [License](#license)



## Introduction
The Smart Gaze project aims to create an interactive mirror that provides real-time information. The mirror uses a Raspberry Pi to run a web-based interface that displays various widgets, gesture recognition, and smart alarm system.


## Hardware Requirements

1. Raspberry Pi 4 4GB
2. PIR sensor
3. Relay
4. LED Strip
5. HDMI based display
6. Two-way mirror
7. USB camera


## Software Requirements

1. Raspberry Pi OS(64-bit) based on Debian Bookworm
2. Python 3.11
3. NodeJS 18+


## Setup Instructions

>**Please check the DATABASE settings in web_project/settings.py**
>**It should be set to django.db.backends.mysql with appropriate DB CREDENTIALS**

### Setup for the Web App
1. Clone the git repository using the below command in the terminal,
```     
        git clone https://github.com/siddharth200119/SmartGaze.git
```
2. Navigate to the web app directory using the below command,
```
        cd "SmartGaze\Web App"	
```			
3. Create a virtual environment using the command,
```
        virtualenv venv
```	
-   *'venv' is the name of the virtual environment, you can keep whatever you want here*
4. Activate the virtual environment by the command,
```		
        venv\Scripts\activate
```

5. Install the necessary dependencies by reading & installing "requirements.txt" by the command,
```
        pip install -r requirements.txt
```

6.  To setup your database run the below commands in the same order,
```
		python manage.py makemigrations 
```
 >This will make those files which are needed to create your DB
```
		python manage.py migrate 	  		
```
>This will actually create all the tables in your DB and then your DB will we ready.

7. Create a superuser for the Django Admin by running the command, then you need to enter the username, email, password. 
*This will create a administrator for this web app.*
```
        python manage.py createsuperuser
```
>***REMEMBER THESE CREDENTIALS AS IT WILL BE USEFUL WHEN LOGGING INTO DJANGO ADMIN***

8.  Now you are ready to start your server using the below command,
```
		python manage.py runserver 0.0.0.0:8000	
```

9. Check the IP of your PC and set it in the env.txt & set the WEBAPP_PORT to 8000 

10. Copy your Spotify Client ID and Client Secret from the Spotify Developer Portal and paste it in the env.txt 

11. Go to this URL on your default browser & START USING THE WEB APP, on your localhost server.
***http://localhost:8000***
