# Generated by Django 5.0 on 2024-11-10 08:26

import master_petugas.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master_petugas', '0010_masterpetugas_bank_masterpetugas_pemilik_rek_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='masterpetugas',
            name='kode_petugas',
            field=models.CharField(max_length=12, unique=True, verbose_name='Kode Petugas'),
        ),
        migrations.AlterField(
            model_name='masterpetugas',
            name='no_telp',
            field=models.CharField(blank=True, max_length=13, null=True, validators=[master_petugas.validators.int_validators], verbose_name='No. Telp (Ex: 6285712345678)'),
        ),
    ]
