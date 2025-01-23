from django.db import models


# Create your models here.
class SurveyModel(models.Model):
   
   status = (
       ('0', 'Belum Aktif'),
       ('1', 'Berlangsung'),
       ('2', 'Selesai')
    )
   
   nama = models.CharField(max_length=128, null=False, blank=False, verbose_name='Nama Survei' )
   deskripsi = models.TextField(null=False, blank=False, verbose_name='Deskripsi Survei')
   tgl_mulai = models.DateField( null=False, blank=False, verbose_name='Tanggal Mulai')
   tgl_selesai = models.DateField( null=False, blank=False, verbose_name='Tanggal Berakhir')
   state = models.CharField(max_length=1, choices=status, default=0, null=False, blank=False, verbose_name='Status Survei')

   def __str__(self):
      return f"{self.nama} [{self.tgl_mulai} s.d. {self.tgl_selesai}]"

class SubKegiatanSurvei(models.Model):
    status = (
       ('0', 'Belum Aktif'),
       ('1', 'Berlangsung'),
       ('2', 'Selesai')
    )
    
    nama_kegiatan = models.CharField(max_length=256, null=False, blank=False, verbose_name='Nama Kegiatan Penilaian' )
    survey = models.ForeignKey(SurveyModel, on_delete=models.CASCADE, related_name='master_alokasi_survey', verbose_name='Survei/Sensus')
    status = models.CharField(max_length=1, choices=status, default=0, null=False, blank=False, verbose_name='Status Kegiatan')

    def __str__(self):
        return f'{self.pk}. {self.nama_kegiatan} | {self.survey.nama}'