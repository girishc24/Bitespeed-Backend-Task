# Generated by Django 5.0.6 on 2024-06-20 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='linkPrecedence',
            field=models.CharField(default='primary', max_length=10),
        ),
    ]
