# Generated by Django 4.0.6 on 2022-07-24 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_photo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follower',
            fields=[
                ('id_follower', models.AutoField(primary_key=True, serialize=False)),
                ('id_user', models.IntegerField()),
                ('id_user_follower', models.IntegerField()),
            ],
            options={
                'db_table': 'follower',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id_likes', models.AutoField(primary_key=True, serialize=False)),
                ('id_user', models.IntegerField()),
                ('id_photo', models.IntegerField()),
                ('id_user_like', models.IntegerField()),
                ('status', models.IntegerField()),
            ],
            options={
                'db_table': 'likes',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id_messages', models.AutoField(primary_key=True, serialize=False)),
                ('id_user_receiver', models.CharField(max_length=45)),
                ('id_user_sender', models.CharField(max_length=45)),
                ('text', models.CharField(max_length=45)),
                ('status', models.CharField(max_length=45)),
                ('date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'messages',
                'managed': False,
            },
        ),
    ]
