# Generated by Django 2.0.6 on 2020-03-17 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='train',
            name='status',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
    ]
