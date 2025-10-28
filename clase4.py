import flet as ft

def main(page: ft.Page):
    page.title = "CRUD Completo (Agregar, Editar, Eliminar)"
    
    page.window.width = 400
    page.window.height = 600
    page.update()

    # --- 1. DEFINICIÓN DE CONTROLES Y CONTENEDORES ---
    
    dialog_textfield = ft.TextField(label="Valor del ítem", text_size=12)
    
    # 'control_a_editar' guardará el ListTile completo (la fila)
    control_a_editar = [None] 
    
    # La columna que contendrá la lista de ítems
    lista_de_items = ft.Column() 

    # --- 2. DEFINICIÓN DE FUNCIONES (HANDLERS) ---
    
    # (Definimos las funciones *antes* del diálogo para poder
    #  asignarlas directamente a los botones)

    def eliminar_y_cerrar(e):
        """
        Se activa con el botón 'Eliminar' del diálogo.
        Busca el control (ListTile) en la lista y lo borra.
        """
        list_tile_a_eliminar = control_a_editar[0]
        
        if list_tile_a_eliminar:
            lista_de_items.controls.remove(list_tile_a_eliminar)
            print("Ítem eliminado")
        
        page.close(modal_dialog)
        page.update() # Actualiza la página para mostrar la lista sin el ítem

    def guardar_y_cerrar(e): 
        """
        Se activa con el botón 'Guardar'.
        Comprueba si estamos agregando o editando.
        """
        if control_a_editar[0]:
            # --- MODO EDICIÓN ---
            # Si el control existe, es el ListTile.
            # Actualizamos el 'value' de su control 'title'.
            list_tile_a_editar = control_a_editar[0]
            list_tile_a_editar.title.value = dialog_textfield.value
            print("Ítem editado")
        else:
            # --- MODO AGREGAR ---
            # Si el control es None, creamos un ítem nuevo.
            nuevo_texto = ft.Text(dialog_textfield.value)
            
            # 1. Creamos el ListTile (fila)
            nuevo_list_tile = ft.ListTile(title=nuevo_texto)
            
            # 2. Creamos su botón de editar
            boton_editar_nuevo = ft.IconButton(
                icon=ft.Icons.EDIT,
                data=nuevo_list_tile, # Pasamos la fila entera como data
                on_click=abrir_dialogo_editar
            )
            
            # 3. Asignamos el botón a la fila y la fila a la lista
            nuevo_list_tile.trailing = boton_editar_nuevo
            lista_de_items.controls.append(nuevo_list_tile)
            print("Ítem agregado")
        
        page.close(modal_dialog)
        page.update() # Actualiza la página para mostrar los cambios

    def cerrar_dialogo(e):
        """Se activa con 'Cancelar'"""
        page.close(modal_dialog)
        
    
    # --- 3. DEFINICIÓN DEL DIÁLOGO ---

    # Creamos el botón de eliminar por separado
    # para poder controlar su visibilidad
    boton_eliminar = ft.TextButton(
        "Eliminar",
        on_click=eliminar_y_cerrar,
        visible=False, # Invisible por defecto
        style=ft.ButtonStyle(
            # Propiedad 'color' (minúscula), Valor 'ft.colors.RED' (mayúscula)
            color=ft.Colors.RED  
        )
    )

    modal_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(""), # El título se cambiará dinámicamente
        content=dialog_textfield,
        actions=[
            boton_eliminar, # Botón de eliminar
            ft.TextButton("Guardar", on_click=guardar_y_cerrar),
            ft.TextButton("Cancelar", on_click=cerrar_dialogo),
        ],
        actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    # --- 4. FUNCIONES PARA ABRIR EL DIÁLOGO ---

    def abrir_dialogo_editar(e):
        """Modo Edición: Rellena el diálogo con datos existentes"""
        # 'e.control.data' es el ListTile completo
        list_tile_a_editar = e.control.data
        control_a_editar[0] = list_tile_a_editar
        
        # Obtenemos el texto del 'title' del ListTile
        dialog_textfield.value = list_tile_a_editar.title.value 
        
        modal_dialog.title.value = "Editar Ítem"
        boton_eliminar.visible = True # Hacemos visible "Eliminar"
        
        page.open(modal_dialog)
        
    def abrir_dialogo_agregar(e): 
        """Modo Agregar: Limpia el diálogo"""
        control_a_editar[0] = None # No hay nada que editar
        dialog_textfield.value = ""  # Limpiamos el texto
        
        modal_dialog.title.value = "Agregar Nuevo Ítem" 
        boton_eliminar.visible = False # Ocultamos "Eliminar"
        
        page.open(modal_dialog)

    # --- 5. CREACIÓN DE LA LISTA INICIAL ---
    
    print("Creando lista inicial...")
    for i in range(1, 4): 
        texto_del_item = ft.Text(f"Ítem inicial {i}")
        
        # 1. Creamos el ListTile
        list_tile_item = ft.ListTile(title=texto_del_item)
        
        # 2. Creamos el botón (usando ft.Icons con 'I' mayúscula)
        boton_editar_inicial = ft.IconButton(
            icon=ft.Icons.EDIT,
            data=list_tile_item, # Pasamos la fila entera
            on_click=abrir_dialogo_editar
        )
        
        # 3. Asignamos y añadimos
        list_tile_item.trailing = boton_editar_inicial
        lista_de_items.controls.append(list_tile_item)

    # --- 6. AÑADIR CONTROLES A LA PÁGINA ---
    page.add(
        ft.ElevatedButton(
            "Agregar Nuevo Ítem",
            icon=ft.Icons.ADD, # (usando ft.Icons con 'I' mayúscula)
            on_click=abrir_dialogo_agregar
        ), 
        ft.Divider(), 
        lista_de_items # La columna que contiene todos los ítems
    )

# --- EJECUTAR LA APP ---
ft.app(target=main)