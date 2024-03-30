### 如何使用？

```
py -3 -m venv .venv
```

```
.venv\Scripts\activate
```

```
pip install -r requirements.txt 
```

```
flask db migrate -m "Initial migration." 
```

```
flask db upgrade
```

```
flask run
```

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
    {
      "msg": "Unauthorized"
    }
    ```
  - **错误示例**

    ```
    {
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

- **基础URL**: `/api/tasks`
- **认证**: 所有请求都需要JWT认证。在请求头中添加`Authorization: Bearer <your_token>`。

#### 创建任务 (POST)

- **路径**: `/api/tasks`
- **方法**: POST
- **描述**: 创建一个新任务。
- **权限**: 需JWT认证。
- **请求体**:

```
{
  "name": "Sample Task",
  "task_type": "repeat",
  "execute_type": "immediate",
  "schedule": "daily",
  "start_time": "2024-01-01T08:00:00Z",
  "day_of_week": "1"
}
```

- **成功响应** (200): 返回创建的任务详情。
- **失败响应** (400): 请求数据不合法，返回错误信息。

#### 编辑任务 (PUT)

- **路径**: `/api/tasks/<task_id>`

- **方法**: PUT

- **描述**: 编辑指定ID的任务。

- **权限**: 需JWT认证。

- URL参数

  :

  - `task_id`: 任务ID。

- **请求体**:

```
jsonCopy code{
  "name": "Updated Task Name",
  "task_type": "single",
  "execute_type": "scheduled",
  "schedule": "weekly",
  "start_time": "2024-02-01T09:00:00Z",
  "day_of_week": "3"
}
```

- **成功响应** (200): 任务编辑成功，返回编辑后的任务详情。
- **失败响应** (400): 请求数据不合法或任务未找到，返回错误信息。

#### 删除任务 (DELETE)

- **路径**: `/api/tasks/<task_id>`

- **方法**: DELETE

- **描述**: 删除指定ID的任务。

- **权限**: 需JWT认证。

- URL参数

  :

  - `task_id`: 任务ID。

- **成功响应** (200): 任务删除成功，返回成功消息。

- **失败响应** (404): 任务未找到，返回错误信息。

#### 列出所有任务 (GET)

- **路径**: `/api/tasks/tasks_list`
- **方法**: GET
- **描述**: 获取所有任务的列表。
- **权限**: 需JWT认证。
- **成功响应** (200): 返回任务列表。

#### 获取任务详情 (GET)

- **路径**: `/api/tasks/<task_id>`

- **方法**: GET

- **描述**: 获取指定ID的任务详情。

- **权限**: 需JWT认证。

- URL参数

  :

  - `task_id`: 任务ID。

- **成功响应** (200): 返回任务详情。

- **失败响应** (404): 任务未找到，返回错误信息。

### 注意事项

- 所有的时间和日期应使用ISO 8601格式，如`2024-01-01T08:00:00Z`。
- `task_type`可为`single`（单次任务）或`repeat`（重复任务）。
- `execute_type`可为`immediate`（立即执行）或`scheduled`（计划执行）。
- `schedule`在`task_type`为`repeat`时需指定，可选值有`daily`（每天），`hourly`（每小时），`minutely`（每分钟），`monthly`（每月），`weekly`（每周）。
- `day_of_week`用于`weekly`调度，指定星期几执行，值为0到6（0表示周日，6表示周六）。仅当`schedule`为`weekly`时需要此字段。
