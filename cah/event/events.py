import datetime
from typing import Optional, Dict, List, Any

from pydantic import Field, BaseModel

from cah.component.friend import Friend
from cah.component.group import Permission, Group, Member, GroupHonorAction
from cah.event.base import BotEvent, GroupEvent, FriendEvent


class BotOnlineEvent(BotEvent):
    type = "BotOnlineEvent"


class BotOfflineEvent(BotEvent):
    type = "BotOfflineEvent"


class BotOfflineEventForce(BotEvent):
    type = "BotOfflineEventForce"


class BotOfflineEventDropped(BotEvent):
    type = "BotOfflineEventDropped"


class BotReloginEvent(BotEvent):
    type = "BotReloginEvent"


class FriendInputStatusChangedEvent(FriendEvent):
    type = "FriendInputStatusChangedEvent"
    inputting: bool


class FriendNickChangedEvent(FriendEvent):
    type = "FriendNickChangedEvent"
    from_: str = Field(..., alias="from")
    to: str


class FriendRecallEvent(FriendEvent):
    type = "FriendRecallEvent"
    authorId: int
    messageId: int
    time: datetime.datetime
    operator: int


class BotGroupPermissionChangeEvent(GroupEvent):
    type = "BotGroupPermissionChangeEvent"
    origin: Permission
    current: Permission
    group: Group


class BotMuteEvent(GroupEvent):
    type = "BotMuteEvent"
    durationSeconds: int
    operator: Member


class BotUnmuteEvent(GroupEvent):
    type = "BotUnmuteEvent"
    operator: Member


class BotJoinGroupEvent(GroupEvent):
    type = "BotJoinGroupEvent"
    group: Group
    invitor: Optional[Member]


class BotLeaveEventActive(GroupEvent):
    type = "BotLeaveEventActive"
    group: Group


class BotLeaveEventKick(GroupEvent):
    type = "BotLeaveEventKick"
    group: Group
    operator: Member


class GroupRecallEvent(GroupEvent):
    type = "GroupRecallEvent"
    authorId: int
    messageId: int
    time: datetime.datetime
    group: Group
    operator: Member


class GroupNameChangeEvent(GroupEvent):
    type = "GroupNameChangeEvent"
    origin: str
    current: str
    group: Group
    operator: Member


class GroupEntranceAnnouncementChangeEvent(GroupEvent):
    type = "GroupEntranceAnnouncementChangeEvent"
    origin: str
    current: str
    group: Group
    operator: Member


class GroupMuteAllEvent(GroupEvent):
    type = "GroupMuteAllEvent"
    origin: bool
    current: bool
    group: Group
    operator: Member


class GroupAllowAnonymousChatEvent(GroupEvent):
    type = "GroupAllowAnonymousChatEvent"
    origin: bool
    current: bool
    group: Group
    operator: Member


class GroupAllowConfessTalkEvent(GroupEvent):
    type = "GroupAllowAnonymousChatEvent"
    origin: bool
    current: bool
    group: Group


class GroupAllowMemberInviteEvent(GroupEvent):
    type = "GroupAllowMemberInviteEvent"
    origin: bool
    current: bool
    group: Group
    operator: Member


class MemberJoinEvent(GroupEvent):
    type = "MemberJoinEvent"
    member: Member
    invitor: Optional[Member]


class MemberLeaveEventKick(GroupEvent):
    type = "MemberLeaveEventKick"
    member: Member
    operator: Member


class MemberLeaveEventQuit(GroupEvent):
    type = "MemberLeaveEventQuit"
    member: Member


class MemberCardChangeEvent(GroupEvent):
    type = "MemberCardChangeEvent"
    origin: str
    current: str
    member: Member


class MemberSpecialTitleChangeEvent(GroupEvent):
    type = "MemberSpecialTitleChangeEvent"
    origin: str
    current: str
    member: Member


class MemberPermissionChangeEvent(GroupEvent):
    type = "MemberPermissionChangeEvent"
    origin: str
    current: str
    member: Member


class MemberMuteEvent(GroupEvent):
    type = "MemberMuteEvent"
    durationSeconds: int
    member: Member
    operator: Member


class MemberUnmuteEvent(GroupEvent):
    type = "MemberUnmuteEvent"
    member: Member
    operator: Member


class MemberHonorChangeEvent(GroupEvent):
    type = "MemberHonorChangeEvent"
    member: Member
    action: GroupHonorAction
    honor: str


class CommandExecutedEvent(BaseModel):
    type: str = "CommandExecutedEvent"
    name: str
    friend: Optional[Friend]
    member: Optional[Member]
    args: List[Dict[str, Any]]


class _NudgeSubject(BaseModel):
    id: int
    kind: str


class NudgeEvent(BaseModel):
    type: str = "NudgeEvent"
    fromId: int
    subject: _NudgeSubject
    action: str
    suffix: str
    target: int


class NewRequestEvent(BaseModel):
    type: str
    nick: str
    eventId: int
    fromId: int
    groupId: int
    message: Optional[str] = ""


class NewFriendRequestEvent(NewRequestEvent):
    type = "NewFriendRequestEvent"


class MemberJoinRequestEvent(NewRequestEvent):
    type = "MemberJoinRequestEvent"
    groupName: str


class BotInvitedJoinGroupRequestEvent(NewRequestEvent):
    type = "BotInvitedJoinGroupRequestEvent"
    groupName: str
