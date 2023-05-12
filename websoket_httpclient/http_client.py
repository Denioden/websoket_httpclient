import requests
from concurrent.futures import ThreadPoolExecutor
import threading
import os

UR = open('./url_list/urls.txt', 'r').readlines()
URL = UR[-1]

THREADS_SIZE = 4
BLOCK_SIZE = 1024*100

file_name = (URL.split('/'))[-1]


def download_fail(url, start: int, end: int):
    headers = {'Range': f'bytes={start}-{end}'}
    response = requests.get(url, headers=headers)

    with open(f'./files/{file_name}', 'wb') as file:
        file.seek(start)
        file.write(response.content)
        

def download(url, threads, block):

    response_head = requests.head(url).headers
    file_size = int(response_head['Content-Length'])

    supports_ranges = (
        'Accept-Ranges' in response_head and response_head['Accept-Ranges'] == 'bytes'
    )

    if not supports_ranges:
        start = 0
        end = file_size
        download_fail(url, start, end)

    else:
        with ThreadPoolExecutor(max_workers=threads-1) as executor:
            for i in range(0, file_size, block):
                start = i
                end = min(i + block, file_size)
                executor.submit(download_fail, url, start, end)
                threads_size = threading.active_count()
    
    check_file = os.path.exists(f'./files/{file_name}')

    if check_file:
        progres = 'downlanded'
    else:
        progres = 'not downlanded '

    status = f'url:{url}, file_amount_bytes:{file_size}, threads_amount:{threads_size}, progress:{progres}'

    print(status)

    with open("./url_list/url_status.txt", "a") as file:
        file.write(status + '\n')
        file.close()

download(URL, THREADS_SIZE, BLOCK_SIZE)