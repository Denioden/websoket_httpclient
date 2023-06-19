import asyncio
import websockets
import os
import pathlib
from config import HOST, PORT
import validators


async def handler(websocket):
    help_text = (
        'start - Начать запись ссылок'
        'end - Закончить запись ссылок и отправить их на скачивание'
        'queue - Показить ссылки в ожидании'
        'loading - Покать ссылку по которой происходит загрузка'
        'download - Показать сслки по которым загрузились файлы'
    )
    await websocket.send(help_text)
    while True:
        with open("./url_list/flag.txt", "r") as file:
            flag = file.readline()

        comand = await websocket.recv()
        if comand == 'start' and flag == 'end':
            text_error = 'Для добавления новых ссылок на скачивание, дождитесь окончания загрузки'
            await websocket.send(text_error)

        elif comand == 'start':
            url = 'zero'
            url_list = []
            while url != 'end':
                url = await websocket.recv()
                val = validators.url(url)

                if url == 'end':
                    await websocket.send('Отправка ссылок на скачивание')
                    with open("./url_list/flag.txt", "r+") as file:
                        file.write('end')
                    
                elif not val:
                    text_error = 'Ссылка не соответствует формату'
                    await websocket.send(text_error)

                else:
                    file_name = (url.split('/'))[-1]

                    # проверяем наличие файла.
                    check_file = os.path.exists(f'./files/{file_name}')

                    if check_file:
                        path_file = f'file:///{pathlib.Path.cwd()}/url_list/{file_name}'
                        await websocket.send(path_file)

                    else:
                        url_list.append(url)

                        with open("./url_list/urls.txt", "a+") as file:
                            file.write(f'{url}#')
         
        elif comand == 'queue':
            with open("./url_list/urls_queue.txt", "r") as file:
                queue = file.readlines()
                for status in queue:
                    await websocket.send(status)
        
        elif comand == 'loading':
            with open("./url_list/url_loading.txt", "r") as file:
                url = file.readline()
                await websocket.send(url)
        
        elif comand == 'download':
            with open("./url_list/urls_download.txt", "r") as file:
                url_dowload = file.readlines()
                for url in url_dowload:
                    await websocket.send(url)

        elif comand == 'help':
            await websocket.send(help_text)


start_server = websockets.serve(handler, HOST, PORT)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()