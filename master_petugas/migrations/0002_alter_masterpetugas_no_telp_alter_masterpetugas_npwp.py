# Generated by Django 4.2.2 on 2024-12-27 13:41

from django.db import migrations, models
import master_petugas.validators


class Migration(migrations.Migration):

    dependencies = [
        ('master_petugas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='masterpetugas',
            name='no_telp',
            field=models.CharField(max_length=13, validators=[master_petugas.validators.int_validators], verbose_name='No. Telp (Ex: 62..)'),
        ),
        migrations.AlterField(
            model_name='masterpetugas',
            name='npwp',
            field=models.CharField(blank=True, max_length=15, null=True, validators=[master_petugas.validators.int_validators], verbose_name='NPWP'),
        ),
    ]