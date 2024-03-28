from typing import Callable
from threading import Thread
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message

from entities.user import UserCreate
from providers.user_provider import UserProvider
from general import Session, create_session
from services.abstract_service import AbstractService


class TelegramService(AbstractService):

    # Initialization

    def __init__(self, token: str, get_user_provider: Callable[[Session], UserProvider]):
        super().__init__()
        self.token = token
        self.get_user_provider = get_user_provider
        self.bot = Bot(token=self.token)
        self.dp = Dispatcher(self.bot)
        self._register_handlers()

    # override
    def main_loop(self):
        self.dp.run_polling()

    def _loop_iteration(self): pass # don't need it here

    # Endpoints (private)

    def _register_handlers(self):
        self.dp.register_message_handler(self._register, commands=["register"])

    async def _register(self, message: Message):

        _, name, email = message.text.split()
        user = UserCreate(name=name, email=email, password="")

        with create_session() as session:
            self.get_user_provider(session).create_user(user)

        await message.reply("User created!")
