# Generated by Django 2.2.1 on 2022-06-17 21:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Agent', '0005_add_to_store'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Product_Amount_in_Store',
            new_name='Product_Amount_in_Store_agent',
        ),
    ]
