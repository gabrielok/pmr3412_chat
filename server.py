# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 16:03:53 2020

@author: Gabriel
"""

import websockets
import asyncio

connected = {} # dictionary of websockets and their usernames
exitApp = False
sys = {'welcome': 'Bem vindo. Identifique-se com /nome seunome',
'newname': 'Nome alterado para ',
'newuser': ' entrou na sala.',
'userleft': ' saiu da sala.',
'namechange': ' mudou o nome para ',
'nametaken': 'Esse nome já foi escolhido. Tente novamente.'}

def parse(message):
    global sys
    msg_start = message.find('!')
    command_name = message.find('/nome')
    command_pm = message.find('/pm')
    if (command_name >= 0): # change username
        old = message[0:msg_start]
        new = message[msg_start + 7:]
        if (old == ''): # didnt have a name
            msg_content1 = ''
            msg_content2 = new
            msg_all = 0
        else: # already had a name
            msg_content1 = old
            msg_content2 = new
            msg_all = -1
        msg_sender = 'system'
        msg_type = '#'
    elif (command_pm >= 0): # private message
        # determine the receiver of the pm
        rstart = command_pm + 4
        rend = message[rstart + 1:].find(' ') + rstart + 1
        receiver = message[rstart:rend]
        msg_content1 = receiver + '~'
        msg_content2 = message[rend + 1:]
        msg_sender = message[0:msg_start] + ' (privado)'
        msg_type = '~'
        msg_all = 1
    else: # regular broadcast message
        msg_content1 = ''
        msg_content2 = message[msg_start + 1:]
        msg_sender = message[0:msg_start]
        msg_type = '!'
        msg_all = 1
    out = [msg_sender, msg_type, msg_content1, msg_content2, msg_all]
    return out

async def register(websocket):
    connected[websocket] = ''
    welcome_message = 'announcement#' + sys['welcome']
    await websocket.send(welcome_message)
    print('New user connected')

async def unregister(websocket):
    if connected[websocket] != '':
        for conn in connected:
            if conn != websocket:
                msg_send = 'announcement#' + connected[websocket] + sys['userleft']
                await conn.send(msg_send)
        print(connected[websocket] + ' disconnected')
    else:
        print('Unknown disconnected')
    connected.pop(websocket)

async def main(websocket, path):
    # this function is called whenever a new connection is established
    await register(websocket)
    try:
        # this for loop ends when the connection closes
        async for message in websocket:
            # parse the received messages
            msg = parse(message)

            # determine whether the sender wants to change name
            if msg[4] == -1:
                taken = False
                for conn in connected:
                    if msg[3] == connected[conn]:
                        taken = True
            elif msg[4] == 0:
                taken = False
                for conn in connected:
                    if msg[3] == connected[conn]:
                        taken = True

            # decide who to forward the message to
            for conn in connected:
                if conn == websocket:
                    if msg[4] != 1:
                        # sender tried to change name
                        if taken:
                            # sender failed name change
                            msg_send = msg[0] + msg[1] + sys['nametaken']
                        else:
                            # first time or not, same message
                            msg_send = msg[0] + msg[1] + sys['newname'] + msg[3]
                            msg_name = 'namechanged' + msg[1] + msg[3]
                            await conn.send(msg_name)
                            connected[websocket] = msg[3] # update the name on the dictionary
                        await conn.send(msg_send)
                else:
                    if msg[4] == 1:
                        # same message for everyone but the sender
                        msg_send = msg[0] + msg[1] + msg[2] + msg[3]
                        await conn.send(msg_send)
                    elif taken == False:
                        if msg[4] == -1: # not the first time
                            msg_send = msg[0] + msg[1] + msg[2] + sys['namechange'] + msg[3]
                        elif msg[4] == 0: # first time
                            msg_send = msg[0] + msg[1] + msg[3] + sys['newuser']
                        await conn.send(msg_send)
    finally:
        await unregister(websocket)

start_server = websockets.serve(main, "127.0.0.1", 5678)
asyncio.get_event_loop().run_until_complete(start_server)
print('Started! Waiting for connections')
asyncio.get_event_loop().run_forever()
