# Generated by Django 5.0.6 on 2024-06-26 20:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0006_alter_comment_article_alter_comment_author"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={"verbose_name_plural": "categories"},
        ),
    ]
