# Generated by Django 3.2.5 on 2022-05-29 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0007_mypicture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mypicture',
            name='photo',
        ),
        migrations.RemoveField(
            model_name='mypicture',
            name='user',
        ),
        migrations.AddField(
            model_name='mypicture',
            name='headImg',
            field=models.ImageField(default='img/4.jpg', upload_to='img'),
        ),
    ]
