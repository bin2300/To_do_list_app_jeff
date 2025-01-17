import flet as ft
from APP.connection import Database
from APP.user import User

def signup_page(page: ft.Page):
    db = Database()
    user_handler = User(db)

    # Champs de saisie
    name_field = ft.TextField(label="Name", hint_text="Enter your name", width=300)
    email_field = ft.TextField(label="Email", hint_text="Enter your email", width=300)
    password_field = ft.TextField(label="Password", hint_text="Enter your password", width=300, password=True,can_reveal_password=True)

    # Réinitialisation des champs et bannières
    def reset_state():
        if page.banner:
            page.banner.open = False
            page.update()

    def handle_signup(e):
        reset_state()  # Ferme toute bannière existante

        # Récupération des valeurs
        name = name_field.value
        email = email_field.value
        password = password_field.value
        print(name, email, password)
        # Validation et création de l'utilisateur
        success, message = user_handler.create_user(name, email, password)
        if success:
            # En cas de succès, afficher un message vert et rediriger
            page.snack_bar = ft.SnackBar(ft.Text(message), bgcolor=ft.colors.GREEN)
            page.snack_bar.open = True
            page.update()
            page.go("/login")
        else:
            # En cas d'erreur, afficher une bannière rouge avec option de copier le message
            page.banner = ft.Banner(
                content=ft.Row([
                    ft.Text(message),
                    ft.IconButton(
                        icon=ft.icons.COPY,
                        tooltip="Copy error message",
                        on_click=lambda _: page.set_clipboard(message)
                    )
                ]),
                bgcolor=ft.colors.RED,
                actions=[
                    ft.TextButton("Retry", on_click=lambda _: page.banner.open),
                ],
            )
            page.banner.open = True
            page.update()

    # Détecter les changements dans les champs pour masquer les erreurs
    name_field.on_change = lambda _: reset_state()
    email_field.on_change = lambda _: reset_state()
    password_field.on_change = lambda _: reset_state()

    return ft.View(
        "/signup",
        controls=[
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("SIGN UP", size=30, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                        name_field,
                        email_field,
                        password_field,
                        ft.Row(
                            [
                                ft.Checkbox(label="Remember"),
                                ft.TextButton("Already have an account?", on_click=lambda _: page.go("/login")),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            width=300,
                        ),
                        ft.ElevatedButton(
                            "Sign Up",
                            width=300,
                            style=ft.ButtonStyle(
                                bgcolor=ft.colors.BLUE,
                                shape=ft.RoundedRectangleBorder(radius=2),
                                color=ft.colors.WHITE,
                            ),
                            on_click=handle_signup,
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
