# Generated by Django 3.1 on 2020-08-24 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0027_sitefield_exclude'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitefield',
            name='view',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
