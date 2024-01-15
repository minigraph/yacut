# YaCut

# Flask проект коротких ссылок
### Описание
Перед Вами проект сервиса коротких ссылок, реализованный на микрофреймворке Flask. Учебный проект Яндекс.Практикум.
Проект ставит перед собой цели создания и хранения специальных коротких ссылок на разные ресурсы.
Использовано:
* Python v.3.7.5 (https://docs.python.org/3.7/)
* Flask v2.0.2 (https://flask.palletsprojects.com/en/2.0.x/)
* SQL Alchemy v1.4.29 (https://docs.sqlalchemy.org/en/14/)
* Flake 8 v.5.0.4 (https://buildmedia.readthedocs.org/media/pdf/flake8/stable/flake8.pdf)

### Шаблон заполнения .env:
Путь к файлу: 
```
~/.env
```

Ниже представлены примеры заполнения:
* Имя/путь пакета
* Режим запускуа
* Путь к БД
* Секретный ключ для Flask
```
FLASK_APP=yacut
FLASK_ENV=development
DATABASE_URI=sqlite:///db.sqlite3
SECRET_KEY=YOUR_SECRET_KEY
```

### Установка:
Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/minigraph/yacut.git
```

```
cd yacut
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

### Документация. Примеры запросов:
##### Получение данных оригинальной ссылки по короткому идентификатору
```
GET http://localhost/api/id/{short_id}/
```
Ответы:
```
Status code: 200
```
```json
{
  "url": "string",
}
```
```
Status code: 404
```
```json
{
  "message": "string",
}
```

##### Запрос на создание новой короткой ссылки 
```
GET http://localhost/api/id/
```
Данные:
```json
{
  "url": "string",
  "custom_id": "string"
}
```
Ответы:
```
Status code: 201
```
```json
{
  "url": "string",
  "short_link": "string"
}
```
```
Status code: 400
```
```json
{
  "message": "string",
}
```

### Автор:
* Михаил Никитин
* * tlg: @minigraf 
* * e-mail: minigraph@yandex.ru;
