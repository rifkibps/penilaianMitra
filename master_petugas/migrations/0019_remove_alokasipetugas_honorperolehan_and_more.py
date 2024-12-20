# Generated by Django 5.0 on 2024-12-10 02:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master_petugas', '0018_alokasipetugas_nama_kegiatan'),
        ('master_survey', '0005_remove_surveymodel_salary'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alokasipetugas',
            name='honorPerolehan',
        ),
        migrations.RemoveField(
            model_name='alokasipetugas',
            name='nama_kegiatan',
        ),
        migrations.RemoveField(
            model_name='alokasipetugas',
            name='survey',
        ),
        migrations.CreateModel(
            name='SubKegiatanSurvei',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_kegiatan', models.CharField(max_length=256, verbose_name='Nama Kegiatan Penilaian')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='master_alokasi_survey', to='master_survey.surveymodel', verbose_name='Survei/Sensus')),
            ],
        ),
        migrations.AddField(
            model_name='alokasipetugas',
            name='sub_kegiatan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='subkegiatan_survei', to='master_petugas.subkegiatansurvei', verbose_name='Kegiatan Survei'),
        ),
    ]