# Generated by Django 2.1.7 on 2019-03-12 14:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('public_cloud', '0006_hostinfo'),
    ]

    operations = [
        migrations.DeleteModel(
            name='HostInfo',
        ),
    ]