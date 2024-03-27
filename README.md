
### 1. 用户认证

#### 登录

* **URL** : `/api/auth/login`
* **方法** : `POST`
* **请求体** :

```json
{
  "username": "string",
  "password": "string"
}
```


* **响应** :

```json
{
  "token": "string"
}

```


### 2. 日志管理

#### 获取日志列表

* **URL** : `/api/logs`
* **方法** : `GET`
* **查询参数** :
* `date`: `string` (可选，格式为 `YYYY-MM-DD`)
* `ip`: `string` (可选)
* `path`: `string` (可选)
* `http_code`: `int` (可选)
* **响应** :

  ```json
  [
    {
      "id": "int",
      "date": "string",
      "ip": "string",
      "path": "string",
      "http_code": "int",
      "is_invalid": "boolean"
    },
    ...
  ]

  ```
