# Generated by Django 5.0.4 on 2024-04-09 09:50

import datetime
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("file_searcher", "0005_alter_fileanalyzer_created_at_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="fileanalyzer",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="fileanalyzer",
            name="created_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="fileupload",
            name="upload_time",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 4, 9, 9, 50, 4, 257618)
            ),
        ),
    ]
