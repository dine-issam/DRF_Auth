# Generated by Django 4.1.3 on 2024-02-27 17:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_uploadedfile'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UploadedFile',
        ),
        migrations.RemoveField(
            model_name='user',
            name='auth_provider',
        ),
    ]
