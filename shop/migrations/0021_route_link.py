# Generated by Django 3.1 on 2020-08-19 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0020_auto_20200819_1421'),
    ]

    operations = [
        migrations.AddField(
            model_name='route',
            name='link',
            field=models.CharField(default='-', max_length=128),
            preserve_default=False,
        ),
    ]