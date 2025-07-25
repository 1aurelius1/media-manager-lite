import asyncio

from winrt.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as MediaManager

async def get_media_info():
    sessions = await MediaManager.request_async()
    current_session = sessions.get_current_session()
    if current_session:
        info = await current_session.try_get_media_properties_async()

        info_dict = {song_attr: info.__getattribute__(song_attr) for song_attr in dir(info) if song_attr[0] != '_'}

        info_dict['genres'] = list(info_dict['genres'])

        print(info_dict)

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

async def get_timeline():
    sessions = await MediaManager.request_async()
    current_session = sessions.get_current_session()
    if current_session:
        timeline = current_session.get_timeline_properties()
        
        timeline_dict = {
            'start_time': timeline.__getattribute__('start_time'),
            'end_time': timeline.__getattribute__('end_time'),
            'position': timeline.__getattribute__('position')
        }

        print(timeline_dict)

if __name__ == "__main__":
    current_media_info = asyncio.run(get_timeline())