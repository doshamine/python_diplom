# Orders API

## POST `/register/`

Регистрирует нового пользователя в системе. При успешной регистрации на электронную почту пользователя отправляется письмо с подтверждением.

### Параметры запроса

| Поле         | Тип     | Обязательный | Описание                   |
|--------------|---------|--------------|----------------------------|
| username     | string  | да           | Уникальное имя пользователя|
| first_name   | string  | нет          | Имя                        |
| last_name    | string  | нет          | Фамилия                    |
| email        | string  | да           | Электронная почта          |
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

Обновить заказ пользователя.

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

## POST `/cart/`

Добавить товары в корзину. Обработка запросов аналогична POST `/orders/`. Все заказы в корзине имеют статус "new".

## GET `/cart/`

Получить список заказов в корзине текущего пользователя. Обработка запросов аналогична GET `/orders/`. Все заказы в корзине имеют статус "new".

## GET `/cart/{order_id}/`

Получить заказ из корзины пользователя по его id. Обработка запросов аналогична GET `/orders/{order_id}/`. Все заказы в корзине имеют статус "new".

## PATCH `/cart/{order_id}/`

Обновить заказ в корзине пользователя. Обработка запросов аналогична PATCH `/orders/{order_id}/`. Все заказы в корзине имеют статус "new".

## DELETE `/cart/{order_id}/`

Удалить заказ из корзины пользователя по его id. Обработка запросов аналогична DELETE `/cart/{order_id}/`. Все заказы в корзине имеют статус "new".

## POST `/contacts/`

Добавить контакт пользователя. При добавлении адреса доставки на электронную почту пользователя отправляется письмо с подтверждением.

### Параметры запроса

| Поле        | Тип      | Обязательный | Описание                                                   |
|-------------|----------|--------------|------------------------------------------------------------|
| type        | string   | да           | Тип контакта (`address`, `email`, `phone` или `telegram`)  |
| value       | string   | да           | Контакт пользователя                                       |

### Примеры возможных запросов и ответов

#### 201 Created

##### Запрос

POST http://localhost:8000/api/v1/contacts/
Authorization: Token <your_token>

```
{
  "type": "telegram",
  "value": "doshamine"
}
```

##### Ответ

```
{
  "id": 1,
  "type": "telegram",
  "value": "doshamine"
}
```

#### 400 Bad Request

##### Запрос

POST http://localhost:8000/api/v1/contacts/
Authorization: Token <your_token>

```
{
  "type": "vk",
  "value": "doshamine"
}
```

##### Ответ

```
{
  "type": [
    "\"vk\" is not a valid choice."
  ]
}
```

#### 401 Unauthorized

##### Запрос

POST http://localhost:8000/api/v1/contacts/

```
{
  "type": "telegram",
  "value": "doshamine"
}
```

##### Ответ

```
{
  "detail": "Authentication credentials were not provided."
}
```

## GET `/contacts/`

Получить список контактов пользователя.

### Примеры возможных запросов и ответов

#### 200 OK

##### Запрос

GET http://localhost:8000/api/v1/contacts/
Authorization: Token <your_token>

##### Ответ

```
[
  {
    "id": 2,
    "type": "phone",
    "value": "777"
  },
  {
    "id": 1,
    "type": "telegram",
    "value": "doshamine"
  }
]
```

#### 401 Unauthorized

##### Запрос

GET http://localhost:8000/api/v1/contacts/

##### Ответ

```
{
  "detail": "Authentication credentials were not provided."
}
```

## GET `/contacts/{contact_id}/`

Получить заказ из корзины пользователя по его id.

### Параметры запроса

| Параметр   | Тип    | Описание                                        |
|------------|--------|-------------------------------------------------|
| contact_id | int    | id контакта в базе                              |

### Примеры возможных запросов и ответов

#### 200 OK

##### Запрос

```
GET http://localhost:8000/api/v1/contacts/1
Authorization: Token <your_token>
```

##### Ответ

```
{
  "id": 1,
  "type": "telegram",
  "value": "doshamine"
}
```

#### 401 Unauthorized

##### Запрос

