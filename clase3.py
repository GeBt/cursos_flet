import flet as ft

def main(page: ft.Page):
    page.title = "Agenda de tareas"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    lista_tareas = ft.Column()
    def agregar_tarea(tarea):
        if tarea:
            lista_tareas.controls.append(ft.Text(tarea))
            tarea.value = ""
            page.update()
    tarea = ft.TextField(label="Nueva tarea", text_align=ft.TextAlign.CENTER, width=300)

    btn_agregar = ft.ElevatedButton(text="Agregar tarea", on_click=lambda e: agregar_tarea(tarea.value))

    page.add(
        ft.Column(
            controls=[
                tarea,
                btn_agregar,
                lista_tareas
            ]
        )
    )

ft.app(target=main)