import requests
from threading import Thread

# URL для загрузки
url = 'https://dwweb.ru/__a-data/__all_for_scripts/__rar/pro_dw_koments_1_3.rar'

# Размер блока, который будет скачиваться каждым потоком (в байтах) 1 мегабайт
BLOCK_SIZE = 1024*1024

# Количество потоков
THREADS = 4

# Отправляем запрос для получения загаловка
response_head = requests.head(url).headers

# Проверяем, поддерживает ли сервер загрузку по частям
supports_ranges = (
    'Accept-Ranges' in response_head and response_head['Accept-Ranges'] == 'bytes'
)

# Получаем размер файла
file_size = int(response_head['Content-Length'])


# Функция, скачивающая блок файла по указанному диапазону байтов
def download_fail(url, start: int, end: int) -> None:
    headers = {'Range': f'bytes={start}-{end}'}
    response = requests.get(url, headers=headers, stream=True)

    with open('file', 'wb') as f:
        f.seek(start) # зачем
        f.write(response.content)


# Если Ranges не поддерживается, то скачиваем файл полностью
if not supports_ranges:
    download_fail(url, 0, file_size)

# Иначе делим файл на блоки и запускаем на скачивание потоки
else:
    threads = []
    for i in range(0, file_size, BLOCK_SIZE):
        start = i
        end = min(i + BLOCK_SIZE, file_size)
        thread = Thread(target=download_fail, args=(url, start, end))
        threads.append(thread)
        thread.start()

        if len(threads) >= THREADS:
            for thread in threads:
                thread.join()
            threads = []

    for thread in threads:
        thread.join()
