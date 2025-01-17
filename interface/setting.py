import os
from datetime import datetime
import flet as ft
from APP.user import User
from APP.task import Task  # Import de la classe Task
from APP.connection import db

# Variable globale pour sauvegarder les données exportées
exported_data = None

def settings_view(page: ft.Page):
    global exported_data  # Indiquer que cette variable sera utilisée dans la fonction

    # Charger l'ID de l'utilisateur depuis le client storage
    current_user_id = page.client_storage.get("user_id")
    if not current_user_id:
        page.snack_bar = ft.SnackBar(ft.Text("User not logged in! Redirecting to login page."), bgcolor="red")
        page.snack_bar.open = True
        page.update()
        page.go("/login")
        return

    # Instancier les classes utilisateur et tâche
    user = User(db)
    task = Task(db)

    def save_changes(e):
        # Récupérer les nouvelles valeurs des champs
        name = name_field.value
        email = email_field.value
        password = password_field.value

        # Appeler la méthode pour mettre à jour les informations de l'utilisateur
        success, message = user.update_user(current_user_id, name, email, password)

        # Afficher un message de succès ou d'erreur
        if success:
            page.snack_bar = ft.SnackBar(ft.Text("Changes saved successfully!"), bgcolor="green")
        else:
            page.snack_bar = ft.SnackBar(ft.Text(message), bgcolor="red")
        page.snack_bar.open = True
        page.update()

    def export_tasks(e):
        """Exporte les tâches dans un fichier JSON et les sauvegarde dans une variable."""
        global exported_data

        # Obtenir les tâches de l'utilisateur
        tasks = task.get_tasks_by_user(current_user_id)

        if not tasks:
            page.snack_bar = ft.SnackBar(ft.Text("No tasks to export!"), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return

        # Convertir les tâches en JSON
        exported_data = tasks  # Sauvegarder les données dans la variable globale

        # Chemin de sauvegarde
        downloads_dir = os.path.expanduser("~/Planning")
        if not os.path.exists(downloads_dir):
            os.makedirs(downloads_dir)

        today_date = datetime.now().strftime("%Y-%m-%d")
        file_path = os.path.join(downloads_dir, f"Timetable_{today_date}_exported.json")

        # Sauvegarder dans le fichier
        success, message = task.export_tasks_to_json(current_user_id, file_path)

        if success:
            page.snack_bar = ft.SnackBar(ft.Text(f"Tasks exported to {file_path}"), bgcolor="green")
        else:
            page.snack_bar = ft.SnackBar(ft.Text(message), bgcolor="red")
        page.snack_bar.open = True
        page.update()

    # Pré-remplir les champs avec les données actuelles de l'utilisateur
    current_user_data = user.get_user_by_id(current_user_id)
    if not current_user_data:
        page.snack_bar = ft.SnackBar(ft.Text("User data not found!"), bgcolor="red")
        page.snack_bar.open = True
        page.update()
        return

    name_field = ft.TextField(value=current_user_data[1]["name"], height=50, bgcolor="#E0E0E0")
    email_field = ft.TextField(value=current_user_data[1]["email"], height=50, bgcolor="#E0E0E0")
    password_field = ft.TextField(value="***********", height=50, bgcolor="#E0E0E0", password=True, can_reveal_password=True)

    return ft.View(
        "/settings",
        padding=0,
        controls=[
            ft.Row(
                [
                    # Barre latérale
                    ft.Container(
                        width=50,
                        height=page.window_height,
                        bgcolor=ft.colors.LIGHT_BLUE,
                        content=ft.Column(
                            [
                                ft.Container(
                                    content=ft.Icon(ft.icons.HOME, size=30, color="black"),
                                    width=50,
                                    height=50,
                                    alignment=ft.alignment.center,
                                    border_radius=5,
                                    on_click=lambda e: page.go("/history")
                                ),
                                ft.Container(
                                    content=ft.Icon(ft.icons.LIST, size=30, color="black"),
                                    width=50,
                                    height=50,
                                    alignment=ft.alignment.center,
                                    border_radius=5,
                                    on_click=lambda e: page.go("/task_manager")
                                ),
                                ft.Container(
                                    content=ft.Icon(ft.icons.SETTINGS, size=30, color="black"),
                                    width=50,
                                    height=50,
                                    alignment=ft.alignment.center,
                                    border_radius=5,
                                    on_click=lambda e: page.go("/settings")
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=10,
                        ),
                    ),

                    # Conteneur principal avec séparation
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Text(
                                            "OTHER OPTION\nand Other options",
                                            size=24,
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                        ft.Text("Export", size=18, weight=ft.FontWeight.BOLD),
                                        ft.Container(
                                            content=ft.Text("Export to JSON", color="black", size=14),
                                            bgcolor="yellow",
                                            padding=ft.padding.symmetric(vertical=10, horizontal=20),
                                            border_radius=5,
                                            margin=ft.margin.only(top=20, bottom=10),
                                            width=200,
                                            on_click=export_tasks,
                                        ),
                                        ft.Text("Mail gestion", size=18, weight=ft.FontWeight.BOLD),
                                        ft.Container(
                                            content=ft.Text("Send mail", color="white", size=14),
                                            bgcolor="blue",
                                            padding=ft.padding.symmetric(vertical=10, horizontal=20),
                                            border_radius=5,
                                            margin=ft.margin.only(bottom=10),
                                            width=200,
                                        ),
                                        ft.Text("Other option", size=18, weight=ft.FontWeight.BOLD),
                                        ft.Container(
                                            content=ft.Text("Disconnect", color="white", size=14),
                                            bgcolor="red",
                                            padding=ft.padding.symmetric(vertical=10, horizontal=20),
                                            border_radius=5,
                                            margin=ft.margin.only(bottom=10),
                                            width=200,
                                            on_click=lambda e: page.go("/login")
                                        ),
                                        ft.Text("Reset option", size=18, weight=ft.FontWeight.BOLD),
                                        ft.Container(
                                            content=ft.Text("Destroy all data of account", color="white", size=14),
                                            bgcolor="red",
                                            padding=ft.padding.symmetric(vertical=10, horizontal=20),
                                            border_radius=5,
                                            margin=ft.margin.only(bottom=10),
                                        ),
                                    ],
                                    spacing=10,
                                ),
                                width=600,
                            ),
                            ft.VerticalDivider(width=1, color="black"),
                            ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Text(
                                            "Personal Data\nand Other options",
                                            size=24,
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                        ft.Text("Name", size=16),
                                        name_field,
                                        ft.Text("Password", size=16),
                                        password_field,
                                        ft.Text("Email", size=16),
                                        email_field,
                                        ft.Container(
                                            content=ft.Text("Save", size=14, color="white"),
                                            bgcolor="blue",
                                            padding=ft.padding.symmetric(vertical=10, horizontal=20),
                                            alignment=ft.alignment.center,
                                            border_radius=5,
                                            margin=ft.margin.only(top=20),
                                            on_click=save_changes
                                        ),
                                    ],
                                    spacing=10,
                                ),
                                width=500,
                                padding=ft.padding.all(20),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        expand=True,
                    ),
                ],
                spacing=0,
                expand=True,
            )
        ],
    )
