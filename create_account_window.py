import customtkinter as ctk
from account_system import AccountSystem
import tkinter as tk
from PIL import Image


# GUI Class for managing properties of create account interface
class CreateAccountWindow:
    def __init__(self, root, dimensions="750x525"):
        self.root = root
        self.dimensions = dimensions
        self.create_ui()
        self.register_window.protocol("WM_DELETE_WINDOW", self.on_close)

    # Executed when close button is pressed on right hand corner
    def on_close(self):
        self.register_window.destroy()
        self.root.deiconify()

    # Creates user interface with all necessary elements
    def create_ui(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Loads icons for show/hide password
        self.show_password_image = ctk.CTkImage(dark_image = Image.open("C:\\Users\\avnik\\Documents\\python\\Projects\\Hotel Reservation NEA Project\\images\\show_password.jpg"), size=(25, 25))
        self.hide_password_image = ctk.CTkImage(dark_image = Image.open("C:\\Users\\avnik\\Documents\\python\\Projects\\Hotel Reservation NEA Project\\images\\hide_password.jpg"), size=(25, 25))

        # Creates a top level (derived) window from the main menu (parent) window
        self.register_window = ctk.CTkToplevel(self.root)
        self.register_window.geometry(self.dimensions)
        self.register_window.title("Hotel Booking App")

        # Defines space within which elements may be positioned
        self.frame = ctk.CTkFrame(master=self.register_window)
        self.frame.pack(pady=20, padx=60, fill="both", expand=True)

        # Creates a title positioned at the top of the screen
        self.title = ctk.CTkLabel(master=self.frame, text="Please create an account:", font=("Arial", 24))
        self.title.pack(pady=12, padx=10)

        # Field that takes in the user's name
        self.name_label = ctk.CTkLabel(master=self.frame, text="Name", font=("Arial", 18))
        self.name_label.place(x=100, y=100)

        self.name = ctk.CTkEntry(master=self.frame, width=240, height=35, font=("Arial", 16), placeholder_text="Enter your name...")
        self.name.place(x=275, y=100)

        # Field that takes in the user's email address
        self.email_label = ctk.CTkLabel(master=self.frame, text="Email", font=("Arial", 18))
        self.email_label.place(x=100, y=175)

        self.email = ctk.CTkEntry(master=self.frame, width=240, height=35, font=("Arial", 16), placeholder_text="Enter email...")
        self.email.place(x=275, y=175)

        # Field that takes in the user's password
        self.password_label = ctk.CTkLabel(master=self.frame, text="Password", font=("Arial", 18))
        self.password_label.place(x=100, y=250)

        self.password = ctk.CTkEntry(master=self.frame, width=240, height=35, font=("Arial", 16), placeholder_text="Enter a password...", show="*")
        self.password.place(x=275, y=250)

        self.show_password_icon = ctk.CTkButton(master=self.frame, text="", command=self.show_password, image=self.show_password_image, font=('Arial', 24), width=35, height=35)
        self.show_password_icon.place(x=515, y=250)

        #Field that takes in the user's confirmed password
        self.conf_password_label = ctk.CTkLabel(master=self.frame, text="Confirm Password", font=("Arial", 18))
        self.conf_password_label.place(x=100, y=325)

        self.conf_password = ctk.CTkEntry(master=self.frame, width=240, height=35, font=("Arial", 16), placeholder_text="Confirm your password...", show="*")
        self.conf_password.place(x=275, y=325)

        self.show_conf_password_icon = ctk.CTkButton(master=self.frame, text="", command=self.show_conf_password, image=self.show_password_image, font=('Arial', 24), width=35, height=35)
        self.show_conf_password_icon.place(x=515, y=325)
        
        # Field that allows user to submit all their account registration details
        self.submit_button = ctk.CTkButton(master=self.frame, text="Create Account", command=self.submit)
        self.submit_button.place(x=200, y=400)

    # Allows user to show/hide their password
    def show_password(self):
        if self.password.cget('show') == "*":
            self.password.configure(show='') # Shows the actual password
            self.show_password_icon.configure(image=self.hide_password_image) # Updates the icon
        else:
            self.password.configure(show='*') # Shows the hidden password
            self.show_password_icon.configure(image=self.show_password_image) # Updates the icon

    # Allows user to show/hide their confirm password
    def show_conf_password(self):
        if self.conf_password.cget('show') == "*":
            self.conf_password.configure(show='') # Shows the actual password
            self.show_conf_password_icon.configure(image=self.hide_password_image) # Updates the icon
        else:
            self.conf_password.configure(show='*')
            self.show_conf_password_icon.configure(image=self.show_password_image)

    # Will be executed once Create Account button is pressed
    def submit(self):
        # Checks for any blank fields
        if AccountSystem.fields_blank(self.name, self.email, self.password, self.conf_password):
            tk.messagebox.showerror("Error", "All fields are required!")
            return
        
        # Checks if the sign up was successful
        signed_up = AccountSystem.sign_up(self.name, self.email, self.password, self.conf_password)
        if signed_up:
            tk.messagebox.showinfo("Account creation successful", "Successfully created an account!")
            # Closes the register window and loads back the main menu
            self.register_window.destroy()
            self.root.deiconify()


# Allows file to be run independent of the main menu
if __name__ == '__main__':
    root = ctk.CTk()
    app = CreateAccountWindow(root)
    root.mainloop()

