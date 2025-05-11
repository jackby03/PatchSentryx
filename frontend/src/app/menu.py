import flet as ft

def build_sidebar(page):
    def navigate(index):
        if index == 0:
            page.go("/dashboard")
        elif index == 1:
            page.go("/scan")
        elif index == 2:
            page.go("/history")
        elif index == 3:
            page.client_storage.clear()
            page.go("/")

    return ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        leading=ft.Icon(ft.Icons.APPS),
        destinations=[
            ft.NavigationRailDestination(icon=ft.Icons.DASHBOARD, label="Dashboard"),
            ft.NavigationRailDestination(icon=ft.Icons.QR_CODE_SCANNER, label="Escaneo"),
            ft.NavigationRailDestination(icon=ft.Icons.HISTORY, label="Historial"),
            ft.NavigationRailDestination(icon=ft.Icons.LOGOUT, label="Logout"),
        ],
        on_change=lambda e: navigate(e.control.selected_index),
        expand=True
    )
