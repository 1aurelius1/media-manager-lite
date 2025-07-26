import asyncio

from winrt.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as MediaManager
from winrt.windows.storage.streams import DataReader

async def get_media_info():
    sessions = await MediaManager.request_async()
    current_session = sessions.get_current_session()
    if current_session:
        info = await current_session.try_get_media_properties_async()

        info_dict = {
            'artist': info.__getattribute__('artist'),
            'title': info.__getattribute__('title'),
            'thumbnail': info.__getattribute__('thumbnail')
        }

        thumbnail_reference = info_dict['thumbnail']
        if thumbnail_reference is not None:
            stream = await thumbnail_reference.open_read_async()
            size = stream.size

            reader = DataReader(stream)
            await reader.load_async(size)
            buffer = reader.read_buffer(size)
            byte_data = bytes(buffer)

        source_app = current_session.source_app_user_model_id
        return byte_data, info_dict, source_app
    
    else: return None, {}, None