import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import os
from config import THREADS_SIZE, BLOCK_SIZE


def download_file(url, start: int, end: int):
    headers = {
        'Range': f'bytes={start}-{end}'
    }
    response = requests.get(url, headers=headers)
    return response.content


def save_file(data):
    with open(f'./files/{file_name}', 'wb') as file:
        file.write(data)


def progress_proc(data, ranges, file_size, threads_size):
    procent_potok = 100/len(ranges)
    dowland = 0
    for i in as_completed(data):
        dowland += procent_potok
        prog = round(dowland, 1)

        update_status = f'url:{url}, file_amount_bytes:{file_size}, threads_size:{threads_size}, status:{prog}'
        with open('./url_list/url_loading.txt', 'r+') as file:
            file.write(update_status)


def default_status(url_list):
    with open("./url_list/urls_queue.txt", "a") as file:
        for url in url_list:
            status = f'url:{url}, status: В очереди'
            file.write(status + '\n')


def delit_line(file_name):
    with open(f'{file_name}', "r") as f:
        lines = f.readlines()

    with open(f'{file_name}', "w") as f:
        f.writelines(lines[1:])


# Процесс скачивания.
def download(url, threads=THREADS_SIZE, block=BLOCK_SIZE):
    response = requests.head(url).headers
    response_head = response['Content-Length']
    file_size = int(response_head)
    # progress_bar = tqdm(total=file_size, unit='iB', unit_scale=True)

    supports_ranges = (
        'Accept-Ranges' in response and response['Accept-Ranges'] == 'bytes'
    )

    delit_line('./url_list/urls_queue.txt')

    # если файл не поддерживает частичную запись.
    if not supports_ranges:
        start = 0
        end = file_size
        download_file(url, start, end)

    else:
        ranges = [(i*block, (i+1)*block-1) for i in range(file_size//block + 1)]

        with ThreadPoolExecutor(max_workers=threads) as executor:
            results = []

            for i in ranges:
                results.append(executor.submit(download_file, url=url, start=i[0], end=i[1]))
                threads_size = threading.active_count()

            progress_proc(results, ranges, file_size, threads_size)

            downloaded_file = b''.join([r.result() for r in results])

        save_file(downloaded_file)

    os.system(r'>./url_list/url_loading.txt')
    check_file = os.path.exists(f'./files/{file_name}')

    if check_file:
        status = f'url:{url}, file_amount_bytes:{file_size}, status: downloaded'
        with open("./url_list/urls_download.txt", "a") as file:
            file.write(status + '\n')


with open("./url_list/flag.txt", "r") as file:
    while True:
        flag = file.readline()
        if flag == 'end':
            urls = open('./url_list/urls.txt', 'r').readline()
            url_list = urls.split('#')
            url_list.pop(-1)
            default_status(url_list)
    
            for url in url_list:
                file_name = (url.split('/'))[-1]
                download(url)
            os.system(r'>./url_list/urls.txt')
            os.system(r'>./url_list/flag.txt')
        else:
            continue
