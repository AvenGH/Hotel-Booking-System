from db_manager import DBManager
import datacomp as dc
import datetime
import tkinter as tk
import customtkinter as ctk

today = datetime.date.today()

# API for managing booking records

class BookingAPI:
    db = None
    cursor = None

    # Attempts to connect to database and returns error if connection is unsuccessful
    @classmethod
    def connect_db(cls):
        try:
            cls.db = DBManager("Hotel Reservation Management System")
            cls.cursor = cls.db.get_cursor()
            print("Connected to database successfully.")
        except Exception as e:
            print(f"Error connecting to database: {e}")

    # Fetches all bookings from the DB table
    @classmethod
    def get_bookings(cls):
        cls.cursor.execute("SELECT * FROM bookings")
        bookings = cls.cursor.fetchall()
        return bookings
    
    # Fetches a particular booking given the id
    @classmethod
    def fetch_booking_by_id(cls, booking_id):
        cls.cursor.execute(f"SELECT * FROM bookings WHERE \"ID\" = %s", (booking_id, ))
        booking = cls.cursor.fetchone()
        return booking
    
    # Fetches all bookings given a specific room id
    @classmethod
    def fetch_bookings_by_room_id(cls, room_id):
        cls.cursor.execute(f"SELECT * FROM bookings WHERE room_id = %s", (room_id, ))
        bookings = cls.cursor.fetchall()
        return bookings
    
    # Adds a booking record to the database
    @classmethod
    def add_booking(cls, booking_id, customer_id, check_in_date, check_out_date, guests, total_price, room_id):
        cls.cursor.execute(
            """
            INSERT INTO bookings (
                "ID", customer_id, date, check_in_date, check_out_date, guests, total_price, room_id, status
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (booking_id, customer_id, today, check_in_date, check_out_date, guests, total_price, room_id, True)
        )

        return True
    
    # Makes changes to a booking record
    @classmethod
    def modify_booking(cls, booking_id, field, value):
        cls.cursor.execute(
            f"UPDATE bookings SET {field} = %s WHERE ID = %s", (value, booking_id)
        )
    
    # Deletes the booking record from the database
    @classmethod
    def delete_booking(cls, booking_id):
        cls.cursor.execute(
            f"DELETE FROM bookings WHERE ID = %s", booking_id
        )

    # Deletes all bookings from the database
    @classmethod
    def delete_all_bookings(cls):
        cls.cursor.execute(
            f"DELETE FROM bookings"
        )
        

if __name__ == "__main__":
    BookingAPI.connect_db()
    print(BookingAPI.get_bookings())
