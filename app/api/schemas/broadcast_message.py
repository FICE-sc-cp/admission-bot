from typing import List

from pydantic import BaseModel


class BroadcastMessage(BaseModel):
    uids: List[str]
    text: str
    parse_mode: str = "HTML"
