from api_classes.booking_api import BookingAPI
from api_classes.room_api import RoomAPI
from api_classes.customer_api import CustomerAPI

import random

def generate_booking_id():
    existing_booking_ids = [booking["ID"] for booking in BookingAPI.get_bookings()]
    if existing_booking_ids:
        top_id = existing_booking_ids[-1]
        if top_id != "#9999":
            new_id = f'#{int(top_id[1:])+1: 05}'.replace(" ", "")
            return new_id
    return "#0001"

def generate_room_id():
    existing_room_ids = [room["ID"] for room in RoomAPI.get_rooms()]
    new_id = f'#{random.randint(1, 9999): 05}'.replace(" ", "")
    if new_id in existing_room_ids:
        generate_room_id()
    return new_id

def generate_user_id():
    existing_user_ids = [user["ID"] for user in CustomerAPI.get_users()]
    new_id = f'#{random.randint(1, 9999): 05}'.replace(" ", "")
    if new_id in existing_user_ids:
        generate_room_id()
    return new_id
    

if __name__ == "__main__":
    BookingAPI.connect_db()
    test_id = generate_booking_id()
    print(test_id)