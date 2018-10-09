import pyrebase
import argparse

config = {
    "apiKey": "AIzaSyBNn3_RxQr_B2ZvsvxZuMRAuaSoI0__HUg",
    "authDomain": "xpensetracker1.firebaseapp.com",
    "databaseURL": "https://xpensetracker1.firebaseio.com",
    "projectId": "xpensetracker1",
    "storageBucket": "xpensetracker1.appspot.com",
    "messagingSenderId": "59552663723"
  };

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

parser = argparse.ArgumentParser()
parser.add_argument('-p', dest = "optionsAvail", nargs = '*',
                            help='''Options available: 1.) Login 2.) SignUp
                        3.) Forgot Password''')

args = parser.parse_args()
optionsList = args.optionsAvail
optionsHolder = optionsList.pop(0)

def emailEntry():
    email = input("Please enter your email \n")
    return email

def passwordEntry():
    password = input("Please enter your password \n")
    return password


if (optionsHolder == "Login"):
    email = emailEntry()
    password = passwordEntry()
    user = auth.sign_in_with_email_and_password(email, password)
    letUserIn(user)

elif (optionsHolder == "SignUp"):
    email = emailEntry()
    password = passwordEntry()
    user = auth.create_user_with_email_and_password(email, password)
    print('Please verify your email & then get started by running python3 app.py Login')

elif (optionsHolder == "ForgotPassword"):
    email = input("Please enter your email \n")
    user = auth.send_password_reset_email(email)
    print("Check your email!")

