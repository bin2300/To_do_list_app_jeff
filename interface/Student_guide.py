import flet as ft
from datetime import datetime, timedelta
from APP.task import Task  # Import de la classe Task
from APP.connection import db  # Connexion à la base de données

task_manager = Task(db)  # Instance pour gérer les tâches

def student_guide_view(page: ft.Page):
    page.window_padding = 0

    today = datetime.now()
    week_start = today - timedelta(days=today.weekday())
    week_days = [week_start + timedelta(days=i) for i in range(7)]
    
    def List_day_task(date) :
        pass

    def get_tasks_for_week():
        """Récupère les tâches pour chaque jour de la semaine."""
        user_id = page.client_storage.get("user_id")
        tasks_by_day = {day.strftime("%Y-%m-%d"): [] for day in week_days}

        for day in week_days:
            limit_date = day.strftime("%Y-%m-%d")
            tasks = task_manager.get_tasks_by_date(user_id, limit_date)
            tasks_by_day[limit_date] = tasks

        return tasks_by_day

    def build_timetable(tasks_by_day):
        """Construit un tableau d'affichage des tâches sous forme d'emploi du temps simplifié."""
        timetable_controls = []

        # Ligne d'en-tête avec les jours de la semaine
        header_row = ft.Row(
            controls=[
                ft.Text("", size=16, expand=True)
            ] + [
                ft.Text(
                    day.strftime("%A"),
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                    expand=True,
                )
                for day in week_days
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            spacing=20,
        )

        timetable_controls.append(header_row)

        # Création des lignes "morning" et "evening"
        for period in ["morning", "evening"]:
            row_controls = [
                ft.Text(period.capitalize(), size=16, expand=True, text_align=ft.TextAlign.CENTER)
            ]

            for day in week_days:
                date_str = day.strftime("%Y-%m-%d")
                tasks = [task for task in tasks_by_day[date_str] if ("AM" in task[3] if period == "morning" else "PM" in task[3])]
                
                task_texts = [f"- {task[0]} ({task[1]})" for task in tasks[:5]]  # Limite à 5 tâches
                content = ft.Text("\n".join(task_texts), size=14)
                
                row_controls.append(
                    ft.Container(
                        content=content,
                        padding=ft.padding.all(10),
                        bgcolor=ft.colors.LIGHT_BLUE if tasks else ft.colors.WHITE,
                        border_radius=5,
                        expand=True,
                        width=150,
                        height=120,
                    )
                )

            timetable_controls.append(
                ft.Row(
                    controls=row_controls,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    spacing=20,
                )
            )

        return timetable_controls

    def update_timetable():
        """Met à jour l'affichage de l'emploi du temps."""
        tasks_by_day = get_tasks_for_week()
        timetable.controls = build_timetable(tasks_by_day)
        date_range_text.value = f"Semaine du {week_days[0].strftime('%d/%m/%Y')} au {week_days[-1].strftime('%d/%m/%Y')}"
        page.update()

    timetable = ft.Column(spacing=20)

    date_range_text = ft.Text("", size=18, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)

    navigation_row = ft.Row(
        [
            ft.Container(
                content=ft.Icon(ft.icons.CHEVRON_LEFT, size=30),
                on_click=lambda e: navigate_week(-1),
            ),
            date_range_text,
            ft.Container(
                content=ft.Icon(ft.icons.CHEVRON_RIGHT, size=30),
                on_click=lambda e: navigate_week(1),
            ),
            ft.FloatingActionButton(
                icon=ft.icons.ADD,
                bgcolor=ft.colors.GREEN,
                on_click=lambda e: page.go("/create_task"),
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        spacing=20,
    )

    def navigate_week(offset):
        """Navigue entre les semaines et met à jour l'affichage."""
        nonlocal week_start, week_days
        week_start += timedelta(days=offset * 7)
        week_days = [week_start + timedelta(days=i) for i in range(7)]
        update_timetable()

    update_timetable()

    sidebar = ft.Container(
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
    )

    return ft.View(
        "/student_guide",
        padding=0,
        controls=[
            ft.Row(
                [
                    sidebar,
                    ft.Column(
                        [
                            navigation_row,
                            timetable,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        expand=True,
                        spacing=20,
                    ),
                ],
                spacing=0,
                expand=True,
            )
        ],
    )
