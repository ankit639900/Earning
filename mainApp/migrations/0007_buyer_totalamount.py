# Generated by Django 4.1.2 on 2024-06-20 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0006_rename_buyer_withdrawn_buyer'),
    ]

    operations = [
        migrations.AddField(
            model_name='buyer',
            name='totalamount',
            field=models.IntegerField(default=0),
        ),
    ]
