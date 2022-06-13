# Generated by Django 3.2 on 2022-06-12 18:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_category'),
        ('book', '0002_book_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='category',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='web.category'),
            preserve_default=False,
        ),
    ]