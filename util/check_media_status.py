import asyncio

from winrt.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as MediaManager

async def check_media_status():
    sessions = await MediaManager.request_async()
    current_session = sessions.get_current_session()

    if current_session:
        controls = current_session.get_playback_info().controls
        return controls.is_play_enabled