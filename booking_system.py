import datetime
import tkinter as tk
import email_operations as eop
from api_classes.room_api import RoomAPI
from api_classes.booking_api import BookingAPI
from api_classes.customer_api import CustomerAPI
import util.generate_random_id as generate_random_id
from util import write_tools as wt

today = datetime.date.today()

RoomAPI.connect_db()
BookingAPI.connect_db()


class BookingSystem:

    @staticmethod
    def fields_blank(room_category, budget_category):
        return room_category.get() == "Select Room Category" or budget_category.get() == "Select Budget Range"


    @staticmethod
    def valid_dates(check_in_date, check_out_date):
        check_in_date = datetime.datetime.strptime(check_in_date.entry.get(), "%d/%m/%Y").date()
        check_out_date = datetime.datetime.strptime(check_out_date.entry.get(), "%d/%m/%Y").date()
        if check_in_date < today or check_out_date < today:
            tk.messagebox.showerror("Error", "Only future dates can be selected.")
            return
        if check_in_date >= check_out_date:
            tk.messagebox.showerror("Error", "Check-in date must be earlier than check-out date.")
            return

        return check_in_date, check_out_date
    

    @staticmethod
    def valid_guests(adults, children):
        if adults.get() == "0":
            tk.messagebox.showerror("Error", "There must be at least 1 adult.")
            return

        return adults, children
    

    @classmethod
    def validate_details(cls, check_in_date, check_out_date, adults, children):
        if not cls.valid_dates(check_in_date, check_out_date):
            return
        
        if not cls.valid_guests(adults, children):
            return
        
        return True
    

    # Will be executed once 'display available rooms' button is clicked
    @classmethod
    def check_available_rooms(cls, room_category, check_in_date, check_out_date):
        if room_category == "Select Room Category":
            tk.messagebox.showerror("Error", "Please select a room category in order to see available rooms.")
            return
        if not cls.valid_dates(check_in_date, check_out_date):
            return
        
        # Fetches all the available rooms of the specified room category
        available_rooms = [room for room in RoomAPI.fetch_room_by_category(room_category) if room["is_occupied"] == False]

        message = """"""

        # Returns an error if there are no available rooms
        if not available_rooms:
            tk.messagebox.showerror("Error", "Sorry! There are no more rooms available of the chosen category.")
            return

        # Adds each room onto the display message
        for room in available_rooms:
            message += f"Room No: {room["room_no"]}, Room Type: {room['room_type']}"+"\n"

        tk.messagebox.showinfo("Available Rooms", message)


    # Returns the first available room of the specified room type
    @staticmethod
    def select_first_available_room(room_category):
        rooms = RoomAPI.get_rooms()
        for room in rooms:
            if room["room_type"] == room_category and not room["is_occupied"]:
                return room
            

    # Checks the availability of a room based on check-in and check-out dates
    @classmethod
    def check_availability(cls, check_in_date, check_out_date, room_category):
        check_in_date = datetime.datetime.strptime(check_in_date, "%d/%m/%Y")
        check_out_date = datetime.datetime.strptime(check_out_date, "%d/%m/%Y")

        selected_room = cls.select_first_available_room(room_category)

        # Checks if the first room is available. Otherwise will perform an availability check.
        if selected_room:
            return selected_room

        # Fetches all the existing room ids for the specified room category
        room_ids = [room["ID"] for room in RoomAPI.fetch_room_by_category(room_category)]

        available_rooms = []

        # Loops through all rooms and checks for overlaps 
        for room_id in room_ids:
            filtered_bookings = BookingAPI.fetch_bookings_by_room_id(room_id)
            is_overlap = False # A flag which is set to true if an overlap is found

            # Loops through each booking in the filtered bookings for each room id
            for booking in filtered_bookings:              
                if cls.check_overlap(
                    user_check_in=check_in_date,
                    user_check_out=check_out_date,
                    system_check_in=booking["check_in_date"],
                    system_check_out=booking["check_out_date"]
                ):
                    is_overlap = True
                    break # Stops and advances to the next iteration if an overlap is found for a room id

            # Fetches all the booking IDs from the filtered bookings array and finds the most recent booking
            booking_ids = [int(booking["ID"][1:]) for booking in filtered_bookings]
            if not booking_ids:
                return

            most_recent_booking = BookingAPI.fetch_booking_by_id(f"#{max(booking_ids): 05}".replace(" ",""))

            # Checks for an overlap with the most recent booking
            if check_in_date <= datetime.datetime.strptime(str(most_recent_booking["check_out_date"]), "%Y-%m-%d") <= check_out_date:
                is_overlap = True

            # When no overlaps are found
            if not is_overlap:
                return RoomAPI.fetch_room_by_id(room_id) # Returns the first room id for which there are no overlap bookings

    
    @staticmethod
    # Takes in booking dates and checks for overlaps
    def check_overlap(user_check_in, user_check_out, system_check_in, system_check_out):
        # Checks if the check in date is later than the check out date of the most recent booking
        if not((user_check_in < datetime.datetime.strptime(str(system_check_in), "%Y-%m-%d"))
               or (user_check_in > datetime.datetime.strptime(str(system_check_out), "%Y-%m-%d"))
        ):
            return True
        
        # Checks if the check out date is earlier than the check in date of the most recent booking
        if not((user_check_out < datetime.datetime.strptime(str(system_check_in), "%Y-%m-%d"))
               or (user_check_out > datetime.datetime.strptime(str(system_check_out), "%Y-%m-%d"))
        ):
            return True
    

    @staticmethod
    def calculate_price(base_price, adults, children, nights):
        adult_surcharge = max(0, adults - 2) * 0.2 * base_price
        child_surcharge = children * 0.1 * base_price

        total_price = (base_price + adult_surcharge + child_surcharge) * nights

        return total_price
    
    @staticmethod
    def select_user_by_email(email):
        customers = CustomerAPI.get_users()
        for customer in customers:
            if customer["email"] == email:
                return customer
    

    @staticmethod
    def send_email(file_path, email):
        try:
            with open(file_path, "rb") as myfile:
                file_name=myfile.name
                sender_email_id="avnikumar32@gmail.com"
                recipient_email_id=email
                sender="AvenKumar32"
                host_password="ppcv ezqb foay xfrg"
                subject="Booking Confirmation"
                subtype="txt"

                eop.send_email(
                    file_name=file_name,
                    receiver_email=recipient_email_id,
                    email=sender_email_id,
                    sender=sender,
                    subject=subject,
                    data="<This is an automated message. Please do not reply directly to this email.>",
                    subtype=subtype,
                    host_password=host_password
                )
                
        except Exception as e:
            print(f"Something went wrong... Error: {e}")
            exit()

        else:
            print("Email sent successfully!")


    @classmethod
    def submit_booking(cls, selected_room, room_category, adults, children, check_in_date_entry, check_out_date_entry, email):
        check_in_date = datetime.datetime.strptime(check_in_date_entry.entry.get(), "%d/%m/%Y")
        check_out_date = datetime.datetime.strptime(check_out_date_entry.entry.get(), "%d/%m/%Y")

        # Takes in all the necessary arguments and calculates the price
        price = cls.calculate_price(
            base_price = selected_room['price'],
            adults = int(adults),
            children = int(children),
            nights = (check_out_date - check_in_date).days
        )
        
        # Adds the booking to the database
        bookingid = generate_random_id.generate_booking_id()

        BookingAPI.add_booking(
            booking_id = bookingid, 
            customer_id = "292482", 
            room_id = selected_room["ID"], 
            check_in_date = check_in_date, 
            check_out_date = check_out_date, 
            guests = int(adults) + int(children),
            total_price = price 
        )

        # Updates the availability status to 'false'
        RoomAPI.modify_room(
            room_id = selected_room["ID"],
            field="is_occupied",
            value = True
        )

        filepath = f"""Confirmation Statements\\booking{id(bookingid)}.txt"""

        name = cls.select_user_by_email(email)["name"]
        
        wt.write(
            customer_name = name,
            room_no = selected_room["room_no"],
            room_category = room_category,
            room_price = selected_room["price"],
            amenities = selected_room["amenities"],
            adults = adults,
            children = children,
            check_in = check_in_date_entry.entry.get(),
            check_out = check_out_date_entry.entry.get(),
            total_price = price,
            file_path = filepath
        )

        cls.send_email(filepath, email)

        # Displays a confirmation message along with the final price of the booking
        tk.messagebox.showinfo("Booking Confirmation", f"Your booking has successfully been made. Total Price was ${price:.2f}.")
        return True


if __name__ == "__main__":
    pass

