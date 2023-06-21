import asyncio
import websockets
import os
import pathlib
from config import HOST, PORT
import validators
import requests
from texts import (
    FORMAT_URL_ERROR,
    RESPONSE_ERROR,
    MESSAGE_START_DOWNLOAD,
    MESSAGE_URL_DOWNLOAD,
    MESSAGE_WAITING,
    SERVER_COMMAND_ERROR,
    KEY_URL_ERROR,
    EMPTY_LIST
)


# Валидация URL
def validate(url):
    try:
        if url == 'end':
            with open("./data/urls.txt", "r") as file:
                line = file.readlines()

            if line == []:
                return EMPTY_LIST
            else:
                with open("./data/flag.txt", "r+") as file:
                    file.write('end')
                return MESSAGE_START_DOWNLOAD

        val = validators.url(url)
        if not val:
            return FORMAT_URL_ERROR

        response = requests.head(url)
        if response.status_code != 200:
            return RESPONSE_ERROR

        conten_type = response.headers['Content-Type']
        if conten_type == 'text/html; charset=UTF-8':
            return KEY_URL_ERROR

        return 'OK'

    except requests.exceptions.ConnectionError:
        return RESPONSE_ERROR


async def handler(websocket):

    os.system(r'>./data/urls.txt')
    os.system(r'>./data/flag.txt')
    os.system(r'>./data/urls_loading.txt')
    os.system(r'>./data/urls_queue.txt')

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

                val = validate(url)

                if val != 'OK':
                    await websocket.send(val)

                else:
                    file_name = (url.split('/'))[-1]
                    check_file = os.path.exists(f'./files/{file_name}')

                    if check_file:
                        path_file = (
                            f'file:///{pathlib.Path.cwd()}/files/{file_name}'
                        )
                        await websocket.send(
                            f'{MESSAGE_URL_DOWNLOAD} {path_file}'
                        )
                    else:
                        url_list.append(url)
                        with open("./data/urls.txt", "a+") as file:
                            file.write(f'{url}#')

        elif (
            command == 'queue' or
            command == 'loading' or
            command == 'download' or
            command == 'help_command'
        ):
            with open(f'./data/urls_{command}.txt', 'r') as file:
                list_line = file.readlines()
            for line in list_line:
                await websocket.send(line)

        else:
            await websocket.send(SERVER_COMMAND_ERROR)

start_server = websockets.serve(handler, HOST, PORT)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
