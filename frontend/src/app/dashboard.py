import flet as ft
from .menu import build_sidebar

def dashboard_view(page):
    return ft.Column([
        ft.Row([
            ft.Container(build_sidebar(page), expand=False, height=page.height),
            ft.VerticalDivider(width=1),
            ft.Container(
                ft.Column([
                    ft.Text("Bienvenido al Dashboard", size=24, weight=ft.FontWeight.BOLD),
                    ft.Text("Aquí irán tus estadísticas generales, gráficas, etc.")
                ], spacing=10),
                padding=20,
                expand=True
            )
        ], expand=True)
    ], expand=True)
