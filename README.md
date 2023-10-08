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

- `POST /user`
- `GET /user/:userId`
- `PUT /user/:userId`
- `PATCH /user/:userId/:status`
- `DELETE /user/:userId`
