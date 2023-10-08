# Generated by Django 4.2.6 on 2023-10-08 09:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Author",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("createAt", models.DateTimeField()),
                ("updateAt", models.DateTimeField()),
                (
                    "status",
                    models.IntegerField(
                        choices=[
                            (0, "NORMAL"),
                            (1, "TEMP"),
                            (2, "OTHER"),
                            (9, "DELETE"),
                        ]
                    ),
                ),
                ("publishTimes", models.IntegerField()),
            ],
            options={
                "db_table": "author",
            },
        ),
        migrations.CreateModel(
            name="Book",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("createAt", models.DateTimeField()),
                ("updateAt", models.DateTimeField()),
                (
                    "status",
                    models.IntegerField(
                        choices=[
                            (0, "NORMAL"),
                            (1, "TEMP"),
                            (2, "OTHER"),
                            (9, "DELETE"),
                        ]
                    ),
                ),
                ("name", models.CharField(max_length=10)),
                ("publishAt", models.DateTimeField()),
                ("location", models.CharField(max_length=10)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT, to="books.author"
                    ),
                ),
            ],
            options={
                "db_table": "book",
            },
        ),
        migrations.CreateModel(
            name="BookType",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("createAt", models.DateTimeField()),
                ("updateAt", models.DateTimeField()),
                (
                    "status",
                    models.IntegerField(
                        choices=[
                            (0, "NORMAL"),
                            (1, "TEMP"),
                            (2, "OTHER"),
                            (9, "DELETE"),
                        ]
                    ),
                ),
                ("name", models.CharField(max_length=10)),
            ],
            options={
                "db_table": "bookType",
            },
        ),
        migrations.CreateModel(
            name="Reader",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("createAt", models.DateTimeField()),
                ("updateAt", models.DateTimeField()),
                (
                    "status",
                    models.IntegerField(
                        choices=[
                            (0, "NORMAL"),
                            (1, "TEMP"),
                            (2, "OTHER"),
                            (9, "DELETE"),
                        ]
                    ),
                ),
                ("borrowTimes", models.IntegerField()),
                ("violationTimes", models.IntegerField()),
            ],
            options={
                "db_table": "reader",
            },
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("createAt", models.DateTimeField()),
                ("updateAt", models.DateTimeField()),
                (
                    "status",
                    models.IntegerField(
                        choices=[
                            (0, "NORMAL"),
                            (1, "TEMP"),
                            (2, "OTHER"),
                            (9, "DELETE"),
                        ]
                    ),
                ),
                ("name", models.CharField(max_length=10)),
            ],
            options={
                "db_table": "user",
            },
        ),
        migrations.CreateModel(
            name="Report",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("createAt", models.DateTimeField()),
                ("updateAt", models.DateTimeField()),
                (
                    "status",
                    models.IntegerField(
                        choices=[
                            (0, "NORMAL"),
                            (1, "TEMP"),
                            (2, "OTHER"),
                            (9, "DELETE"),
                        ]
                    ),
                ),
                ("content", models.CharField(max_length=3000)),
                (
                    "book",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT, to="books.book"
                    ),
                ),
                (
                    "read",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT, to="books.reader"
                    ),
                ),
            ],
            options={
                "db_table": "report",
            },
        ),
        migrations.AddField(
            model_name="reader",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.RESTRICT, to="books.user"
            ),
        ),
        migrations.CreateModel(
            name="Borrow",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("createAt", models.DateTimeField()),
                ("updateAt", models.DateTimeField()),
                (
                    "status",
                    models.IntegerField(
                        choices=[
                            (0, "NORMAL"),
                            (1, "TEMP"),
                            (2, "OTHER"),
                            (9, "DELETE"),
                        ]
                    ),
                ),
                ("borrowAt", models.DateTimeField()),
                ("returnAt", models.DateTimeField()),
                ("times", models.IntegerField()),
                (
                    "book",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT, to="books.book"
                    ),
                ),
                (
                    "read",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT, to="books.reader"
                    ),
                ),
            ],
            options={
                "db_table": "borrow",
            },
        ),
        migrations.AddField(
            model_name="book",
            name="bookType",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.RESTRICT, to="books.booktype"
            ),
        ),
        migrations.AddField(
            model_name="author",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.RESTRICT, to="books.user"
            ),
        ),
    ]
