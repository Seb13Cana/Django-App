# Generated by Django 4.2.1 on 2023-06-01 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='pub_update',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
