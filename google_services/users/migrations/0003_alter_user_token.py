# Generated by Django 5.0.4 on 2024-04-08 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_remove_user_auction_user_id_remove_user_user_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="token",
            field=models.CharField(
                blank=True, max_length=2048, null=True, verbose_name="Token"
            ),
        ),
    ]
