import flet as ft
from interface.login import login_page
from interface.signup import signup_page
from interface.History import history_view
from interface.task_manager import task_manager_view
from interface.setting import settings_view
from interface.new_task import create_task_view
from interface.notification import create_notifications_view
from interface.Student_guide import student_guide_view
from interface.edit_task import edit_task_view

def main(page: ft.Page):
    # Configuration initiale de la fenêtre
    page.padding = 0  # Suppression du padding
    page.margin = 0   # Suppression de la marge
    page.window_padding = 0  # Suppression du padding de la fenêtre
    page.window_margin = 0   # Suppression de la marge de la fenêtre

    # Fonction appelée lorsqu'une route change
    def route_change(route):
        print(f"Route changed to: {route}")
        page.views.clear()  # Effacer les vues précédentes

        # Correspondance des routes avec les vues
        routes = {
            "/login": login_page,
            "/signup": signup_page,
            "/history": history_view,
            "/task_manager": task_manager_view,
            "/settings": settings_view,
            "/create_task": create_task_view,
            "/notifications": create_notifications_view,
            "/student_guide": student_guide_view,
            "/edit_task": edit_task_view,
        }

        # Charger la vue correspondante ou afficher une erreur 404
        if page.route in routes:
            page.views.append(routes[page.route](page))
        else:
            page.views.append(
                ft.View(
                    route="404",
                    controls=[
                        ft.Text(
                            "404 - Page Not Found",
                            size=30,
                            weight=ft.FontWeight.BOLD,
                            color="red",
                        )
                    ],
                )
            )
        page.update()  # Appliquer les changements de vue

    # Fonction appelée lorsqu'une vue est fermée (pop)
    def view_pop(view):
        print(f"View popped: {view}")
        page.go("/login")  # Retourner à la page de connexion par défaut

    # Définition des événements de changement de route et de fermeture de vue
    page.on_route_change = route_change
    page.on_view_pop = view_pop

    # Navigation initiale vers la page de connexion
    page.go("/login")

ft.app(target=main)
