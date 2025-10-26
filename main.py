import flet as ft 
def main(page: ft.Page):
    page.bgcolor = ft.Colors.BLUE_GREY_800
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.title = "Mi primera aplicación Flet"

    texto1_1 = ft.Text("Texto 1-1", color=ft.Colors.WHITE, size=30)
    texto1_2 = ft.Text("Texto 1-2", color=ft.Colors.WHITE, size=30)
    texto1_3 = ft.Text("Texto 1-3", color=ft.Colors.WHITE, size=30)

    texto2_1 = ft.Text("Texto 2-1", color=ft.Colors.WHITE, size=30)
    texto2_2 = ft.Text("Texto 2-2", color=ft.Colors.WHITE, size=30)
    texto2_3 = ft.Text("Texto 2-3", color=ft.Colors.WHITE, size=30)

    

    fila1Textos = ft.Row(
        controls=[texto1_1, texto1_2, texto1_3], alignment=ft.MainAxisAlignment.CENTER, spacing=10
        )

    fila2Textos = ft.Row(
        controls=[texto2_1, texto2_2, texto2_3], alignment=ft.MainAxisAlignment.CENTER, spacing=10
        )

    columnas1 = ft.Column(
            controls=[fila1Textos], spacing=10
        )

    columnas2 = ft.Column(
            controls=[fila2Textos], spacing=10
        )

    fila1Textos = ft.Row(
        controls=[columnas1, columnas2], alignment=ft.MainAxisAlignment.START, spacing=30
        )

    page.add(fila1Textos)

ft.app(target=main)

