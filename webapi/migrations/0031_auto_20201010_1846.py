# Generated by Django 3.1.1 on 2020-10-10 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapi', '0030_article_trending'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='link',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='tag',
            name='type',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
