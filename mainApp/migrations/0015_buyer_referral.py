# Generated by Django 4.1.2 on 2024-06-26 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0014_withdrawn_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='buyer',
            name='referral',
            field=models.CharField(default='', max_length=100, unique=True),
        ),
    ]
