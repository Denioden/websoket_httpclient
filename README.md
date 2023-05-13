# HTTP CLIENT + WEBSOCKET SERVER

## Задание

    Реализовать многопоточный HTTP клиент + websocket сервер.

    1) Клиенту передается URL, каждый поток скачивает X байт параллельно другим, кол-во потоков и кол-во байт на поток ограничено сверху посредством конфига. При передаче URL клиенту, нужно проверить, поддерживаются ли ranges.

    2) websocket - сервер, отдает список URL для скачивания, и их статус (размер, потоков запущено на обработку, прогресс), если контент скачан, то ссылку на файловую систему по протоколу file:///

    Код задания предоставить в виде репозитория на github\gitlab\bitbucket
    В README.md должна содержаться инструкция по запуску

## Установка

Клонировать репозиторий и перейти в него в командной строке:

```
$ git clone git@github.com:Denioden/websoket_httpclient.git
```

Cоздать и активировать виртуальное окружение:

```
$ python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    $ source env/bin/activate
    ```

* Если у вас windows

    ```
    $ source env/scripts/activate
    ```

```
(venv) $ python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
(venv) $ pip install -r requirements.txt
```

## Настройка config.py

__THREADS_SIZE__ - Максимальное количество потоков

__BLOCK_SIZE__ - Размер диапазона скачивания для скачивания по частям

__HOST__ - Хост, по умолчанию стоит localhost

__PORT__ - Порт, по умолчанию стоит 8765


## Запуск проекта

Переходим в деректорию /websocket_httpclient/websocket_httpclient
Переходим в терменал, следующие 3 команды запускаем каждую в своем терменале.

Запускаем сервер.
```
python3 server.py
```
Запускаем клиента.
```
python3 http_client.py
```
Подключаемся к серверу, и вводим ссылку для скачивания файла.
```
python3 -m websockets ws://localhost:8765/
> https://download.samplelib.com/png/sample-hut-400x300.png
```
Если файл был скачен, тогда сервер вернёт нам ссылке на файловую систему по протоколу file:///
```
> file:////home/daniil/test-work/websoket_httpclient/websoket_httpclient/url_list/sample-hut-400x300.png
```
Если файл не был скачен, тогда вернётся статус(url, размер файла, кол-во запущенных потоков, прогресс)
```
> url:https://download.samplelib.com/png/sample-clouds2-400x300.png, file_amount_bytes:124864, threads_amount:3, progress:downlanded
```
Для остановки Клиента и Сервера нужна перейти в нужный терминал и ввести:
```
Ctr+C
```
### Файлы скачиваются в деррикотрю files.
### Текстовые файл находящиеся в папке url_list, служат для временного сохранения информации если файлы удалить возникнет ошибка.

URL для тестирвания:
https://download.samplelib.com/png/sample-clouds2-400x300.png
https://download.samplelib.com/png/sample-hut-400x300.png


