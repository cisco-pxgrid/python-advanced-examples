import asyncio
import io
import unittest

from pxgrid_util.stomp import StompFrame
from pxgrid_util.ws_stomp import WebSocketStomp


class StubWebSocket:
    def __init__(self):
        self.sent = []

    async def send(self, data):
        self.sent.append(data)


class TestWebSocketStomp(unittest.TestCase):
    def test_stomp_subscribe_without_filter_header(self):
        async def run_test():
            ws = WebSocketStomp("wss://example", "user", "secret", None)
            ws.ws = StubWebSocket()
            await ws.stomp_subscribe("/topic/com.cisco.ise.session")
            frame = StompFrame.parse(io.StringIO(ws.ws.sent[0].decode("utf-8")))
            self.assertEqual(frame.get_header("destination"), "/topic/com.cisco.ise.session")
            self.assertEqual(frame.get_header("id"), "my-id")
            self.assertNotIn("filter", frame.headers)

        asyncio.run(run_test())

    def test_stomp_subscribe_with_filter_header(self):
        async def run_test():
            ws = WebSocketStomp("wss://example", "user", "secret", None)
            ws.ws = StubWebSocket()
            await ws.stomp_subscribe(
                "/topic/com.cisco.ise.session",
                headers={"filter": "sessions[?state == 'STARTED']"},
            )
            frame = StompFrame.parse(io.StringIO(ws.ws.sent[0].decode("utf-8")))
            self.assertEqual(frame.get_header("filter"), "sessions[?state == 'STARTED']")

        asyncio.run(run_test())


if __name__ == "__main__":
    unittest.main()
