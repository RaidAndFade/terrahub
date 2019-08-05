#from __future__ import annotations
from terrelay.tconnection import TPlugin, TClientConnection, TRelayServer
from terrelay.tcommands import reg_command
from plugins.discordchat.creds import clienttkn
import asyncio
#import docker
from subprocess import PIPE
import signal
import select
import os

import tsecrets

class TerraHub(TPlugin):
    def __init__(self):
        pass        

    async def fake_superadmin(self,host,code):
        from .fakeplayer import FakePlayerConnection
        fpc = FakePlayerConnection()
        await fpc.connect(host)
        while not fpc.ready:
            await asyncio.sleep(0.5)
        await fpc.sendchat("/auth "+code)
        await fpc.sendchat("/user add "+tsecrets.su+" superadmin")
        await fpc.sendchat("/login "+tsecrets.su)
        await fpc.sendchat("/auth")
        await fpc.close()

    async def process_stream(self,stream,prefix,host): 
        while True:
            l = (await stream.readline()).decode("utf-8")
            if "To become superadmin, join the game and type /auth " in l:
                await self.fake_superadmin(host,l[51:])
            print(prefix + l,end="")

    async def on_plugin_load(self,srv:TRelayServer):
        self.hubserver = await asyncio.create_subprocess_exec("/bin/bash","-c",'cd /terrahub/bin && /usr/bin/mono TerrariaServer.exe -world '+tsecrets.hub['world']+' -port '+tsecrets.hub['port']+' -autocreate 1 --stats-optout -configpath '+tsecrets.hub['config'], stdout=PIPE, stderr=PIPE, stdin=PIPE)
        asyncio.get_event_loop().create_task(self.process_stream(self.hubserver.stdout,"[HUB] ",("localhost",tsecrets.hub['port'])))
        
    async def on_plugin_unload(self,srv:TRelayServer):
        self.hubserver.send_signal(signal.SIGINT)

    async def on_chat_message(self,srv:TRelayServer,cl:TClientConnection,msg:str,emote:bool):
        pass
    async def on_connection(self,srv:TRelayServer,cl:TClientConnection):

        pass
    async def on_server_join(self,srv:TRelayServer,cl:TClientConnection,server:str):
        pass
    async def on_server_leave(self,srv:TRelayServer,cl:TClientConnection,server:str):
        pass
    async def on_disconnect(self,srv:TRelayServer,cl:TClientConnection):
        pass
