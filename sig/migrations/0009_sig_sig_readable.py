# Generated by Django 3.2.9 on 2022-07-07 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sig', '0008_auto_20220706_1557'),
    ]

    operations = [
        migrations.AddField(
            model_name='sig',
            name='sig_readable',
            field=models.TextField(null=True),
        ),
    ]