import flet as ft

def main(page: ft.Page):
    page.title = "CRUD con Búsqueda"
    
    page.window.width = 400
    page.window.height = 600
    page.update()

    # --- 1. DEFINICIÓN DE CONTROLES Y CONTENEDORES ---
    
    dialog_textfield = ft.TextField(label="Valor del ítem", text_size=12)
    
    # NUEVO: Barra de búsqueda
    search_bar = ft.TextField(
        label="Buscar ítems...",
        prefix_icon=ft.Icons.SEARCH,
        text_size=12
    )
    
    control_a_editar = [None] 
    lista_de_items = ft.Column(scroll=ft.ScrollMode.ADAPTIVE, expand=True) # MODIFICADO: Añadido scroll y expand

    # --- 2. DEFINICIÓN DE FUNCIONES (HANDLERS) ---

    def eliminar_y_cerrar(e):
        list_tile_a_eliminar = control_a_editar[0]
        if list_tile_a_eliminar:
            lista_de_items.controls.remove(list_tile_a_eliminar)
            print("Ítem eliminado")
        
        page.close(modal_dialog)
        page.update()

    def guardar_y_cerrar(e): 
        
        current_filter = search_bar.value.lower() # MODIFICADO: Obtenemos el filtro actual

        if control_a_editar[0]:
            # --- MODO EDICIÓN ---
            list_tile_a_editar = control_a_editar[0]
            nuevo_valor = dialog_textfield.value
            list_tile_a_editar.title.value = nuevo_valor
            
            # MODIFICADO: Comprobar si el ítem editado debe ser visible
            if current_filter not in nuevo_valor.lower():
                list_tile_a_editar.visible = False
            else:
                list_tile_a_editar.visible = True
            
            print("Ítem editado")
        else:
            # --- MODO AGREGAR ---
            nuevo_valor = dialog_textfield.value
            nuevo_texto = ft.Text(nuevo_valor)
            nuevo_list_tile = ft.ListTile(title=nuevo_texto)
            
            boton_editar_nuevo = ft.IconButton(
                icon=ft.Icons.EDIT,
                data=nuevo_list_tile, 
                on_click=abrir_dialogo_editar
            )
            
            nuevo_list_tile.trailing = boton_editar_nuevo
            
            # MODIFICADO: Comprobar si el ítem nuevo debe ser visible
            if current_filter not in nuevo_valor.lower():
                nuevo_list_tile.visible = False
            
            lista_de_items.controls.append(nuevo_list_tile)
            print("Ítem agregado")
        
        page.close(modal_dialog)
        page.update() 

    def cerrar_dialogo(e):
        page.close(modal_dialog)
        
    
    # NUEVA FUNCIÓN DE BÚSQUEDA
    def filtrar_lista(e):
        """
        Se activa en cada cambio del TextField de búsqueda.
        Recorre la lista y ajusta la visibilidad de los ítems.
        """
        search_text = e.control.value.lower() # Texto de búsqueda en minúsculas
        print(f"Filtrando por: '{search_text}'")

        for item in lista_de_items.controls:
            # item es el ListTile, item.title es el ft.Text
            item_text = item.title.value.lower()
            
            if search_text in item_text:
                item.visible = True
            else:
                item.visible = False
        
        page.update() # Actualiza la página para mostrar/ocultar ítems
        
    # --- 3. DEFINICIÓN DEL DIÁLOGO ---

    boton_eliminar = ft.TextButton(
        "Eliminar",
        on_click=eliminar_y_cerrar,
        visible=False,
        style=ft.ButtonStyle(
            color=ft.Colors.RED  
        )
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

    def abrir_dialogo_editar(e):
        list_tile_a_editar = e.control.data
        control_a_editar[0] = list_tile_a_editar
        dialog_textfield.value = list_tile_a_editar.title.value 
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
    
    print("Creando lista inicial...")
    for i in range(1, 15): # Más ítems para probar el scroll y la búsqueda
        texto_del_item = ft.Text(f"Ítem inicial {i}")
        list_tile_item = ft.ListTile(title=texto_del_item)
        
        boton_editar_inicial = ft.IconButton(
            icon=ft.Icons.EDIT,
            data=list_tile_item, 
            on_click=abrir_dialogo_editar
        )
        
        list_tile_item.trailing = boton_editar_inicial
        lista_de_items.controls.append(list_tile_item)

    
    # MODIFICADO: Conectar la barra de búsqueda a su función
    search_bar.on_change = filtrar_lista

    # --- 6. AÑADIR CONTROLES A LA PÁGINA ---
    page.add(
        search_bar, # <-- NUEVO
        ft.ElevatedButton(
            "Agregar Nuevo Ítem",
            icon=ft.Icons.ADD, 
            on_click=abrir_dialogo_agregar
        ), 
        ft.Divider(), 
        lista_de_items # <-- MODIFICADO (Ahora tiene scroll y expand)
    )

# --- EJECUTAR LA APP ---
ft.app(target=main)