import flet as ft
from datetime import datetime

from APP.task import Task
from APP.notification import Notification  # Importer la classe Notification
from APP.connection import db  # Assurez-vous que cette connexion est partagée

task_manager = Task(db)
notification_manager = Notification(db)  # Instancier la gestion des notifications

def create_task_view(page: ft.Page):
    # Récupérer l'utilisateur et la date par défaut depuis le stockage local
    user_id = page.client_storage.get("user_id")
    default_date = page.client_storage.get("selected_date")

    if not default_date:
        default_date = datetime.now().strftime("%Y-%m-%d")

    # Gestion des champs de saisie
    name_field = ft.TextField(label="Task Name", filled=True, bgcolor="#F0F4F7")
    note_field = ft.TextField(
        label="Note",
        filled=True,
        bgcolor="#F0F4F7",
        multiline=True,
        height=200,
    )
    deadline_field = ft.TextField(
        label="Date of Deadline",
        filled=True,
        bgcolor="#F0F4F7",
        value=default_date,
    )

    def save_task(_):
        name = name_field.value.strip()
        note = note_field.value.strip()
        deadline = deadline_field.value.strip()

        # Valider les données
        if not name:
            page.snack_bar = ft.SnackBar(ft.Text("Task Name is required!"))
            page.snack_bar.open = True
            page.update()
            return

        try:
            # Vérifier le format de la date
            datetime.strptime(deadline, "%Y-%m-%d")
        except ValueError:
            page.snack_bar = ft.SnackBar(ft.Text("Invalid date format. Use YYYY-MM-DD."))
            page.snack_bar.open = True
            page.update()
            return

        # Créer la tâche dans la base de données
        try:
            task_manager.create_task(
                id_user=int(user_id),
                name_task=name,
                note_task=note,
                status_task="pending",  # Statut par défaut
                limit_date=deadline,
            )

            # Créer une notification pour l'utilisateur
            notification_manager.create_notification(
                user_id=int(user_id),
                message=f"New task '{name}' created with deadline {deadline}."
            )

            page.snack_bar = ft.SnackBar(ft.Text("Task added successfully!"))
            page.snack_bar.open = True
            page.go("/task_manager")
        except Exception as e:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {e}"))
            page.snack_bar.open = True
            page.update()

    return ft.View(
        "/create_task",
        padding=0,
        controls=[
            ft.Row(
                [
                    ft.Container(
                        width=300,
                        height=page.height,
                        bgcolor="#3498DB",
                        content=ft.Column(
                            [
                                ft.ElevatedButton(
                                    "Go to History",
                                    style=ft.ButtonStyle(
                                        bgcolor="white",
                                        color="black",
                                        shape=ft.RoundedRectangleBorder(radius=8),
                                    ),
                                    on_click=lambda _: page.go("/history"),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            spacing=20,
                        ),
                    ),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Text(
                                            "CREATE TASK",
                                            size=25,
                                            weight=ft.FontWeight.BOLD,
                                            color="black",
                                        ),
                                        ft.ElevatedButton(
                                            "Save",
                                            style=ft.ButtonStyle(
                                                bgcolor="blue",
                                                color="white",
                                                shape=ft.RoundedRectangleBorder(radius=0),
                                            ),
                                            height=40,
                                            width=100,
                                            on_click=save_task,
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                                name_field,
                                deadline_field,
                                note_field,
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=20,
                        ),
                        padding=30,
                        expand=True,
                        alignment=ft.alignment.center,
                    ),
                ],
                spacing=0,
                expand=True,
            )
        ],
    )
