# Generated by Django 3.0.7 on 2020-08-16 09:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='phone',
            name='type',
            field=models.CharField(choices=[('p', 'Phone'), ('o', 'Other')], default='p', max_length=1, verbose_name='Type'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=128, verbose_name='Author')),
                ('content', models.TextField()),
                ('visible_status', models.CharField(choices=[('v', 'Visible'), ('i', 'Invisible')], default='v', max_length=1, verbose_name='Visible status')),
                ('phone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Phone')),
            ],
        ),
    ]
