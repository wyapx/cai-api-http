from enum import Enum
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, HttpUrl


class MessageModelTypes(str, Enum):
    Source = "Source"
    Plain = "Plain"
    Face = "Face"
    At = "At"
    AtAll = "AtAll"
    Image = "Image"
    Quote = "Quote"
    Xml = "Xml"
    Json = "Json"
    App = "App"
    Poke = "Poke"
    FlashImage = "FlashImage"
    Voice = "Voice"
    Forward = "Forward"
    File = "File"
    Dice = "Dice"
    MusicShare = "MusicShare"


class MessageModel(BaseModel):
    type: MessageModelTypes


class RemoteResource(BaseModel):
    url: Optional[HttpUrl]
    path: Optional[Path]
    base64: Optional[str]


class Client(BaseModel):
    id: int
    platform: Optional[str]
