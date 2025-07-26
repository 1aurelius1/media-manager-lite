import asyncio
from winrt.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as MediaManager

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

        return timeline_dict