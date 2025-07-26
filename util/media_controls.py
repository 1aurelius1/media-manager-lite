import asyncio

from winrt.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as MediaManager

async def toggle_play_pause():
    sessions = await MediaManager.request_async()
    current_session = sessions.get_current_session()
    if current_session:
        await current_session.try_toggle_play_pause_async()

async def skip_next():
    sessions = await MediaManager.request_async()
    current_session = sessions.get_current_session()
    if current_session:
        await current_session.try_skip_next_async()

async def skip_previous():
    sessions = await MediaManager.request_async()
    current_session = sessions.get_current_session()
    if current_session:
        await current_session.try_skip_previous_async()