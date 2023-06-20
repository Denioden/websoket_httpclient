import asyncio
import websockets
import os
import pathlib
from config import HOST, PORT
import validators
import requests
from texts import (
    FORMAT_URL_ERROR,
    MESSAGE_START_DOWNLOAD,
    MESSAGE_WAITING,
    RESPONSE_ERROR,
    SERVER_COMMAND_ERROR
)


async def handler(websocket):
    while True:
        with open("./data/flag.txt", "r") as file:
            flag = file.readline()

        command = await websocket.recv()

        if command == 'start' and flag == 'end':
            await websocket.send(MESSAGE_WAITING)

        elif command == 'start':
            url = 'null'
            url_list = []
            while url != 'end':
                url = await websocket.recv()
                val = validators.url(url)
                response = requests.head(url)

                if url == 'end':
                    await websocket.send(MESSAGE_START_DOWNLOAD)
                    with open("./data/flag.txt", "r+") as file:
                        file.write('end')
                    
                elif not val:
                    await websocket.send(FORMAT_URL_ERROR)
                
                elif response.status_code != 200:
                    await websocket.send(RESPONSE_ERROR)

                else:
                    file_name = (url.split('/'))[-1]
                    check_file = os.path.exists(f'./files/{file_name}')

                    if check_file:
                        path_file = f'file:///{pathlib.Path.cwd()}/files/{file_name}'
                        await websocket.send(path_file)

                    else:
                        url_list.append(url)
                        with open("./data/urls.txt", "a+") as file:
                            file.write(f'{url}#')

        elif command == ('queue') or ('loading') or ('download') or ('help_command'):
            with open(f'./data/urls_{command}.txt', 'r') as file:
                list_line = file.readlines()
            for line in list_line:
                await websocket.send(line)

        else:
            await websocket.send(SERVER_COMMAND_ERROR)

start_server = websockets.serve(handler, HOST, PORT)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
