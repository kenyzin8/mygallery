# Generated by Django 5.0.1 on 2024-01-29 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_alter_imageview_ip_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='public/videos/'),
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='public/images/'),
        ),
    ]
