# Generated by Django 5.0.4 on 2025-01-14 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('honeyapp', '0007_alter_review_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='category',
            field=models.CharField(default='Dry Fruit', max_length=40),
            preserve_default=False,
        ),
    ]
