import os
import random
from enum import Enum
from io import BytesIO
from typing import Optional, Union, Literal, BinaryIO

from pydantic import Json as Json_t

from .base import MessageModel, RemoteResource, MessageModelTypes
from ..component.group import Member


class Source(MessageModel):
    type = MessageModelTypes.Source
    id: int
    time: int

    def __init__(self, id: int, time: int, **_):
        super(Source, self).__init__(
            id=id,
            time=time
        )

    def __int__(self):
        return self.id

    def __str__(self):
        return f"[source:{self.id}]"


class Plain(MessageModel):
    type = MessageModelTypes.Plain
    text: str

    def __init__(self, text: str, **_):
        super(Plain, self).__init__(text=text)

    def __str__(self):
        return self.text


class At(MessageModel):
    type = MessageModelTypes.At
    target: int

    def __init__(self, target: Union[int, Member], **_):
        super(At, self).__init__(target=target)

    def __str__(self):
        return f"[mirai:at:{self.target}]"


class AtAll(MessageModel):
    type = MessageModelTypes.AtAll

    def __str__(self):
        return "[mirai:atall]"


class Face(MessageModel):
    type = MessageModelTypes.Face
    faceId: int
    name: str

    def __init__(self, faceId: int, name: str, **_):
        super(Face, self).__init__(
            faceId=faceId,
            name=name
        )

    def __str__(self):
        return f"[mirai:face:{self.faceId}]"


class Image(MessageModel, RemoteResource):
    type = MessageModelTypes.Image
    imageId: Optional[str]

    def __init__(self, imageId=None, path=None, url=None, base64=None, **_):
        """
        :type imageId: str
        :type path: Path
        :type url: HttpUrl
        :type base64: str
        """
        super(Image, self).__init__(
            imageId=imageId,
            path=path,
            url=url,
            base64=base64
        )

    @classmethod
    def from_path(cls, path: str):
        if not os.path.isfile(path):
            raise FileNotFoundError(path)
        return UnpreparedResource(cls, "uploadImage", io=open(path, "rb"))

    @classmethod
    def from_io(cls, obj: BinaryIO):
        return UnpreparedResource(cls, "uploadImage", io=obj)

    @classmethod
    def from_bytes(cls, data: bytes):
        return cls.from_io(BytesIO(data))

    def __str__(self):
        return f"[mirai:image:{self.imageId}]"


class FlashImage(Image):
    type = MessageModelTypes.FlashImage

    def __str__(self):
        return f"[mirai:flash:{self.imageId}]"


class Voice(MessageModel, RemoteResource):
    type = MessageModelTypes.Voice
    length: Optional[int] = 0
    voiceId: Optional[str]

    def __init__(self, voiceId=None, path=None, url=None, base64=None, **_):
        """
        :type voiceId: str
        :type path: Path
        :type url: HttpUrl
        :type base64: str
        """
        super(Voice, self).__init__(
            voiceId=voiceId,
            path=path,
            url=url,
            base64=base64
        )

    @classmethod
    def from_path(cls, path: str):
        if not os.path.isfile(path):
            raise FileNotFoundError(path)
        return UnpreparedResource(cls, "uploadVoice", io=open(path, "rb"))

    @classmethod
    def from_io(cls, obj: BinaryIO):
        return UnpreparedResource(cls, "uploadVoice", io=obj)

    @classmethod
    def from_bytes(cls, data: bytes):
        return cls.from_io(BytesIO(data))

    def __str__(self):
        return f"[mirai:voice:{self.voiceId}]"


class Xml(MessageModel):
    type = MessageModelTypes.Xml
    xml: str

    def __init__(self, xml: str, **_):
        super(Xml, self).__init__(xml=xml)

    def __str__(self):
        return f"[mirai:xml:{self.xml}]"


