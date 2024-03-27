### 1. 用户认证

#### 注册

- ##### URL

```
/api/auth/register
```

- ##### 方法

```
POST
```

1. ##### 请求体

- **username** (string): 用户名，必须唯一。
- **password** (string): 用户的密码。

##### 请求体示例

```
{
  "username": "newuser",
  "password": "password123"
}
```

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



#### 登出

- **URL**：`/api/auth/logout`

- **方法**：`GET`

- **鉴权**：是（需要JWT）

- **URL参数**：无

- **请求体**：无

- ##### **成功响应**：

- **代码**：200 OK

- 内容示例：

  ```json
  {
    "msg": "Successfully logged out"
  }
  ```



### 2. 日志管理

* ### 获取日志文件列表

  获取日志文件列表，支持根据日期、IP、路径和HTTP状态码筛选。
  
  - **URL**
  
    `/api/logs`
  
  - **方法**
  
    `GET`
  
  - **请求头**
  
    无
  
  - **URL参数**
  
    | 参数      | 类型   | 描述                       | 是否必需 |
    | --------- | ------ | -------------------------- | -------- |
    | date      | string | 日志日期，格式为YYYY-MM-DD | 否       |
    | ip        | string | IP地址                     | 否       |
    | path      | string | 请求路径                   | 否       |
    | http_code | int    | HTTP状态码                 | 否       |
  
  - **请求示例**
  
    ```
    GET /api/logs?date=2023-03-27&ip=192.168.1.1&http_code=200
    ```
  
  - **响应**
  
    200 OK`：成功获取日志文件列表
  
    ```
    jsonCopy code[
      {
        "id": 1,
        "date": "2023-03-27",
        "ip": "192.168.1.1",
        "path": "/api/example",
        "http_code": 200,
        "is_invalid": false
      },
      {
        "id": 2,
        "date": "2023-03-27",
        "ip": "192.168.1.2",
        "path": "/api/test",
        "http_code": 404,
        "is_invalid": true
      }
    ]
    ```
  
  - **错误响应**
  
    `401 Unauthorized`：未经身份验证的访问
  
    ```
    e{
      "msg": "Unauthorized"
    }
    ```
  
  - **错误示例**
  
    ```
    e{
      "error": "Invalid date format"
    }
    ```

- **URL**: `/api/logs/<id>`

- **方法**: `GET`

- 响应

  :

  ```json
  {
    "id": "int",
    "date": "string",
    "ip": "string",
    "path": "string",
    "http_code": "int",
    "is_invalid": "boolean"
  }
  ```

### 3. 任务管理

#### 获取任务列表

- **URL**: `/api/tasks`

- **方法**: `GET`

- 响应

  :

  ```json
  [
    {
      "id": "int",
      "name": "string",
      "status": "string", // "running", "stopped"
      "creation_date": "string",
      "last_run": "string" // "YYYY-MM-DD HH:MM:SS"
    },
    ...
  ]
  ```

#### 新增任务

- **URL**: `/api/tasks`

- **方法**: `POST`

- 请求体

  :

  ```json
  {
    "name": "string",
    "schedule": "string" // Cron 表达式或其他定时格式
  }
  ```

- 响应

  :

  ```json
  {
    "id": "int",
    "message": "Task created successfully."
  }
  ```

#### 编辑任务

- **URL**: `/api/tasks/<id>`

- **方法**: `PUT`

- 请求体

  :

  ```json
  {
    "name": "string",
    "schedule": "string"
  }
  ```

- 响应

  :

  ```json
  {
    "message": "Task updated successfully."
  }
  ```

#### 删除任务

- **URL**: `/api/tasks/<id>`

- **方法**: `DELETE`

- 响应

  :

  ```json
  {
    "message": "Task deleted successfully."
  }
  ```

#### 启动/停止任务

- **URL**: `/api/tasks/<id>/<action>` // `action` 可以是 `start` 或 `stop`

- **方法**: `POST`

- 响应

  :

  ```json
  {
    "message": "Task <action> successfully." // <action> 将被替换为 "started" 或 "stopped"
  }
  ```
