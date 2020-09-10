# Generated by Django 3.0.8 on 2020-08-18 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapi', '0020_auto_20200817_2052'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='maker_name',
            field=models.CharField(default='moroccan', max_length=50),
        ),
        migrations.AddField(
            model_name='token',
            name='expired',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='maker_id',
            field=models.IntegerField(default=-1),
        ),
    ]