class Json(MessageModel):
    """
    废弃的方法，请使用App代替
    """

    type = MessageModelTypes.Json
    Json: str

    def __init__(self, json: str, **_):
        super(Json, self).__init__(Json=json)

    def dict(self, *_, **kwargs) -> dict:
        data = dict(
            *self._iter(
                to_dict=True,
                **kwargs
            )
        )
        data["json"] = data.pop("Json")
        return data

    def __str__(self):
        return f"[mirai:json:{self.Json}]"


class App(MessageModel):
    type = MessageModelTypes.App
    content: Json_t

    def __init__(self, content: str, **_):
        super(App, self).__init__(content=content)

    def to_dict(self) -> dict:
        return dict(self.content)

    def __str__(self):
        return f"[mirai:app:{self.content}]"


class Poke(MessageModel):
    type = MessageModelTypes.Poke
    name: str

    class InternalType(Enum):
        SixSixSix = ("SixSixSix", 5, -1)
        ShowLove = ("ShowLove", 2, -1)
        Like = ("Like", 3, -1)
        Heartbroken = ("Heartbroken", 4, -1)
        FangDaZhao = ("FangDaZhao", 6, -1)
        ChuoYiChuo = ("ChuoYiChuo", 1, -1)

    class Type(str, Enum):
        ChuoYiChuo = "ChuoYiChuo"
        BiXin = "BiXin"
        Rose = "Rose"
        QiaoMen = "QiaoMen"
        XinSui = "XinSui"
        BaoBeiQiu = "BaoBeiQiu"
        GouYin = "GouYin"
        SuiPing = "SuiPing"
        DianZan = "DianZan"
        FangDaZhao = "FangDaZhao"
        ShouLei = "ShouLei"
        RangNiPi = "RangNiPi"
        ZhaoHuanShu = "ZhaoHuanShu"
        ZhuaYiXia = "ZhuaYiXia"
        LiuLiuLiu = "LiuLiuLiu"
        JeiYin = "JeiYin"

    @classmethod
    def random_type(cls):
        return cls(random.choice(list(cls.Type)))

    def __init__(self, name: Type, **_):
        if isinstance(name, self.Type):
            super(Poke, self).__init__(name=name.value)
        else:
            super(Poke, self).__init__(name=name)

    def __str__(self):
        # mapper: https://github.com/mamoe/mirai/blob/dev/mirai-core-api/src/commonMain/kotlin/message/data/PokeMessage.kt#L60
        return "[mirai:poke:{0},{1},{2}]".format(*getattr(self.InternalType, self.name).value)


class Dice(MessageModel):
    type = MessageModelTypes.Dice
    value: int

    def __init__(self, value: Literal[1, 2, 3, 4, 5, 6], **_):
        if not 1 <= value <= 6:
            raise OverflowError(
                f"value must be in 1 to 6, {value} got"
            )
        super(Dice, self).__init__(value=value)

    def __int__(self):
        return self.value

    def __str__(self):
        return f"[mirai:dice:{self.value}]"


class MusicShare(MessageModel):
    type = MessageModelTypes.MusicShare
    kind: str
    title: str
    summary: str
    jumpUrl: str
    pictureUrl: str
    musicUrl: str
    brief: str

    def __init__(self, kind: str, title: str, summary: str, jump_url: str, pic_url: str, music_url: str, brief: str):
        super(MusicShare, self).__init__(
            kind=kind,
            title=title,
            summary=summary,
            jumpUrl=jump_url,
            pictureUrl=pic_url,
            musicUrl=music_url,
            brief=brief
        )

    def __str__(self):
        return f"[MusicShare::title='{self.title}',musicUrl='{self.musicUrl}']"


class File(MessageModel):
    type = MessageModelTypes.File
    name: str
    size: Optional[int]

    def __str__(self):
        return f"[File::name='{self.name}']"


message_model = {
    "Source": Source,
    "Plain": Plain,
    "At": At,
    "AtAll": AtAll,
    "Face": Face,
    "Image": Image,
    "FlashImage": FlashImage,
    "Voice": Voice,
    "Xml": Xml,
    "Json": Json,
    "App": App,
    "Poke": Poke,
    "Dice": Dice,
    "MusicShare": MusicShare,
    "File": File
}
