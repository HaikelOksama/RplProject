# Generated by Django 3.2.7 on 2022-04-08 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_event_lokasi'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='jadwal',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]