import flet as ft
from .auth import (
    user_exists, save_user, hash_password, validate_email, validate_password
)

def register_view(page):
    status = ft.Text("", color="red600")

    name = ft.TextField(label="Nombre", icon=ft.Icons.PERSON)
    lastname = ft.TextField(label="Apellidos", icon=ft.Icons.PEOPLE)
    email = ft.TextField(label="Correo", icon=ft.Icons.EMAIL)
    username = ft.TextField(label="Nombre de Usuario", icon=ft.Icons.PERSON_OUTLINE)
    password = ft.TextField(label="Contraseña", password=True, can_reveal_password=True)
    confirm_password = ft.TextField(label="Repetir Contraseña", password=True, can_reveal_password=True)

    def handle_register(e):
        if not all([name.value, lastname.value, email.value, username.value, password.value, confirm_password.value]):
            status.value = "Todos los campos son obligatorios."
        elif not validate_email(email.value):
            status.value = "Correo inválido."
        elif user_exists(username.value, email.value):
            status.value = "Usuario o correo ya existen."
        elif not validate_password(password.value):
            status.value = "Contraseña insegura (8-12 carac., A-Z, a-z, num, @)."
        elif password.value != confirm_password.value:
            status.value = "Las contraseñas no coinciden."
        else:
            save_user({
                "name": name.value,
                "lastname": lastname.value,
                "email": email.value,
                "username": username.value,
                "password": hash_password(password.value)
            })
            status.value = "Registro exitoso. ¡Inicia sesión!"
            status.color = "green"
            page.go("/")
        page.update()

    return ft.Container(
        ft.Column([
            ft.Text("Registrarse", size=24, weight=ft.FontWeight.BOLD),
            name, lastname, email, username,
            password, confirm_password,
            ft.ElevatedButton("Registrar", icon=ft.Icons.PERSON_ADD, on_click=handle_register),
            ft.TextButton("¿Ya tienes cuenta? Inicia sesión", on_click=lambda _: page.go("/")),
            status
        ], spacing=10),
        padding=30,
        border_radius=10,
        bgcolor="white",
        width=400
    )
