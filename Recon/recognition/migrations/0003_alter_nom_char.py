# Generated by Django 5.0.4 on 2024-07-13 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recognition', '0002_nom_char'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nom',
            name='char',
            field=models.CharField(blank=True, max_length=10000000000000000303786028427003666890752),
        ),
    ]
