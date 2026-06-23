import time
import json
import urllib.request
import urllib.error
import webbrowser
import flet as ft

def check_new_version(current_version, page: ft.Page = None):
    if not page:
        return

    version_url = "https://raw.githubusercontent.com/JuanBindez/DYGTube/main/version.json"

    try:
        with urllib.request.urlopen(version_url) as response:
            version_info = response.read().decode().strip()

        version_data = json.loads(version_info)
        latest_version = version_data.get("version", "")

        if latest_version != current_version:
            message = f"DYGTube {latest_version} Available!\n\n"
            message += f"Release Date: {version_data.get('release_date', '')}\n"
            message += f"\nNew:\n{version_data.get('new', '- ')}"

            link_update = version_data.get('link', '')
            link = link_update[0] if isinstance(link_update, list) else link_update

            def on_confirm(e):
                webbrowser.open(link)
                page.window_close()

            def on_cancel(e):
                dialog.open = False
                page.update()

            dialog = ft.AlertDialog(
                title=ft.Text("DYGTube Downloader"),
                content=ft.Text(message + "\n\nWant to update?"),
                actions=[
                    ft.TextButton("Yes", on_click=on_confirm),
                    ft.TextButton("No", on_click=on_cancel),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            page.overlay.append(dialog)
            dialog.open = True
            page.update()

    except urllib.error.URLError:
        def close_error(e):
            error_dialog.open = False
            page.update()

        error_dialog = ft.AlertDialog(
            title=ft.Text("Caution"),
            content=ft.Text("No internet connection"),
            actions=[ft.TextButton("OK", on_click=close_error)],
        )
        page.overlay.append(error_dialog)
        error_dialog.open = True
        page.update()