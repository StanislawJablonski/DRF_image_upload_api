# Generated by Django 4.2.5 on 2023-09-22 10:55

from django.db import migrations, models
import images.models
import images.validators


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0002_rename_created_date_image_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(max_length=255, upload_to=images.models.image_upload_path, validators=[images.validators.validate_expiring_time]),
        ),
    ]
