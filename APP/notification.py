from datetime import datetime

class Notification:
    def __init__(self, database_connection):
        self.database_connection = database_connection

    def create_notification(self, user_id, message):
        """Créer une nouvelle notification pour un utilisateur."""
        creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            self.database_connection.cursor.execute('''
                INSERT INTO notification (id_user, message, is_read, creation_date)
                VALUES (?, ?, 0, ?)
            ''', (user_id, message, creation_date))
            self.database_connection.conn.commit()
            return True, "Notification created successfully."
        except Exception as e:
            print(f"Database Error: {e}")
            return False, str(e)

    def get_notifications_by_user(self, user_id, only_unread=False):
        """Récupérer les notifications d'un utilisateur.
        Si `only_unread` est True, ne renvoie que les notifications non lues.
        """
        try:
            if only_unread:
                self.database_connection.cursor.execute('''
                    SELECT id_notification, message, is_read, creation_date 
                    FROM notification WHERE id_user = ? AND is_read = 0
                    ORDER BY creation_date DESC
                ''', (user_id,))
            else:
                self.database_connection.cursor.execute('''
                    SELECT id_notification, message, is_read, creation_date 
                    FROM notification WHERE id_user = ?
                    ORDER BY creation_date DESC
                ''', (user_id,))
            notifications = self.database_connection.cursor.fetchall()
            return True, [
                {"id_notification": n[0], "message": n[1], "is_read": n[2], "creation_date": n[3]}
                for n in notifications
            ]
        except Exception as e:
            print(f"Database Error: {e}")
            return False, str(e)

    def mark_notification_as_read(self, notification_id):
        """Marquer une notification comme lue."""
        try:
            self.database_connection.cursor.execute('''
                UPDATE notification SET is_read = 1 WHERE id_notification = ?
            ''', (notification_id,))
            self.database_connection.conn.commit()
            return True, "Notification marked as read."
        except Exception as e:
            print(f"Database Error: {e}")
            return False, str(e)

    def delete_notification(self, notification_id):
        """Supprimer une notification."""
        try:
            self.database_connection.cursor.execute('''
                DELETE FROM notification WHERE id_notification = ?
            ''', (notification_id,))
            self.database_connection.conn.commit()
            return True, "Notification deleted successfully."
        except Exception as e:
            print(f"Database Error: {e}")
            return False, str(e)
