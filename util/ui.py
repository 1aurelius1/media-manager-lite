import tkinter as tk
import io
import asyncio
import threading
from winrt.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as MediaManager
from winrt.windows.media.control import GlobalSystemMediaTransportControlsSessionPlaybackStatus
from tkinter import ttk, Label, Button
from PIL import ImageTk, Image
from pull_media_info import pull_media_info
from check_media_status import check_media_status
from media_controls import toggle_play_pause, skip_previous, skip_next
from media_info import get_media_info

async_loop = asyncio.new_event_loop()
def run_loop():
    asyncio.set_event_loop(async_loop)
    async_loop.run_forever()

threading.Thread(target=run_loop, daemon=True).start()

def run_async(coro):
    asyncio.run_coroutine_threadsafe(coro, async_loop)

async def watch_for_track_changes(callback):
    session_manager = await MediaManager.request_async()
    current_session = session_manager.get_current_session()

    if not current_session:
        return
    
    def playback_changed_handler(session, _):
        callback()
    
    current_session.add_playback_info_changed(playback_changed_handler)

    while True:
        await asyncio.sleep(1)

def start_track_watcher():
    loop = asyncio.new_event_loop()
    threading.Thread(target=loop.run_forever, daemon=True).start()

    asyncio.run_coroutine_threadsafe(
        watch_for_track_changes(update_ui),
        loop
    )

def update_ui():
    run_async(update_song())

start_track_watcher()

root = tk.Tk()
root.title('')
root.geometry('300x300')
root.resizable(False, False)

root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=5)
root.rowconfigure(2, weight=1)
root.rowconfigure(3, weight=1)
root.rowconfigure(4, weight=1)

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.columnconfigure(3, weight=1)
root.columnconfigure(4, weight=1)
root.columnconfigure(5, weight=1)
root.columnconfigure(6, weight=1)

thumbnail, info_dict = pull_media_info()

img = ImageTk.PhotoImage(thumbnail)
cover = Label(root, image = img)
cover.image = img
cover.grid(column=2, row=1, columnspan=3)

title = Label(root, text=f"{info_dict['title']} — {info_dict['artist']}")
title.grid(column=2, row=2, columnspan=3)

skip_previous_icon = tk.PhotoImage(file='./assets/skip_previous.png')
play_icon = tk.PhotoImage(file='./assets/play.png')
pause_icon = tk.PhotoImage(file='./assets/pause.png')
skip_next_icon = tk.PhotoImage(file='./assets/skip_next.png')

def check_button_state():
    if play_pause['image'] == 'pyimage3':
        play_pause.configure(image=pause_icon)
    else:
        play_pause.configure(image=play_icon)

def sync_play_pause():
    is_paused = asyncio.run(check_media_status())
    if is_paused == True:
        play_pause.configure(image=play_icon)
    else:
        play_pause.configure(image=pause_icon)

def _play_pause():
    asyncio.run(toggle_play_pause())
    check_button_state()

async def update_song():
    _, old_info, _ = await get_media_info()
    max_retries = 10
    for _ in range(max_retries):
        await asyncio.sleep(0.2)
        byte_data, new_info, source_app = await get_media_info()
        if new_info['title'] != old_info['title']:
            break

    if byte_data and new_info:
        thumbnail = Image.open(io.BytesIO(byte_data))
        if source_app == 'Spotify.exe':
            thumbnail = thumbnail.crop((33, 0, 267, 234))
        
        def update_ui():
            async def delayed_update():
                await asyncio.sleep(0.3)
                await update_song()

                img = ImageTk.PhotoImage(thumbnail)
                cover.configure(image=img)
                cover.image = img
                title.configure(text=f"{new_info['title']} — {new_info['artist']}")
            run_async(delayed_update())

        root.after(0, update_ui)

def _skip_previous():
    async def _skip_and_update():
        await skip_previous()

        await asyncio.sleep(0.5)

        byte_data, info_dict, source_app = await get_media_info()

        if byte_data and info_dict:
            thumbnail = Image.open(io.BytesIO(byte_data))
            if source_app == 'Spotify.exe':
                thumbnail = thumbnail.crop((33, 0, 267, 234))
        
            def update_ui():
                img = ImageTk.PhotoImage(thumbnail)
                cover.configure(image=img)
                cover.image = img
                title.configure(text=f"{info_dict['title']} — {info_dict['artist']}")
            
            root.after(0, update_ui)
        
        play_pause.configure(image=pause_icon)

    run_async(_skip_and_update())
    
def _skip_next():
    async def _skip_and_update():
        await skip_next()

        await asyncio.sleep(0.5)

        byte_data, info_dict, source_app = await get_media_info()

        if byte_data and info_dict:
            thumbnail = Image.open(io.BytesIO(byte_data))
            if source_app == 'Spotify.exe':
                thumbnail = thumbnail.crop((33, 0, 267, 234))
        
            def update_ui():
                img = ImageTk.PhotoImage(thumbnail)
                cover.configure(image=img)
                cover.image = img
                title.configure(text=f"{info_dict['title']} — {info_dict['artist']}")
            
            root.after(0, update_ui)

        play_pause.configure(image=pause_icon)

    run_async(_skip_and_update())


skip_previous_button = Button(
    root,
    image=skip_previous_icon,
    command=_skip_previous,
    border=0
)
skip_previous_button.grid(column=2, row=3, sticky='E')

play_pause = Button(
    root,
    image=pause_icon,
    command=_play_pause,
    border=0
)
play_pause.grid(column=3, row=3)
sync_play_pause()

skip_next_button = Button(
    root,
    image=skip_next_icon,
    command=_skip_next,
    border=0
)
skip_next_button.grid(column=4, row=3, sticky='W')

root.mainloop()