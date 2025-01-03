# Generated by Django 4.2.6 on 2024-12-21 04:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('create_at', models.DateTimeField()),
                ('update_at', models.DateTimeField()),
                ('status', models.IntegerField(choices=[(0, 'NORMAL'), (1, 'TEMP'), (2, 'OTHER'), (9, 'DELETE')])),
                ('publish_times', models.IntegerField()),
            ],
            options={
                'db_table': 'author',
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('create_at', models.DateTimeField()),
                ('update_at', models.DateTimeField()),
                ('status', models.IntegerField(choices=[(0, 'NORMAL'), (1, 'TEMP'), (2, 'OTHER'), (9, 'DELETE')])),
                ('name', models.CharField(max_length=10)),
                ('publish_at', models.DateTimeField()),
                ('location', models.CharField(max_length=10)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='bookapp.author')),
            ],
            options={
                'db_table': 'book',
            },
        ),
        migrations.CreateModel(
            name='BookType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('create_at', models.DateTimeField()),
                ('update_at', models.DateTimeField()),
                ('status', models.IntegerField(choices=[(0, 'NORMAL'), (1, 'TEMP'), (2, 'OTHER'), (9, 'DELETE')])),
                ('name', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'book_type',
            },
        ),
        migrations.CreateModel(
            name='Reader',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('create_at', models.DateTimeField()),
                ('update_at', models.DateTimeField()),
                ('status', models.IntegerField(choices=[(0, 'NORMAL'), (1, 'TEMP'), (2, 'OTHER'), (9, 'DELETE')])),
                ('borrow_times', models.IntegerField()),
                ('violation_times', models.IntegerField()),
            ],
            options={
                'db_table': 'reader',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('create_at', models.DateTimeField()),
                ('update_at', models.DateTimeField()),
                ('status', models.IntegerField(choices=[(0, 'NORMAL'), (1, 'TEMP'), (2, 'OTHER'), (9, 'DELETE')])),
                ('name', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('create_at', models.DateTimeField()),
                ('update_at', models.DateTimeField()),
                ('status', models.IntegerField(choices=[(0, 'NORMAL'), (1, 'TEMP'), (2, 'OTHER'), (9, 'DELETE')])),
                ('content', models.CharField(max_length=3000)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='bookapp.book')),
                ('reader', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='bookapp.reader')),
            ],
            options={
                'db_table': 'report',
            },
        ),
        migrations.AddField(
            model_name='reader',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='bookapp.user'),
        ),
        migrations.CreateModel(
            name='Borrow',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('create_at', models.DateTimeField()),
                ('update_at', models.DateTimeField()),
                ('status', models.IntegerField(choices=[(0, 'NORMAL'), (1, 'TEMP'), (2, 'OTHER'), (9, 'DELETE')])),
                ('borrow_at', models.DateTimeField()),
                ('return_at', models.DateTimeField(null=True)),
                ('times', models.IntegerField()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='bookapp.book')),
                ('reader', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='bookapp.reader')),
            ],
            options={
                'db_table': 'borrow',
            },
        ),
        migrations.AddField(
            model_name='book',
            name='book_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='bookapp.booktype'),
        ),
        migrations.AddField(
            model_name='author',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='bookapp.user'),
        ),
    ]
