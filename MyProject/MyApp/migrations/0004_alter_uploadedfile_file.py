# Generated by Django 5.0.3 on 2024-04-03 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0003_uploadedfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadedfile',
            name='file',
            field=models.FileField(default=None, upload_to=''),
        ),
    ]
