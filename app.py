import pyrebase
import argparse
from random import randint

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
db = firebase.database()

def checkOptionEntered(actionOption,nameUser):

    if (actionOption == 'Add'):
        print(""" School, DailyExpenses, Food, Party, MISC """)
        valueKind = input("Please enter your expense kind \n")
        expenseDate = input("Enter Date: \n")
        expenseReason = input("Enter your expense: \n")
        expenseprice = input("Enter Price: $ \n")
        expensenotes = input("Enter any notes: \n")

        data = {
            "Date": expenseDate,
            "ExpenseType": expenseReason,
            "ExpensePrice": expenseprice,
            "notesIfAny": expensenotes
        }
        db.child("users").child(nameUser).child(randomToken).child(valueKind).set(data)

    if (actionOption == 'View'):
        # all_user = db.child("users").child(nameUser).child("randomToken").child("valueKind").get()
        # for user in all_user.each():
        #     print(all_user.key())

        all_user = db.child("users").child(nameUser).child("536").get()
        print(all_user.key())
        print(all_user.val())

        #
        # for userid in all_user.shallow().get().each():
        #     expenseDB = all_user.child(userid).child("536").get()
        #     print(expenseDB.val())




def menuHandler(optionsList):
    optionsHolder = optionsList.pop(0)

    def emailEntry():
        email = input("Please enter your email: \n")
        return email

    def passwordEntry():
        password = input("Please enter your password: \n")
        return password


    def letUserIn(user):
        if user:
            value = auth.get_account_info(user['idToken'])
            temp = value['users'][0]['email']
            tmp = temp.split('@')
            nameUser = tmp[0]
            print("Hello {}".format(nameUser))

            print ("""1.) Add your expenses: Add 2.) Delete your expenses: Delete
                      3.) Update your expenses: Update 4.) View your overall expenses: View """)
            actionOption = input("Enter your choice of entry: ")
            checkOptionEntered(actionOption,nameUser)


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

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', dest="optionsAvail", nargs='*',
                        help='''Options available: 1.) Login 2.) SignUp
                            3.) Forgot Password''')

    args = parser.parse_args()
    optionsList = args.optionsAvail
    menuHandler(optionsList)
