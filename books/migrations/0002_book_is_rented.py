# Generated by Django 2.0.3 on 2018-03-16 00:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='is_rented',
            field=models.BooleanField(default=False),
        ),
    ]