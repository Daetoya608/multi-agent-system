from pyrogram import Client

class TelegramClientAdapter:
    def __init__(self, app: Client):
        self._app = app

