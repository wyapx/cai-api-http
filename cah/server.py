import asyncio
import os

from aiohttp import web

from typing import TYPE_CHECKING, Dict, List, Optional
from .decoder import handlers
from .method import Request, Response

if TYPE_CHECKING:
    from aiohttp.client_ws import WSMessage


class MainServer:
    def __init__(self, dispatcher, verify_key="TestOnly"):
        self.dispatcher = dispatcher
        self.app = web.Application()
        self._verify_key = verify_key
        self.sessions: Dict[str, int] = {}
        self._ws_bound: Dict[int, List[web.WebSocketResponse]] = {}

    async def emit(self, qq: int, data: dict):
        for ws in self._ws_bound[qq]:
            await ws.send_json(data)

    async def task(self, ws: web.WebSocketResponse):
        count = 0
        await asyncio.sleep(1)
        while True:
            if count > 40000:
                print("done")
                break
            else:
                count += 1
            await ws.send_json(
                {
                    "syncId": "-1",
                    "data": {
                        "type": "GroupMessage",
                        "messageChain": [{"type": "Plain", "text": "老阿姨"}],
                        "sender": {
                            "id": 1,
                            "memberName": "?",
                            "permission": "MEMBER",
                            "group": {
                                "id": 2,
                                "name": "??",
                                "permission": "MEMBER"
                            }
                        }
                    }
                }
            )
            #await asyncio.sleep(0.01)

    def register(self):
        self.app.add_routes([
            web.get("/all", self.listen_all),
            web.get("/message", self.listen_all),
            web.get("/event", self.blocker)
        ])

    async def blocker(self, request: web.Request):
        ws = await self._verify_and_prepare(request)
        async for msg in ws:
            pass

    async def _verify_and_prepare(self, request: web.Request) -> Optional[web.WebSocketResponse]:
        ws = web.WebSocketResponse(autoping=False, autoclose=True)
        if not ws.can_prepare(request) or not ("qq" and "verifyKey" in request.query):
            return
        elif request.query.get("verifyKey") == self._verify_key:
            await ws.prepare(request)
            return ws

    async def receiver(self, ws: web.WebSocketResponse):
        async for msg in ws:  # type: WSMessage
            if msg.type == web.WSMsgType.TEXT:
                req = Request.parse_obj(msg.json())  # type: Request
                if req.syncId and req.content["sessionKey"] in self.sessions:
                    if req.command in handlers:
                        await ws.send_json(
                            Response(
                                syncId=req.syncId,
                                data=await handlers[req.command](req.content)
                            ).dict()
                        )
            elif msg.type == web.WSMsgType.PING:
                await ws.pong()
            elif msg.type == web.WSMsgType.CLOSE:
                break

    async def listen_all(self, request: web.Request):
        ws = await self._verify_and_prepare(request)
        if ws == None:
            return web.HTTPBadRequest()
        verify_key, qq, session = (
            request.query.get("verifyKey"),
            int(request.query.get("qq")),
            os.urandom(16).hex()
        )
        self.sessions[session] = qq
        if qq in self._ws_bound:
            self._ws_bound[qq].append(ws)
        else:
            self._ws_bound[qq] = [ws]
        await ws.send_json({"syncId": 0, "data": {"code": 0, "session": session}})
        asyncio.create_task(self.task(ws))
        try:
            await self.receiver(ws)
        finally:
            self.sessions.pop(session)
            self._ws_bound[qq].remove(ws)
        print("done!！")

    async def _run(self, port, host):
        self.register()
        await web._run_app(self.app, host=host, port=port)

    def run(self, port: int, host="0.0.0.0"):
        asyncio.run(self._run(port, host))
