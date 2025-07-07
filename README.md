# Документация Orders API

## POST `/register/`

Регистрирует нового пользователя в системе.

### Параметры запроса

| Поле         | Тип     | Обязательный | Описание                   |
|--------------|---------|--------------|----------------------------|
| username     | string  | да           | Уникальное имя пользователя|
| first_name   | string  | нет          | Имя                        |
| last_name    | string  | нет          | Фамилия                    |
| email        | string  | нет          | Электронная почта          |
| password     | string  | да           | Пароль пользователя        |

### Пример возможных запросов и ответов

#### 201 Created

##### Запрос

```
POST http://localhost:8000/api/v1/register/
Content-Type: application/json

{
"username": "newuser",
"first_name": "John",
"last_name": "Doe",
"email": "john@example.com",
"password": "secret123"
}
```

##### Ответ

```
{
  "token": "fa073f4f2562c5123f4d1a83eeee509f60d62a47"
}
```

#### 400 Bad Request

##### Запрос

```
POST http://localhost:8000/api/v1/register/
Content-Type: application/json

{
"username": "newuser",
"first_name": "Johny",
"last_name": "Do",
"email": "joh@example.com",
"password": "123"
}
```

##### Ответ

```
{
  "username": [
    "A user with that username already exists."
  ]
}
```

#### 400 Bad Request

##### Запрос

```
POST http://localhost:8000/api/v1/register/
Content-Type: application/json

{
"username": "",
"first_name": "Johny",
"last_name": "Do",
"email": "joh@example.com",
"password": "123"
}
```

##### Ответ

```
{
  "username": [
    "This field may not be blank."
  ]
}
```

#### 400 Bad Request

##### Запрос

```
POST http://localhost:8000/api/v1/register/
Content-Type: application/json

{
"username": "newuser",
"first_name": "Jojo",
"last_name": "Dodo",
"email": "jk@example.com",
}
```

##### Ответ

{
  "password": [
    "This field is required."
  ]
}
