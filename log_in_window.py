import tkinter as tk
import customtkinter as ctk
from PIL import Image
from account_system import AccountSystem
from .dashboard import Dashboard

# GUI Class for managing properties of login interface
class LoginWindow:
    def __init__(self, root, dimensions="700x425"):
        self.root = root
        self.dimensions = dimensions
        self.create_ui()
        self.login_window.protocol("WM_DELETE_WINDOW", self.on_close)

    # Executed when close button is pressed on right hand corner
    def on_close(self):
        self.login_window.destroy()
        self.root.deiconify()

    # Creates user interface with all necessary elements
    def create_ui(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Creates a top level (derived) window from the main menu (parent) window
        self.login_window = ctk.CTkToplevel(self.root)
        self.login_window.geometry(self.dimensions)
        self.login_window.title("Hotel Booking App")

        self.show_password_image = ctk.CTkImage(dark_image = Image.open("C:\\Users\\avnik\\Documents\\python\\Projects\\Hotel Reservation NEA Project\\images\\show_password.jpg"), size=(25, 25))
        self.hide_password_image = ctk.CTkImage(dark_image = Image.open("C:\\Users\\avnik\\Documents\\python\\Projects\\Hotel Reservation NEA Project\\images\\hide_password.jpg"), size=(25, 25))

        # Defines space within which elements may be positioned
        self.frame = ctk.CTkFrame(master=self.login_window)
        self.frame.pack(pady=20, padx=60, fill="both", expand=True)
        
        # Creates a title positioned at the top of the screen
        self.title = ctk.CTkLabel(master=self.frame, text="Please log in to your account:", font=("Arial", 24))
        self.title.pack(pady=12, padx=10)

        # Field that takes in the user's email
        self.email_label = ctk.CTkLabel(master=self.frame, text="Email", font=("Arial", 18))
        self.email_label.place(x=100, y=100)

        self.email = ctk.CTkEntry(master=self.frame, width=240, height=35, font=("Arial", 16), placeholder_text="Please enter your email...")
        self.email.place(x=275, y=100)

        # Field that takes in the user's password
        self.password_label = ctk.CTkLabel(master=self.frame, text="Password", font=("Arial", 18))
        self.password_label.place(x=100, y=175)

        self.password = ctk.CTkEntry(master=self.frame, width=240, height=35, font=("Arial", 16), show="*", placeholder_text="Please enter your password...")
        self.password.place(x=275, y=175)

        self.show_password_icon = ctk.CTkButton(master=self.frame, text="", command=self.show_password, image=self.show_password_image, font=('Arial', 24), width=35, height=35)
        self.show_password_icon.place(x=515, y=175)

        # Field that allows user to submit all their login details
        self.submit_button = ctk.CTkButton(master=self.frame, text="Log in to Account", command=lambda: self.submit_booking())
        self.submit_button.place(x=200, y=250)

        self.reset_password_link = ctk.CTkButton(master=self.frame, text="Forgot Password?", command=self.reset_password)
        self.reset_password_link.place(x=200, y=325)

    # Allows user to show/hide their password
    def show_password(self):
        if self.password.cget('show') == "*":
            self.password.configure(show='')
            self.show_password_icon.configure(image=self.hide_password_image)
        else:
            self.password.configure(show='*')
            self.show_password_icon.configure(image=self.show_password_image)

    # Will be executed once Reset Password Button is pressed
    def reset_password(self):
        AccountSystem.reset_password(self.email)

    # Will be executed once Create Account button is pressed
    def submit_booking(self):
        # Checks for any blank fields
        if self.email.get()=="" or self.password.get()=="":
            tk.messagebox.showerror("Error", "All fields are required!")
            return

        user = AccountSystem.login(self.email, self.password)
        if user:
            self.login_window.destroy()
            self.dashboard = Dashboard(self.root, user)
            

# Allows file to be run independent of the main menu
if __name__ == "__main__":
    root = ctk.CTk()
    app = LoginWindow(root)
    root.mainloop()
    


    