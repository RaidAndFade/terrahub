from terrelay.tconnection import TerrariaConnection, prepstr
import asyncio
import uuid
class FakePlayerConnection(TerrariaConnection):
    def __init__(self):
        self.ready = False
        TerrariaConnection.__init__(self,None,None)

    async def connect(self,dest):
        self.reader,self.writer = await asyncio.open_connection(dest[0],dest[1])
        asyncio.get_event_loop().create_task(self.listen())
        await self.writepkt(b"\x01"+prepstr("Terraria194"))

    async def sendchat(self, msg:str):
        await self.writepkt(b"\x52\x01"+self.pid+b"\x03\x53\x61\x79"+prepstr(msg))

    async def handle_pkt(self,pkt):
        if pkt[0] == 0x03: # player
            self.pid = bytes([pkt[1]])
            await self.writepkt(b"\x04"+self.pid+b"\x00\x00"+prepstr("SERVER")+b"\x00\x00\x00\x00"+b"\x00\x00\x00"*7+b"\x00")
            await self.writepkt(b"\x44"+prepstr(str(uuid.uuid4())))
            await self.writepkt(b"\x10"+self.pid+b"\x99\x99")
            await self.writepkt(b"\x2a"+self.pid+b"\x99\x99")
            await self.writepkt(b"\x32"+self.pid+b"\x35\xbe"+b"\x00"*20)
            for x in range(0,0xdb+1):
                await self.writepkt(b"\x05"+self.pid+bytes(x)+b"\x00\x00\x00\x00\x00")
            await self.writepkt(b"\x06")
        elif pkt[0] == 0x07: # world info
            await self.writepkt(b"\x08\xff\xff\xff\xff\xff\xff\xff\xff")
        elif pkt[0] == 0x31:
            await self.writepkt(b"\x0c"+self.pid+b"\xff\xff\xff\xff")
            self.ready = True
    