# HTTP CLIENT + WEBSOCKET SERVER

## Задание

    Реализовать многопоточный HTTP клиент + websocket сервер.

    1) Клиенту передается URL, каждый поток скачивает X байт параллельно другим, кол-во потоков и кол-во байт на поток ограничено сверху посредством конфига. При передаче URL клиенту, нужно проверить, поддерживаются ли ranges.

    2) websocket - сервер, отдает список URL для скачивания, и их статус (размер, потоков запущено на обработку, прогресс), если контент скачан, то url на файловую систему по протоколу file:///

    Код задания предоставить в виде репозитория на github\gitlab\bitbucket
    В README.md должна содержаться инструкция по запуску

## Установка

Клонировать репозиторий и перейти в него в командной строке:

```
$ git clone https://github.com/Denioden/websoket_httpclient.git
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
    $ venv\Scripts\activate.bat
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

Переходим в директорию /websocket_httpclient/websocket_httpclient
Переходим в терминал, следующие 3 команды запускаем каждую в своем терминале.

Запускаем сервер.
```
python3 server.py
```
Запускаем клиента в отдельном терминале.
```
python3 http_client.py
```
Подключаемся к серверу в отдельном терминале.
```
python3 -m websockets ws://localhost:8765/
> 
```

## Взаимодействие с сервером осуществляется при помощи команд, далее приведён перечень доступных команд их описания и примеры.

- help_command - Перечень доступных команд.
- start - Начать запись url.
- end - Закончить запись url и отправить на обработку.
- queue - Показать url в ожидании.
- loading - Показать url ,по которой происходит загрузка.
- download - Показать url ,по которым загрузились файлы.

### help_command - Выведет перечень доступных команд.
......................................................................
#### Comand
    > help_command
         
#### Response
    < help_command - Перечень доступных команд.
    < start - Начать запись url.
    < end - Закончить запись url и отправить на обработку.
    < queue - Показать url в ожидании.
    < loading - Показать url ,по которой происходит загрузка.
    < download - Показать url ,по которым загрузились файлы.
......................................................................
#### Comand
    > start
    >
    > end     
#### Response
    > start
    > https://download.samplelib.com/mp4/sample-5s.mp4
    > https://download.samplelib.com/png/sample-boat-400x300.png
    > end
    < Отправка urls на обработку.

Если ни одного url добавлено не было, сервер вернёт:

    > start
    > end
    < Не добавлено ни одного url для скачивания.

Если url не соответствует формату url, сервер вернёт:

    > start
    > urlllll
    <> url не соответствует формату.

Если url не предназначена для скачивания файла, сервер вернёт:

    > start
    > https://python-scripts.com/
    < Данный url не предназначена для скачивания файла.

Если url не действительна, сервер вернёт:

    > start
    > https://download.saelib.com/mp4/sample-5s.mp4
    < url не действительна.


Если файл был скачен, тогда сервер вернёт нам сообщение и адрес на файловую систему по протоколу file:///

    > start
    > https://download.samplelib.com/png/sample-hut-400x300.png
    < Файл по данному url был скачен ранее и находится по адресу: file:////home/daniil/test-work/websoket_httpclient/websoket_httpclient/url_list/sample-hut-400x300.png

......................................................................

#### Comand
    > queue

#### Response
    < url:https://download.samplelib.com/mp4/sample-30s.mp4, status: В очереди
......................................................................

#### Comand
    > loading
         
#### Response
    < url:https://download.samplelib.com/mp4/sample-30s.mp4, file_amount_bytes:21657943, threads_size:5, status:17.0
......................................................................
#### Comand
    > download
         
#### Response
    < url:https://download.samplelib.com/mp4/sample-30s.mp4, file_amount_bytes:21657943, patch: file:////home/daniil/test-work/websoket_httpclient/websocket_httpclient/files/sample-30s.mp4
......................................................................

Для остановки Клиента и Сервера нужна перейти в нужный терминал и ввести:
```
Ctr+C
```
### Файлы скачиваются в директорию files.


## Внимание !!!!!
Добавлять новые url для скачивания можно только после загрузки отправленных ранее. 
Если попытаться добавить новые url для записи, до завершения загрузки сервер вернет:
    
    > start
    < Для добавления новых url на скачивание, дождитесь окончания загрузки отправленных ранее.
    
## Нельзя удалять папку data, и находящиеся в ней файлы. В случае удаления или изменения имени файла, программа будет работать некорректно, могут возникнуть ошибки!


URL для тестирования:
- https://download.samplelib.com/png/sample-boat-400x300.png
- https://download.samplelib.com/png/sample-hut-400x300.png
- https://download.samplelib.com/xls/sample-simple-1.xls
- https://download.samplelib.com/mp4/sample-20s.mp4
- https://download.samplelib.com/mp4/sample-30s.mp4

