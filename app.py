import pyrebase
import argparse
import smtplib

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

def openFile():
    f=open("data.txt", "r", encoding="utf-8")
    if f.mode=='r':
        contents = f.read()
        return contents

def responseHolderfun(actionOption, nameUser, user):
    responseHolder = input("Do you want to {} once more? Y/N ".format(actionOption))
    while True:
        if (responseHolder == ('Y' or 'y')):
            checkOptionEntered(actionOption, nameUser, user)
        else:
            break
    letUserIn(user)

def checkOptionEntered(actionOption,nameUser, user):

    if (actionOption == 'Add'):
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
        db.child("users").child(nameUser).push(data)

        responseHolderfun(actionOption, nameUser, user)

    if (actionOption == 'View'):

        fruits = []
        file = open("data.txt", "w")
        all_user = db.child("users").child(nameUser).get()
        # print(all_user.key())
        dictKey = all_user.val()
        #
        print(dictKey) #prints out the whole key value dict
        for k, v in dictKey.items():
            #print ('  {}'.format( v))
            for ke, va in v.items():
                contentHolder = ( '\n{} : {}\n'.format(ke, va))
                fruits.append(va)
                print(contentHolder)
                file.write(contentHolder)
            lineDivider = ('------------------------')
            print(lineDivider)
            file.write(lineDivider)

        file.close()


        responseEmailHolder = input ("Would you like an email of your expenses: Y/N\n")
        if (responseEmailHolder == ('Y' or 'y')):
            MY_ADDRESS = "mail.expenseTracker@gmail.com"
            PASSWORD = "test123*"
            email = input ("Please enter your email address!\n")
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(MY_ADDRESS, PASSWORD)

            msg = "Your expense report...\n" + openFile() + "\nThank you for using expenseTracker!!\n"
            server.sendmail(MY_ADDRESS, email, msg)
            server.quit()
            print("Email sent!! Please check your email address!!")
        responseHolderfun(actionOption, nameUser, user)

    if (actionOption == 'Update'):
        #db.child("users").child(nameUser).update({"ExpenseType": "carrot" })
        print("Still working on the functionality !!!")

    if (actionOption == 'Delete'):
        #db.child("users").child(nameUser).remove()
        print("Still working on the functionality !!!")

    if (actionOption == 'Logout'):
        print ("Bye....... see you soon! :) ")



#Query to extract ExpensePrice
        # snapshot = all_user.order_by_key().get()
        # for user in snapshot:
        #     print (user.val()) #object not iterable


def letUserIn(user):
    if user:
        value = auth.get_account_info(user['idToken'])
        temp = value['users'][0]['email']
        tmp = temp.split('@')
        nameUser = tmp[0]
        print("Hello {}".format(nameUser))

        print ("""1.) Add your expenses: Add 2.) Delete your expenses: Delete
                  3.) Update your expenses: Update 4.) View your overall expenses: View 5.) Exit application: Logout """)
        actionOption = input("Enter your choice of entry: ")
        checkOptionEntered(actionOption,nameUser, user)


def menuHandler(optionsList):
    optionsHolder = optionsList.pop(0)

    def emailEntry():
        email = input("Please enter your email: \n")
        return email

    def passwordEntry():
        password = input("Please enter your password: \n")
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

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', dest="optionsAvail", nargs='*',
                        help='''Options available: 1.) Login 2.) SignUp
                            3.) Forgot Password''')

    args = parser.parse_args()
    optionsList = args.optionsAvail
    menuHandler(optionsList)
