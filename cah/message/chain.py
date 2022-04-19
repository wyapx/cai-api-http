import time
from typing import List, Union, Type, Optional, Any, Tuple, Generator, Iterable

from pydantic import BaseModel, validator

from .base import MessageModel, RemoteResource, MessageModelTypes
from .models import message_model, Source

MODEL_ARGS = Type[Union[RemoteResource, MessageModel]]


class MessageChain(BaseModel):
    __root__: List[Any]

    @validator("__root__")
    def create(cls, obj):
        ret = []
        for item in obj:
            if isinstance(item, dict):
                ret.append(message_model[item["type"]].parse_obj(item))
            elif isinstance(item, MessageModel):
                ret.append(item)
            else:
                raise ValueError(item)
        return ret

    def get_first_model(self, model_type: Union[Tuple[MODEL_ARGS], MODEL_ARGS]) \
            -> Union[MessageModel, RemoteResource, None]:
        for item in self:
            if isinstance(item, model_type):
                return item

    def get_all_model(self, model_type: Union[Tuple[MODEL_ARGS], MODEL_ARGS]) \
            -> Generator[Union[RemoteResource, MessageModel], None, None]:
        for item in self:
            if isinstance(item, model_type):
                yield item

    def get_source(self) -> Optional[Source]:
        if Source in self:
            return self.__root__[0]

    def get_quote(self) -> Optional["Quote"]:
        return self.get_first_model(Quote)

    def __add__(self, value):
        if isinstance(value, MessageModel):
            self.__root__.append(value)
        elif isinstance(value, MessageChain):
            self.__root__ += value.__root__
        return self

    def __iter__(self):
        if Source in self:
            yield from self.__root__[1:]
        else:
            yield from self.__root__

    def __getitem__(self, index):
        return self.__root__[index]

    def __len__(self):
        return len(self.__root__)

    def __str__(self):
        return "".join([str(item) for item in self])

    def __contains__(self, item):
        for e in self.__root__:
            if isinstance(e, item):
                return True
        return False

    __repr__ = __str__


class CacheMessage(BaseModel):
    type: str
    messageChain: MessageChain


class Quote(MessageModel):
    type = MessageModelTypes.Quote
    id: int
    groupId: int
    senderId: int
    targetId: int
    origin: MessageChain

    def __str__(self):
        return f"[Quote::id={self.id}]"


class MessageNode(BaseModel):
    senderId: int
    time: int
    senderName: Optional[str]
    messageChain: Optional[MessageChain]
    messageId: Optional[int]

    def __repr__(self):
        return f'[Node::sender="{self.senderName}({self.senderId})",time="{self.time}"]'


message_model["Quote"] = Quote
