# Generated by Django 3.1 on 2020-08-19 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0018_auto_20200816_1630'),
    ]

    operations = [
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('base', models.CharField(max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='View',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('view_name', models.CharField(max_length=128)),
                ('phone_type', models.CharField(choices=[('a', 'A'), ('b', 'B'), ('c', 'C')], max_length=1)),
            ],
        ),
        migrations.AlterField(
            model_name='phone',
            name='type',
            field=models.CharField(choices=[('a', 'A'), ('b', 'B'), ('c', 'C')], default='p', max_length=1, verbose_name='Type'),
        ),
    ]
