# Generated by Django 5.0.3 on 2024-03-07 03:17

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("course", "0002_course"),
    ]

    operations = [
        migrations.AlterField(
            model_name="course",
            name="description",
            field=ckeditor.fields.RichTextField(null=True),
        ),
    ]
