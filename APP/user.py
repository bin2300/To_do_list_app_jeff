from datetime import datetime
import re
import hashlib


class User:
    def __init__(self, database_connection):
        self.database_connection = database_connection

    @staticmethod
    def hash_password(password):
        """Hash a password using SHA256."""
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def validate_user_data(self, name, email, password):
        """Validate user data with basic rules."""
        if not name or len(name) < 3:
            return False, "Name must be at least 3 characters long."
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            return False, "Invalid email format."
        if password and len(password) < 6:
            return False, "Password must be at least 6 characters long."
        return True, ""

    def create_user(self, name, email, password):
        """Create a new user."""
        is_valid, message = self.validate_user_data(name, email, password)
        if not is_valid:
            return False, message

        # Hash the password before storing it
        hashed_password = self.hash_password(password)
        creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            self.database_connection.cursor.execute('''
                INSERT INTO user (name, email, password, creation_date)
                VALUES (?, ?, ?, ?)
            ''', (name, email, hashed_password, creation_date))
            self.database_connection.conn.commit()
            return True, "User created successfully."
        except Exception as e:
            print(f"Database Error: {e}")
            return False, str(e)

    def authenticate_user(self, email, password):
        """Authenticate user by email and password."""
        try:
            # Hash the input password to compare with stored hash
            hashed_password = self.hash_password(password)
            self.database_connection.cursor.execute('''
                SELECT id_user FROM user WHERE email = ? AND password = ?
            ''', (email, hashed_password))
            user = self.database_connection.cursor.fetchone()
            if user:
                return True, user[0]  # Return True and the user ID
            else:
                return False, "Invalid email or password."
        except Exception as e:
            print(f"Database Error: {e}")
            return False, str(e)

    def update_user(self, user_id, name=None, email=None, password=None):
        """Update user information."""
        updates = []
        params = []

        if name:
            updates.append("name = ?")
            params.append(name)
        if email:
            updates.append("email = ?")
            params.append(email)
        if password:
            # Hash the password before updating it
            hashed_password = self.hash_password(password)
            updates.append("password = ?")
            params.append(hashed_password)

        if not updates:
            return False, "No updates provided."

        params.append(user_id)
        query = f"UPDATE user SET {', '.join(updates)} WHERE id_user = ?"

        try:
            self.database_connection.cursor.execute(query, tuple(params))
            self.database_connection.conn.commit()
            return True, "User information updated successfully."
        except Exception as e:
            print(f"Database Error: {e}")
            return False, str(e)

    def get_user_by_id(self, user_id):
        """Fetch user information by ID."""
        try:
            self.database_connection.cursor.execute('''
                SELECT name, email, creation_date FROM user WHERE id_user = ?
            ''', (user_id,))
            user = self.database_connection.cursor.fetchone()
            if user:
                return True, {"name": user[0], "email": user[1], "creation_date": user[2]}
            else:
                return False, "User not found."
        except Exception as e:
            print(f"Database Error: {e}")
            return False, str(e)
