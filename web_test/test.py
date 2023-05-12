import os.path
from pathlib import Path

check_file = os.path.exists('/home/daniil/test-work/websoket_httpclient/websoket_httpclient/http_client.py')

print(check_file)

if check_file:
    print("yes")
else:
    print("no")

if Path('websoket_httpclient/files/17539586d5bb4e528d94f3bc4131e6c0?s=23&d=identicon&r=PG').is_file():
    print ("File exist")
else:
    print ("File not exist")
