import pyrebase
import tkinter as tk
from email_validator import validate_email
import string
import util.generate_random_id as generate_random_id
from api_classes.customer_api import CustomerAPI

# Sets up the initial firebase configurations
firebaseConfig = {
    'apiKey': "AIzaSyBkEqgJdF-QwWboEuyRVhV0sYQp9gjnzE4",
    'authDomain': "authdemo-5ce04.firebaseapp.com",
    'databaseURL': "https://console.firebase.google.com/u/0/project/authdemo-5ce04/database/authdemo-5ce04-default-rtdb/data/~2F",
    'projectId': "authdemo-5ce04",
    'storageBucket': "authdemo-5ce04.firebasestorage.app",
    'messagingSenderId': "453994953985",
    'appId': "1:453994953985:web:54469abb7d879736686f00"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

CustomerAPI.connect_db()

class AccountSystem:

    # Checks if any fields are left blank
    @staticmethod
    def fields_blank(name, email, password, conf_password):
        return name.get() == "" or email.get() == "" or password.get() == "" or conf_password.get() == ""
    
    
    # Checks if both entered passwords match
    @staticmethod
    def validate_passwords(password, conf_password):
        if password.get() != conf_password.get():
            tk.messagebox.showerror("Error", "Passwords do not match.")
            return
        return True
    

    # Validates the email address
    @staticmethod
    def email_valid(email):
        try:
            emailinfo = validate_email(email.get(), check_deliverability=False)
            email = emailinfo.normalized
            return True
        except Exception as e:
            tk.messagebox.showerror("Error", f"Email is not valid: {e}")
            return
    

    # Sends a password reset link to the given email address
    @classmethod
    def reset_password(cls, email):
        if not cls.email_valid(email):
            return
        try:
            auth.send_password_reset_email(email.get())
            #tk.messagebox.showinfo("Reset Password", "A password reset link email has been sent to your inbox!")
            tk.messagebox.askyesno("Question","Are you sure you would like to reset your password?")
        except:
            tk.messagebox.showerror("Error", "Something went wrong. Please try again later...")


    # Deletes a user account
    @classmethod
    def delete_account(cls, user):
        try:
            auth.delete_user_account(user["idToken"])
            tk.messagebox.showinfo("Account Deletion", f"Your account has successfully been deleted.")
            return True
        except:
            tk.messagebox.showerror("Error", "Something went wrong. Please try again later...")

    
    # Checks if a password is secure
    @staticmethod
    def password_is_secure(pwd):
        if len(pwd) < 8:
            tk.messagebox.showerror("Error", "Password should be minimum 8 characters long.")
            return

        # Fetches each of the different character types and stores them in separate identifiers
        upper = string.ascii_uppercase
        lower = string.ascii_lowercase
        digits = string.digits
        special = string.punctuation

        # Status variables which indicate the presence of each character type
        has_upper = False
        has_lower = False
        has_digit = False
        has_special = False

        # Loops through each character of the password and updates the status variables
        for i in pwd:
            if i in upper:
                has_upper = True
            elif i in lower:
                has_lower = True
            elif i in digits:
                has_digit = True
            elif i in special:
                has_special = True

        # Checks if the password consists of all the different character types
        if not (has_upper and has_lower and has_digit and has_special):
            tk.messagebox.showerror("Error", "Password should contain a mix of upper/lower case letters, digits and special characters.")
            return
        
        return True


    # Function that authenticates login details
    @staticmethod
    def login(email, password):
        try:
            auth.sign_in_with_email_and_password(email.get(), password.get())
            user = CustomerAPI.fetch_customer_by_email(email.get())
            return user
        except Exception as e:
            tk.messagebox.showerror("Error", "Invalid email or password.")
            print(e)
        return

    # Function that authenticates registration details
    @classmethod
    def sign_up(cls, name, email, password, conf_password):
        if not cls.validate_passwords(password, conf_password):
            return
        
        if not cls.password_is_secure(password.get()):
            return
        
        if not cls.email_valid(email):
            return
        
        # Attempts to create an account with the email and password
        try:
            user = auth.create_user_with_email_and_password(email.get(), password.get())
            auth.send_email_verification(user["idToken"])
        except:
            tk.messagebox.showerror("Error", "Email already exists.")
        else:
            userid = int(generate_random_id.generate_user_id()[1:])
            CustomerAPI.add_customer(userid, name.get(), email.get()) # Adds the customer record to the database
            return True




