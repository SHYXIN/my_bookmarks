# Generated by Django 3.2 on 2022-10-31 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0003_alter_image_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='total_like',
            field=models.PositiveIntegerField(db_index=True, default=0, verbose_name='赞总数'),
        ),
    ]
