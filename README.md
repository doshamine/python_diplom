# Orders API

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

### Примеры возможных запросов и ответов

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

```
{
  "password": [
    "This field is required."
  ]
}
```

## POST `/login/`

Позволяет пользователю войти в систему и получить токен аутентификации.

### Параметры запроса

| Поле      | Тип    | Обязательный | Описание                      |
|-----------|--------|--------------|-------------------------------|
| username  | string | да           | Имя пользователя              |
| password  | string | да           | Пароль пользователя           |

### Примеры возможных запросов и ответов

#### 201 Created

##### Запрос

```
POST http://localhost:8000/api/v1/login/
Content-Type: application/json

{
"username": "newuser",
"password": "secret123"
}
```

##### Ответ

```
{
  "token": "fa073f4f2562c5123f4d1a83eeee509f60d62a47"
}
```

#### 200 OK

##### Запрос

```
POST http://localhost:8000/api/v1/login/
Content-Type: application/json

{
"username": "newuser",
"password": "123"
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
POST http://localhost:8000/api/v1/login/
Content-Type: application/json

{
"username": "newuser",
"password": "12"
}
```

##### Ответ

```
{
  "non_field_errors": [
    "Unable to log in with provided credentials."
  ]
}
```

## GET `/products/`

Получить список продуктов с возможностью фильтрации, поиска и сортировки.

### Параметры запроса

| Параметр   | Тип    | Описание                                                                 |
|------------|--------|--------------------------------------------------------------------------|
| min_price  | float  | Минимальная цена продукта (фильтрация по цене)                           |
| max_price  | float  | Максимальная цена продукта (фильтрация по цене)                          |
| shop_id    | int    | ID магазина (фильтрация по магазину)                                     |
| search     | string | Поиск по названию продукта                                               |
| ordering   | string | Сортировка списка (например, `name` — по имени продукта)                 |

### Примеры возможных запросов и ответов

#### 200 OK

##### Запрос

```
POST http://localhost:8000/api/v1/products/?shop_id=1&max_price=1000
Content-Type: application/json
```

##### Ответ

```
[
  {
    "id": 123234575,
    "name": "TCL 6-Series 55\" 4K UHD Smart TV",
    "model": "tcl/6-series",
    "product_info": [
      {
        "shop": {
          "id": 1,
          "name": "МТС",
          "url": "https://shop.mts.ru"
        },
        "price": "700.00",
        "price_rrc": "799.00",
        "quantity": 10
      }
    ]
  },
  {
    "id": 1235434570,
    "name": "USB Flash Drive Kingston DataTraveler 32GB (red)",
    "model": "kingston/datatraveler-32gb",
    "product_info": [
      {
        "shop": {
          "id": 1,
          "name": "МТС",
          "url": "https://shop.mts.ru"
        },
        "price": "1000.00",
        "price_rrc": "1290.00",
        "quantity": 8
      }
    ]
  }
]
```

## GET `/products/{product_id}/`

Получить информацию о продукте с данным id.

### Параметры запроса

| Параметр   | Тип    | Описание                                        |
|------------|--------|-------------------------------------------------|
| product_id | int    | id продукта в базе                              |

### Примеры возможных запросов и ответов

#### 200 OK

##### Запрос

```
POST http://localhost:8000/api/v1/products/4216292
Content-Type: application/json
```

##### Ответ

```
{
  "id": 4216292,
  "name": "Смартфон Apple iPhone XS Max 512GB (золотистый)",
  "model": "apple/iphone/xs-max",
  "product_info": [
    {
      "shop": {
        "id": 1,
        "name": "МТС",
        "url": "https://shop.mts.ru"
      },
      "price": "110000.00",
      "price_rrc": "116990.00",
      "quantity": 14
    }
  ]
}
```

#### 404 Not Found

##### Запрос

```
POST http://localhost:8000/api/v1/products/421629
Content-Type: application/json
```

##### Ответ

```
{
  "detail": "No Product matches the given query."
}
```

## POST `/orders/`

Создать новый заказ.

### Параметры запроса

| Поле        | Тип      | Обязательный | Описание                                                 |
|-------------|----------|--------------|----------------------------------------------------------|
| status      | string   | да           | Статус заказа (`new`, `paid`, `shipped` или `canceled`)  |
| order_items | массив   | да           | Список позиций заказа                                    |
| order_items[].product | int | да      | ID продукта                                              |
| order_items[].shop    | int | да      | ID магазина                                              |
| order_items[].quantity| int | да      | Количество                                               |

### Примеры возможных запросов и ответов

#### 201 Created

##### Запрос

POST http://localhost:8000/api/v1/orders/
Authorization: Token <your_token>

```
{
  "order_items": [
    {
      "product": 1235464569,
      "shop": 1,
      "quantity": 2
    },
    {
      "product": 5000123,
      "shop": 2,
      "quantity": 1
    }
  ]
}
```

##### Ответ

```
{
  "id": 1,
  "user": 3,
  "dt": "2025-07-07T12:59:49.297600Z",
  "status": "new",
  "order_items": [
    {
      "id": 1,
      "product": 1235464569,
      "shop": 1,
      "quantity": 2
    },
    {
      "id": 2,
      "product": 5000123,
      "shop": 2,
      "quantity": 1
    }
  ]
}
```

#### 400 Bad Request

##### Запрос

POST http://localhost:8000/api/v1/orders/
Authorization: Token <your_token>

```
{
  "order_items": [
    {
      "shop": 1,
      "quantity": 2
    },
    {
      "product": 5000123,
      "shop": 2,
      "quantity": 1
    }
  ]
}
```

##### Ответ

