# Generated by Django 4.0.1 on 2022-02-14 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('draft', 'Draft')], default='draft', max_length=10),
        ),
    ]
