from datetime import timedelta
from APP.task import Task
from APP.connection import db  # Import the database connection
import flet as ft

def get_week_days(today):
    week_start = today - timedelta(days=today.weekday())
    return [week_start + timedelta(days=i) for i in range(7)]

def update_calendar_ui(calendar_row, week_days, today, selected_date, select_day_callback):
    calendar_row.controls.clear()
    for day in week_days:
        is_today = day.date() == today.date()
        is_selected = day.date() == selected_date.date()
        calendar_row.controls.append(
            ft.Container(
                content=ft.Text(
                    f"{day.strftime('%a')}\n{day.day}",
                    size=16,
                    text_align=ft.TextAlign.CENTER,
                    color=ft.colors.WHITE if is_today or is_selected else ft.colors.BLACK,
                ),
                padding=ft.padding.all(8),
                bgcolor=ft.colors.BLUE if is_today or is_selected else ft.colors.WHITE,
                width=170,
                height=130,
                alignment=ft.alignment.center,
                border_radius=5,
                on_click=lambda e, date=day: select_day_callback(date),
            )
        )

def get_tasks(user_id, limit_date):
    task_manager = Task(db)  # Pass the database connection here
    return task_manager.get_tasks_by_date(user_id, limit_date)

def delete_task(user_id, task_name, limit_date, refresh_callback):
    task_manager = Task(db)  # Pass the database connection here
    task_manager.delete_task(user_id, task_name, limit_date)
    refresh_callback()

def toggle_task_status(user_id, task_name, limit_date, new_status, refresh_callback):
    task_manager = Task(db)  # Pass the database connection here
    task_manager.update_task_status(user_id, task_name, limit_date, new_status)
    refresh_callback()
