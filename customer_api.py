from db_manager import DBManager

class CustomerAPI:
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

    # Fetches all customers from the DB table
    @classmethod
    def get_users(cls):
        cls.cursor.execute("SELECT * FROM customers")
        bookings = cls.cursor.fetchall()
        return bookings
    
    # Fetches a particular customer given the id
    @classmethod
    def fetch_customer_by_id(cls, user_id):
        cls.cursor.execute(f"SELECT * FROM customers WHERE \"ID\" = %s", (user_id, ))
        customer = cls.cursor.fetchone()
        return customer

    # Adds a customer record to the database
    @classmethod
    def add_customer(cls, customer_id, name, email):
        cls.cursor.execute(
            """
            INSERT INTO customers (
                "ID", name, email
            ) VALUES (%s, %s, %s)
            """, (customer_id, name, email)
        )

        return True
    
    # Makes changes to a customer record
    @classmethod
    def modify_customer(cls, customer_id, field, value):
        cls.cursor.execute(
            f"UPDATE customers SET {field} = %s WHERE ID = %s", (value, customer_id)
        )
    
    # Deletes the customer record from the database
    @classmethod
    def delete_customer(cls, customer_id):
        cls.cursor.execute(
            f"DELETE FROM customers WHERE ID = %s", customer_id
        )

    # Deletes all customers from the database
    @classmethod
    def delete_all_customers(cls):
        cls.cursor.execute(
            f"DELETE FROM customers"
        )