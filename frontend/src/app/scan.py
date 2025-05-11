import flet as ft
import os
import io
import csv
import json
from .menu import build_sidebar
from .utils import validate_fields, append_to_history


def scan_view(page):
    user = page.client_storage.get("user")
    user_name = user["name"] if user else "usuario"
    username_id = user["username"] if user else "desconocido"

    file_picker = ft.FilePicker()
    page.overlay.append(file_picker)

    # Elementos de la UI
    upload_result = ft.Text()
    error_message = ft.Text(color="red600")

    # Campos del formulario manual
    form_fields = [
        nombre_firewall := ft.TextField(
            label="Nombre del Firewall",
            hint_text="Ej: FirewallPrincipal",
            expand=True
        ),
        hostname := ft.TextField(
            label="Hostname",
            hint_text="Ej: fw01.empresa.com",
            expand=True
        ),
        version := ft.TextField(
            label="Versión",
            hint_text="Ej: 6.0.5",
            expand=True
        ),
        marca := ft.TextField(
            label="Marca",
            hint_text="Ej: Cisco, Fortinet",
            expand=True
        ),
        build := ft.TextField(
            label="Build",
            hint_text="Ej: 1234",
            expand=True
        ),
        location := ft.TextField(
            label="Ubicación",
            hint_text="Ej: Data Center Principal",
            expand=True
        ),
        grupo_id := ft.TextField(
            label="ID de Grupo",
            hint_text="Ej: GRP-001",
            expand=True
        )
    ]

    def handle_file_selection(e: ft.FilePickerResultEvent):
        try:
            if not e.files:
                upload_result.value = "Ningún archivo seleccionado."
                page.update()
                return

            selected_file = e.files[0]
            file_path = selected_file.path
            with open(file_path, "rb") as f:
                file_bytes = f.read()

            decoded = file_bytes.decode("utf-8")
            extension = os.path.splitext(selected_file.name)[1].lower()
            data = []

            if extension == ".csv":
                reader = csv.DictReader(io.StringIO(decoded))
                data = list(reader)
            elif extension == ".json":
                data = json.loads(decoded)
            else:
                error_message.value = "Solo se aceptan archivos .csv o .json"
                page.update()
                return

            print("📄 Encabezados detectados:", data[0].keys() if data else "vacío")

            if not validate_fields(data):
                error_message.value = "⚠️ El archivo no contiene todos los campos requeridos."
                page.update()
                return

            append_to_history(username_id, data)
            upload_result.value = f"✅ {selected_file.name} cargado con éxito. Registros: {len(data)}"
            error_message.value = ""
        except Exception as ex:
            error_message.value = f"❌ Error al procesar archivo: {ex}"
        page.update()

    def handle_manual_submission(e):
        try:
            # Crear diccionario con los datos del formulario
            manual_data = {
                "nombre_firewall": nombre_firewall.value,
                "hostname": hostname.value,
                "version": version.value,
                "marca": marca.value,
                "build": build.value,
                "location": location.value,
                "grupo_id": grupo_id.value
            }

            if validate_fields([manual_data]):
                append_to_history(username_id, [manual_data])

            # Validar campos vacíos
            if any(value.strip() == "" for value in manual_data.values()):
                error_message.value = "⚠️ Todos los campos son obligatorios"
                page.update()
                return

            # Validar estructura con la misma función que para archivos
            if not validate_fields([manual_data]):
                error_message.value = "⚠️ Los datos no cumplen con el formato requerido"
                page.update()
                return

            append_to_history(username_id, [manual_data])

            # Limpiar formulario y mostrar resultado
            for field in form_fields:
                field.value = ""

            upload_result.value = "✅ Registro manual agregado con éxito"
            error_message.value = ""

        except Exception as ex:
            error_message.value = f"❌ Error al agregar registro manual: {ex}"
        page.update()

    file_picker.on_result = handle_file_selection

    return ft.Column([
        ft.Row([
            ft.Container(build_sidebar(page), expand=False, height=page.height),
            ft.VerticalDivider(width=1),
            ft.Container(
                ft.Column([
                    ft.Text(f"Hola, {user_name}", size=22, weight=ft.FontWeight.BOLD),
                    ft.Text("Aquí podrás subir tu data o agregar registros manualmente:"),

                    # Sección de carga de archivo
                    ft.ElevatedButton(
                        "Subir archivo (.csv o .json)",
                        icon=ft.Icons.UPLOAD_FILE,
                        on_click=lambda _: file_picker.pick_files(
                            allowed_extensions=["csv", "json"],
                            allow_multiple=False,
                            file_type=ft.FilePickerFileType.CUSTOM
                        )
                    ),
                    upload_result,
                    error_message,
                    ft.Divider(height=20),

                    # Sección de formulario manual
                    ft.Text("Agregar registro manual:", size=18, weight=ft.FontWeight.BOLD),
                    ft.Column(
                        form_fields,
                        spacing=10
                    ),
                    ft.ElevatedButton(
                        "Guardar registro manual",
                        icon=ft.Icons.SAVE,
                        on_click=handle_manual_submission
                    )
                ], spacing=15),
                padding=30,
                expand=True
            )
        ], expand=True)
    ], expand=True)