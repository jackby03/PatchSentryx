import flet as ft
from datetime import datetime
from .utils import HISTORY_FILE, read_json
from .menu import build_sidebar  # Asegúrate de tener este import

def history_view(page):
    user = page.client_storage.get("user")
    username_id = user["username"] if user else "desconocido"

    # Contenedor principal
    main_column = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO)

    # Componentes de filtrado
    search_field = ft.TextField(
        label="Buscar por nombre de firewall",
        prefix_icon=ft.Icons.SEARCH,
        on_change=lambda e: update_display(),
        expand=True
    )

    date_picker = ft.DatePicker()
    page.overlay.append(date_picker)

    selected_date = ft.Text()

    def update_date_display(e):
        if date_picker.value:
            selected_date.value = date_picker.value.strftime("%Y-%m-%d")
        else:
            selected_date.value = None
        update_display()

    date_picker.on_change = update_date_display

    def clear_date_filter(e):
        date_picker.value = None
        selected_date.value = None
        update_display()

    date_filter = ft.TextButton(
        text="Filtrar por fecha",
        icon=ft.Icons.CALENDAR_MONTH,
        on_click=lambda _: date_picker.pick_date(),
    )

    clear_date_btn = ft.TextButton(
        text="Limpiar fecha",
        icon=ft.Icons.CLEAR,
        on_click=clear_date_filter,
        visible=False
    )

    # Tarjetas de resultados
    def create_scan_card(scan):
        fecha = datetime.fromisoformat(scan["timestamp"]).strftime("%d/%m/%Y %H:%M")
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.ListTile(
                        title=ft.Text(f"Fecha: {fecha}"),
                    ),
                    ft.Divider(),
                    *[
                        ft.Column([
                            ft.Text(f"🔥 Firewall: {record['nombre_firewall']}", weight=ft.FontWeight.BOLD),
                            ft.Text(f"🌐 Hostname: {record['hostname']}"),
                            ft.Text(f"🛡️ Versión: {record['version']}"),
                            ft.Text(f"🏷️ Marca: {record['marca']}"),
                            ft.Text(f"🔨 Build: {record['build']}"),
                            ft.Text(f"📍 Ubicación: {record['location']}"),
                            ft.Text(f"👥 Grupo: {record['grupo_id']}"),
                        ])
                        for record in scan["records"]
                    ]
                ], spacing=10),
                padding=15,
            )
        )

    def update_display():
        main_column.controls.clear()
        filtered = []

        try:
            history = read_json(HISTORY_FILE).get("scans", [])
            user_scans = [s for s in history if s["user"] == username_id]

            # Obtener fecha del date_picker (no del botón)
            filter_date = date_picker.value.date() if date_picker.value else None

            # Aplicar filtros
            for scan in user_scans:
                scan_date = datetime.fromisoformat(scan["timestamp"]).date()

                # 1. Filtro por fecha
                if filter_date and scan_date != filter_date:
                    continue

                # 2. Filtro por nombre
                matches_search = any(
                    search_field.value.lower() in record["nombre_firewall"].lower()
                    for record in scan["records"]
                ) if search_field.value else True

                if matches_search:
                    filtered.append(scan)

            # Eliminar duplicados (por si hay múltiples coincidencias en un mismo scan)
            filtered = list({scan["timestamp"]: scan for scan in filtered}.values())

            # Mostrar resultados
            if filtered:
                for scan in filtered:
                    main_column.controls.append(create_scan_card(scan))
            else:
                main_column.controls.append(
                    ft.Text("No se encontraron resultados", size=18, color=ft.colors.GREY)
                )

        except Exception as e:
            main_column.controls.append(
                ft.Text(f"Error cargando historial: {str(e)}", color="red")
            )

        # Actualizar visibilidad del botón de limpiar
        clear_date_btn.visible = bool(date_picker.value)
        page.update()

    date_picker.on_change = lambda e: update_display()

    # Cargar datos iniciales
    update_display()

    return ft.Column([
        ft.Row([
            ft.Container(build_sidebar(page), expand=False),
            ft.VerticalDivider(width=1),
            ft.Container(
                ft.Column([
                    ft.Text("Historial de Escaneos", size=24, weight=ft.FontWeight.BOLD),
                    ft.Row([
                        search_field,
                        date_filter,
                        clear_date_btn
                    ], spacing=15),
                    ft.Divider(),
                    main_column
                ], expand=True),
                padding=20,
                expand=True
            )
        ], expand=True)
    ], expand=True)
