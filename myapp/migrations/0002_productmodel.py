# Generated by Django 4.1.5 on 2023-02-01 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='productmodel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productname', models.CharField(max_length=30)),
                ('price', models.IntegerField()),
                ('discription', models.CharField(max_length=100)),
                ('image', models.FileField(upload_to='myapp/static')),
            ],
        ),
    ]