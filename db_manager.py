import psycopg
import os

class DBManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        if not self.connection:
            try:
                self.connection = psycopg.connect(
                    dbname=self.db_name,
                    user=os.getenv("DB_USER", "postgres"),  
                    password=os.getenv("DB_PASSWORD", "password"),  
                    host=os.getenv("DB_HOST", "localhost"),
                    port=os.getenv("DB_PORT", 5432)
                )
                self.connection.autocommit = True
                self.cursor = self.connection.cursor(row_factory=psycopg.rows.dict_row)
            except psycopg.OperationalError as e:
                print(f"Error connecting to the database: {e}")
                self.connection = None

    def get_cursor(self):
        if not self.cursor:
            raise Exception(f"Database '{self.db_name}' not connected. Call connect() first.")
        return self.cursor

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            try:
                self.connection.close()
            except psycopg.Error as e:
                print(f"Error closing connection: {e}")
        self.connection = self.cursor = None

    def __del__(self):
        self.close()

