import flet as ft

# --- 1. Importa tu componente ---
# (Asegúrate que 'crud_componente.py' esté en la misma carpeta)
from crud_componente import CrudApp

# --- 2. Define tus configuraciones ---

# Configuración 1: Ítems Simples
FIELDS_ITEMS = [
    {"name": "id", "label": "ID", "readonly": True},
    {"name": "valor", "label": "Valor del Ítem", "searchable": True}
]

# Configuración 2: Clientes
FIELDS_CLIENTES = [
    {"name": "id", "label": "ID", "readonly": True},
    {"name": "nombre", "label": "Nombre", "searchable": True},
    {"name": "email", "label": "Correo", "searchable": True},
    {"name": "telefono", "label": "Teléfono", "searchable": False}
]

# --- 3. Define tu función main ---
def main(page: ft.Page):
    
    page.window.width = 500
    page.window.height = 700
    
    # --- Elige qué CRUD quieres mostrar ---
    
    # Opción 1: (Comenta la Opción 2 para usar esta)
    app_crud = CrudApp(
        page_title="CRUD de Ítems",
        fields=FIELDS_ITEMS
    )
    
    # Opción 2: (Descomenta esta y comenta la Opción 1 para probar)
    # app_crud = CrudApp(
    #     page_title="Gestión de Clientes",
    #     fields=FIELDS_CLIENTES
    # )

    page.add(app_crud)

# --- 4. Ejecuta la app ---
if __name__ == "__main__":
    ft.app(target=main)