# this is part of the DYGtube Downloader project.
#
# Release: v8.0-rc1
#
# Copyright ©  2022 - 2026  Juan Bindez  <juanbindez780@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#  
# repo: https://github.com/juanBindez


import os
import logging
import urllib3
import time
import base64
import webbrowser
import requests
from io import BytesIO
import flet as ft

from pytubefix import YouTube, Playlist
from pytubefix.cli import on_progress
from pytubefix.innertube import *
from pytubefix.innertube import InnerTube
from pytubefix.exceptions import AgeRestrictedError
from mutagen.mp4 import MP4, MP4Cover

from src.views.about_view import about_software
from src.services.images_service import *
from src.services.debug_service import DebugInfo
from src.services.check_update_service import check_new_version
from src.views.version import *

ERROR_001 = False
ERROR_002 = False
ERROR_003 = False


def add_m4a_metadata(file_path, track_number, title, artist, album, total_tracks, cover_url=None):
    try:
        audio = MP4(file_path)
        audio["\xa9nam"] = title  
        audio["\xa9ART"] = artist  
        audio["\xa9alb"] = album    
        audio["\xa9day"] = "2026"   
        audio["\xa9gen"] = "Alternative"  
        audio["trkn"] = [(track_number, total_tracks)]
        
        if cover_url:
            try:
                response = requests.get(cover_url)
                if response.status_code == 200:
                    cover_data = BytesIO(response.content).getvalue()
                    audio["covr"] = [MP4Cover(cover_data, imageformat=MP4Cover.FORMAT_JPEG)]
            except:
                print("Could not download cover")
        
        audio.save()
        print(f"Metadata added: Track {track_number} - {title}")
    except Exception as e:
        print(f"Error adding metadata: {e}")

