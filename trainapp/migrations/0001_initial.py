# Generated by Django 2.0.6 on 2020-03-17 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Train',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('gender', models.BooleanField()),
                ('phone', models.CharField(max_length=13)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('addr', models.CharField(max_length=30)),
                ('head', models.FileField(upload_to='heads')),
            ],
            options={
                'db_table': 'train',
            },
        ),
    ]
