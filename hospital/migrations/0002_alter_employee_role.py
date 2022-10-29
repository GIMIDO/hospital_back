# Generated by Django 4.1.2 on 2022-10-28 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='role',
            field=models.CharField(choices=[('Admin', 'Admin'), ('Doctor', 'Doctor'), ('Reception', 'Reception')], default='Doctor', max_length=20),
        ),
    ]