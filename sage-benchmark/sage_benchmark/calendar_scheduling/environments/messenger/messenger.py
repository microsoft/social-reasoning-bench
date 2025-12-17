from collections import defaultdict

from pydantic import BaseModel


class Message(BaseModel):
    to: str
    from_: str
    message: str


class Messenger:
    def __init__(self):
        self._messages: list[Message] = []
        self._last_read_index: dict[str, int] = defaultdict(int)

    def send_message(self, message: Message):
        self._messages.append(message)

    def get_unread_messages(self, to: str):
        last_read_index = self._last_read_index[to]
        self._last_read_index[to] = len(self._messages)
        return [message for message in self._messages[last_read_index:] if message.to == to]

    def get_all_messages(self, to: str):
        self._last_read_index[to] = len(self._messages)
        return [message for message in self._messages if message.to == to]
