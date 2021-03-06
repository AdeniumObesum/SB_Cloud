# Generated by Django 2.1.7 on 2019-03-11 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public_cloud', '0002_menu'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Family',
        ),
        migrations.DeleteModel(
            name='Menu',
        ),
        migrations.AddField(
            model_name='firminfo',
            name='icon_name',
            field=models.CharField(max_length=100, null=True, verbose_name='图标名'),
        ),
        migrations.AddField(
            model_name='regioninfo',
            name='is_delete',
            field=models.IntegerField(default=0, verbose_name='是否删除'),
        ),
        migrations.AlterField(
            model_name='accountinfo',
            name='is_delete',
            field=models.IntegerField(default=0, verbose_name='是否删除'),
        ),
    ]
