import flet as ft
from src.views.version import VERSION

def about_software(page: ft.Page):
    """Displays information about the program safely across all Flet versions."""
    
    if not page:
        return

    def close_dialog(e):
        dialog.open = False
        page.update()

    dialog = ft.AlertDialog(
        title=ft.Text("DYGTube", size=20, weight="bold", text_align="center"),
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text(VERSION, size=14, color="grey", text_align="center"),
                    ft.Divider(height=10, color="transparent"),
                    
                    ft.Text("(MPEG-4 AAC audio codec)", size=13),
                    ft.Text("DYGTube: downloads MP4 video and audio MP3.", size=13),
                    ft.Text("This software comes with absolutely no warranty.", size=13, weight="w500"),
                    ft.Text(
                        "For more details, visit the GNU General Public License, version 2", 
                        size=12, 
                    ),
                    
                    ft.Divider(height=15, color="transparent"),
                    ft.Text("Copyright © 2022 - 2026 Juan Bindez", size=11, color="grey"),
                ],
                tight=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=400,
            height=230,
        ),
        actions=[
            ft.TextButton("Close", on_click=close_dialog)
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Garante a abertura adicionando ao overlay e forçando o estado de abertura simultaneamente
    page.overlay.append(dialog)
    dialog.open = True
    page.update()