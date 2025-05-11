import flet as ft
from .auth import verify_credentials, get_user_by_identifier

def login_view(page):
    status = ft.Text("", color="red600")

    username_or_email = ft.TextField(label="Usuario o Correo", icon=ft.Icons.PERSON)
    password = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, icon=ft.Icons.LOCK)

    def handle_login(e):
        if not username_or_email.value or not password.value:
            status.value = "Completa todos los campos."
        elif verify_credentials(username_or_email.value, password.value):
            print("Redirigiendo al dashboard...")
            user = get_user_by_identifier(username_or_email.value)
            page.client_storage.set("user", user)
            page.go("/dashboard")
            page.update()  # 🔥 Necesario para ejecutar navegación
            return
        else:
            status.value = "Credenciales incorrectas."
        page.update()

    return ft.Container(
        ft.Column([
            ft.Text("Iniciar Sesión", size=24, weight=ft.FontWeight.BOLD),
            username_or_email,
            password,
            ft.ElevatedButton("Entrar", icon=ft.Icons.LOGIN, on_click=handle_login),
            ft.TextButton("¿No tienes cuenta? Regístrate", on_click=lambda _: page.go("/register")),
            status
        ], spacing=12),
        padding=30,
        border_radius=10,
        bgcolor="white",
        width=400
    )
