import json

class Task:
    def __init__(self, database_connection):
        self.database_connection = database_connection

    def create_task(self, id_user, name_task, note_task, status_task, limit_date):
        try:
            self.database_connection.cursor.execute('''
                INSERT INTO task (id_user, name_task, note_task, status_task, limit_date)
                VALUES (?, ?, ?, ?, ?)
            ''', (id_user, name_task, note_task, status_task, limit_date))
            self.database_connection.conn.commit()
        except Exception as e:
            raise ValueError(f"Failed to create task: {e}")

    def get_tasks_by_date(self, id_user, date):
        try:
            self.database_connection.cursor.execute('''
                SELECT name_task, note_task, status_task, limit_date, id_task
                FROM task 
                WHERE id_user = ? AND limit_date = ?
            ''', (id_user, date))
            
            return self.database_connection.cursor.fetchall()
        
        except Exception as e:
            raise ValueError(f"Failed to retrieve tasks by date: {e}")

    def get_tasks_by_status(self, id_user, status):
        """Récupère les tâches d'un utilisateur en fonction de leur statut."""
        try:
            self.database_connection.cursor.execute('''
                SELECT name_task, note_task, status_task, limit_date 
                FROM task 
                WHERE id_user = ? AND status_task = ?
            ''', (id_user, status))
            return self.database_connection.cursor.fetchall()
        except Exception as e:
            raise ValueError(f"Failed to retrieve tasks by status: {e}")

    def delete_task(self, id_user, name_task, limit_date):
        """Supprime une tâche spécifique de l'utilisateur."""
        try:
            self.database_connection.cursor.execute('''
                DELETE FROM task 
                WHERE id_user = ? AND name_task = ? AND limit_date = ?
            ''', (id_user, name_task, limit_date))
            self.database_connection.conn.commit()
        except Exception as e:
            raise ValueError(f"Failed to delete task: {e}")

    def update_task_status(self, user_id, task_name, limit_date, status):
        """Met à jour le statut d'une tâche."""
        try:
            query = """
                UPDATE task
                SET status_task = ?
                WHERE id_user = ? AND name_task = ? AND limit_date = ?
            """
            self.database_connection.cursor.execute(
                query, 
                ("completed" if status else "pending", user_id, task_name, limit_date)
            )
            self.database_connection.conn.commit()
        except Exception as e:
            raise ValueError(f"Failed to update task status: {e}")

    def get_tasks_as_dict(self, user_id):
        """Retourne les tâches sous forme de dictionnaire JSON."""
        try:
            self.database_connection.cursor.execute('''
                SELECT name_task, note_task, status_task, limit_date ,  id_task 
                FROM task 
                WHERE id_user = ?
            ''', (user_id,))
            tasks = self.database_connection.cursor.fetchall()
            return [
                {"name_task": task[0], "note_task": task[1], "status_task": task[2], "limit_date": task[3], "task_id": task[4]}
                for task in tasks
            ]
        except Exception as e:
            raise ValueError(f"Failed to retrieve tasks: {e}")

    def export_tasks_to_json(self, user_id, file_path="save.json"):
        """Exporte les tâches de l'utilisateur vers un fichier JSON."""
        try:
            tasks_list = self.get_tasks_as_dict(user_id)

            # Écrire les données dans un fichier JSON
            with open(file_path, 'w') as json_file:
                json.dump(tasks_list, json_file, indent=4)

            return True, f"Tasks exported successfully to {file_path}."
        except Exception as e:
            return False, str(e)

    def get_tasks_by_user(self, user_id):
        """Récupère toutes les tâches d'un utilisateur donné."""
        try:
            self.database_connection.cursor.execute('''
                SELECT name_task, note_task, status_task, limit_date 
                FROM task 
                WHERE id_user = ?
            ''', (user_id,))
            tasks = self.database_connection.cursor.fetchall()
            return [
                {"name_task": task[0], "note_task": task[1], "status_task": task[2], "limit_date": task[3]}
                for task in tasks
            ]
        except Exception as e:
            raise ValueError(f"Failed to retrieve tasks for user {user_id}: {e}")
    # fonction pour mettre les taches a jour
    def update_task(self, task_id, name_task, note_task, limit_date):
        """Met à jour une tâche spécifique."""
        try:
            query = """
                UPDATE task
                SET name_task = ?, note_task = ?, limit_date = ?
                WHERE id_task = ?
            """
            self.database_connection.cursor.execute(query, (name_task, note_task, limit_date, task_id))
            self.database_connection.conn.commit()
        except Exception as e:
            raise ValueError(f"Failed to update task: {e}")


    def get_task_by_id(self, task_id):
        """Récupère les détails d'une tâche spécifique par son ID."""
        try:
            query = "SELECT name_task, note_task, limit_date FROM task WHERE id_task = ?"
            self.database_connection.cursor.execute(query, (task_id,))
            task = self.database_connection.cursor.fetchone()
            if task:
                return {"name_task": task[0], "note_task": task[1], "limit_date": task[2]}
            else:
                raise ValueError(f"No task found with id {task_id}.")
        except Exception as e:
            raise ValueError(f"Failed to retrieve task: {e}")

