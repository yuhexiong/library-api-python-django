from django.db import models

STATUS = [
    (0, "NORMAL"),
    (1, "TEMP"),
    (2, "OTHER"),
    (9, "DELETE"),
]


class User(models.Model):  # 使用者
    id = models.AutoField(primary_key=True)  # id
    createAt = models.DateTimeField()  # 建立時間
    updateAt = models.DateTimeField()  # 更新時間
    status = models.IntegerField(choices=STATUS)  # 狀態
    name = models.CharField(max_length=10)  # 姓名

    class Meta:
        db_table = 'user'


class Author(models.Model):  # 作者
    id = models.AutoField(primary_key=True)  # id
    createAt = models.DateTimeField()  # 建立時間
    updateAt = models.DateTimeField()  # 更新時間
    status = models.IntegerField(choices=STATUS)  # 狀態
    user = models.ForeignKey(User, on_delete=models.RESTRICT)  # 使用者
    publishTimes = models.IntegerField()  # 出版次數

    class Meta:
        db_table = 'author'


class Reader(models.Model):  # 讀者
    id = models.AutoField(primary_key=True)  # id
    createAt = models.DateTimeField()  # 建立時間
    updateAt = models.DateTimeField()  # 更新時間
    status = models.IntegerField(choices=STATUS)  # 狀態
    user = models.ForeignKey(User, on_delete=models.RESTRICT)  # 使用者
    borrowTimes = models.IntegerField()  # 借書次數
    violationTimes = models.IntegerField()  # 違規次數

    class Meta:
        db_table = 'reader'


class BookType(models.Model):  # 書本類型
    id = models.AutoField(primary_key=True)  # id
    createAt = models.DateTimeField()  # 建立時間
    updateAt = models.DateTimeField()  # 更新時間
    status = models.IntegerField(choices=STATUS)  # 狀態
    name = models.CharField(max_length=10)  # 姓名

    class Meta:
        db_table = 'bookType'


class Book(models.Model):  # 書本
    id = models.AutoField(primary_key=True)  # id
    createAt = models.DateTimeField()  # 建立時間
    updateAt = models.DateTimeField()  # 更新時間
    status = models.IntegerField(choices=STATUS)  # 狀態
    name = models.CharField(max_length=10)  # 姓名
    bookType = models.ForeignKey(BookType, on_delete=models.RESTRICT)  # 書本類型
    publishAt = models.DateTimeField()  # 出版時間
    author = models.ForeignKey(Author, on_delete=models.RESTRICT)  # 作者
    location = models.CharField(max_length=10)  # 位置

    class Meta:
        db_table = 'book'


class Borrow(models.Model):  # 借書紀錄
    id = models.AutoField(primary_key=True)  # id
    createAt = models.DateTimeField()  # 建立時間
    updateAt = models.DateTimeField()  # 更新時間
    status = models.IntegerField(choices=STATUS)  # 狀態
    book = models.ForeignKey(Book, on_delete=models.RESTRICT)  # 書本
    reader = models.ForeignKey(Reader, on_delete=models.RESTRICT)  # 讀者
    borrowAt = models.DateTimeField()  # 借出時間
    returnAt = models.DateTimeField(null=True)  # 歸還時間
    times = models.IntegerField()  # 借出次數

    class Meta:
        db_table = 'borrow'


class Report(models.Model):  # 心得
    id = models.AutoField(primary_key=True)  # id
    createAt = models.DateTimeField()  # 建立時間
    updateAt = models.DateTimeField()  # 更新時間
    status = models.IntegerField(choices=STATUS)  # 狀態
    book = models.ForeignKey(Book, on_delete=models.RESTRICT)  # 書本
    reader = models.ForeignKey(Reader, on_delete=models.RESTRICT)  # 讀者
    content = models.CharField(max_length=3000)  # 內文

    class Meta:
        db_table = 'report'
