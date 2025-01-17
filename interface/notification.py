import flet as ft
from datetime import datetime
from APP.notification import Notification
from APP.connection import db  # Connexion partagée à la base de données

notification_manager = Notification(db)

def create_notifications_view(page: ft.Page):
    # Récupérer l'utilisateur depuis le stockage local
    user_id = page.client_storage.get("user_id")
    
    if not user_id:
        page.snack_bar = ft.SnackBar(ft.Text("User not logged in."))
        page.snack_bar.open = True
        page.update()
        return

    # Récupérer les notifications de l'utilisateur
    success, notifications = notification_manager.get_notifications_by_user(int(user_id))
    if not success:
        page.snack_bar = ft.SnackBar(ft.Text(f"Error: {notifications}"))
        page.snack_bar.open = True
        page.update()
        return

    def mark_as_read(notification_id):
        """Marquer une notification comme lue."""
        success, message = notification_manager.mark_notification_as_read(notification_id)
        if success:
            page.snack_bar = ft.SnackBar(ft.Text("Notification marked as read."))
            page.snack_bar.open = True
            page.update()
        else:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {message}"))
            page.snack_bar.open = True
            page.update()
        refresh_notifications()

    def delete_notification(notification_id):
        """Supprimer une notification."""
        success, message = notification_manager.delete_notification(notification_id)
        if success:
            page.snack_bar = ft.SnackBar(ft.Text("Notification deleted."))
            page.snack_bar.open = True
            page.update()
        else:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {message}"))
            page.snack_bar.open = True
            page.update()
        refresh_notifications()

    def refresh_notifications():
        """Rafraîchir la liste des notifications."""
        page.go("/notifications")  # Recharge la vue des notifications

    # Générer les conteneurs pour chaque notification
    notification_items = [
        ft.Container(
            content=ft.Row(
                [
                    ft.Text(notification["message"], expand=True, color="black"),
                    ft.Container(
                        bgcolor="green" if notification["is_read"] else "red",
                        width=10,
                        height=10,
                        border_radius=10,
                    ),
                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.icons.CHECK,
                                icon_size=20,
                                tooltip="Mark as read",
                                on_click=lambda _, nid=notification["id_notification"]: mark_as_read(nid),
                            ),
                            ft.IconButton(
                                icon=ft.icons.DELETE,
                                icon_size=20,
                                tooltip="Delete notification",
                                on_click=lambda _, nid=notification["id_notification"]: delete_notification(nid),
                            ),
                        ],
                        spacing=5,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            bgcolor="#f0f0f0",
            padding=10,
            border_radius=5,
            margin=5,
        )
        for notification in notifications
    ]

    return ft.View(
        "/notifications",
        padding=0,
        controls=[
            ft.Row(
                [
                    # Barre latérale
                    ft.Container(
                        width=50,
                        bgcolor=ft.colors.LIGHT_BLUE,
                        content=ft.Column(
                            [
                                ft.IconButton(
                                    icon=ft.icons.HOME,
                                    icon_size=30,
                                    icon_color=ft.colors.BLACK,
                                    on_click=lambda e: page.go("/history"),
                                ),
                                ft.IconButton(
                                    icon=ft.icons.LIST,
                                    icon_size=30,
                                    icon_color=ft.colors.BLACK,
                                    on_click=lambda e: page.go("/task_manager"),
                                ),
                                ft.IconButton(
                                    icon=ft.icons.SETTINGS,
                                    icon_size=30,
                                    icon_color=ft.colors.BLACK,
                                    on_click=lambda e: page.go("/settings"),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            expand=True,
                            spacing=10,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                    ),

                    # Contenu principal avec la liste des notifications
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Column(
                                            [
                                                ft.Text(
                                                    "Notifications",
                                                    size=24,
                                                    weight=ft.FontWeight.BOLD,
                                                    color="black",
                                                ),
                                                ft.Text(
                                                    datetime.now().strftime("%d %B %Y"),
                                                    size=16,
                                                    color="black",
                                                ),
                                            ],
                                            spacing=0,
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                                ft.Column(notification_items, spacing=5),
                            ],
                        ),
                        expand=True,
                        padding=20,
                    ),
                ],
                expand=True,
                spacing=0,
            ),
        ],
    )