def main(page: ft.Page):
    page.title = "DYGTube Downloader"
    page.window_width = 550
    page.window_height = 480
    page.window_resizable = False
    

    check_new_version(CHECK_VERSION, page)


    save_path = "downloads_DYGtube"
    os.makedirs(save_path, exist_ok=True)

    def show_message(title, message):
        def close_dialog(e):
            dialog.open = False
            page.update()
            
        dialog = ft.AlertDialog(
            title=ft.Text(title),
            content=ft.Text(message),
            actions=[ft.TextButton("OK", on_click=close_dialog)],
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    def source_code_page(e):
        webbrowser.open("https://github.com/JuanBindez/DYGTube-Downloader")

    def check_quality(e):
        link = entrada_de_dados.value
        if not link:
            show_message("DYGTube Downloader", "The field is empty, paste a URL...")
            return

        if check_is_playlist.value:
            try:
                pl = Playlist(link)
                show_message("DYGTube", f"Playlist: {pl.title}\nTotal videos: {len(pl.videos)}")
            except Exception as ex:
                DebugInfo.logger_error.error(ex, exc_info=True)
                show_message("DYGTube", "Error checking playlist.")
        else:
            try:
                video = YouTube(link)
                resolucoes = [stream.resolution for stream in video.streams if stream.resolution]
                show_message("DYGTube", f"Resolutions available for {video.title}: {', '.join(set(resolucoes))}")
            except Exception as ex:
                DebugInfo.logger_error.error(ex, exc_info=True)

    def process_download_video(e):
        global ERROR_001, ERROR_002
        link = entrada_de_dados.value
        if not link:
            show_message("DYGTube Downloader", "The field is empty!")
            return

        if check_is_playlist.value:
            try:
                pl = Playlist(link)
                for index, video in enumerate(pl.videos, start=1):
                    try:
                        ys = video.streams.get_highest_resolution()
                        ys.download(save_path)
                    except Exception as playlist_err:
                        DebugInfo.logger_error.error(playlist_err, exc_info=True)
                show_message("DYG Downloader", "Playlist MP4 Download Completed")
            except Exception as ex:
                show_message("DYG Downloader", "Something went wrong with playlist download!")
                DebugInfo.logger_error.error(ex, exc_info=True)
        else:
            video = YouTube(link)
            try:
                video_stream = None
                if check_1080p.value: video_stream = video.streams.filter(res="1080p").first()
                elif check_720p.value: video_stream = video.streams.filter(res="720p").first()
                elif check_480p.value: video_stream = video.streams.filter(res="480p").first()
                elif check_360p.value: video_stream = video.streams.filter(res="360p").first()
                elif check_240p.value: video_stream = video.streams.filter(res="240p").first()
                elif check_144p.value: video_stream = video.streams.filter(res="144p").first()

                if video_stream is not None:
                    DebugInfo.logger_info.info("[INFO] Starting download: %s", link)
                    video_stream.download(save_path)
                    show_message("DYG Downloader", "Download Completed")
                else:
                    try:
                        yt = YouTube(link, on_progress_callback=on_progress)
                        ys = yt.streams.get_highest_resolution()
                        ys.download(save_path)
                        if not ERROR_001:
                            show_message("DYG Downloader", "Download Completed")
                    except AgeRestrictedError as ageerror:
                        DebugInfo.logger_error.error(ageerror, exc_info=True)
                        show_message("DYG Downloader", "Attention! Age Restricted Video")
                    except Exception as ex:
                        ERROR_001 = True
                        show_message("DYG Downloader", "Something went wrong!")
                        DebugInfo.logger_error.error(ex, exc_info=True)
            except AgeRestrictedError:
                show_message("DYG Downloader", "Age Restricted Error")
            except KeyError:
                show_message("DYG Downloader", "Unable to download, Youtube changes detected.")
                DebugInfo.logger_error.error(KeyError, exc_info=True)
            except Exception as ex:
                ERROR_002 = True
                show_message("DYG Downloader", "Something went wrong!")
                DebugInfo.logger_error.error(ex, exc_info=True)

    def process_download_mp3(e):
        global ERROR_003
        link = entrada_de_dados.value
        if not link:
            show_message("DYGTube Downloader", "The field is empty!")
            return

        if check_is_playlist.value:
            try:
                pl = Playlist(link)
                total_videos = len(pl.videos)
                
                for index, video in enumerate(pl.videos, start=1):
                    try:
                        audio_stream = video.streams.get_audio_only()
                        clean_title = "".join(c for c in video.title if c.isalnum() or c in (' ', '-', '_')).rstrip()
                        filename = f"{index:02d} - {clean_title}.m4a"
                        full_path = os.path.join(save_path, filename)
                        
                        audio_stream.download(output_path=save_path, filename=filename)
                        
                        cover_url = video.thumbnail_url if hasattr(video, 'thumbnail_url') else None
                        
                        add_m4a_metadata(
                            full_path,
                            track_number=index,
                            title=f"{index:02d} - {video.title}",
                            artist="Artist",
                            album=pl.title,
                            total_tracks=total_videos,
                            cover_url=cover_url
                        )
                    except Exception as playlist_audio_err:
                        DebugInfo.logger_error.error(playlist_audio_err, exc_info=True)
                
                show_message("DYG Downloader", f"Playlist Download complete! {total_videos} files processed.")
            except Exception as ex:
                show_message("DYG Downloader", "Something went wrong with playlist audio download!")
                DebugInfo.logger_error.error(ex, exc_info=True)
        else:
            try:
                yt = YouTube(link, on_progress_callback=on_progress)
                ys = yt.streams.get_audio_only()
                ys.download(save_path, mp3=True)
                time.sleep(3)
                if not ERROR_003:
                    show_message("DYG Downloader", "Download Completed")
            except AgeRestrictedError:
                show_message("DYG Downloader", "Age Restricted Error")
            except Exception as ex:
                ERROR_003 = True
                show_message("DYG Downloader", "Something went wrong!")
                DebugInfo.logger_error.error(ex, exc_info=True)

  
    page.appbar = ft.AppBar(
        title=ft.Text("DYGTube Menu"),
        actions=[
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(content=ft.Text("Help"), on_click=lambda _: about_software(page)),
                    ft.PopupMenuItem(content=ft.Text("Source Code"), on_click=source_code_page),
                ]
            )
        ],
    )

    banner_img = ft.Image(src=f"data:image/png;base64,{BANNER_LOGO}", width=530, height=120, fit="contain")
    entrada_de_dados = ft.TextField(label="Paste YouTube URL here", width=500)

    check_is_playlist = ft.Checkbox(label="Is Playlist", value=False, fill_color="#00E9CA")
    
    check_1080p = ft.Checkbox(label="1080p", value=False)
    check_720p = ft.Checkbox(label="720p", value=False)
    check_480p = ft.Checkbox(label="480p", value=False)
    check_360p = ft.Checkbox(label="360p", value=False)
    check_240p = ft.Checkbox(label="240p", value=False)
    check_144p = ft.Checkbox(label="144p", value=False)

    row_checkboxes = ft.Row(
        [check_1080p, check_720p, check_480p, check_360p, check_240p, check_144p],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    btn_quality = ft.ElevatedButton("Check Quality", on_click=check_quality, width=500)
    btn_video = ft.ElevatedButton("Download MP4", on_click=process_download_video, width=500, bgcolor='#191A1A', color='#00E9CA')
    btn_mp3 = ft.ElevatedButton("Download MP3", on_click=process_download_mp3, width=500, bgcolor='#191A1A', color='#00E9CA')
    
    lbl_version = ft.Text(VERSION, size=12)

    page.add(
        ft.Column(
            [
                banner_img,
                entrada_de_dados,
                ft.Row([check_is_playlist], alignment=ft.MainAxisAlignment.CENTER),
                row_checkboxes,
                btn_quality,
                btn_video,
                btn_mp3,
                lbl_version
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

if __name__ == "__main__":
    ft.app(target=main)