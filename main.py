import asyncio
import threading
import io
import tkinter as tk
from tkinter import ttk, Label, Button
from PIL import ImageTk, Image
from util import media_controls, media_info, media_timeline, check_media_status

# cache current, previous, and next covers and titles for usage