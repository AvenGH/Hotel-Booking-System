from api_classes.room_api import RoomAPI
from api_classes.booking_api import BookingAPI
from api_classes.customer_api import CustomerAPI
import util.generate_random_id as generate_random_id
import access_data as ad

rooms = ad.loadData("txt", "obj_files\\room_properties.json")

class AdminConsole:

    @classmethod
    def add_room(cls, roomno, roomtype, roomprice):
        if roomtype in rooms:
            budget = rooms[roomtype]["budget_range"]
            roomamenities = rooms[roomtype]["amenities"]
            max_capacity = rooms[roomtype]["max_capacity"]
        else:
            print("Error: Room type does not exist")
            return
        
        min_budget, max_budget = map(int, budget.split("-"))

        if min_budget <= roomprice <= max_budget:  
            RoomAPI.add_room(
                room_id = generate_random_id.generate_room_id(),
                room_no = roomno,
                room_type = roomtype,
                price = roomprice,
                available = True,
                amenities = roomamenities,
                max_capacity = max_capacity
            )
        else:
            print("Error: Price is not within specified budget range.")

    @classmethod
    def reset_room_status(cls, roomid):
        if roomid in [room["ID"] for room in RoomAPI.get_rooms()]:
            RoomAPI.modify_room(roomid, "available", True)
        else:
            print("Error: Room ID does not exist.")

    @classmethod
    def reset_all_rooms_and_bookings(cls):
        for roomid in [room["ID"] for room in RoomAPI.get_rooms()]:
            RoomAPI.modify_room(roomid, "available", True)
        BookingAPI.delete_all_bookings()

    
    @classmethod
    def delete_all_customers(cls):
        CustomerAPI.delete_all_customers()


if __name__ == "__main__":  
    RoomAPI.connect_db()
    BookingAPI.connect_db()
    AdminConsole.reset_all_rooms_and_bookings()