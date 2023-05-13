import asyncio
import websockets
import os
import pathlib
from config import HOST, PORT


async def handler(websocket):
    while True:
        url = await websocket.recv()

        file_name = (url.split('/'))[-1]

        check_file = os.path.exists(f'./files/{file_name}')

        if check_file:
            path_file = f'file:///{pathlib.Path.cwd()}/url_list/{file_name}'
            await websocket.send(path_file)
        else:
            with open("./url_list/urls.txt", "r+") as file:
                file.write(url)

            while True:
                with open("./url_list/url_status.txt", "r") as file:
                    status = file.readlines()
                    if status == []:
                        continue
                    else:
                        await websocket.send(status)
                        os.system(r'>./url_list/url_status.txt')
                        break

start_server = websockets.serve(handler, HOST, PORT)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
