import flet as ft
from APP.task import Task  # Import de la classe Task
from APP.connection import db  # Connexion à la base de données

task_manager = Task(db)  # Instance pour gérer les tâches

def history_view(page: ft.Page):
    user_id = page.client_storage.get("user_id")

    # Récupération des statistiques
    def get_task_statistics():
        total_tasks = len(task_manager.get_tasks_by_status(user_id, "pending")) + len(task_manager.get_tasks_by_status(user_id, "completed"))
        completed_tasks = len(task_manager.get_tasks_by_status(user_id, "completed"))
        pending_tasks = len(task_manager.get_tasks_by_status(user_id, "pending"))
        return total_tasks, completed_tasks, pending_tasks

    # Chargement des tâches
    def load_task_history():
        tasks_completed = task_manager.get_tasks_by_status(user_id, "completed")
        tasks_pending = task_manager.get_tasks_by_status(user_id, "pending")
        task_rows = []

        # Ajouter les tâches complétées
        for index, task in enumerate(tasks_completed, start=1):
            name, note, status, limit_date = task
            task_rows.append(
                ft.Row(
                    [
                        ft.Text(f"{index}.", size=16, color=ft.colors.BLACK),
                        ft.Checkbox(value=True, disabled=True),
                        ft.Text(name, size=16, color=ft.colors.BLACK, expand=True),
                        ft.Text(limit_date, size=14, color=ft.colors.GREY),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=10,
                )
            )

        # Ajouter les tâches non complétées
        start_index = len(tasks_completed) + 1
        for index, task in enumerate(tasks_pending, start=start_index):
            name, note, status, limit_date = task
            task_rows.append(
                ft.Row(
                    [
                        ft.Text(f"{index}.", size=16, color=ft.colors.BLACK),
                        ft.Checkbox(value=False, disabled=True),
                        ft.Text(name, size=16, color=ft.colors.BLACK, expand=True),
                        ft.Text(limit_date, size=14, color=ft.colors.GREY),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=10,
                )
            )
        return task_rows

    # Calcul des statistiques
    total_tasks, completed_tasks, pending_tasks = get_task_statistics()

    # Barre latérale
    sidebar = ft.Container(
        width=50,
        height=page.window_height,
        bgcolor=ft.colors.LIGHT_BLUE,
        content=ft.Column(
            [
                ft.IconButton(
                    icon=ft.icons.HOME,
                    icon_size=30,
                    icon_color="black",
                    on_click=lambda e: page.go("/history"),
                ),
                ft.IconButton(
                    icon=ft.icons.LIST,
                    icon_size=30,
                    icon_color="black",
                    on_click=lambda e: page.go("/task_manager"),
                ),
                ft.IconButton(
                    icon=ft.icons.SETTINGS,
                    icon_size=30,
                    icon_color="black",
                    on_click=lambda e: page.go("/settings"),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        ),
    )

    # En-tête
    header = ft.Row(
        [
            ft.Container(
                content=ft.Text(
                    "Historique des Tâches",
                    size=25,
                    weight=ft.FontWeight.BOLD,
                    color="black",
                ),
                margin=ft.margin.only(left=20),
                expand=1,
            ),
            ft.IconButton(
                ft.icons.ACCOUNT_CIRCLE,
                icon_size=40,
                on_click=lambda e: page.go("/notifications")
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        height=70,
    )

    # Cartes de statistiques
    stats_cards = ft.Row(
        [
            ft.Container(
                width=400,
                height=150,
                bgcolor="#F0F4F7",
                content=ft.Row(
                    [
                        ft.Icon(ft.icons.TASK_ALT, size=50, color="black"),
                        ft.Column(
                            [
                                ft.Text(f"{total_tasks}", size=30, weight=ft.FontWeight.BOLD),
                                ft.Text("Total Tasks"),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ],
                    spacing=20,
                ),
                padding=ft.padding.all(20),
            ),
            ft.Container(
                width=400,
                height=150,
                bgcolor="#E1F7E7",
                content=ft.Row(
                    [
                        ft.Icon(ft.icons.CHECK_CIRCLE_OUTLINE, size=50, color="#0DD2B3"),
                        ft.Column(
                            [
                                ft.Text(f"{completed_tasks}", size=30, weight=ft.FontWeight.BOLD),
                                ft.Text("Completed Tasks"),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ],
                    spacing=20,
                ),
                padding=ft.padding.all(20),
            ),
            ft.Container(
                width=400,
                height=150,
                bgcolor="#FEE2E2",
                content=ft.Row(
                    [
                        ft.Icon(ft.icons.CHECK_BOX_OUTLINE_BLANK, size=50, color="#FF6B6B"),
                        ft.Column(
                            [
                                ft.Text(f"{pending_tasks}", size=30, weight=ft.FontWeight.BOLD),
                                ft.Text("Pending Tasks"),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ],
                    spacing=20,
                ),
                padding=ft.padding.all(20),
            ),
        ],
        alignment=ft.MainAxisAlignment.START,
        spacing=20,
    )

    # Historique des tâches
    history_section = ft.Container(
        content=ft.Column(
            load_task_history(),
            spacing=10,
        ),
        padding=10,
    )

    # Pagination
    pagination = ft.Row(
        [
            ft.Icon(ft.icons.CHEVRON_LEFT, size=30, color="black"),
            ft.Text("1", size=20, weight=ft.FontWeight.BOLD),
            ft.Icon(ft.icons.CHEVRON_RIGHT, size=30, color="black"),
        ],
        alignment=ft.MainAxisAlignment.END,
        height=50,
    )

    # Contenu principal
    main_content = ft.Container(
        content=ft.Column(
            [
                header,
                stats_cards,
                history_section,
                pagination,
            ],
            spacing=20,
            expand=True,
        ),
        padding=15,
    )

    # Disposition globale
    return ft.View(
        route="/history",
        padding=0,
        controls=[
            ft.Row(
                [
                    sidebar,
                    ft.Container(
                        content=main_content,
                        expand=True,
                    ),
                ],
                spacing=0,
                expand=True,
            )
        ],
    )