```
{
  "order_items": [
    {
      "product": [
        "This field is required."
      ]
    },
    {}
  ]
}
```

#### 401 Unauthorized

##### Запрос

POST http://localhost:8000/api/v1/orders/

```
{
  "order_items": [
    {
      "product": 1235464569,
      "shop": 1,
      "quantity": 2
    },
    {
      "product": 5000123,
      "shop": 2,
      "quantity": 1
    }
  ]
}
```

##### Ответ

```
{
  "detail": "Authentication credentials were not provided."
}
```

## GET `/orders/`

Получить список заказов текущего пользователя.

### Примеры возможных запросов и ответов

#### 200 OK

##### Запрос

GET http://localhost:8000/api/v1/orders/
Authorization: Token <your_token>

##### Ответ

```
[
  {
    "id": 1,
    "user": 3,
    "dt": "2025-07-07T12:59:49.297600Z",
    "status": "paid",
    "order_items": [
      {
        "id": 1,
        "product": 1235464569,
        "shop": 1,
        "quantity": 2
      },
      {
        "id": 2,
        "product": 5000123,
        "shop": 2,
        "quantity": 1
      }
    ]
  }
]
```

#### 401 Unauthorized

##### Запрос

GET http://localhost:8000/api/v1/orders/

##### Ответ

```
{
  "detail": "Authentication credentials were not provided."
}
```

## GET `/orders/{order_id}/`

Получить заказ пользователя по его id.

### Параметры запроса

| Параметр   | Тип    | Описание                                        |
|------------|--------|-------------------------------------------------|
| order_id   | int    | id заказа в базе                                |

### Примеры возможных запросов и ответов

#### 200 OK

##### Запрос

```
GET http://localhost:8000/api/v1/orders/1
Authorization: Token <your_token>
```

##### Ответ

```
{
  "id": 1,
  "user": 3,
  "dt": "2025-07-07T12:59:49.297600Z",
  "status": "paid",
  "order_items": [
    {
      "id": 1,
      "product": 1235464569,
      "shop": 1,
      "quantity": 2
    },
    {
      "id": 2,
      "product": 5000123,
      "shop": 2,
      "quantity": 1
    }
  ]
}
```

#### 401 Unauthorized

##### Запрос

```
GET http://localhost:8000/api/v1/orders/1/
```

##### Ответ

```
{
  "detail": "Authentication credentials were not provided."
}
```

#### 404 Not Found

##### Запрос

```
GET http://localhost:8000/api/v1/orders/2/
Authorization: Token <your_token>
```

##### Ответ

```
{
  "detail": "No Order matches the given query."
}
```

## PATCH `/orders/{order_id}/`

Обновить статус заказа пользователя.

### Параметры запроса

| Поле        | Тип      | Обязательный | Описание                                                 |
|-------------|----------|--------------|----------------------------------------------------------|
| order_id    | int      | да           | id заказа в базе                                         |
| status      | string   | да           | Статус заказа (`new`, `paid`, `shipped` или `canceled`)  |
| order_items | массив   | да           | Список позиций заказа                                    |
| order_items[].product | int | да      | ID продукта                                              |
| order_items[].shop    | int | да      | ID магазина                                              |
| order_items[].quantity| int | да      | Количество                                               |

### Примеры возможных запросов и ответов

#### 200 OK

##### Запрос

```
PATCH http://localhost:8000/api/v1/orders/1/
Content-Type: application/json
Authorization: Token <your_token>

{
  "status": "canceled"
}
```

##### Ответ

```
{
  "id": 1,
  "user": 3,
  "dt": "2025-07-07T12:59:49.297600Z",
  "status": "canceled",
  "order_items": [
    {
      "id": 1,
      "product": 1235464569,
      "shop": 1,
      "quantity": 2
    },
    {
      "id": 2,
      "product": 5000123,
      "shop": 2,
      "quantity": 1
    }
  ]
}
```

#### 400 Bad Request

##### Запрос

```
PATCH http://localhost:8000/api/v1/orders/1/
Content-Type: application/json

{
  "status": "cancelled"
}
```

##### Ответ

```
{
  "status": [
    "\"cancelled\" is not a valid choice."
  ]
}
```

#### 401 Unauthorized

##### Запрос

```
PATCH http://localhost:8000/api/v1/orders/1/
Content-Type: application/json

{
  "status": "canceled"
}
```

##### Ответ

```
{
  "detail": "Authentication credentials were not provided."
}
```

#### 404 Not Found

##### Запрос

```
PATCH http://localhost:8000/api/v1/orders/3/
Content-Type: application/json
Authorization: Token {{TOKEN}}

{
  "status": "canceled"
}
```

##### Ответ

```
{
  "detail": "No Order matches the given query."
}
```

## DELETE `/orders/{order_id}/`

Удалить заказ пользователя по его id.

### Параметры запроса

| Параметр   | Тип    | Описание                                        |
|------------|--------|-------------------------------------------------|
| order_id   | int    | id заказа в базе                                |

### Примеры возможных запросов и ответов

#### 204 No Content

##### Запрос

```
DELETE http://localhost:8000/api/v1/orders/1/
Authorization: Token <your_token>
```

##### Ответ

```
{}
```

#### 401 Unauthorized

##### Запрос

```
DELETE http://localhost:8000/api/v1/orders/1/
Authorization: Token <your_token>
```

##### Ответ

```
{
  "detail": "Authentication credentials were not provided."
}
```

#### 404 Not Found

##### Запрос

```
DELETE http://localhost:8000/api/v1/orders/1/
Authorization: Token <your_token>
```

##### Ответ

```
{
  "detail": "No Order matches the given query."
}
```

