# Generated by Django 3.0.6 on 2020-07-24 11:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sig', '0005_auto_20200724_1056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sigreviewed',
            name='sig_parsed',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sig_reviewed', to='sig.SigParsed'),
        ),
    ]
