# Generated by Django 4.2.2 on 2024-12-22 04:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('master_petugas', '0001_initial'),
        ('master_survey', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndikatorKegiatanPenilaian',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scale', models.CharField(choices=[('0', 'Ordinal'), ('1', 'Numerik')], default=0, max_length=1, verbose_name='Skala Penilaian')),
                ('n_min', models.IntegerField(default=1, verbose_name='Batas Minimum')),
                ('n_max', models.IntegerField(default=5, verbose_name='Batas Maksimal')),
            ],
        ),
        migrations.CreateModel(
            name='IndikatorPenilaian',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_indikator', models.CharField(max_length=128, verbose_name='Indikator Penilaian')),
                ('deskripsi_penilaian', models.TextField(blank=True, null=True, verbose_name='Deskripsi Penilaian')),
            ],
        ),
        migrations.CreateModel(
            name='MasterPenilaianPetugas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(choices=[('0', 'Blacklist'), ('1', 'Tidak Direkomendasikan'), ('2', 'Direkomendasikan')], default=2, max_length=1, verbose_name='Status Mitra')),
                ('penilai', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='penilai', to='master_petugas.alokasipetugas')),
                ('penilaian', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='indikator_kegiatan_penilaian', to='master_penilaian.indikatorkegiatanpenilaian')),
                ('petugas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nilai_petugas', to='master_petugas.alokasipetugas')),
            ],
        ),
        migrations.CreateModel(
            name='MasterNilaiPetugas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nilai', models.SmallIntegerField(blank=True, null=True, verbose_name='Nilai Kegiatan Petugas')),
                ('catatan', models.TextField(blank=True, null=True, verbose_name='Catatan Personal')),
                ('penilaian', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detail_nilai', to='master_penilaian.masterpenilaianpetugas')),
            ],
        ),
        migrations.CreateModel(
            name='KegiatanPenilaianModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tgl_penilaian', models.DateField(verbose_name='Tanggal Penilaian')),
                ('status', models.CharField(choices=[('0', 'Tidak Aktif'), ('1', 'Berlangsung'), ('2', 'Selesai')], default=0, max_length=1, verbose_name='Status Penilaian')),
                ('kegiatan_survey', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='penilaian_survei', to='master_survey.subkegiatansurvei', verbose_name='Kegiatan Survei')),
                ('role_penilai_permitted', models.ManyToManyField(related_name='role_permitted_penilai', to='master_petugas.rolemitra', verbose_name='Role Penilai')),
                ('role_permitted', models.ManyToManyField(related_name='role_permitted_petugas', to='master_petugas.rolemitra', verbose_name='Role Petugas')),
            ],
        ),
        migrations.AddField(
            model_name='indikatorkegiatanpenilaian',
            name='indikator_penilaian',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='indikator_penilaian_petugas', to='master_penilaian.indikatorpenilaian'),
        ),
        migrations.AddField(
            model_name='indikatorkegiatanpenilaian',
            name='kegiatan_penilaian',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kegiatan_penilaian_petugas', to='master_penilaian.kegiatanpenilaianmodel'),
        ),
    ]
