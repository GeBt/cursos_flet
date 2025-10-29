import flet as ft

def main(page: ft.Page):
    page.title = "CRUD con DataTable y Limpiar Búsqueda"
    
    page.window.width = 800
    page.window.height = 600
    page.update()

    # --- 1. DEFINICIÓN DE CONTROLES Y CONTENEDORES ---
    
    dialog_textfield = ft.TextField(label="Valor del ítem", text_size=12)
    
    # <--- NUEVO: Definimos el botón de limpiar primero
    boton_limpiar = ft.IconButton(
        icon=ft.Icons.CLOSE,
        icon_size=18
    )
    
    # <--- MODIFICADO: Añadimos el 'suffix' al search_bar
    search_bar = ft.TextField(
        label="Buscar ítems...",
        prefix_icon=ft.Icons.SEARCH,
        text_size=12,
        on_change=lambda e: filtrar_lista(e),
        suffix=boton_limpiar # Asignamos el botón "X"
    )
    
    control_a_editar = [None] 
    
    datatable = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Valor del Ítem")),
            ft.DataColumn(ft.Text("Acciones"), numeric=True),
        ],
        rows=[]
    )

    # --- 2. DEFINICIÓN DE FUNCIONES (HANDLERS) ---

    def eliminar_y_cerrar(e):
        row_a_eliminar = control_a_editar[0]
        if row_a_eliminar:
            datatable.rows.remove(row_a_eliminar)
            print("Ítem eliminado")
        page.close(modal_dialog)
        page.update()

    def guardar_y_cerrar(e): 
        current_filter = search_bar.value.lower()

        if control_a_editar[0]:
            # --- MODO EDICIÓN ---
            row_a_editar = control_a_editar[0]
            nuevo_valor = dialog_textfield.value
            row_a_editar.cells[0].content.value = nuevo_valor
            
            row_a_editar.visible = current_filter in nuevo_valor.lower()
            print("Ítem editado")
        else:
            # --- MODO AGREGAR ---
            nuevo_valor = dialog_textfield.value
            nuevo_texto = ft.Text(nuevo_valor)
            
            boton_editar_nuevo = ft.IconButton(
                icon=ft.Icons.EDIT,
                on_click=abrir_dialogo_editar
            )
            nueva_fila = ft.DataRow(
                cells=[
                    ft.DataCell(nuevo_texto),
                    ft.DataCell(boton_editar_nuevo)
                ]
            )
            boton_editar_nuevo.data = nueva_fila
            
            nueva_fila.visible = current_filter in nuevo_valor.lower()
            
            datatable.rows.append(nueva_fila)
            print("Ítem agregado")
        
        page.close(modal_dialog)
        page.update() 

    def cerrar_dialogo(e):
        page.close(modal_dialog)
        
    def filtrar_lista(e):
        search_text = e.control.value.lower()
        print(f"Filtrando por: '{search_text}'")
        for row in datatable.rows:
            item_text = row.cells[0].content.value.lower()
            row.visible = search_text in item_text
        page.update()
    
    # <--- NUEVA FUNCIÓN ---
    def limpiar_busqueda(e):
        """Limpia el TextField y resetea la visibilidad de la tabla"""
        search_bar.value = "" # Limpia el texto
        print("Búsqueda limpiada.")
        
        # Vuelve a mostrar todas las filas
        for row in datatable.rows:
            row.visible = True
        
        page.update() # Actualiza la UI
        

    # --- 3. DEFINICIÓN DEL DIÁLOGO ---
    # (Esta sección no cambia)
    boton_eliminar = ft.TextButton(
        "Eliminar",
        on_click=eliminar_y_cerrar,
        visible=False,
        style=ft.ButtonStyle(color=ft.Colors.RED)
    )
    modal_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(""), 
        content=dialog_textfield,
        actions=[
            boton_eliminar, 
            ft.TextButton("Guardar", on_click=guardar_y_cerrar),
            ft.TextButton("Cancelar", on_click=cerrar_dialogo),
        ],
        actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    # --- 4. FUNCIONES PARA ABRIR EL DIÁLOGO ---
    # (Esta sección no cambia)
    def abrir_dialogo_editar(e):
        row_a_editar = e.control.data
        control_a_editar[0] = row_a_editar
        dialog_textfield.value = row_a_editar.cells[0].content.value
        modal_dialog.title.value = "Editar Ítem"
        boton_eliminar.visible = True 
        page.open(modal_dialog)
        
    def abrir_dialogo_agregar(e): 
        control_a_editar[0] = None 
        dialog_textfield.value = ""  
        modal_dialog.title.value = "Agregar Nuevo Ítem" 
        boton_eliminar.visible = False 
        page.open(modal_dialog)

    # --- 5. CREACIÓN DE LA LISTA INICIAL ---
    # (Esta sección no cambia)
    print("Creando tabla inicial...")
    for i in range(1, 15): 
        texto_del_item = ft.Text(f"Ítem inicial {i}")
        
        boton_editar_inicial = ft.IconButton(
            icon=ft.Icons.EDIT,
            on_click=abrir_dialogo_editar
        )
        fila_item = ft.DataRow(
            cells=[
                ft.DataCell(texto_del_item),
                ft.DataCell(boton_editar_inicial)
            ]
        )
        boton_editar_inicial.data = fila_item
        
        datatable.rows.append(fila_item)

    # --- 6. CONECTAR HANDLERS Y AÑADIR CONTROLES A LA PÁGINA ---
    
    tabla_container = ft.Column(
        controls=[datatable], 
        scroll=ft.ScrollMode.ADAPTIVE, 
        expand=True
    )
    
    # <--- MODIFICADO: Conectamos el on_click del botón de limpiar
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