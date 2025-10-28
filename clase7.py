import flet as ft
import itertools # <--- NUEVO: Para generar IDs

def main(page: ft.Page):
    page.title = "CRUD con DataTable e ID"
    
    page.window.width = 400
    page.window.height = 600
    page.update()

    # --- 1. DEFINICIÓN DE CONTROLES Y CONTENEDORES ---
    
    # <--- NUEVO: Generador de IDs únicos
    id_counter = itertools.count(start=1) 
    
    # <--- MODIFICADO: Añadimos un TextField para el ID (no editable)
    dialog_id_field = ft.TextField(label="ID", read_only=True, text_size=12)
    dialog_textfield = ft.TextField(label="Valor del ítem", text_size=12)
    
    boton_limpiar = ft.IconButton(
        icon=ft.Icons.CLOSE,
        icon_size=18
    )
    
    search_bar = ft.TextField(
        label="Buscar ítems...",
        prefix_icon=ft.Icons.SEARCH,
        text_size=12,
        on_change=lambda e: filtrar_lista(e),
        suffix=boton_limpiar
    )
    
    control_a_editar = [None] # Sigue guardando el ft.DataRow
    
    datatable = ft.DataTable(
        columns=[
            # <--- MODIFICADO: Añadimos columna de ID
            ft.DataColumn(ft.Text("ID"), numeric=True), 
            ft.DataColumn(ft.Text("Valor")),
            ft.DataColumn(ft.Text("Acciones"), numeric=True),
        ],
        rows=[]
    )

    # --- 2. DEFINICIÓN DE FUNCIONES (HANDLERS) ---
    # (eliminar_y_cerrar y cerrar_dialogo no cambian)

    def eliminar_y_cerrar(e):
        row_a_eliminar = control_a_editar[0]
        if row_a_eliminar:
            datatable.rows.remove(row_a_eliminar)
            print(f"Ítem ID={row_a_eliminar.data} eliminado") # <--- MODIFICADO: Usamos el ID
        page.close(modal_dialog)
        page.update()

    def guardar_y_cerrar(e): 
        current_filter = search_bar.value.lower()

        if control_a_editar[0]:
            # --- MODO EDICIÓN ---
            row_a_editar = control_a_editar[0]
            nuevo_valor = dialog_textfield.value
            
            # Actualizamos la celda 1 (Valor)
            row_a_editar.cells[1].content.value = nuevo_valor 
            
            row_a_editar.visible = current_filter in nuevo_valor.lower()
            print(f"Ítem ID={row_a_editar.data} editado") # <--- MODIFICADO: Usamos el ID
        else:
            # --- MODO AGREGAR ---
            nuevo_id = next(id_counter) # <--- NUEVO: Obtenemos ID
            nuevo_valor = dialog_textfield.value
            
            nuevo_texto_id = ft.Text(str(nuevo_id))
            nuevo_texto_valor = ft.Text(nuevo_valor)
            
            boton_editar_nuevo = ft.IconButton(
                icon=ft.Icons.EDIT,
                on_click=abrir_dialogo_editar
            )
            
            nueva_fila = ft.DataRow(
                cells=[
                    ft.DataCell(nuevo_texto_id), # Celda 0: ID
                    ft.DataCell(nuevo_texto_valor), # Celda 1: Valor
                    ft.DataCell(boton_editar_nuevo) # Celda 2: Botón
                ]
            )
            
            # <--- MODIFICADO: Guardamos el ID en el 'data' de la fila
            nueva_fila.data = nuevo_id 
            boton_editar_nuevo.data = nueva_fila # El botón sigue guardando la fila
            
            nueva_fila.visible = current_filter in nuevo_valor.lower()
            
            datatable.rows.append(nueva_fila)
            print(f"Ítem ID={nuevo_id} agregado")
        
        page.close(modal_dialog)
        page.update() 

    def cerrar_dialogo(e):
        page.close(modal_dialog)
        
    def filtrar_lista(e):
        search_text = e.control.value.lower()
        for row in datatable.rows:
            # <--- MODIFICADO: Buscamos en la celda 1 (Valor)
            item_text = row.cells[1].content.value.lower() 
            row.visible = search_text in item_text
        page.update()
    
    def limpiar_busqueda(e):
        search_bar.value = ""
        for row in datatable.rows:
            row.visible = True
        page.update()
        
    # --- 3. DEFINICIÓN DEL DIÁLOGO ---

    boton_eliminar = ft.TextButton(
        "Eliminar",
        on_click=eliminar_y_cerrar,
        visible=False,
        style=ft.ButtonStyle(color=ft.Colors.RED)
    )

    modal_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(""), 
        # <--- MODIFICADO: Usamos una Columna para poner ambos TextFields
        content=ft.Column(
            controls=[
                dialog_id_field,
                dialog_textfield,
            ],
            tight=True, # Ajusta el tamaño
        ),
        actions=[
            boton_eliminar, 
            ft.TextButton("Guardar", on_click=guardar_y_cerrar),
            ft.TextButton("Cancelar", on_click=cerrar_dialogo),
        ],
        actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    # --- 4. FUNCIONES PARA ABRIR EL DIÁLOGO ---

    def abrir_dialogo_editar(e):
        row_a_editar = e.control.data
        control_a_editar[0] = row_a_editar
        
        # <--- MODIFICADO: Leemos el ID desde row.data
        dialog_id_field.value = str(row_a_editar.data)
        dialog_id_field.visible = True
        
        # <--- MODIFICADO: Leemos el valor desde la celda 1
        dialog_textfield.value = row_a_editar.cells[1].content.value
        
        modal_dialog.title.value = "Editar Ítem"
        boton_eliminar.visible = True 
        
        page.open(modal_dialog)
        
    def abrir_dialogo_agregar(e): 
        control_a_editar[0] = None 
        
        # <--- MODIFICADO: Ocultamos el campo de ID
        dialog_id_field.visible = False
        dialog_textfield.value = ""
        
        modal_dialog.title.value = "Agregar Nuevo Ítem" 
        boton_eliminar.visible = False 
        
        page.open(modal_dialog)

    # --- 5. CREACIÓN DE LA LISTA INICIAL ---
    
    print("Creando tabla inicial...")
    for i in range(1, 15): 
        nuevo_id = next(id_counter) # <--- NUEVO: Obtenemos ID
        
        texto_del_id = ft.Text(str(nuevo_id))
        texto_del_valor = ft.Text(f"Ítem inicial {i}")
        
        boton_editar_inicial = ft.IconButton(
            icon=ft.Icons.EDIT,
            on_click=abrir_dialogo_editar
        )
        
        fila_item = ft.DataRow(
            cells=[
                ft.DataCell(texto_del_id), # Celda 0
                ft.DataCell(texto_del_valor), # Celda 1
                ft.DataCell(boton_editar_inicial) # Celda 2
            ]
        )
        
        # <--- MODIFICADO: Guardamos datos en ambas 'data'
        fila_item.data = nuevo_id # La fila guarda su ID
        boton_editar_inicial.data = fila_item # El botón guarda la fila
        
        datatable.rows.append(fila_item)

    # --- 6. AÑADIR CONTROLES A LA PÁGINA ---
    
    tabla_container = ft.Column(
        controls=[datatable], 
        scroll=ft.ScrollMode.ADAPTIVE, 
        expand=True
    )
    
    boton_limpiar.on_click = limpiar_busqueda
    
    page.add(
        search_bar,
        ft.ElevatedButton(
            "Agregar Nuevo Ítem",
            icon=ft.Icons.ADD, 
            on_click=abrir_dialogo_agregar
        ), 
        ft.Divider(), 
        tabla_container
    )

# --- EJECUTAR LA APP ---
ft.app(target=main)