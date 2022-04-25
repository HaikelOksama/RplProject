# Generated by Django 3.2.7 on 2022-04-23 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0019_userprofile_fakultas'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pertanyaan',
            name='topic',
        ),
        migrations.RemoveField(
            model_name='pertanyaan',
            name='user',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='follow',
            field=models.ManyToManyField(blank=True, related_name='follow', to='base.Organisasi'),
        ),
        migrations.DeleteModel(
            name='Choice',
        ),
        migrations.DeleteModel(
            name='Pertanyaan',
        ),
    ]
