# Generated by Django 3.2 on 2022-10-25 09:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name': 'Profile-用户简介', 'verbose_name_plural': 'Profile-用户简介'},
        ),
    ]
