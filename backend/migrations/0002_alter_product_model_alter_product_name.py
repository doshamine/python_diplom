# Generated by Django 5.2.3 on 2025-06-15 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='model',
            field=models.CharField(max_length=50, verbose_name='model'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=50, verbose_name='name'),
        ),
    ]
