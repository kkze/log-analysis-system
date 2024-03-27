
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

#### 获取日志详情

- **URL**: `/api/logs/<id>`

- **方法**: `GET`

- 响应

  :

  ```json
  jsonCopy code{
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
  jsonCopy code[
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
  jsonCopy code{
    "name": "string",
    "schedule": "string" // Cron 表达式或其他定时格式
  }
  ```

- 响应

  :

  ```json
  jsonCopy code{
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
  jsonCopy code{
    "name": "string",
    "schedule": "string"
  }
  ```

- 响应

  :

  ```json
  jsonCopy code{
    "message": "Task updated successfully."
  }
  ```

#### 删除任务

- **URL**: `/api/tasks/<id>`

- **方法**: `DELETE`

- 响应

  :

  ```json
  jsonCopy code{
    "message": "Task deleted successfully."
  }
  ```

#### 启动/停止任务

- **URL**: `/api/tasks/<id>/<action>` // `action` 可以是 `start` 或 `stop`

- **方法**: `POST`

- 响应

  :

  ```json
  jsonCopy code{
    "message": "Task <action> successfully." // <action> 将被替换为 "started" 或 "stopped"
  }
  ```
