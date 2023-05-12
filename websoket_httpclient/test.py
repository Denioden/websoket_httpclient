import asyncio
import websockets
import time
import os
import pathlib
from pathlib import Path

url = 'https://dwweb.ru/__a-data/__all_for_scripts/__rar/pro_dw_koments_1_3.rar'
    
file_name = (url.split('/'))[-1]
    
check_file = os.path.exists(f'./files/{file_name}')
    
path_file = (f'file:///{pathlib.Path.cwd()}/url_list/{file_name}')

print(path_file)