# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 16:03:53 2020

@author: Gabriel
"""

import websockets
import asyncio
import datetime

async def time(websocket, path):
    while True:
        now = datetime.datetime.utcnow().isoformat() + "Z"
        await websocket.send('Robson!Oi')
        await websocket.send('Manuel!oi')
        await asyncio.sleep(5)

start_server = websockets.serve(time, "127.0.0.1", 5678)
print('Connected!')

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
