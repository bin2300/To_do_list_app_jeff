import sqlite3
import os

USER_TABLE = "user"
TASK_TABLE = "task"
NOTIFICATION_TABLE = "notification"
USER_ID = "id_user"

class Database:
    def __init__(self, db_name="DATA/exemple.db"):
        folder_path = os.path.dirname(db_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        self.db_name = db_name
        
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        # Création des tables si elles n'existent pas
        self.create_tables()

    def create_tables(self):
        try:
            self.cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {USER_TABLE} (
                    {USER_ID} INTEGER PRIMARY KEY AUTOINCREMENT, 
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    password TEXT NOT NULL,
                    creation_date TEXT NOT NULL
                )
            ''')
            self.cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {TASK_TABLE} (
                    id_task INTEGER PRIMARY KEY AUTOINCREMENT, 
                    id_user INTEGER NOT NULL,
                    name_task TEXT NOT NULL,
                    note_task TEXT,
                    status_task TEXT NOT NULL,          
                    limit_date TEXT NOT NULL
                )
            ''')
            self.cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {NOTIFICATION_TABLE} (
                    id_notification INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_user INTEGER NOT NULL,
                    message TEXT NOT NULL,
                    is_read INTEGER DEFAULT 0, -- 0 = non lu, 1 = lu
                    creation_date TEXT NOT NULL,
                    FOREIGN KEY (id_user) REFERENCES {USER_TABLE} ({USER_ID})
                )
            ''')
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Erreur lors de la création des tables: {e}")
    
    def close_connection(self):
        self.conn.close()

# Instanciation de la base de données et création des tables
db = Database()
