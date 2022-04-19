from typing import Optional

from pydantic import BaseModel

from .message.chain import MessageChain


class Response(BaseModel):
    syncId: str
    data: dict


class BaseSession(BaseModel):
    sessionKey: str


class Request(BaseModel):
    syncId: str
    command: str
    subCommand: Optional[str]
    content: dict


class NewResponse(BaseSession):
    eventId: int
    fromId: int
    groupId: int
    message: Optional[str] = ""
    sessionKey: str
    operate: int


class SendMessage(BaseSession):
    target: int
    quote: Optional[int]
    messageChain: MessageChain


class SendTempMessage(BaseSession):
    qq: int
    group: int
    quote: Optional[int]
    messageChain: MessageChain


class GetInfoFromTarget(BaseSession):
    target: int


class GetInfoFromId(BaseSession):
    id: int


class GetMemberProfile(GetInfoFromTarget):
    memberId: int


class SetMemberPermission(GetMemberProfile):
    assign: bool


class FileOperation(GetInfoFromTarget):
    id: str
    group: Optional[int]
    qq: Optional[int]


class GetFile(FileOperation):
    withDownloadInfo: bool = True


class MakeDir(FileOperation):
    directoryName: str


class MoveFile(FileOperation):
    moveTo: str


class SendNudge(GetInfoFromTarget):
    subject: int
    kind: str


class MuteMember(GetMemberProfile):
    time: int


class KickMember(GetMemberProfile):
    msg: Optional[str]
