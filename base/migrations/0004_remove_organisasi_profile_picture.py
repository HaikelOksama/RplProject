# Generated by Django 3.2.7 on 2022-04-07 17:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_organisasi_profile_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organisasi',
            name='profile_picture',
        ),
    ]
