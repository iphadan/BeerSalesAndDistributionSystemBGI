# Generated by Django 2.2.1 on 2022-06-17 21:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Agent', '0004_product_amount_in_store'),
    ]

    operations = [
        migrations.CreateModel(
            name='add_to_store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.CharField(blank=True, max_length=200, null=True)),
                ('qunitiy', models.IntegerField(null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('Store', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Agent.Agent_Store')),
            ],
        ),
    ]
