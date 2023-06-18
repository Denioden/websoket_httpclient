import requests
from concurrent.futures import ThreadPoolExecutor
import threading
import os
from config import THREADS_SIZE, BLOCK_SIZE

import validators # !!!

from clint.textui import progress




url = input()
val = validators.url(url)
file_name = (url.split('/'))[-1]
if val:
    response = requests.head(url)
    '''
    with open(f'./files/{file_name}', 'wb') as file:
        file.write(response.content)
    '''
    print(response.headers)
else:
    print('Ссылка не соответствует формату')

