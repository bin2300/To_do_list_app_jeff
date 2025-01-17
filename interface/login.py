import flet as ft
from APP.connection import Database
from APP.user import User

def login_page(page: ft.Page):
    db = Database()
    user_handler = User(db)

    email_field = ft.TextField(label="Email", hint_text="Enter your email", width=300)
    password_field = ft.TextField(label="Password", hint_text="Enter your password", width=300, password=True,can_reveal_password=True)

    def reset_banner():
        if page.banner:
            page.banner.open = False
            page.update()

    def handle_login(e):
        reset_banner()
        email = email_field.value
        password = password_field.value

        success, result = user_handler.authenticate_user(email, password)
        if success:
            page.client_storage.set("user_id", result)  # Stocke l'ID utilisateur dans le stockage local
            print(f"{page.client_storage.get("user_id")}")
            page.go("/task_manager")  # Redirige vers la page de gestion des tâches
        else:
            page.banner = ft.Banner(
                content=ft.Row([
                    ft.Text(result),
                    ft.IconButton(
                        icon=ft.icons.COPY,
                        tooltip="Copy error message",
                        on_click=lambda _: page.set_clipboard(result)
                    )
                ]),
                bgcolor=ft.colors.RED,
                actions=[
                    ft.TextButton("Retry", on_click=lambda _: reset_banner()),
                ],
            )
            page.banner.open = True
            page.update()

    email_field.on_change = lambda _: reset_banner()
    password_field.on_change = lambda _: reset_banner()

    return ft.View(
        "/login",
        controls=[
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("LOGIN", size=30, weight=ft.FontWeight.BOLD, font_family="Poppins", text_align=ft.TextAlign.CENTER),
                        email_field,
                        password_field,
                        ft.Row(
                            [
                                ft.Checkbox(label="Remember"),
                                ft.TextButton("No account? Sign Up", on_click=lambda _: page.go("/signup")),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            width=300,
                        ),
                        ft.ElevatedButton(
                            "Sign In",
                            width=300,
                            style=ft.ButtonStyle(
                                bgcolor=ft.colors.BLUE,
                                shape=ft.RoundedRectangleBorder(radius=2),
                                color=ft.colors.WHITE,
                            ),
                            on_click=handle_login,
                            height=50,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                width=page.window_width,
                height=page.window_height,
                bgcolor=ft.colors.WHITE,
                alignment=ft.alignment.center,
            )
        ],
    )
