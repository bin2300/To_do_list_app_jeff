import flet as ft
from datetime import datetime, timedelta
from APP.task import Task  # Import de la classe Task
from APP.connection import db  # Connexion à la base de données
from APP.notification import Notification

task_manager = Task(db)  # Instance pour gérer les tâches
notification_manager = Notification(db)
def task_manager_view(page: ft.Page):
    page.window_padding = 0

    today = datetime.now()
    selected_date = today
    week_start = today - timedelta(days=today.weekday())
    week_days = [week_start + timedelta(days=i) for i in range(7)]

    def update_calendar():
        calendar_row.controls.clear()  # Réinitialiser la ligne du calendrier
        for day in week_days:
            is_today = day.date() == today.date()  # Vérifier si c'est aujourd'hui
            is_selected = day == selected_date  # Vérifier si c'est le jour sélectionné
            calendar_row.controls.append(
                ft.Container(
                    content=ft.Text(
                        f"{day.strftime('%a')}\n{day.day}",
                        size=16,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.colors.WHITE if is_today or is_selected else ft.colors.BLACK,  # Mettre la couleur du texte en fonction de la sélection
                    ),
                    padding=ft.padding.all(8),
                    bgcolor=ft.colors.BLUE if is_today or is_selected else ft.colors.WHITE,  # Mettre la couleur du fond en bleu si c'est le jour sélectionné
                    width=170,
                    height=130,
                    alignment=ft.alignment.center,
                    border_radius=5,
                    on_click=lambda e, date=day: select_day(date),  # Sélectionner le jour
                )
            )
        page.update()


    def select_day(date):
        nonlocal selected_date
        selected_date = date  # Mettre à jour le jour sélectionné
        page.client_storage.set("selected_date", selected_date.strftime("%Y-%m-%d"))
        update_title()  # Mettre à jour le titre avec la nouvelle date
        update_calendar()  # Mettre à jour le calendrier
        get_tasks_for_selected_date()  # Mettre à jour les tâches pour ce jour

    def update_title():
        # Met à jour le titre avec la date sélectionnée
        title_column.controls[0].value = selected_date.strftime("%B %d")
        title_column.controls[1].value = selected_date.strftime("%A")
        page.update()

    def edit_task(task,task_id):
        # name, note, status, limit_date,id_task = task
        page.client_storage.set("task_id", task_id)
   
        page.go("/edit_task")  # Redirection vers la vue d'édition


    def navigate_week(offset):
        nonlocal week_days
        week_days = [day + timedelta(days=offset * 7) for day in week_days]
        update_calendar()

    def show_date_picker(e):
        def on_date_selected(event):
            nonlocal selected_date
            if event.data:
                selected_date = datetime.fromisoformat(event.data).date()  # Utilisation de fromisoformat pour gérer la date sans l'heure
                print(f"Date sélectionnée : {selected_date.strftime('%Y-%m-%d')}")  # Affiche la date dans le terminal
                select_day(selected_date)  # Sélectionner le jour et mettre à jour l'UI

        date_picker = ft.DatePicker(
            first_date=today - timedelta(days=365),
            last_date=today + timedelta(days=365),
            on_change=on_date_selected,
        )
        page.open(date_picker)  # Utilisez `page.open()` au lieu de `date_picker.open()`
        page.update()  # Mettre à jour la page pour afficher le DatePicker

    def delete_task(name_task):
        user_id = page.client_storage.get("user_id")
        limit_date = page.client_storage.get("selected_date")
        task_manager.delete_task(user_id, name_task, limit_date)
        notification_manager.create_notification(user_id=int(user_id),message=f"Task {name_task} Destroy Succesful")
        get_tasks_for_selected_date()

    def toggle_task_status(task_name, new_status):
        user_id = page.client_storage.get("user_id")
        limit_date = page.client_storage.get("selected_date")
        task_manager.update_task_status(user_id, task_name, limit_date, new_status)
        notification_manager.create_notification(user_id=int(user_id),message=f"Task {task_name} toggle Succesful")
        get_tasks_for_selected_date()

    def get_tasks_for_selected_date():
        user_id = page.client_storage.get("user_id")
        limit_date = page.client_storage.get("selected_date")
        tasks = task_manager.get_tasks_by_date(user_id, limit_date)
        print(f"DU poiint de vue de task_manager :{tasks}")
        task_list.controls.clear()
        if not tasks:
            print("Step completed")
            task_list.controls.append(
                ft.Text("Aucune tâche disponible.", size=16, color=ft.colors.BLACK, text_align=ft.TextAlign.CENTER)
            )
        else:
            print("Step completed")
            for task in tasks:
                name, note, status,date_task,id_task = task
                print(name, note, status,id_task)
                color = ft.colors.YELLOW if status == "pending" else ft.colors.RED

                task_list.controls.append(
                    ft.Row(
                        [
                            ft.Checkbox(
                                value=status == "completed",
                                on_change=lambda e, task_name=name: toggle_task_status(task_name, e.control.value),
                            ),
                            ft.Text("9 PM", size=16, color=ft.colors.BLACK),
                            ft.Text(name, size=16, color=ft.colors.BLACK, expand=True),
                            ft.CircleAvatar(bgcolor=color, radius=10),
                            ft.IconButton(
                                icon=ft.icons.EDIT,
                                icon_color=ft.colors.BLUE,
                                on_click=lambda e, task=name,id_task_ = id_task: edit_task(task,id_task),
                            ),
                            ft.IconButton(
                                icon=ft.icons.DELETE,
                                icon_color=ft.colors.RED,
                                on_click=lambda e, task_name=name: delete_task(task_name),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        spacing=10,
                    )
                )

        page.update()

    task_list = ft.Column(spacing=10)

    title_column = ft.Column(
        [
            ft.Text(today.strftime("%B %d"), size=24, color=ft.colors.BLACK, weight=ft.FontWeight.BOLD),
            ft.Text(today.strftime("%A"), size=16, color=ft.colors.BLACK),
        ],
        spacing=0,
    )

    navigation_row = ft.Row(
        [
            ft.IconButton(
                icon=ft.icons.CHEVRON_LEFT,
                icon_size=30,
                icon_color=ft.colors.BLACK,
                on_click=lambda e: navigate_week(-1),
            ),
            ft.IconButton(
                icon=ft.icons.CALENDAR_MONTH,
                icon_size=30,
                icon_color=ft.colors.BLACK,
                on_click=show_date_picker,  # Ajout du bouton Calendrier
            ),
            ft.IconButton(
                icon=ft.icons.CHEVRON_RIGHT,
                icon_size=30,
                icon_color=ft.colors.BLACK,
                on_click=lambda e: navigate_week(1),
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    calendar_row = ft.Row(spacing=5, alignment=ft.MainAxisAlignment.START)
    update_calendar()  # Initialisation du calendrier

    task_container = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("Tasks", size=20, color=ft.colors.BLACK, weight=ft.FontWeight.BOLD, expand=True),
                        ft.FloatingActionButton(icon=ft.icons.ADD, bgcolor=ft.colors.BLUE, on_click=lambda e: page.go("/create_task")),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                task_list,
            ],
            spacing=20,
        ),
        padding=20,
    )

    get_tasks_for_selected_date()

    return ft.View(
        "/task_manager",
        padding=0,
        controls=[
            ft.Row(
                [
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
                    ft.Column(
                        [
                            ft.Container(
                                content=ft.Row(
                                    [title_column, navigation_row],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                                padding=ft.padding.symmetric(vertical=10, horizontal=10),
                                border_radius=5,
                            ),
                            calendar_row,
                            task_container,
                        ],
                        expand=True,
                        spacing=20,
                    ),
                ],
                spacing=0,
                expand=True,
            )
        ]
    )
