# Generated by Django 4.0 on 2022-02-14 01:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0004_login_table_user_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_table',
            name='user_pow',
        ),
    ]
