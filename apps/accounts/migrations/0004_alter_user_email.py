# Generated by Django 3.2.4 on 2021-06-08 09:49

import apps.accounts.models
import django.core.validators
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=apps.accounts.models.UserEmailField(max_length=254, unique=True, validators=[django.core.validators.EmailValidator]),
        ),
    ]
