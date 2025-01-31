from master_petugas import models as model_petugas
from master_pegawai import models as model_pegawai
from master_petugas.models import AlokasiPetugas
from . import models
from django.db.models import Q

def convert_table_penilaian(nilai_mitra, indicators, empty = False):

    opt = ''
    for idx, dt in enumerate(indicators):
        nilai, catatan = '', ''

        if empty is False:
            nilai_mitra_ = nilai_mitra.filter(detail_nilai__indikator_penilaian = dt.pk ).values('detail_nilai__nilai', 'detail_nilai__catatan')
            if nilai_mitra_.exists():
                nilai = nilai_mitra_.first().get('detail_nilai__nilai')
                catatan = nilai_mitra_.first().get('detail_nilai__catatan')

        opt +=  f"""<tr>
                <td>{idx+1}</td>
                <td>{dt.indikator_penilaian.nama_indikator}</td>
                <td>
                    <input type="number" class="form-control d-inline" name="nilai_indikator_{dt.pk}" value="{nilai}" placeholder="Isikan nilai" alt="Isikan nilai" min="{dt.n_min}" max="{dt.n_max}" onkeyup="if(this.value > {dt.n_max} || this.value < {dt.n_min}) this.value = null;">   
                </td>
                <td>
                    <textarea class="form-control" name="catatan_indikator_{dt.pk}" cols="30" rows="5">{catatan}</textarea>
                </td>
            </tr>"""

    if len(opt) == 0:
        opt = '<tr><td colspan="4" class="text-center">Kegiatan Penilaian Belum Memiliki Indiktor Penilaian/ Kegiatan sedang Tidak Aktif</td></tr>'

    return opt

def get_summarize_penilaian(user_id):
    data_pegawai= model_pegawai.MasterPegawaiModel.objects.filter(user=user_id)
        
    jml_kegiatan = 0
    jml_penilaian_aktif = 0
    jml_mitra_belum_dinilai = 0
    jml_mitra_dinilai = 0

    if data_pegawai.exists():
        alokasi_pegawai = AlokasiPetugas.objects.filter(pegawai = data_pegawai.first().id).values('sub_kegiatan', 'role', 'id').distinct()
        jml_kegiatan = alokasi_pegawai.count()
        
        if jml_kegiatan != 0:
            for dt_kegiatan in alokasi_pegawai:
                penilaian_aktif = models.KegiatanPenilaianModel.objects.filter(~Q(status = '0') & Q(kegiatan_survey = dt_kegiatan['sub_kegiatan']))

                if penilaian_aktif.exists():
                    for dt_ in  penilaian_aktif:
                        for role_mitra in dt_.role_permitted.values_list('pk', flat=True).all():
                            alokasi_mitra = AlokasiPetugas.objects.filter(role = role_mitra, sub_kegiatan = dt_.kegiatan_survey.id, pegawai = None)
                            
                            if alokasi_mitra.exists():
                                jml_mitra_belum_dinilai += alokasi_mitra.count()
                                
                                for dt__ in alokasi_mitra:
                                    nilai_mitra = models.MasterPenilaianPetugas.objects.filter(penilai = dt_kegiatan['id'], petugas = dt__.pk)
                                    if nilai_mitra.exists():
                                        jml_mitra_dinilai += 1 

                        if dt_kegiatan['role'] in dt_.role_penilai_permitted.values_list('pk', flat=True).all():
                            jml_penilaian_aktif += 1

    return {
        'jml_kegiatan' : jml_kegiatan,
        'jml_penilaian_aktif' : jml_penilaian_aktif,
        'jml_mitra_belum_dinilai' : jml_mitra_belum_dinilai,
        'jml_mitra_dinilai' : jml_mitra_dinilai,
    }