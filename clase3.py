import flet as ft

def main(page: ft.Page):
    page.title = "Mi Lista de Tareas"
    #page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    page.window_min_width = 350
    page.window_min_height = 450
    page.update()

    titulo = ft.Text("Lista de Tareas", size=14, weight=ft.FontWeight.BOLD)

    tareas = []

    def obtener_siguiente_id():
        if not tareas:
            return 1
        max_id = max(t.data['id'] for t in tareas)
        return max_id + 1

    def seleccionar_tarea(e):
        for tarea in tareas:
            print(f"Tarea ID: {tarea.data['id']}, Título: {tarea.title.value}, Seleccionada: {tarea.leading.value}")        
        
        seleccionada = [t.title.value for t in tareas if t.leading.value]
        tareas_seleccionadas.value = "Tareas seleccionadas: " + ", ".join(seleccionada)
        page.update()

    def actualizar_lista():
        lista_tareas.controls.clear()
        lista_tareas.controls.extend(tareas)
        page.update()   
        
    def item_seleccionado(e):
        tarea = e.control
        print("Tarea seleccionada:", tarea.title.value)
        seleccionar_tarea(e)    

    def agregar_tarea(e):
        if campo_tarea.value:
            tarea = ft.ListTile(title=ft.Text(campo_tarea.value),
                                data={"id": obtener_siguiente_id()},
                                subtitle=ft.Text("Pendiente", size=10, color=ft.Colors.RED),
                                leading=ft.Checkbox(on_change=seleccionar_tarea))
                                #on_click=item_seleccionado)
            print(tarea.title.value, tarea.data['id'])
            tareas.append(tarea)
            campo_tarea.value = ""
            actualizar_lista()
            

    campo_tarea = ft.TextField(label="Nueva Tarea", width=300, hint_text="Escribe una tarea...", text_size=12)
    btn_agregar = ft.FilledButton("Agregar Tarea", on_click=lambda e: agregar_tarea(campo_tarea.value))

    lista_tareas = ft.ListView(
        expand=True, 
        spacing=3, 
        auto_scroll=True,
    )
    
    contenedor_lista_tareas = ft.Container(
        content=lista_tareas,
        expand=True,
        bgcolor=ft.Colors.LIGHT_BLUE_50,
    )

    tareas_seleccionadas = ft.Text(value="", size=12, weight=ft.FontWeight.BOLD)
    
    def page_resized(e):    
        nueva_altura = page.height - 100
        contenedor_lista_tareas.height = max(nueva_altura, MIN_HEIGHT:=300)
        page.update()
    
    page.on_resize = page_resized
    
    page_resized(None)

    page.add(titulo, campo_tarea, btn_agregar, contenedor_lista_tareas, tareas_seleccionadas)


ft.app(target=main)