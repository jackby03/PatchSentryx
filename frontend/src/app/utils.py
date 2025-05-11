import datetime
import os
import json
import csv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HISTORY_FILE = os.path.join(BASE_DIR, "..", "data", "history.json")

REQUIRED_FIELDS = ["nombre_firewall", "hostname", "version", "marca", "build", "location", "grupo_id"]

def validate_fields(data):
    if not isinstance(data, list):
        return False
    return all(all(field in item for field in REQUIRED_FIELDS) for item in data)

def read_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

def read_csv(file_path):
    with open(file_path, "r", newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        print("📄 Encabezados detectados:", headers)
        return list(reader)


def append_to_history(username, records):
    history = {"scans": []}

    # 1. Cargar historial existente si el archivo existe
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                history = json.load(f)
        except json.JSONDecodeError:
            history = {"scans": []}

    # 2. Estructurar correctamente los nuevos registros
    new_scan = {
        "user": username,
        "timestamp": datetime.datetime.now().isoformat(),  # Agregar marca de tiempo
        "records": [
            {
                "nombre_firewall": record.get("nombre_firewall", ""),
                "hostname": record.get("hostname", ""),
                "version": record.get("version", ""),
                "marca": record.get("marca", ""),
                "build": record.get("build", ""),
                "location": record.get("location", ""),
                "grupo_id": record.get("grupo_id", "")
            } for record in records
        ]
    }

    # 3. Agregar el nuevo escaneo al historial
    history["scans"].append(new_scan)

    # 4. Guardar en el archivo
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)  # Crear directorio si no existe
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4, ensure_ascii=False)

def read_json(file_path):
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"scans": []}  # Retorna estructura vacía si hay errores
