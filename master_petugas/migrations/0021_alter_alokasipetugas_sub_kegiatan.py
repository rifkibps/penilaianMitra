# Generated by Django 5.0 on 2024-12-10 03:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master_petugas', '0020_alter_alokasipetugas_sub_kegiatan_and_more'),
        ('master_survey', '0007_alter_subkegiatansurvei_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alokasipetugas',
            name='sub_kegiatan',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.RESTRICT, related_name='subkegiatan_survei', to='master_survey.subkegiatansurvei', verbose_name='Kegiatan Survei'),
            preserve_default=False,
        ),
    ]