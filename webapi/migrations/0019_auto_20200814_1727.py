# Generated by Django 3.0.8 on 2020-08-14 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapi', '0018_image_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='path',
            field=models.CharField(max_length=256, null=True),
        ),
    ]
