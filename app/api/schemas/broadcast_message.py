from typing import List
from aiogram.enums.parse_mode import ParseMode

from pydantic import BaseModel


class BroadcastMessage(BaseModel):
    uids: List[str]
    text: str
    parse_mode: ParseMode = ParseMode.HTML
