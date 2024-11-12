# Generated by Django 5.0 on 2024-11-12 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='JabatanPegawaiModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jabatan', models.CharField(max_length=64, verbose_name='Jabatan')),
            ],
        ),
        migrations.CreateModel(
            name='pangkatPegawaiModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('golongan', models.CharField(max_length=64, verbose_name='Golongan')),
                ('pangkat', models.CharField(max_length=64, verbose_name='Pangkat')),
            ],
        ),
    ]
