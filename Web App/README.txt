======================================================INSTRUCTIONS TO START THE DJANGO WEB APP on WINDOWS====================================================

1. Create a virtual environment using the command,
		"virtualenv venv"
	here, 'venv' is the name of the virtual environment, you can keep whatever you want here

2. Activate the virtual environment by the command,
		"venv\Scripts\activate"

3. Install the necessary dependencies by reading & installing "requirements.txt" by the command,
		"pip install -r requirements.txt"

4. Create a superuser for the Django Admin by running the command,
		"python manage.py createsuperuser"
	REMEMBER THESE CREDENTIALS WILL BE USEFUL TO LOGIN INTO DJANGO ADMIN

5. To start the server follow the below commands in the mentioned order,
		"python manage.py makemigrations" ,
		"python manage.py migrate" ,
		"python manage.py runserver localhost:8000"

6. Go to the the URL mentioned in the output on the terminal i.e., 'localhost:8000', on your default browser & START USING THE WEB APP, on your localhost server.


==================================================CHANGED TO BE MADE IN THE CODE BEFORE STARTING THE WEB APP================================================

-------------------------In the "views.py" file---------------------
1. Update the client_ID on lines 245, 303, 319

2. Update the client_secret on lines 246, 320

-------------------------In the "settings.py" file---------------------

1. Set the details of your MySQL such as, name of your DB, DB user & password in the DATABASES section (line 79 onwards)
