# Generated by Django 4.2.2 on 2024-11-29 14:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('master_pegawai', '0005_alter_masterpegawaimodel_user'),
        ('master_petugas', '0016_alokasipetugas_organik_alter_alokasipetugas_petugas'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alokasipetugas',
            name='organik',
        ),
        migrations.AddField(
            model_name='alokasipetugas',
            name='pegawai',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='master_alokasi_pegawai', to='master_pegawai.masterpegawaimodel', verbose_name='Pegawai'),
        ),
    ]
