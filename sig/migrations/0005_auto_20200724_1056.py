# Generated by Django 3.0.6 on 2020-07-24 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sig', '0004_auto_20200715_0116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sigparsed',
            name='strength',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='sigparsed',
            name='strength_max',
            field=models.FloatField(null=True),
        ),
    ]
