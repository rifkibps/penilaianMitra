# Generated by Django 4.2.2 on 2023-10-12 13:02

from django.db import migrations, models
import django.db.models.deletion
import master_petugas.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('master_survey', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MasterPetugas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kode_petugas', models.CharField(max_length=16, unique=True, verbose_name='Kode Petugas/ID Sobat')),
                ('nama_petugas', models.CharField(max_length=64, verbose_name='Nama Petugas')),
                ('nik', models.CharField(max_length=16, unique=True, validators=[master_petugas.validators.int_validators], verbose_name='NIK')),
                ('npwp', models.CharField(max_length=15, unique=True, validators=[master_petugas.validators.int_validators], verbose_name='NPWP')),
                ('tgl_lahir', models.DateField(verbose_name='Tanggal Lahir')),
                ('pendidikan', models.CharField(choices=[('0', 'SD/MI Sederajat'), ('1', 'SMP/SLTP Sederajat'), ('2', 'SMA/SLTA Sederajat'), ('3', 'DI-DIII'), ('4', 'DV/S1'), ('5', 'S2'), ('6', 'S3')], max_length=1, verbose_name='Pendidikan Terakhir')),
                ('pekerjaan', models.CharField(max_length=128, verbose_name='Pekerjaan')),
                ('agama', models.CharField(choices=[('0', 'Islam'), ('1', 'Kristen'), ('2', 'Hindu'), ('3', 'Budha')], max_length=1, verbose_name='Agama')),
                ('email', models.EmailField(max_length=128, unique=True, verbose_name='Email')),
                ('no_telp', models.CharField(max_length=13, validators=[master_petugas.validators.int_validators], verbose_name='No. Telp')),
                ('alamat', models.CharField(max_length=256, verbose_name='Alamat Domisili')),
                ('status', models.CharField(choices=[('0', 'Aktif'), ('1', 'Non Aktif'), ('3', 'Organik')], max_length=1, verbose_name='Status Mitra')),
            ],
        ),
        migrations.CreateModel(
            name='RoleMitra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jabatan', models.CharField(max_length=128, verbose_name='Jabatan/Peran')),
            ],
        ),
        migrations.CreateModel(
            name='RekeningPetugas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jenis_bank', models.CharField(choices=[('002', 'Bank Rakyat Indonesia (BRI)'), ('008', 'Bank Mandiri'), ('009', 'Bank Negara Indonesia (BNI)'), ('011', 'Bank Danamon'), ('014', 'Bank Central Asia (BCA)'), ('451', 'Bank Syariah Indonsia (BSI-Mandiri)')], max_length=3, verbose_name='Jenis Bank')),
                ('no_rek', models.CharField(max_length=20, unique=True, verbose_name='No Rekening')),
                ('rek_utama', models.CharField(choices=[('0', 'Bukan Rek. Utama'), ('1', 'Rek. Utama')], default=1, max_length=1, verbose_name='Status Rekening')),
                ('petugas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='master_petugas', to='master_petugas.masterpetugas')),
            ],
        ),
        migrations.CreateModel(
            name='AlokasiPetugas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('petugas', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='master_alokasi_petugas', to='master_petugas.masterpetugas')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='master_alokasi_role', to='master_petugas.rolemitra')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='master_alokasi_survey', to='master_survey.surveymodel')),
            ],
        ),
    ]
