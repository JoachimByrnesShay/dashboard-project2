# Generated by Django 3.2.4 on 2021-06-08 08:56

import apps.accounts.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=apps.accounts.models.UserNameField(max_length=200, unique=True),
        ),
    ]
