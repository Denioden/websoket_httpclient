import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import os
from config import THREADS_SIZE, BLOCK_SIZE

import validators # !!!

# from clint.textui import progress
from tqdm import tqdm

# Скачивания файла целиком или по частям


def download_file(url, start: int, end: int):
    headers = {
        'Range': f'bytes={start}-{end}'
    }
    response = requests.get(url, headers=headers)
    return response.content


def save_file(data):
    with open(f'./files/{file_name}', 'wb') as file:
        file.write(data)



def progress_proc(data, ranges):
    procent_potok = 100/len(ranges)
    dowland = 0
    for i in as_completed(data):
        dowland += procent_potok
        prog = round(dowland, 1)
        print(f"{prog}% downloaded", end='\r')
        with open(f'./url_list/progress.txt', 'r+') as file:
            file.write(str(prog))
         


# Процесс скачивания.
def download(url, threads=THREADS_SIZE, block=BLOCK_SIZE):
    response = requests.head(url).headers
    response_head = response['Content-Length']
    file_size = int(response_head)
    # progress_bar = tqdm(total=file_size, unit='iB', unit_scale=True)

    supports_ranges = (
        'Accept-Ranges' in response and response['Accept-Ranges'] == 'bytes'
    )

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
                # threads_size = threading.active_count()
      
            progress_proc(results, ranges)

            downloaded_file = b''.join([r.result() for r in results])
       
        save_file(downloaded_file)


    check_file = os.path.exists(f'./files/{file_name}')
    
    if check_file:
        progres = 'downlanded'
    else:
        progres = 'not downlanded'

    status = f'url:{url}, file_amount_bytes:{file_size}, status:{progres}'

    print(status)

    with open("./url_list/url_status.txt", "a") as file:
        file.write(status + '\n')


# Проверяем наличие ссылки если ссылка есть тогда скачиваем файл

urls = open('./url_list/urls.txt', 'r').readline()
url_list = urls.split('#')
#print(url_list)
url_list.pop(-1)
for url in url_list:
    #print(url)
    file_name = (url.split('/'))[-1]
    download(url)

#file_name = (url.split('/'))[-1]
#print(url)
#download(url)
'''
url_list = open('./url_list/urls.txt', 'r').readlines()
if url_list == []:
    print('Файл пуст')
else:
    for url in url_list:
        file_name = (url.split('/'))[-1]
        
        print(url)
    # os.system(r'>./url_list/urls.txt')
'''


'''
url = input()
val = validators.url(url)

if val:
    file_name = (url.split('/'))[-1]
    download(url)
else:
    print('Ссылка не соответствует формату')
'''


#os.system(r'>./url_list/urls.txt')

'''
def progress(data):
    progres_bar = tqdm(
        as_completed(data),
        total=len(data),
        desc="Downloading",
        #file='./url_list/progress.txt',
    )
    for future in progres_bar:
        pass
'''




# print(as_completed(results))
'''
for future in as_completed(results):
    downloaded = file_size / (future.result()[1]*block)
    print(f"{downloaded}% downloaded")
'''

'''
downloaded = 0
for future in as_completed(results):
            
    downloaded += future.result()[1]
    percent = downloaded / file_size * 100

    print(f"{percent}% downloaded")
'''









'''
def download_chunk(url, start: int, end: int):
    req = urllib.request.Request(url)
    req.headers['Range'] = f'bytes={start}-{end}'
    response = urllib.request.urlopen(req)
    return response.read()


def download_file(url, start: int, end: int):
    chunk = download_chunk(url, start, end)
    with open(f'./files/{file_name}', 'wb') as file:
        # file.seek(start)
        file.write(chunk)

with open(f'./files/{file_name}', 'wb') as file:
        #file.seek(start)
        file.write(response.content)
        
'''
'''
        block_list = []
        for i in range(0, file_size, block):   
            start = i
            end = min(start+block, file_size-1)
            bloc = [start, end]
            block_list.append(bloc)


        thread = []
        for i in range(threads):
            start = i * block
            end = min(start + block - 1, file_size)
            t = threading.Thread(target=download_file, args=(url, start, end))
            t.start()
            thread.append(t)

        for t in thread:
            t.join()
'''