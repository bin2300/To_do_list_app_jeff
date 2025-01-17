import flet as ft
from datetime import datetime
from APP.task import Task
from APP.connection import db  # Import the database connection

task_manager = Task(db)  # Pass the database connection here


def edit_task_view(page: ft.Page):
    # Retrieve task ID from client storage
    task_id = page.client_storage.get("task_id")
    
    if not task_id:
        page.snack_bar = ft.SnackBar(ft.Text("Task ID is missing!"))
        page.snack_bar.open = True
        page.go("/task_manager")
        return

    # Fetch task details from the database
    try:
        task = task_manager.get_task_by_id(task_id)
        if not task:
            page.snack_bar = ft.SnackBar(ft.Text("Task not found!"))
            page.snack_bar.open = True
            page.go("/task_manager")
            return
    except Exception as e:
        page.snack_bar = ft.SnackBar(ft.Text(f"Error retrieving task: {e}"))
        page.snack_bar.open = True
        page.go("/task_manager")
        return

    # Populate fields with task data
    label_field = ft.TextField(
        label="Task Label",
        filled=True,
        bgcolor="#F0F4F7",
        value=task["name_task"]
    )

    deadline_field = ft.TextField(
        label="Deadline (YYYY-MM-DD)",
        filled=True,
        bgcolor="#F0F4F7",
        value=task["limit_date"]
    )

    note_field = ft.TextField(
        label="Notes",
        filled=True,
        bgcolor="#F0F4F7",
        multiline=True,
        height=200,
        value=task["note_task"]
    )

    def save_task(_):
        # Retrieve field values
        label = label_field.value.strip()
        deadline = deadline_field.value.strip()
        note = note_field.value.strip()

        # Validate fields
        if not label:
            page.snack_bar = ft.SnackBar(ft.Text("Task label is required!"))
            page.snack_bar.open = True
            page.update()
            return

        try:
            # Validate deadline format
            datetime.strptime(deadline, "%Y-%m-%d")
        except ValueError:
            page.snack_bar = ft.SnackBar(ft.Text("Invalid date format. Use YYYY-MM-DD."))
            page.snack_bar.open = True
            page.update()
            return

        try:
            # Update task in the database
            task_manager.update_task(
                task_id=task_id,
                name_task=label,
                note_task=note,
                limit_date=deadline
            )

            # Notify user and navigate back
            page.snack_bar = ft.SnackBar(ft.Text("Task updated successfully!"))
            page.snack_bar.open = True
            page.go("/task_manager")
        except Exception as e:
            # Handle any other errors
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {e}"))
            page.snack_bar.open = True
            page.update()

    return ft.View(
        "/edit_task",
        padding=0,
        controls=[
            ft.Row(
                [
                    ft.Container(
                        width=300,
                        height=page.height,
                        bgcolor="#E7E342",
                        content=ft.Column(
                            [
                                ft.ElevatedButton(
                                    "Go Back",
                                    style=ft.ButtonStyle(
                                        bgcolor="white",
                                        color="black",
                                        shape=ft.RoundedRectangleBorder(radius=8),
                                    ),
                                    on_click=lambda _: page.go("/task_manager"),
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
                                            "UPDATE TASK",
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
                                label_field,
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
