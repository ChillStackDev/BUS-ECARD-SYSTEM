# Generated by Django 5.0.3 on 2024-04-28 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='coursename',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='student',
            name='data_integrity_hash',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AddField(
            model_name='student',
            name='image',
            field=models.ImageField(blank=True, default='dp.png', null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='student',
            name='sscBoard',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='student',
            name='sscHNO',
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AddField(
            model_name='student',
            name='sscPass',
            field=models.CharField(blank=True, max_length=6),
        ),
        migrations.AlterField(
            model_name='student',
            name='building_number',
            field=models.CharField(max_length=15),
        ),
    ]