import flet as ft
import inspect # <-- 1. AÑADE ESTA LÍNEA
import itertools
from typing import List, Dict, Any

# --- 2. AÑADE ESTAS LÍNEAS DE DEBUG ---
print("--- INICIO DE DEBUG ---")
print(f"Versión de Flet detectada: {ft.__version__}")
print(f"Ruta del módulo 'flet' importado: {inspect.getfile(ft)}")
print("--- FIN DE DEBUG ---")
# --- FIN DE DEBUG ---

class CrudApp(ft.UserControl):
    """
    Un componente CRUD genérico y reutilizable para Flet.

    Parámetros:
    - page_title (str): El título que se mostrará en la página.
    - fields (List[Dict]): La configuración de los campos.
    """
    
    def __init__(self, page_title: str, fields: List[Dict[str, Any]]):
        super().__init__(expand=True)
        
        # --- 1. Configuración y Estado ---
        self.page_title = page_title
        self.fields = fields
        
        # Encuentra los campos clave desde la configuración
        self.readonly_fields = {f['name'] for f in fields if f.get('readonly', False)}
        self.searchable_indices = [i for i, f in enumerate(fields) if f.get('searchable', False)]
        
        self.id_counter = itertools.count(start=1)
        self.control_a_editar = [None] # Almacenará el DataRow a editar

        # --- 2. Creación de Controles Internos ---
        
        # --- A. Controles del Diálogo (Dinámicos) ---
        self.dialog_controls = {} # Diccionario para guardar los TextFields del diálogo
        dialog_content_controls = []
        for field in self.fields:
            tf = ft.TextField(
                label=field['label'],
                read_only=field.get('readonly', False),
                text_size=12
            )
            self.dialog_controls[field['name']] = tf
            dialog_content_controls.append(tf)

        self.boton_eliminar = ft.TextButton(
            "Eliminar",
            on_click=self.eliminar_y_cerrar,
            visible=False,
            style=ft.ButtonStyle(color=ft.Colors.RED)
        )
        
        self.modal_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(""),
            content=ft.Column(controls=dialog_content_controls, tight=True, spacing=15),
            actions=[
                self.boton_eliminar,
                ft.TextButton("Guardar", on_click=self.guardar_y_cerrar),
                ft.TextButton("Cancelar", on_click=self.cerrar_dialogo),
            ],
            actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

        # --- B. Controles Principales (DataTable, Búsqueda) ---
        self.boton_limpiar = ft.IconButton(
            icon=ft.Icons.CLOSE,
            icon_size=18,
            on_click=self.limpiar_busqueda
        )
        
        self.search_bar = ft.TextField(
            label="Buscar...",
            prefix_icon=ft.Icons.SEARCH,
            text_size=12,
            on_change=self.filtrar_lista,
            suffix=self.boton_limpiar
        )
        
        self.add_button = ft.ElevatedButton(
            "Agregar Nuevo",
            icon=ft.Icons.ADD,
            on_click=self.abrir_dialogo_agregar
        )

        # Columnas de la tabla (Dinámicas)
        data_columns = [ft.DataColumn(ft.Text(f['label'])) for f in self.fields]
        data_columns.append(ft.DataColumn(ft.Text("Acciones"), numeric=True))
        
        self.datatable = ft.DataTable(
            columns=data_columns,
            rows=[]
        )
        
    def build(self):
        """
        Construye la interfaz visual del componente.
        Este método es llamado por Flet.
        """
        # Establecemos el título de la página cuando se construye
        if self.page: # Asegurarse que la página existe
            self.page.title = self.page_title
        
        tabla_container = ft.Column(
            controls=[self.datatable],
            scroll=ft.ScrollMode.ADAPTIVE,
            expand=True
        )
        
        # Retornamos el layout completo del UserControl
        return ft.Column(
            controls=[
                self.search_bar,
                self.add_button,
                ft.Divider(),
                tabla_container
            ],
            expand=True
        )
        
    # --- 3. Lógica y Handlers (Métodos de la clase) ---

    def did_mount(self):
        """
        Se llama después de que el control se añade a la página.
        Usado para cargar datos iniciales.
        """
        # Asignar page.title aquí es más seguro
        self.page.title = self.page_title
        self.cargar_datos_iniciales()
        self.update()

    def cargar_datos_iniciales(self):
        """Crea algunos datos de ejemplo."""
        print("Cargando datos iniciales...")
        for i in range(1, 5):
            new_id = next(self.id_counter)
            new_cells = []
            
            # Lógica para crear la fila inicial
            boton_editar = ft.IconButton(
                icon=ft.Icons.EDIT,
                on_click=self.abrir_dialogo_editar
            )
            
            # Llenamos las celdas basadas en la config
            for field in self.fields:
                if field['name'] == 'id':
                    new_cells.append(ft.DataCell(ft.Text(str(new_id))))
                else:
                    new_cells.append(ft.DataCell(ft.Text(f"Valor de {field['label']} {i}")))

            new_cells.append(ft.DataCell(boton_editar))
            
            nueva_fila = ft.DataRow(cells=new_cells, data=new_id)
            boton_editar.data = nueva_fila
            self.datatable.rows.append(nueva_fila)

    def eliminar_y_cerrar(self, e):
        row_a_eliminar = self.control_a_editar[0]
        if row_a_eliminar:
            self.datatable.rows.remove(row_a_eliminar)
            print(f"Ítem ID={row_a_eliminar.data} eliminado")
        self.page.close(self.modal_dialog)
        self.update() # Actualiza el UserControl

    def guardar_y_cerrar(self, e):
        current_filter = self.search_bar.value.lower()
        search_match = False
        search_text_combined = ""

        if self.control_a_editar[0]:
            # --- MODO EDICIÓN ---
            row_a_editar = self.control_a_editar[0]
            
            for i, field in enumerate(self.fields):
                # Solo actualiza campos que no son readonly
                if field['name'] not in self.readonly_fields:
                    new_val = self.dialog_controls[field['name']].value
                    row_a_editar.cells[i].content.value = new_val
                
                # Revisa si coincide con la búsqueda
                if i in self.searchable_indices:
                    search_text_combined += row_a_editar.cells[i].content.value.lower()

            row_a_editar.visible = current_filter in search_text_combined
            print(f"Ítem ID={row_a_editar.data} editado")

        else:
            # --- MODO AGREGAR ---
            new_id = next(self.id_counter)
            new_cells = []
            
            boton_editar_nuevo = ft.IconButton(
                icon=ft.Icons.EDIT,
                on_click=self.abrir_dialogo_editar
            )
            
            for field in self.fields:
                if field['name'] == 'id':
                    new_val = str(new_id)
                    new_cells.append(ft.DataCell(ft.Text(new_val)))
                else:
                    new_val = self.dialog_controls[field['name']].value
                    new_cells.append(ft.DataCell(ft.Text(new_val)))
                
                # Revisa si coincide con la búsqueda
                if field.get('searchable', False):
                    search_text_combined += new_val.lower()

            new_cells.append(ft.DataCell(boton_editar_nuevo))
            
            nueva_fila = ft.DataRow(cells=new_cells, data=new_id)
            boton_editar_nuevo.data = nueva_fila
            
            nueva_fila.visible = current_filter in search_text_combined
            
            self.datatable.rows.append(nueva_fila)
            print(f"Ítem ID={new_id} agregado")
        
        self.page.close(self.modal_dialog)
        self.update() # Actualiza el UserControl

    def cerrar_dialogo(self, e):
        self.page.close(self.modal_dialog)

    def filtrar_lista(self, e):
        search_text = self.search_bar.value.lower()
        
        for row in self.datatable.rows:
            search_text_combined = ""
            # Buscamos en todas las celdas marcadas como 'searchable'
            for i in self.searchable_indices:
                search_text_combined += row.cells[i].content.value.lower()
                
            row.visible = search_text in search_text_combined
        self.update()

    def limpiar_busqueda(self, e):
        self.search_bar.value = ""
        for row in self.datatable.rows:
            row.visible = True
        self.update()

    def abrir_dialogo_editar(self, e):
        row_a_editar = e.control.data
        self.control_a_editar[0] = row_a_editar
        
        # Rellena el diálogo dinámicamente
        for i, field in enumerate(self.fields):
            self.dialog_controls[field['name']].value = row_a_editar.cells[i].content.value
            self.dialog_controls[field['name']].visible = True
            
        self.modal_dialog.title.value = "Editar Ítem"
        self.boton_eliminar.visible = True
        self.page.open(self.modal_dialog)

    def abrir_dialogo_agregar(self, e):
        self.control_a_editar[0] = None
        
        # Limpia el diálogo dinámicamente
        for field in self.fields:
            if field.get('readonly', False):
                self.dialog_controls[field['name']].visible = False # Oculta IDs
            else:
                self.dialog_controls[field['name']].value = "" # Limpia texto
                self.dialog_controls[field['name']].visible = True
                
        self.modal_dialog.title.value = "Agregar Ítem"
        self.boton_eliminar.visible = False
        self.page.open(self.modal_dialog)