```
GET http://localhost:8000/api/v1/contacts/1
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
GET http://localhost:8000/api/v1/contacts/3
Authorization: Token <your_token>
```

##### Ответ

```
{
  "detail": "No Order matches the given query."
}
```

## PATCH `/contacts/{contact_id}/`

Обновить контакт пользователя.

### Параметры запроса

| Поле        | Тип      | Обязательный | Описание                                                   |
|-------------|----------|--------------|------------------------------------------------------------|
| contact_id  | int      | да           | id контакта в базе                                         |
| type        | string   | да           | Тип контакта (`address`, `email`, `phone` или `telegram`)  |
| value       | string   | да           | Контакт пользователя                                       |

### Примеры возможных запросов и ответов

#### 200 OK

##### Запрос

```
PATCH http://localhost:8000/api/v1/contacts/2/
Content-Type: application/json
Authorization: Token <your_token>

{
  "type": "phone",
  "value": "666"
}
```

##### Ответ

```
{
  "id": 2,
  "type": "phone",
  "value": "666"
}
```

#### 400 Bad Request

##### Запрос

PATCH http://localhost:8000/api/v1/contacts/2/
Content-Type: application/json

```
{
  "type": "phon",
  "value": "666"
}
```

##### Ответ

```
{
  "type": [
    "\"phon\" is not a valid choice."
  ]
}
```

#### 401 Unauthorized

##### Запрос

PATCH http://localhost:8000/api/v1/contacts/2/
Content-Type: application/json

```
{
  "type": "phone",
  "value": "666"
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

PATCH http://localhost:8000/api/v1/orders/3/
Content-Type: application/json
Authorization: Token {{TOKEN}}

```
{
  "type": "phone",
  "value": "666"
}
```

##### Ответ

```
{
  "detail": "No Contact matches the given query."
}
```

## DELETE `/contacts/{contact_id}/`

Удалить контакт пользователя.

### Параметры запроса

| Параметр   | Тип    | Описание                                        |
|------------|--------|-------------------------------------------------|
| contact_id | int    | id контакта в базе                              |

### Примеры возможных запросов и ответов

#### 204 No Content

##### Запрос

DELETE http://localhost:8000/api/v1/contacts/1/
Authorization: Token <your_token>

##### Ответ

```
{}
```

#### 401 Unauthorized

##### Запрос

DELETE http://localhost:8000/api/v1/contacts/1/
Authorization: Token <your_token>

##### Ответ

```
{
  "detail": "Authentication credentials were not provided."
}
```

#### 404 Not Found

##### Запрос

DELETE http://localhost:8000/api/v1/contacts/1/
Authorization: Token <your_token>

##### Ответ

```
{
  "detail": "No Contact matches the given query."
}
```

## POST `/confirm/`

Подтвердить заказ пользователя.

### Параметры запроса

| Поле        | Тип      | Обязательный | Описание                                                   |
|-------------|----------|--------------|------------------------------------------------------------|
| order_id    | int      | да           | id заказа                                                  |
| contact_id  | int      | да           | id контакта пользователя                                   |

### Примеры возможных запросов и ответов

#### 200 OK

##### Запрос

POST http://localhost:8000/api/v1/confirm/
Content-Type: application/json
Authorization: Token {{TOKEN}}

```
{
  "order_id": 1,
  "contact_id": 1
}
```

##### Ответ

```
{
  "message": "Order confirmed successfully."
}
```

#### 400 Bad Request

##### Запрос

POST http://localhost:8000/api/v1/confirm/
Content-Type: application/json
Authorization: Token {{TOKEN}}

```
{
  "order_id": 1,
  "contact_id": 1
}
```

##### Ответ

```
{
  "error": "Only new orders can be confirmed."
}
```


#### 401 Unauthorized

##### Запрос

POST http://localhost:8000/api/v1/confirm/
Content-Type: application/json

```
{
  "order_id": 1,
  "contact_id": 1
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

POST http://localhost:8000/api/v1/confirm/
Content-Type: application/json

```
{
  "order_id": 3,
  "contact_id": 1
}
```

##### Ответ

```
{
  "error": "Order not found."
}
```
