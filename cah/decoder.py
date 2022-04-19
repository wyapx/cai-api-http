from .method import SendMessage, Response


async def send_group_message(content: dict) -> dict:
    return {
        "code": 0,
        "messageId": -1
    }


handlers = {
    "sendGroupMessage": send_group_message
}