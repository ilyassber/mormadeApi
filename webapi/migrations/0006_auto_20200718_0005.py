# Generated by Django 3.0.7 on 2020-07-17 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapi', '0005_auto_20200717_1828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(max_length=254),
        ),
    ]
