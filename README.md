# User Registration
A Django project which protected by Email and mobile OTP verification for the login process...

## Instructions
In order to setup twilio to send a message to the user, follow the instructions at [this gist](https://gist.github.com/mukeshgurpude/9f42b22463c014cc109ea6f747926006)

### How to run locally
- Download this repository as [zip](https://github.com/Incognitosin01/User_registration/archive/refs/heads/main.zip) or clone it using the github repository link https://github.com/Incognitosin01/User_registration.git

- `cd` to the working directory
- Download required modules
  ```bash
  pip install -r requirements.txt
  ```
- Setup database and static files using following commands
 ```bash
 cd Internship_task
 python3 manage.py makemigrations
 python3 manage.py migrate
 python3 manage.py collectstatic
 ```
- Setup twilio as per [instructions](https://gist.github.com/mukeshgurpude/9f42b22463c014cc109ea6f747926006)

- Just run the development server
 ```bash
 python3 manage.py runserver
 ```
 Open http://localhost:8000 in your browser to view the app
