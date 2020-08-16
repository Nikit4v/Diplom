# Generated by Django 3.0.7 on 2020-08-16 11:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_auto_20200816_1400'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='ratio',
            field=models.CharField(choices=[('a', '★★★★★'), ('b', '★★★★'), ('c', '★★★'), ('d', '★★'), ('e', '★')], default='c', max_length=1, verbose_name='Ratio'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='phone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='shop.Phone'),
        ),
        migrations.AlterField(
            model_name='sitefield',
            name='dropdown_fields',
            field=models.ManyToManyField(blank=True, to='shop.SiteField'),
        ),
    ]