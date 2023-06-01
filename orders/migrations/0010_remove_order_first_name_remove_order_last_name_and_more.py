# Generated by Django 4.2 on 2023-05-31 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_alter_orderitem_size'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='order',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='order',
            name='middle_name',
        ),
        migrations.AddField(
            model_name='order',
            name='full_name',
            field=models.CharField(default=1, max_length=150),
            preserve_default=False,
        ),
    ]