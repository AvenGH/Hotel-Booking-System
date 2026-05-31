from db_manager import DBManager
import datacomp as dc
import datetime
import tkinter as tk
import customtkinter as ctk

today = datetime.date.today()


class RoomAPI:
    db = None
    cursor = None

    @classmethod
    def connect_db(cls):
        try:
            cls.db = DBManager("Hotel Reservation Management System")
            cls.cursor = cls.db.get_cursor()
            print("Connected to database successfully.")
        except Exception as e:
            print(f"Error connecting to database: {e}")

    @classmethod
    def get_rooms(cls):
        cls.cursor.execute("SELECT * FROM rooms")
        rooms = cls.cursor.fetchall()
        return rooms
    
    @classmethod
    def fetch_room_by_id(cls, room_id):
        cls.cursor.execute(f"SELECT * FROM rooms WHERE \"ID\" = %s", (room_id,))
        room = cls.cursor.fetchone()
        return room
    
    @classmethod
    def fetch_room_by_category(cls, room_type):
        cls.cursor.execute(f"SELECT * FROM rooms WHERE room_type = %s", (room_type,))
        rooms = cls.cursor.fetchall()
        return rooms
    
    @classmethod
    def add_room(cls, room_id, room_no, room_type, price, is_occupied, amenities):
        cls.cursor.execute(
            """
            INSERT INTO rooms (
                "ID", room_no, room_type, price, is_occupied, amenities
            ) VALUES (%s, %s, %s, %s, %s, %s)
            """, (room_id, room_no, room_type, price, is_occupied, amenities)
        )

    @classmethod
    def modify_room(cls, room_id, field, value):
        cls.cursor.execute(
            f"UPDATE rooms SET {field} = %s WHERE \"ID\" = %s", (value, room_id)  
        )

    @classmethod
    def delete_room(cls, room_id):
        cls.cursor.execute(
            f"DELETE FROM rooms WHERE \"ID\" = %s", room_id
        )


if __name__ == "__main__":
    RoomAPI.connect_db()

