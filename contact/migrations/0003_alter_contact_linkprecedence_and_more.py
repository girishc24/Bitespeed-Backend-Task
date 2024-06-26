# Generated by Django 5.0.6 on 2024-06-20 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0002_alter_contact_linkprecedence'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='linkPrecedence',
            field=models.CharField(choices=[('primary', 'Primary'), ('secondary', 'Secondary')], max_length=10),
        ),
        migrations.AlterField(
            model_name='contact',
            name='phoneNumber',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
