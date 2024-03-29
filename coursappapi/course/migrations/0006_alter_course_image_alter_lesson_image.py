# Generated by Django 5.0.3 on 2024-03-07 04:19

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("course", "0005_rename_tags_tag"),
    ]

    operations = [
        migrations.AlterField(
            model_name="course",
            name="image",
            field=cloudinary.models.CloudinaryField(max_length=255),
        ),
        migrations.AlterField(
            model_name="lesson",
            name="image",
            field=cloudinary.models.CloudinaryField(max_length=255),
        ),
    ]
