import flet as ft

from .history import history_view
from .login import login_view
from .register import register_view
from .dashboard import dashboard_view
from .scan import scan_view
from flet import AppView

def launch_app():
    ft.app(target=main, view=AppView.FLET_APP)
# ft.app(target=main)

def main(page: ft.Page):
    page.title = "Flet Auth App"
    page.window_width = 480
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.bgcolor = "#f0f2f5"

    def route_change(e):
        page.views.clear()

        if page.route == "/":
            page.views.append(ft.View("/", [login_view(page)]))
        elif page.route == "/register":
            page.views.append(ft.View("/register", [register_view(page)]))
        elif page.route == "/dashboard":
            page.views.append(ft.View("/dashboard", [dashboard_view(page)]))
        elif page.route == "/scan":
            page.views.append(ft.View("/scan", [scan_view(page)]))
        elif page.route == "/history":  # Nueva ruta
            page.views.append(ft.View("/history", [history_view(page)]))

        page.update()

    page.on_route_change = route_change
    page.go("/")
