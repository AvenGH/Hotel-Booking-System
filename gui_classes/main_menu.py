import customtkinter as ctk
from .create_account_window import CreateAccountWindow
from .log_in_window import LoginWindow

# GUI Class for managing properties of main menu interface
class MainMenu:
    root = ''

    def __init__(self, root):
        self.root = root
        self.create_ui()

    # Creates user interface with all necessary elements
    def create_ui(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Defines space within which elements may be positioned
        self.frame = ctk.CTkFrame(master=self.root)
        self.frame.pack(pady=20, padx=60, fill="both", expand=True)

        # Sets the title of this application
        self.title = ctk.CTkLabel(master=self.frame, text="Hotel Booking System Application", font=("Arial", 24))
        self.title.pack(pady=12, padx=10)

        # Allows user to navigate to create account window
        self.create_account_button = ctk.CTkButton(master=self.frame, text="Create Account", command=self.create_account)
        self.create_account_button.pack(padx=20, pady=20)

        # Allows user to navigate to login window
        self.login_button = ctk.CTkButton(master=self.frame, text="Login", command=self.login)
        self.login_button.pack(padx=20, pady=20)
    
    # Will be executed once create account button is pressed
    def create_account(self):
        CreateAccountWindow(self.root)
        self.root.withdraw()

    # Will be executed once login button is pressed
    def login(self):
        LoginWindow(self.root)
        self.root.withdraw()

    



