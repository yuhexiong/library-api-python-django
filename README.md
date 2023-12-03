# Library API

## Overview

- Language: Python v3.9.15
- Web FrameWork: Django v4.2.6

### ENV

set database parameter in library/library/setting

```
'HOST':
'PORT':
'USER':
'PASSWORD':
'NAME':
```

### run migration

```
python library/manage.py migrate
```

### run

```
python library/manage.py runserver
```

## ER Diagram
![image](https://github.com/yuhexiong/library-api-python-django/blob/main/library/image/library_schema.png)

## API

### user

- POST /user : 新增使用者
- GET /user : 取得所有生效的使用者
- DELETE /user/{userId} : 停用使用者

### author

- POST /author : 新增作者，不帶使用者 id 時則一併新增使用者
- GET /author : 取得所有生效的作者
- DELETE /author/{authorId} : 停用作者

### reader

- POST /reader : 新增讀者，不帶使用者 id 時則一併新增使用者
- GET /reader : 取得所有生效的讀者
- DELETE /reader/{readerId} : 停用讀者

### bookType

- POST /bookType : 新增書本類型
- GET /bookType : 取得所有生效的書本類型
- DELETE /bookType/{bookTypeId} : 停用書本類型

### book

- POST /book : 新增書本
- GET /book : 取得所有生效的書本
- DELETE /book/{bookId} : 停用書本

### borrow, renew, return

- POST /borrow/{bookId}/{readerId} : 借書, 書本的狀態改為停用, 一次借書30天
- POST /renew/{bookId}/{readerId} : 續借, 最多續借2次
- POST /return/{bookId}/{readerId} : 還書, 超時會被記錄違規次數

### report

- POST /report : 新增心得
- GET /report : 取得所有生效的心得
- PATCH /report : 更新心得內文
- DELETE /report/{reportId} : 停用心得

### rank

- POST /rank/borrowTimes : 取得讀者借書次數排名
- POST /rank/violationTimes : 取得讀者違規次數排名
- POST /rank/publishTimes : 取得作者出版次數排名

## Custom Error Code

In library/books/view

```
SUCCESSFUL = 0
INVALID_API = 117
INVALID_PARAMETER = 118
INSUFFICIENT_PARAMETER = 119
OVER_BORROW_TIMES_LIMIT = 120
```
