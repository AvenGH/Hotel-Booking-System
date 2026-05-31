import tkinter as tk
import customtkinter as ctk
import tkkbootstrap as tb
from ttkbootstrap.constants import *
#from booking_system import BookingSystem
from PIL import Image
import access_data as ad


# GUI Class for managing properties of booking interface
class BookingWindow:
    def __init__(self, root, dimensions="750x600",):
        self.root = root
        #self.dashboard = dashboard
        self.dimensions = dimensions

        # Creates variables of data type string for the initial adults and children and sets their values to '0'
        self.adults_text_variable = ctk.StringVar()
        self.adults_text_variable.set("0")

        self.children_text_variable = ctk.StringVar()
        self.children_text_variable.set("0")

        # Stores the available room and budget options which the user can select from
        self.room_options = ["Single", "Double", "Suite"]
        self.budget_options = ["$500-1000", "$1500-2000", "$2500-3000"]

        #self.room_properties = ad.loadData("txt", "obj_files\\room_properties.json")

        self.create_ui()
        self.booking_window.protocol("WM_DELETE_WINDOW", self.on_close)


    # Executed when close button is pressed on right hand corner
    def on_close(self):
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
        self.title = ctk.CTkLabel(master=self.frame, text=f'Welcome to the Booking System!', font=('Arial', 24))
        self.title.pack(pady=12, padx=10)

        # Field that takes in the user's chosen room category via a drop down menu
        self.room_category_label = ctk.CTkLabel(master=self.frame, text="Room Category", font=("Arial", 18))
        self.room_category_label.place(x=100, y=100)

        self.room_category = ctk.CTkComboBox(master=self.frame, values=self.room_options, width=240, height=35, font=("Arial", 16), state="readonly")
        self.room_category.set("Select Room Category")
        self.room_category.place(x=275, y=100)

        # Field that takes in the user's check-in date via a date picker
        self.check_in_date_label = ctk.CTkLabel(master=self.frame, text="Check In Date", font=("Arial", 18))
        self.check_in_date_label.place(x=100, y=175)

        self.check_in_date = tb.DateEntry(master=self.frame, bootstyle="darkly")
        self.check_in_date.place(x=345, y=222)

        # Field that takes in the user's check-out date via a date picker
        self.check_out_date_label = ctk.CTkLabel(master=self.frame, text="Check Out Date", font=("Arial", 18))
        self.check_out_date_label.place(x=100, y=250)

        self.check_out_date = tb.DateEntry(master=self.frame, bootstyle="darkly")
        self.check_out_date.place(x=345, y=317)

        # Field that takes in the number of adults
        self.adults_label = ctk.CTkLabel(master=self.frame, text="Adults", font=("Arial", 18))
        self.adults_label.place(x=100, y=325)

        # Allows the user to increment the number of adults
        self.adults_increment_button = ctk.CTkButton(master=self.frame, corner_radius=0, text="+", width=40, font=("Arial", 20), command=lambda : self.increment("adults", self.adults.get()))
        self.adults_increment_button.place(x=275, y=325)

        # Value gets updated every time the user clicks on a '+' or '-' button
        self.adults = ctk.CTkEntry(master=self.frame, corner_radius=0, textvariable = self.adults_text_variable, width=60, font=("Arial", 18), state="disabled")
        self.adults.place(x=215, y=325)

        # Allows the user to decrement the number of adults
        self.adults_decrement_button = ctk.CTkButton(master=self.frame, corner_radius=0, text="-", width=40, font=("Arial", 20), command=lambda : self.decrement("adults", self.adults.get()), state = ctk.DISABLED)
        self.adults_decrement_button.place(x=175, y=325)

        # Field that takes in the number of children
        self.children_label = ctk.CTkLabel(master=self.frame, text="Children", font=("Arial", 18))
        self.children_label.place(x=350, y=325)

        # Allows the user to increment the number of children
        self.children_increment_button = ctk.CTkButton(master=self.frame, corner_radius=0, text="+", width=40, font=("Arial", 20), command=lambda : self.increment("children", self.children.get()))
        self.children_increment_button.place(x=550, y=325)

        # Value gets updated every time the user clicks on a '+' or '-' button
        self.children = ctk.CTkEntry(master=self.frame, corner_radius=0, textvariable = self.children_text_variable, width=60, font=("Arial", 18), state="disabled")
        self.children.place(x=490, y=325)

        # Allows the user to decrement the number of children
        self.children_decrement_button = ctk.CTkButton(master=self.frame, corner_radius=0, text="-", width=40, font=("Arial", 20), command=lambda:self.decrement("children", self.children.get()), state = ctk.DISABLED)
        self.children_decrement_button.place(x=450, y=325)
        
        # Field that takes in the user's chosen budget range via a drop down menu
        self.budget_category_label = ctk.CTkLabel(master=self.frame, text="Budget", font=("Arial", 18))
        self.budget_category_label.place(x=100, y=400)
        
        self.budget_category = ctk.CTkComboBox(master=self.frame, values=self.budget_options, width=240, height=35, font=("Arial", 16), state="readonly")
        self.budget_category.set("Select Budget Range")
        self.budget_category.place(x=275, y=400)

        # Displays the available rooms based on room category and budget
        self.display_button = ctk.CTkButton(master=self.frame, fg_color="dark blue", text="Check Available Rooms", command=lambda:BookingSystem.check_available_rooms(self.room_category.get(), self.check_in_date, self.check_out_date))
        self.display_button.place(x=100, y=475)

        # Field that allows user to submit all their booking details
        self.submit_button = ctk.CTkButton(master=self.frame, fg_color="green", text="Confirm and Submit", command=self.submit)
        self.submit_button.place(x=400, y=475)

        # Displays a small room preview of the selected room type
        self.information_icon = ctk.CTkButton(master=self.frame, text="i", command=self.show_room_preview, font=('Arial', 24), width=35, height=35)
        self.information_icon.place(x=515, y=100)


    def check_dates():
        while True:
            pass
        

    # Will be executed once the information icon is clicked
    def show_room_preview(self):
        if self.room_category.get() == "Select Room Category":
            tk.messagebox.showerror("Error", "Please select a room category in order to see preview")
            return
        if not BookingSystem.valid_dates(self.check_in_date, self.check_out_date):
            return

        # Sets up the initial configurations
        self.room_preview_window = ctk.CTkToplevel(self.root)
        self.room_preview_window.geometry("500x300")
        self.room_preview_window.title("Room Preview")

        # Where the room image will be displayed
        image_label = ctk.CTkLabel(master=self.room_preview_window, text= "", image = "")
        image_label.pack()

        selected_room = BookingSystem.check_availability(self.check_in_date.entry.get(), self.check_out_date.entry.get(), self.room_category.get())

        if not selected_room:
            tk.messagebox.showerror("Error", "No preview is available for the selected room category. Please select a different category or set of dates.")
            return

        # Fetches the particular room image associated with the specified room category
        room_image_path = self.room_properties[self.room_category.get()]['image']
        room_image = ctk.CTkImage(dark_image = Image.open(room_image_path), size=(400, 200))
        image_label.configure(image=room_image)

        amenities_label = ctk.CTkLabel(master=self.room_preview_window, text = selected_room["amenities"])
        amenities_label.pack()

        price_label = ctk.CTkLabel(master = self.room_preview_window, text = selected_room["price"])
        price_label.pack()     


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
            if self.adults_text_variable.get() == "0":
                self.adults_decrement_button.configure(state=ctk.DISABLED)
            if self.children_text_variable.get() == "0":
                self.children_decrement_button.configure(state=ctk.DISABLED)


    # Will be executed once 'submit' button is clicked
    def submit(self):
        # Checks for any blank fields 
        if BookingSystem.fields_blank(self.room_category, self.budget_category):
            tk.messagebox.showerror("Error", "All fields are required!")
            return
 
        # Checks to see if all fields are valid, if valid sends the details onto the backend
        booking_validated = BookingSystem.validate_details(self.check_in_date, self.check_out_date, self.adults, self.children)

        # Checks if a booking has successfully been confirmed
        if booking_validated:
            selected_room = BookingSystem.check_availability(self.check_in_date.entry.get(), self.check_out_date.entry.get(), self.room_category.get())

            # When no rooms exist of the specified category, or an overlap booking has been found
            if not selected_room:
                tk.messagebox.showerror("Error", f"Sorry, there are no more {self.room_category.get()} rooms available on these dates.")
                return
            
            result = BookingSystem.submit_booking(self.user, selected_room, self.room_category.get(), self.adults.get(), self.children.get(), self.check_in_date, self.check_out_date)

            # Closes the booking window once a booking has successfully been made
            self.booking_window.destroy()
            self.dashboard.deiconify()


# Executed when file is being run
if __name__ == '__main__':
    root = ctk.CTk()
    app = BookingWindow(root)
    root.mainloop()

