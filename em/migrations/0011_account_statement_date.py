# Generated by Django 3.1.7 on 2021-04-14 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('em', '0010_auto_20210407_1105'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='statement_date',
            field=models.DateField(blank=True, help_text='Statement Date', null=True),
        ),
    ]