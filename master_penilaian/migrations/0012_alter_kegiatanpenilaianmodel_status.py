# Generated by Django 5.0 on 2024-12-06 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master_penilaian', '0011_alter_kegiatanpenilaianmodel_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kegiatanpenilaianmodel',
            name='status',
            field=models.CharField(choices=[('0', 'Tidak Aktif'), ('1', 'Berlangsung'), ('2', 'Selesai')], default=0, max_length=1, verbose_name='Status Penilaian'),
        ),
    ]
