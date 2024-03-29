# Generated by Django 3.1.1 on 2020-10-07 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapi', '0027_auto_20200928_2115'),
    ]

    operations = [
        migrations.CreateModel(
            name='message',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('email', models.EmailField(max_length=254)),
                ('text', models.CharField(default='', max_length=1000)),
                ('date', models.DateField(null=True)),
                ('time', models.DateTimeField(null=True)),
            ],
        ),
    ]
