# Generated by Django 4.1.3 on 2022-11-27 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='base/static/images/avatar.svg', null=True, upload_to=''),
        ),
    ]