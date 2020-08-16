# Generated by Django 3.0.7 on 2020-08-16 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_sitefield'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitefield',
            name='visible_status',
            field=models.CharField(choices=[('v', 'Visible'), ('i', 'Invisible')], default='v', max_length=1, verbose_name='Visible status'),
        ),
    ]
