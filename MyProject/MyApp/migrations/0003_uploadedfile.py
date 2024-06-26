# Generated by Django 5.0.3 on 2024-04-02 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0002_customuser_username_alter_customuser_address_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(null=True)),
                ('title', models.CharField(max_length=255)),
                ('visibility', models.BooleanField(default=True)),
                ('description', models.CharField(max_length=500)),
                ('cost', models.IntegerField()),
                ('year_of_published', models.IntegerField()),
                ('file', models.FileField(default=None, upload_to='uploads_books/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
