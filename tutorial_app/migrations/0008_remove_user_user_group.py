# Generated by Django 2.2.9 on 2020-02-04 10:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("tutorial_app", "0007_auto_20200203_1044"),
    ]

    operations = [
        migrations.RemoveField(model_name="user", name="user_group",),
    ]
