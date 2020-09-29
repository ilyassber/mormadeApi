# Generated by Django 3.1.1 on 2020-09-24 10:10

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapi', '0025_auto_20200913_1658'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='url',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='images',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.JSONField(), blank=True, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='tag',
            name='images',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.JSONField(), blank=True, null=True, size=None),
        ),
    ]