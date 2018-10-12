from abc import ABC, abstractmethod
import pyrebase
import argparse
import smtplib
import sys
from twilio.rest import Client
import socket
import datetime


config = {
    "apiKey": "AIzaSyBNn3_RxQr_B2ZvsvxZuMRAuaSoI0__HUg",
    "authDomain": "xpensetracker1.firebaseapp.com",
    "databaseURL": "https://xpensetracker1.firebaseio.com",
    "projectId": "xpensetracker1",
    "storageBucket": "xpensetracker1.appspot.com",
    "messagingSenderId": "59552663723"
  };

# account_sid = 'AC29fbf392a271a38e6e3172bdef459cab'
# auth_token = '778cb9ee4aaa654a412c18552a11dd66'
# client = Client(account_sid, auth_token)

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()

class HelperBase():
    def __init__(self, para):
        self.para = para

    #helper function
    def responseHolderfun(self, actionOption, nameUser, user):
        responseHolder = input("Do you want to {} once more? Y/N ".format(actionOption))
        while True:
            if (responseHolder == ('Y' or 'y')):
                crud1 = CrudInAction("crud1")
                crud1.checkOptionEntered(actionOption, nameUser, user)
            else:
                break
        letUserIn(user)

    #helper function
    def openFile(self):
        f=open("data.txt", "r", encoding="utf-8")
        if f.mode=='r':
            contents = f.read()
            return contents

    #helper function
    def callForEmail(self):
        MY_ADDRESS = "mail.expenseTracker@gmail.com"
        PASSWORD = "test123*"
        email = input("Please enter your email address!\n")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(MY_ADDRESS, PASSWORD)

        msg = "Your expense report...\n" + self.openFile() + "\nThank you for using expenseTracker!!\n"
        server.sendmail(MY_ADDRESS, email, msg)
        server.quit()
        print("Email sent!! Please check your email address!!")


class CrudBase(ABC):
    def __init__(self, para):
        self.para = para

    def checkOptionEntered(self, para0, para1, para2):
        raise NotImplementedError("Subclass must implement this abstract method")

class CrudInAction(CrudBase):
    def __init__(self, f):
        super().__init__(f)

    def checkOptionEntered(self, actionOption, nameUser, user):

        if (actionOption == 'Add'):
            expenseDate = input("Enter Date): \n")
            expenseReason = input("Enter your expense : \n")
            expenseprice = input("Enter Price:  $ \n")
            expensenotes = input("Enter any notes: \n")

            data = {
                "Date": expenseDate,
                "ExpenseType": expenseReason,
                "ExpensePrice": expenseprice,
                "notesIfAny": expensenotes
            }
            db.child("users").child(nameUser).push(data)
            holder = HelperBase("holder")
            holder.responseHolderfun(actionOption, nameUser, user)

        if (actionOption == 'View'):

            file = open("data.txt", "w")
            all_user = db.child("users").child(nameUser).get()
            dictKey = all_user.val()

            for k, v in dictKey.items():
                for ke, va in v.items():
                    contentHolder = ( '\n{} : {}\n'.format(ke, va))
                    print(contentHolder)
                    file.write(contentHolder)
                lineDivider = ('------------------------')
                print(lineDivider)
                file.write(lineDivider)

            file.close()

            responseEmailHolder = input ("Would you like an email of your expenses: Y/N\n")
            if (responseEmailHolder == ('Y' or 'y')):

                emailCall = HelperBase("emailCall")
                emailCall.callForEmail()
            responseCall = HelperBase("responseCall")
            responseCall.responseHolderfun(actionOption, nameUser, user)

        if (actionOption == 'Update'):
            #db.child("users").child(nameUser).update({"ExpenseType": "carrot" })
            print("Still working on the functionality !!!")

        if (actionOption == 'Delete'):
            #db.child("users").child(nameUser).remove()
            print("Still working on the functionality !!!")

        if (actionOption == 'Logout'):
            print ("Bye....... see you soon! :) ")
            sys.exit()

        else:
            print("Retype your entry!!")
            letUserIn(user)

#Query to extract ExpensePrice
        # snapshot = all_user.order_by_key().get()
        # for user in snapshot:
        #     print (user.val()) #object not iterable

#bridge function
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
        crud = CrudInAction("crud")
        crud.checkOptionEntered(actionOption,nameUser, user)

# def smsPhone(): #Only my number works for Twilio Free Trial sorry!!
#     # ipLocation = socket.gethostbyname(socket.gethostname())
#     # currentDT = datetime.datetime.now()
#     # datePrint = print(currentDT.strftime("%Y-%m-%d %H:%M:%S"))
#     # ipPrint = print(ipLocation)
#     message = client.messages \
#         .create(
#         body=("Logged in from"),
#         from_='+12019184251',
#         menuPhone = MenuHandlerBase("menuPhone")
#         menuPhone.phoneEntry()
#
#     )
#     print(message.sid)

class MenuAction(ABC):
    def __init__(self, par):
        self.par = par

    @abstractmethod
    def emailEntry(self):
        raise NotImplementedError("Subclass must implement this abstract method")

    @abstractmethod
    def passwordEntry(self):
        raise NotImplementedError("Subclass must implement this abstract method")

    @abstractmethod
    def phoneEntry(self):
        raise NotImplementedError("Subclass must implement this abstract method")

    @abstractmethod
    def menuHandler(self, f):
        raise NotImplementedError("Subclass must implement this abstract method")


class MenuHandlerBase(MenuAction):
    def __init__(self, f):
        super().__init__(f)

    def emailEntry(self):
        email = input("Please enter your email: \n")
        return email

    def passwordEntry(self):
        password = input("Please enter your password: \n")
        return password

    def phoneEntry(self):
        phoneNum = input("Please enter your phone: \n")
        return phoneNum

    def menuHandler(self, optionsList):

        optionsHolder = optionsList.pop(0)
        if (optionsHolder == "Login"):
            email = self.emailEntry()
            password = self.passwordEntry()
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                print ('Login Successful')
                # message = client.messages \
                #     .create(
                #     body="Login Successful.",
                #     from_='+12019184251',
                #     to=self.phoneEntry()
                # )
                # print(message.sid)
                letUserIn(user)
                sys.exit()
            except:
                print ('Login Unsuccessful, please check your credentials=!')

        elif (optionsHolder == "SignUp"):
            email = self.emailEntry()
            password = self.passwordEntry()
            try:
                print ("Creating a new account!")
                user = auth.create_user_with_email_and_password(email, password)
                print ('Account Created')

                # message = client.messages \
                #     .create(
                #     body="Login Successful.",
                #     from_='+12019184251',
                #     to=self.phoneEntry()
                # )
                # print(message.sid)

                letUserIn(user)
            except:
                print ('User already exists, please check your credentials!')

        elif (optionsHolder == "ForgotPassword"):
            try:
                email = input("Please enter your email \n")
                user = auth.send_password_reset_email(email)
                print("Check your email!")
            except:
                print('Wrong email, please check your credentials!')


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', dest="optionsAvail", nargs='*',
                        help='''Options available: 1.) Login 2.) SignUp
                            3.) Forgot Password''')

    args = parser.parse_args()
    optionsList = args.optionsAvail
    menu = MenuHandlerBase("menu")
    menu.menuHandler(optionsList)
