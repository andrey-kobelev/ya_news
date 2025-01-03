# YaNews

> **YaNews** - новостной сайт, где пользователи могут оставлять комментарии к новостям.

Добро пожаловать в проект! Знакомьтесь:

- На главной странице проекта отображаются 10 последних новостей. Главная страница доступна любому пользователю. Новости отображаются в сокращённом виде (видно только первые 15 слов).
- У каждой новости есть своя страница, с полным текстом новости; там же отображаются и комментарии пользователей.
- Любой пользователь может самостоятельно зарегистрироваться на сайте.
- Залогиненный (авторизованный) пользователь может оставлять комментарии, редактировать и удалять свои комментарии.
- Если к новости есть комментарии — их количество отображается на главной странице под новостью.
- В коде проекта есть список запрещённых слов, которые нельзя использовать в комментариях, например, «редиска» и «негодяй».


## Как развернуть проект локально

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/andrey-kobelev/ya_news.git
```

```
cd ya_news
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env  
```

```
source env/bin/activate  
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip  
```

```
pip install -r requirements.txt  
```

Выполнить миграции:

```
python3 manage.py migrate  
```

Для загрузки заготовленных новостей после применения миграций выполните команду: 

```bash  
python manage.py loaddata news.json
```

Запустить проект:

```
python3 manage.py runserver  
```


## Запуск тестов: pytest

```
pytest
```

## Автор тестов

[Kobelev Andrey](https://github.com/andrey-kobelev)

### Стек

- [Python 3.9](https://www.python.org/downloads/release/python-390/)
- [Django3.2](https://docs.djangoproject.com/en/5.1/releases/3.2/)