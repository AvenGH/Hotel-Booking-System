import datetime

today = datetime.date.today()


def write_booking_confirmation(
        room_no, room_category="", room_price=0, amenities="", adults=0, children=0, 
        check_in="", check_out="", total_price=0, file_path="", customer_name="Customer", ref_no=""
):

        with open (file_path, "w", encoding="utf-8",) as myfile:
                myfile.write(
                        f"""
        {today}

        
        Dear {customer_name},

        Your Hotel Room Has Successfully Been Booked.

        Room Number: {room_no} | Room Price: ${room_price:.2f} | Room Category: {room_category}

        Amenities provided: {amenities}

        Adults: {adults} | Children: {children}

        Check In Date: {check_in} | Check Out Date: {check_out}

        Total Price of Booking: £{total_price:.2f}

        Booking Reference Number: {ref_no}

                        """
                )


def write_booking_modification(
        room_no, room_category="", room_price=0, amenities="", adults=0, children=0, 
        check_in="", check_out="", total_price=0, file_path="", customer_name="Customer", ref_no=""        
):
        
        with open (file_path, "w", encoding="utf-8",) as myfile:
                myfile.write(
                        f"""
        {today}

        
        Dear {customer_name},

        Your Hotel Booking Has Successfully Been Modified.

        Room Number: {room_no} | Room Price: ${room_price:.2f} | Room Category: {room_category}

        Amenities provided: {amenities}

        Adults: {adults} | Children: {children}

        New Check In Date: {check_in} | New Check Out Date: {check_out}

        New Total Price of Booking: £{total_price:.2f}

        Booking Reference Number: {ref_no}

                        """
                )


def write_booking_cancellation(customer_name, ref_no, total_price, file_path=""):
        with open (file_path, "w", encoding="utf-8",) as myfile:
                myfile.write(
                        f"""
        {today}

        
        Dear {customer_name},

        Your Booking Has Successfully Been Cancelled.

        Booking ID: {ref_no}

        Total Price of Booking: £{total_price:.2f}

        A refund will be issued to you in the next 3-5 business days.

                        """)