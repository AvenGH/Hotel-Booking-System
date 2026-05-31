import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from .booking_window_new import BookingWindow
from PIL import Image
from api_classes.booking_api import BookingAPI
from api_classes.room_api import RoomAPI
from booking_system_new import BookingSystem
#from ttkbootstrap.constants import *


class Dashboard:
    def __init__(self, root, user, dimensions="750x500"):
        self.root = root
        self.dimensions = dimensions
        self.hotel_options = ["Jet2Hotels", "PyTrustHotels", "JoyFunHotels"]
        self.user = user
        self.data=[]

        self.logout_image = ctk.CTkImage(dark_image = Image.open("images\\logout2.jpg"), size=(25, 25))
        self.bookings_image = ctk.CTkImage(dark_image = Image.open("images\\bookings_icon.png"), size=(35, 25))
        self.create_ui()
        self.dashboard.protocol("WM_DELETE_WINDOW", self.on_close)


    # Executed when close button is pressed on right hand corner
    def on_close(self):
        self.dashboard.destroy()
        self.root.deiconify()


    def create_ui(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        #style = Style(theme="darkly")
        #style.configure("Treeview", font=("Arial", 12))
        #style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

        style = ttk.Style()
        style.theme_use("clam")

        bg = "#2b2b2b"
        fg = "white"
        select = "#3a7ebf"

        style.configure(
            "Treeview",
            background=bg,
            foreground=fg,
            fieldbackground=bg,
            font=("Arial", 12),
        )

        style.configure(
            "Treeview.Heading",
            background="#1f1f1f",
            foreground="white",
            font=("Arial", 12, "bold")
        )

        style.map(
            "Treeview.Heading",
            background=[("active", "#1f1f1f")],
            foreground=[("active", "white")]
        )

        self.dashboard = ctk.CTkToplevel(self.root)
        self.dashboard.geometry(self.dimensions)
        self.dashboard.title("Dashboard")

        # Defines space within which elements may be positioned
        self.dashboard_frame = ctk.CTkFrame(master=self.dashboard)
        self.dashboard_frame.pack(pady=20, padx=60, fill="both", expand=True)

        # Creates a title positioned at the top of the screen
        self.title = ctk.CTkLabel(master=self.dashboard_frame, text="Welcome! Please choose a hotel:", font=("Arial", 24))
        self.title.pack(pady=12, padx=10)

        self.logout_button = ctk.CTkButton(master=self.dashboard_frame, text="", image=self.logout_image, width=40, height=40, command=self.on_close)
        self.logout_button.place(x=50, y=50)

        self.bookings_button = ctk.CTkButton(master=self.dashboard_frame, text="", image=self.bookings_image, width=40, height=40, command=self.load_bookings)
        self.bookings_button.place(x=525, y=50)

        self.hotel = ctk.CTkComboBox(master=self.dashboard_frame, values=self.hotel_options, width=240, height=35, font=("Arial", 16), state="readonly")
        self.hotel.set("Select Hotel")
        self.hotel.pack(pady=12, padx=10)

        # Field that allows user to submit all their account registration details
        self.submit_button = ctk.CTkButton(master=self.dashboard_frame, text="Book Room", command=self.submit)
        self.submit_button.pack(pady=12, padx=10)

        self.modify_button = ctk.CTkButton(master=self.dashboard_frame, text="Modify Booking", command=self.modify)
        self.modify_button.pack(pady=12, padx=10)

        self.cancel_button = ctk.CTkButton(master=self.dashboard_frame, text="Cancel Booking", fg_color="red", command=self.cancel)
        self.cancel_button.pack(pady=12)

        self.bookings_frame = ctk.CTkScrollableFrame(master=self.dashboard, width=630, height=460) 

        self.back_button = ctk.CTkButton(master=self.bookings_frame, text="", image=self.logout_image, width=40, height=40, command=self.close_bookings_window)
        self.back_button.place(x=1, y=1)

        self.title = ctk.CTkLabel(master=self.bookings_frame, text="Your Reservations:", font=("Arial", 24))
        self.title.pack(pady=10)


        self.tree = ttk.Treeview(
            master=self.bookings_frame, 
            columns=("ID", "Date", "Check-In", "Check-Out", "Guests", "Total Price", "Room No", "Category", "Status"),
            show="headings", height=30
        )

        self.tree.heading("ID", text="ID", anchor="center")
        self.tree.heading("Date", text="Date", anchor="center")
        self.tree.heading("Check-In", text="Check-In", anchor="center")
        self.tree.heading("Check-Out", text="Check-Out", anchor="center")
        self.tree.heading("Guests", text="Guests", anchor="center")
        self.tree.heading("Total Price", text="Total Price", anchor="center")
        self.tree.heading("Room No", text="Room No", anchor="center")
        self.tree.heading("Category", text="Category", anchor="center")
        self.tree.heading("Status", text="Status", anchor="center")

        self.tree.column("ID", anchor="center", width=100)
        self.tree.column("Date", anchor="center", width=100)
        self.tree.column("Check-In", anchor="center", width=100)
        self.tree.column("Check-Out", anchor="center", width=100)
        self.tree.column("Guests", anchor="center", width=100)
        self.tree.column("Total Price", anchor="center", width=100)
        self.tree.column("Room No", anchor="center", width=100)
        self.tree.column("Category", anchor="center", width=100)
        self.tree.column("Status", anchor="center", width=100)


    def load_bookings(self):
        # Hide the main dashboard
        self.dashboard_frame.pack_forget()
        # Show the bookings
        self.bookings_frame.pack(pady=20, padx=20, fill="both", expand=True)

        for item in self.tree.get_children():
            self.tree.delete(item)

        self.data.clear()
        self.fetch_user_bookings()

        for item in self.data:
            self.tree.insert("", "end", values=item)

        self.tree.pack()

    
    def fetch_user_bookings(self):
        seperator = []
        for _ in range(9):
            seperator.append("----------------------")
        self.data.append(tuple(seperator))

        bookings = BookingAPI.fetch_bookings_by_user_id(self.user["ID"])

        for booking in bookings:
            self.data.append(
                (
                    ""
                )
            )
            self.data.append(
                (
                    booking["ID"],
                    booking["date"],
                    booking["check_in_date"],
                    booking["check_out_date"],
                    booking["guests"],
                    booking["total_price"],
                    RoomAPI.fetch_room_by_id(booking["room_id"])["room_no"],
                    RoomAPI.fetch_room_by_id(booking["room_id"])["room_type"],
                    booking["status"]
                )
            ) 


    def close_bookings_window(self):
        # Hide the bookings
        self.bookings_frame.pack_forget()
        # Bring the dashboard back
        self.dashboard_frame.pack(pady=20, padx=60, fill="both", expand=True)
    

    def submit(self):
        if self.hotel.get() == "Select Hotel":
            tk.messagebox.showerror("Error","Please select a hotel option.")
            return
        
        try:
            BookingWindow(self.root, self.user, self.dashboard)
            self.dashboard.withdraw()
        except Exception as e:
            tk.messagebox.showerror("Error", e)


    def modify(self):
        self.modify_window = ctk.CTkToplevel(self.dashboard)
        self.modify_window.geometry("500x300")
        self.modify_window.title("Modify Window")

        self.modify_frame = ctk.CTkFrame(master=self.modify_window)
        self.modify_frame.pack(pady=20, padx=60, fill="both", expand=True)

        # Sets the title of this application
        self.title = ctk.CTkLabel(master=self.modify_frame, text="Please enter your booking reference ID:", font=("Arial", 18))
        self.title.pack(pady=12, padx=10)

        self.booking_id = ctk.CTkEntry(master=self.modify_frame, width=240, height=35, font=("Arial", 16), placeholder_text="Enter booking ID...")
        self.booking_id.pack(pady=12, padx=10)

        # Field that allows user to submit all their account registration details
        self.modify_button = ctk.CTkButton(master=self.modify_frame, text="Modify Booking", fg_color="red", command = self.modify_booking)
        self.modify_button.pack(pady=12, padx=10)


    def modify_booking(self):
        booking = BookingAPI.fetch_booking_by_ref_no(self.booking_id.get())
        if not booking:
            tk.messagebox.showerror("Error", f"Booking not found.")
            return
        
        if booking["status"] == "Cancelled":
            tk.messagebox.showerror("Error", f"Booking has been cancelled.")
            return
        
        self.modify_window.destroy()
        self.dashboard.withdraw()

        BookingWindow(
            self.root,
            self.user,
            self.dashboard,
            cmd="modify",
            booking=booking
        )


    def cancel(self):
        self.cancel_window = ctk.CTkToplevel(self.dashboard)
        self.cancel_window.geometry("500x300")
        self.cancel_window.title("Cancel Window")

        self.cancel_frame = ctk.CTkFrame(master=self.cancel_window)
        self.cancel_frame.pack(pady=20, padx=60, fill="both", expand=True)

        # Sets the title of this application
        self.title = ctk.CTkLabel(master=self.cancel_frame, text="Please enter your booking reference ID:", font=("Arial", 18))
        self.title.pack(pady=12, padx=10)

        self.booking_id = ctk.CTkEntry(master=self.cancel_frame, width=240, height=35, font=("Arial", 16), placeholder_text="Enter booking ID...")
        self.booking_id.pack(pady=12, padx=10)

        # Field that allows user to submit all their account registration details
        self.cancel_button = ctk.CTkButton(master=self.cancel_frame, text="Cancel Booking", fg_color="red", command = self.cancel_booking)
        self.cancel_button.pack(pady=12, padx=10)


    def cancel_booking(self):
        booking = BookingAPI.fetch_booking_by_ref_no(self.booking_id.get())
        if not booking:
            tk.messagebox.showerror("Error", f"Booking not found.")
            return
        
        if booking["status"] == "Cancelled":
            tk.messagebox.showerror("Error", f"Booking has already been cancelled.")
            return
        
        BookingSystem.cancel_booking(booking, self.user)
        self.cancel_window.destroy()
        

# Allows file to be run independent of the main menu
if __name__ == '__main__':
    root = ctk.CTk()
    app = Dashboard(root)
    root.mainloop()
