import tkinter as tk
import customtkinter as ctk
import tkkbootstrap as tb
from ttkbootstrap.constants import *
#from booking_system import BookingSystem
from PIL import Image
import access_data as ad
#from api_classes.room_api import RoomAPI
#from api_classes.booking_api import BookingAPI
from tkinter import ttk
from tkcalendar import Calendar
from datetime import date


# GUI Class for managing properties of booking interface
class BookingWindow:
    def __init__(self, root, user, dashboard, cmd="book", booking={"ID":None}, dimensions="750x475"):
        self.root = root
        self.user = user
        self.booking=booking
        self.dashboard = dashboard
        self.cmd = cmd
        self.dimensions = dimensions

        # Creates variables of data type string for the initial adults and children and sets their values to '0'
        self.adults_text_variable = ctk.StringVar()
        self.adults_text_variable.set("1")

        self.children_text_variable = ctk.StringVar()
        self.children_text_variable.set("0")

        # Stores the available room and budget options which the user can select from
        self.room_options = ["Single", "Double", "Suite"]
        self.budget_options = ["$500-1000", "$1500-2000", "$2500-3000"]

        self.room_properties = ad.loadData("txt", "obj_files\\room_properties.json")

        self.available_rooms = []
        self.filtered_rooms = []

        self.calendar_image = ctk.CTkImage(dark_image = Image.open("images\\calendar_icon.png"), size=(35, 35))
        self.create_ui()
        self.booking_window.protocol("WM_DELETE_WINDOW", self.on_close)


    # Executed when close button is pressed on right hand corner
    def on_close(self):
        self.filtered_rooms.clear()
        self.booking_window.destroy()
        self.dashboard.deiconify()


    # Creates user interface with all necessary elements
    def create_ui(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Sets the date picker theme to dark 
        style = tb.Style(theme="darkly")

        # Creates a top level (derived) window from the main menu (parent) window
        self.booking_window = ctk.CTkToplevel(self.root)
        self.booking_window.geometry(self.dimensions)
        self.booking_window.title("Hotel Booking App")

        # Defines space within which elements may be positioned
        self.frame = ctk.CTkFrame(master=self.booking_window)
        self.frame.pack(pady=20, padx=60, fill="both", expand=True)

        # Sets the title of this application
        self.title = ctk.CTkLabel(master=self.frame, text='Welcome to the Booking System!', font=('Arial', 24))
        self.title.pack(pady=12, padx=10)

        # Field that takes in the user's check-in date via a date picker
        self.check_in_date_label = ctk.CTkLabel(master=self.frame, text="Check In Date", font=("Arial", 18))
        self.check_in_date_label.place(x=100, y=100)

        self.check_in_date = tb.DateEntry(master=self.frame, bootstyle="darkly")
        self.check_in_date.place(x=345, y=127)

        # Field that takes in the user's check-out date via a date picker
        self.check_out_date_label = ctk.CTkLabel(master=self.frame, text="Check Out Date", font=("Arial", 18))
        self.check_out_date_label.place(x=100, y=175)

        self.check_out_date = tb.DateEntry(master=self.frame, bootstyle="darkly")
        self.check_out_date.place(x=345, y=222)

        # Field that takes in the number of adults
        self.adults_label = ctk.CTkLabel(master=self.frame, text="Adults", font=("Arial", 18))
        self.adults_label.place(x=100, y=250)

        # Allows the user to increment the number of adults
        self.adults_increment_button = ctk.CTkButton(master=self.frame, corner_radius=0, text="+", width=40, font=("Arial", 20), command=lambda : self.increment("adults", self.adults.get()))
        self.adults_increment_button.place(x=275, y=250)

        # Value gets updated every time the user clicks on a '+' or '-' button
        self.adults = ctk.CTkEntry(master=self.frame, corner_radius=0, textvariable = self.adults_text_variable, width=60, font=("Arial", 18), state="disabled")
        self.adults.place(x=215, y=250)

        # Allows the user to decrement the number of adults
        self.adults_decrement_button = ctk.CTkButton(master=self.frame, corner_radius=0, text="-", width=40, font=("Arial", 20), command=lambda : self.decrement("adults", self.adults.get()), state = ctk.DISABLED)
        self.adults_decrement_button.place(x=175, y=250)

        # Field that takes in the number of children
        self.children_label = ctk.CTkLabel(master=self.frame, text="Children", font=("Arial", 18))
        self.children_label.place(x=350, y=250)

        # Allows the user to increment the number of children
        self.children_increment_button = ctk.CTkButton(master=self.frame, corner_radius=0, text="+", width=40, font=("Arial", 20), command=lambda : self.increment("children", self.children.get()))
        self.children_increment_button.place(x=550, y=250)

        # Value gets updated every time the user clicks on a '+' or '-' button
        self.children = ctk.CTkEntry(master=self.frame, corner_radius=0, textvariable = self.children_text_variable, width=60, font=("Arial", 18), state="disabled")
        self.children.place(x=490, y=250)

        # Allows the user to decrement the number of children
        self.children_decrement_button = ctk.CTkButton(master=self.frame, corner_radius=0, text="-", width=40, font=("Arial", 20), command=lambda:self.decrement("children", self.children.get()), state = ctk.DISABLED)
        self.children_decrement_button.place(x=450, y=250)

        # Displays the available rooms based on room category and budget
        self.display_button = ctk.CTkButton(master=self.frame, fg_color="dark blue", text="Check Available Rooms", command=self.validate_details, width=200)
        self.display_button.place(x=225, y=325)

    
    def on_date_select(self, event):
        selected = self.cal.get_date()
        self.label.configure(text=f"Selected Date: {selected}")


    def validate_details(self):
        # Checks to see if all fields are valid, if valid sends the details onto the backend
        booking_validated = BookingSystem.validate_details(self.check_in_date, self.check_out_date, self.adults, self.children)

        # Checks if a booking has successfully been confirmed
        if booking_validated:
            self.show_room_preview()
        

    # Will be executed once the information icon is clicked
    def show_room_preview(self):
        self.room_preview_window = ctk.CTkToplevel(self.booking_window)
        self.room_preview_window.geometry("950x900")
        self.room_preview_window.title("Hotel Booking App")

        # Defines space within which elements may be positioned
        self.jframe = ctk.CTkScrollableFrame(master=self.room_preview_window, width=875, height=850)
        self.jframe.pack(pady=20, padx=20, fill="both", expand=True)
        self.jframe.rowconfigure(0, weight=1)
        self.jframe.rowconfigure(1, weight=1)
        self.jframe.rowconfigure(2, weight=1)
        self.jframe.rowconfigure(3, weight=1)
        self.jframe.columnconfigure(0, weight=1)
        self.jframe.columnconfigure(1, weight=1)
        self.jframe.columnconfigure(2, weight=1)
        self.jframe.columnconfigure(3, weight=1)
        self.jframe.columnconfigure(4, weight=1)

        self.room_category_label = ctk.CTkLabel(master=self.jframe, text= "Room category: ", font=("Arial", 14))
        self.room_category_label.grid(row=0, column=0)

        self.room_category = ctk.CTkComboBox(master=self.jframe, values=self.room_options, width=160, height=25, font=("Arial", 12), state="readonly")
        self.room_category.set("Select Room Category")
        self.room_category.grid(row=0, column=1)

        self.apply_button = ctk.CTkButton(master=self.jframe, text="Apply filters", width=75, height=20, command=self.filter_rooms)
        self.apply_button.grid(row=0, column=2)

        self.clear_button = ctk.CTkButton(master=self.jframe, fg_color="red", text="Clear filters", width=100, height=20, command=self.clear_filters)
        self.clear_button.grid(row=0, column=3)

        self.submit_button = ctk.CTkButton(master=self.jframe, fg_color="green", text="Book room", width=100, height=20, command=self.submit, state="disabled")
        self.submit_button.grid(row=0, column=4)

        self.filtered_rooms = []

        self.fetch_available_rooms()
        self.fetch_suitable_rooms()

        self.display_rooms()


    def display_rooms(self):        
        self.submit_button.configure(state=ctk.DISABLED)
        self.radio_var = tk.StringVar(value="")

        rooms = self.filtered_rooms if self.filtered_rooms!=[] else self.available_rooms

        if not rooms:
            self.empty_label = ctk.CTkLabel(
                master=self.jframe, 
                text="Sorry! No results match your search.", 
                font=("Arial", 18),
                )
            self.empty_label.grid(row=1, column=1, padx=20, pady=20, sticky="nws")
        
        row_index = 0
        for room in rooms:
            self.choose_button = ctk.CTkRadioButton(master=self.jframe, text=f"No. {room["room_no"]} {room["room_type"]} Room -£{room["price"]}", command=self.enable_submit, variable= self.radio_var, value=room["ID"])
            self.choose_button.grid(row=row_index+1, column=0, padx=10, pady=(0, 50), sticky="nws")

            self.room_info_label = ctk.CTkLabel(
                master=self.jframe, 
                text=f"""Max Guests: {room["max_capacity"]}\n\nAmenities: {room["amenities"]}\n\nCurrently Available: {room["available"]}""", 
                font=("Arial", 10),
                justify="left",
                anchor="w"
                )
            self.room_info_label.grid(row=row_index+1, column=1, padx=20, pady=20, sticky="w")

            self.room_available_label = ctk.CTkLabel(
                master=self.jframe, 
                text=f"{room["available"]}",
                font=("Arial", 10),
                text_color="green" if room["available"] else "red"
            )
            #self.room_available_label.grid(row=row_index+1, column=1, padx=40, pady=20)

            image_label = ctk.CTkLabel(master=self.jframe, text= "", image = "")
            image_label.grid(row=row_index+1, column=2, padx=20, pady=20, sticky="w")
            self.room_image = ctk.CTkImage(dark_image = Image.open(self.room_properties[room["room_type"]]["image"]), size=(200, 100))
            image_label.configure(image=self.room_image)

            row_index += 1


    def enable_submit(self):
        self.submit_button.configure(state=ctk.NORMAL)


    def submit(self):
        self.selected_room = RoomAPI.fetch_room_by_id(self.radio_var.get())
        BookingSystem.submit_booking(
            self.user,
            self.cmd,
            self.booking,
            self.selected_room,
            self.selected_room["room_type"],
            self.adults.get(),
            self.children.get(),
            self.check_in_date,
            self.check_out_date
        )
        self.booking_window.destroy()
        self.dashboard.deiconify()


    def fetch_available_rooms(self):
        self.available_rooms = [
            room for room in RoomAPI.get_rooms() 
            if bool(BookingSystem.check_availability(
                self.check_in_date.entry.get(), 
                self.check_out_date.entry.get(),
                room["ID"],
                self.booking 
            ))
        ]


    def fetch_suitable_rooms(self):
        guests = int(self.adults.get()) + int(self.children.get())
        self.suitable_rooms = []
        for room in self.available_rooms:
            if guests <= room["max_capacity"]:
                self.suitable_rooms.append(room)

        self.available_rooms = self.suitable_rooms


    def clear_page(self):
        for widget in self.jframe.winfo_children():
            if isinstance(widget, (ctk.CTkLabel, ctk.CTkRadioButton)):
                widget.destroy()

        self.room_category_label = ctk.CTkLabel(master=self.jframe, text= "Room category: ", font=("Arial", 14))
        self.room_category_label.grid(row=0, column=0)


    def filter_rooms(self):
        self.clear_page()

        if self.room_category.get() in self.room_options:
            self.filtered_rooms = [room for room in self.available_rooms if room["room_type"] == self.room_category.get()] # Not true
        self.display_rooms()

    
    def clear_filters(self):
        self.filtered_rooms = []
        self.room_category.set("Select Room Category")
        self.display_rooms()


    # Will be executed once '+' button is clicked
    def increment(self, type, value):
        if type == "adults":
            # Increments the value and then enables the decrement button
            self.adults_text_variable.set(str(int(value) + 1))
            self.adults_decrement_button.configure(state=ctk.NORMAL)
        else:
            self.children_text_variable.set(str(int(value) + 1))
            self.children_decrement_button.configure(state=ctk.NORMAL)
        

    # Will be executed once '-' button is clicked
    def decrement(self, type, value):
        # Checks if the value is greater than zero, otherwise cannot be decremented as it results in a negative value
        if int(value) > 0:
            if type == "adults":
                # Decrements the value
                self.adults_text_variable.set(str(int(value) - 1))
            else:
                self.children_text_variable.set(str(int(value) - 1))

            # Disables the decrement buttons if the values cannot be decremented further
            if self.adults_text_variable.get() == "1":
                self.adults_decrement_button.configure(state=ctk.DISABLED)
            if self.children_text_variable.get() == "0":
                self.children_decrement_button.configure(state=ctk.DISABLED)


if __name__ == "__main__":
    root = ctk.CTk()
    app = BookingWindow(root, "user", "dashboard")
    root.mainloop()