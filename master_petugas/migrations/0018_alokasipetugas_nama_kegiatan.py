# Generated by Django 5.0 on 2024-12-10 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master_petugas', '0017_remove_alokasipetugas_organik_alokasipetugas_pegawai'),
    ]

    operations = [
        migrations.AddField(
            model_name='alokasipetugas',
            name='nama_kegiatan',
            field=models.CharField(default='Kegiatan Lapangan', max_length=256, verbose_name='Nama Kegiatan Penilaian'),
            preserve_default=False,
        ),
    ]
