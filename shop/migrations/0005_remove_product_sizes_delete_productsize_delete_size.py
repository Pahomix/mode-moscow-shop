# Generated by Django 4.2 on 2023-05-28 22:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_alter_size_options_remove_size_quantity_productsize'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='sizes',
        ),
        migrations.DeleteModel(
            name='ProductSize',
        ),
        migrations.DeleteModel(
            name='Size',
        ),
    ]
