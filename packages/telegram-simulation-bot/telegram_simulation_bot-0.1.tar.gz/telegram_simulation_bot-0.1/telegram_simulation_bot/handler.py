import os
from telethon import events


class Handler:
    """Base class for the telegrambot event handler."""

    def __init__(self, bot):
        self.directory = os.getcwd()
        self.directory_name = os.path.relpath(self.directory, os.pardir)
        self._bot = bot
        self.setup()
        self._add_subscribtions()

    def setup(self):
        """Setup children."""
        pass

    def _add_subscribtions(self):
        """Subscribe to the different events."""
        # should be overloaded in childclass.
        return

    def _subscribe(self, pattern, callback):
        """Subscribe to new messages that follow a certain pattern"""
        self._bot.add_event_handler(callback, events.NewMessage(pattern=pattern))
