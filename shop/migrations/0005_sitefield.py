# Generated by Django 3.0.7 on 2020-08-16 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20200816_1259'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Field name')),
                ('is_dropdown', models.BooleanField()),
                ('handler', models.CharField(max_length=128)),
                ('dropdown_fields', models.ManyToManyField(to='shop.SiteField')),
            ],
        ),
    ]
