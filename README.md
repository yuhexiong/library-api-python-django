# Library API

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

### 執行程式

```
python library/manage.py runserver
```

## API

- POST /user : 新增使用者
- GET /user : 取得所有生效的使用者
- DELETE /user/{userId} : 停用使用者

- POST /author : 新增作者，不帶使用者 id 時則一併新增使用者
- GET /author : 取得所有生效的作者
- DELETE /author/{authorId} : 停用作者

- POST /reader : 新增讀者，不帶使用者 id 時則一併新增使用者
- GET /reader : 取得所有生效的讀者
- DELETE /reader/{readerId} : 停用讀者

## Reference

[Lemon-412: Library-System](https://github.com/Lemon-412/Library-System)
[JarvisLu1029: 實作一套個人書籍管理系統的後端 API](https://github.com/JarvisLu1029/ntnu_job)
