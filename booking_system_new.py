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
    def valid_dates(check_in_date, check_out_date):
        check_in_date = datetime.datetime.strptime(check_in_date, "%Y-%m-%d").date()
        check_out_date = datetime.datetime.strptime(check_out_date, "%Y-%m-%d").date()
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
            

    # Checks the availability of a room based on check-in and check-out dates
    @classmethod
    def check_availability(cls, check_in_date, check_out_date, room_id, your_booking):
        check_in_date = datetime.datetime.strptime(check_in_date, "%Y-%m-%d")
        check_out_date = datetime.datetime.strptime(check_out_date, "%Y-%m-%d")

        if RoomAPI.fetch_room_by_id(room_id)["available"]:
            return True 
        
        print(f"\nChecking availability of {room_id}:")
        filtered_bookings = BookingAPI.fetch_bookings_by_room_id(room_id)
        is_overlap = False # A flag which is set to true if an overlap is found

        print(filtered_bookings)

        # Loops through each booking in the filtered bookings for each room id
        for booking in filtered_bookings:              
            if cls.check_overlap(
                user_check_in=check_in_date,
                user_check_out=check_out_date,
                system_check_in=booking["check_in_date"],
                system_check_out=booking["check_out_date"]
            ) and booking["ID"] != your_booking["ID"]:
                
                print("An overlap was found.")
                print(f"""Evidence:\nYour booking ({check_in_date}-{check_out_date}) \noverlaps with another booking ({booking["check_in_date"]}-{booking["check_out_date"]})""")
                is_overlap = True
                break # Stops and advances to the next iteration if an overlap is found for a room id

        # Fetches all the booking IDs from the filtered bookings array and finds the most recent booking
        booking_ids = [int(booking["ID"][1:]) for booking in filtered_bookings]
        if not booking_ids:
            return

        most_recent_booking = BookingAPI.fetch_booking_by_id(f"#{max(booking_ids): 05}".replace(" ",""))

        # Checks for an overlap with the most recent booking
        if (
            check_in_date <= datetime.datetime.strptime(str(most_recent_booking["check_out_date"]), "%Y-%m-%d") <= check_out_date
        ) and most_recent_booking["ID"] != your_booking["ID"]:

            print("An overlap was found with the most recent booking")
            print(f"""Evidence:\nYour booking ({check_in_date}-{check_out_date}) \noverlaps with another booking ({most_recent_booking["check_in_date"]}-{most_recent_booking["check_out_date"]})""")
            is_overlap = True

        # When no overlaps are found
        if not is_overlap:
            print("No overlaps found. This room is available to book on the chosen dates.")
            return True

    
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
    def send_email(file_path, email, subject):
        try:
            with open(file_path, "rb") as myfile:
                file_name=myfile.name
                sender_email_id="avnikumar32@gmail.com"
                recipient_email_id=email
                sender="AvenKumar32"
                host_password="ppcv ezqb foay xfrg"
                subject=subject
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
    def submit_booking(cls, user, cmd, booking, selected_room, room_category, adults, children, check_in_date_entry, check_out_date_entry):
        check_in_date = datetime.datetime.strptime(check_in_date_entry, "%Y-%m-%d")
        check_out_date = datetime.datetime.strptime(check_out_date_entry, "%Y-%m-%d")

        # Takes in all the necessary arguments and calculates the price
        price = cls.calculate_price(
            base_price = selected_room['price'],
            adults = int(adults),
            children = int(children),
            nights = (check_out_date - check_in_date).days
        )
        
        if cmd=="book":
            # Adds the booking to the database
            bookingid = generate_random_id.generate_booking_id()
            ref_no = id(bookingid)

            BookingAPI.add_booking(
                booking_id = bookingid, 
                customer_id = user["ID"], 
                room_id = selected_room["ID"], 
                check_in_date = check_in_date, 
                check_out_date = check_out_date, 
                guests = int(adults) + int(children),
                total_price = price,
                ref_no=ref_no 
            )

            # Updates the availability status to 'false'
            RoomAPI.modify_room(
                room_id = selected_room["ID"],
                field="available",
                value = False
            )

            filepath = f"""Confirmation Statements\\booking{ref_no}.txt"""
            
            wt.write_booking_confirmation(
                customer_name = user["name"],
                room_no = selected_room["room_no"],
                room_category = room_category,
                room_price = selected_room["price"],
                amenities = selected_room["amenities"],
                adults = adults,
                children = children,
                check_in = check_in_date,
                check_out = check_out_date,
                total_price = price,
                ref_no=ref_no,
                file_path = filepath
            )

            cls.send_email(filepath, user["email"], "Booking Confirmation")

            # Displays a confirmation message along with the final price of the booking
            tk.messagebox.showinfo("Booking Confirmation", f"Your booking has successfully been made. Total Price was ${price:.2f}.")
            return True
    
        else:
            BookingSystem.modify_booking(
                user,
                booking["ID"],
                booking["reference_no"],
                selected_room,
                selected_room["room_type"],
                adults,
                children,
                check_in_date,
                check_out_date
            )
    

    @classmethod
    def modify_booking(cls, user, booking_id, ref_no, selected_room, room_category, adults, children, check_in_date, check_out_date):
        # Takes in all the necessary arguments and calculates the price
        price = cls.calculate_price(
            base_price = selected_room['price'],
            adults = int(adults),
            children = int(children),
            nights = (check_out_date - check_in_date).days
        )

        BookingAPI.modify_booking(
            booking_id = booking_id,
            field="check_in_date",
            value = check_in_date
        )
        BookingAPI.modify_booking(
            booking_id = booking_id,
            field="check_out_date",
            value = check_out_date
        )
        BookingAPI.modify_booking(
            booking_id = booking_id,
            field="guests",
            value = int(adults) + int(children)
        )
        BookingAPI.modify_booking(
            booking_id = booking_id,
            field="total_price",
            value = price
        )
        BookingAPI.modify_booking(
            booking_id = booking_id,
            field="room_id",
            value = selected_room["ID"]
        )

        RoomAPI.modify_room(
            room_id = selected_room["ID"],
            field="available",
            value = False
        )

        BookingAPI.modify_booking(booking_id, "status", "Modified")

        filepath = f"""Modification Statements\\booking{ref_no}.txt"""
        
        wt.write_booking_modification(
            customer_name = user["name"],
            room_no = selected_room["room_no"],
            room_category = room_category,
            room_price = selected_room["price"],
            amenities = selected_room["amenities"],
            adults = adults,
            children = children,
            check_in = check_in_date,
            check_out = check_out_date,
            total_price = price,
            ref_no=ref_no,
            file_path = filepath
        )

        cls.send_email(filepath, user["email"], "Booking Modification")

        # Displays a confirmation message along with the final price of the booking
        tk.messagebox.showinfo("Booking Modification", f"Your booking has successfully been modified. Total Price was ${price:.2f}.")
        return True
    

    @classmethod
    def cancel_booking(cls, booking, user):
        ref_no = booking["reference_no"]
        BookingAPI.modify_booking(booking["ID"], "status", "Cancelled")
        RoomAPI.modify_room(booking["room_id"], "available", True)

        filepath = f"""Cancellation Statements\\cancellation{ref_no}.txt"""
        wt.write_booking_cancellation(user["name"], ref_no, booking["total_price"], filepath)
        cls.send_email(filepath, user["email"], "Booking Cancellation")

        tk.messagebox.showinfo("Booking Cancellation", f"Your booking has successfully been cancelled.")
        return True


if __name__ == "__main__":
    pass

