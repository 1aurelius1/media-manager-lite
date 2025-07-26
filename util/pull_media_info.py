import asyncio
import media_info
import io
from PIL import ImageTk, Image

def pull_media_info():
    byte_data, info_dict, source_app = asyncio.run(media_info.get_media_info())
    if byte_data: thumbnail = Image.open(io.BytesIO(byte_data))
    if source_app == 'Spotify.exe': thumbnail = thumbnail.crop((33, 0, 267, 234))
    return thumbnail, info_dict