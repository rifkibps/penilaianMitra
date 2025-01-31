from django import forms
from . import models
from master_petugas.models import AlokasiPetugas
from django.core.validators import FileExtensionValidator
from master_petugas import utils
import pandas as pd
from pprint import pprint
from io import BytesIO

from django.db.models import Q

class IndikatorPenilaianForm(forms.ModelForm):
    
    class Meta:

        model = models.IndikatorPenilaian
        fields = [
            'nama_indikator', 
            'deskripsi_penilaian'
        ]

        labels = {
            'nama_indikator' : 'Nama Indikator', 
            'deskripsi_penilaian'  : 'Deskripsi Penilaian'
        }

        attrs_input = {
            'class' : 'form-control',
            'required': 'required',
            'placeholder': '...'
        }

        widgets = {
            'nama_indikator': forms.TextInput(
                attrs = attrs_input
            ),
            'deskripsi_penilaian': forms.Textarea(
                attrs = attrs_input
            )            
        }

class KegiatanPenilaianForm(forms.ModelForm):
    
    class Meta:

        model = models.KegiatanPenilaianModel
        fields = [
            'kegiatan_survey', 
            'tgl_penilaian',
            'status',
            'role_permitted',
            'role_penilai_permitted',
        ]

        labels = {
            'nama_kegiatan' : 'Nama Kegiatan', 
            'survey'  : 'Nama Survei',
            'tgl_penilaian' : 'Tanggal Penilaian',
            'status' : 'Status Penilaian'
        }

        attrs_input = {
            'class' : 'form-control',
            'required': 'required',
            'placeholder': '...'
        }

        widgets = {
            'kegiatan_survey': forms.Select(
                attrs = attrs_input | {'class' : 'form-select'}
            ),
            'tgl_penilaian': forms.DateInput(
                attrs = attrs_input  | {'type' : 'date'}
            ),
            'role_permitted': forms.SelectMultiple(
                 attrs = attrs_input | {'size' : '10', 'style' : "height: 100%;"}
            ),
             'role_penilai_permitted': forms.SelectMultiple(
                 attrs = attrs_input | {'size' : '10', 'style' : "height: 100%;"}
            ),
                  'status': forms.Select(
                attrs = attrs_input | {'class' : 'form-select'}
            ),
        }


class IndikatorKegiatanPenilaianForm(forms.ModelForm):
    
    class Meta:

        model = models.IndikatorKegiatanPenilaian
        fields = [
            'kegiatan_penilaian', 
            'indikator_penilaian',
            'scale',
            'n_min',
            'n_max'
        ]

        labels = {
            'kegiatan_penilaian' : 'Kegiatan Penilaian', 
            'indikator_penilaian'  : 'Indikator Penilaian',
        }

        attrs_input = {
            'class' : 'form-control form-control-sm',
            'placeholder': '...'
        }

        widgets = {
            'kegiatan_penilaian': forms.Select(
                attrs = attrs_input | {'class' : 'form-select', 'id' : 'id_kegiatan_penilaian_id'}
            ),
            'indikator_penilaian': forms.Select(
                attrs = attrs_input | {'class' : 'form-select', 'id' : 'id_indikator_penilaian_id'}
            ),
            'scale': forms.Select(
                attrs = attrs_input | {'class' : 'form-select'}
            ),
            'n_min': forms.NumberInput(
                attrs = attrs_input
            ),
            'n_max': forms.NumberInput(
                attrs = attrs_input
            ),
        }


class PenilaianMitraForm(forms.Form):

    def clean(self):
        df = []
        base_errors = []
        for key, value in self.data.items():
            if 'nilai_indikator_' in key:
                indikator_penilaian = key.replace('nilai_indikator_', '')
                indikator_penilaian_model = models.IndikatorKegiatanPenilaian.objects.filter(pk = indikator_penilaian)
                if indikator_penilaian_model.exists():
                    n_min = indikator_penilaian_model.first().n_min
                    n_max = indikator_penilaian_model.first().n_max

                    if value.isnumeric() == False or len(value) == 0:
                        base_errors.append('Nilai petugas tidak boleh kosong.') # Sesuaikan sama threshold nilainya yaaaaaaa
                    else:
                        nilai = int(value)
                        if nilai > n_max or nilai < n_min:
                            base_errors.append(f'Nilai petugas harus berkisar [{n_min} - {n_max}]') # Sesuaikan sama threshold nilainya yaaaaaaa

                    df.append({
                        'petugas' : self.data['field_mitra'], #ID ALOKASI
                        'penilai' : self.data['field_id_penilai'], #ID ALOKASI
                        'penilaian' : indikator_penilaian,
                        'nilai': value
                    })
                else:
                    base_errors.append('Terdapat indikator penilaian yang tidak relevan.')
                    continue

            if 'catatan_indikator_' in key:
                check_exist = [index for (index, d) in enumerate(df) if d["penilaian"] == key.replace('catatan_indikator_', '')]
                if len(check_exist) > 0:
                    df[check_exist[0]]['catatan'] = value

        if len(base_errors) > 0:
            self._errors['nilai_petugas'] = self.error_class(base_errors)
            return self._errors['nilai_petugas'] 
        
        self.cleaned_data = df
        return self.cleaned_data    


class NilaiFormUpload(forms.Form):
    import_file = forms.FileField(allow_empty_file=False,validators=[FileExtensionValidator(allowed_extensions=['xlsx'])], label="Import Alokasi Petugas", widget=forms.FileInput(
                              attrs={'class': "form-control"}))
    
    def clean(self):
        try:
            data = self.cleaned_data.get('import_file').read()
            df = pd.read_excel(BytesIO(data), skiprows=1, dtype='str')
        except:
            self._errors['import_file'] = self.error_class(['Format template tidak sesuai. Silahkan gunakan template yang telah disediakan.'])
            return self._errors['import_file']
        
        df.dropna(axis=0, how='all', inplace=True)
        base_errors = []

       ### PENGECEKAN FORMAT TEMPLATE ###
        headers = ['No', 'ID Alokasi Mitra', 'ID Kegiatan Penilaian', 'Kode Petugas', 'Nama Petugas', 'Survei', 'Jabatan', 'Kegiatan Penilaian']  
        for header in headers:
            if header not in df.columns:
                self._errors['import_file'] = self.error_class(['Format template tidak sesuai. Silahkan gunakan template yang telah disediakan.'])
                return self._errors['import_file']
        
        ### VALIDASI NULL UNTUK COMMOM HEADER
        df_id = df[['ID Alokasi Mitra', 'ID Kegiatan Penilaian']]
        df_null = df_id[df_id.isna().any(axis=1)]
        for idx, i in df_null.iterrows():
            self._errors['import_file'] = self.error_class([f'Nilai kosong pada <b>Baris {idx+1}</b> ditemukan. Periksa kolom <b>ID Alokasi Mitra (Kol. B)</b> atau <b>ID Kegiatan Penilaian (Kol. C)</b>'])
            return self._errors['import_file']
        
        # CHECK HANYA ADA SATU KEGIATAN PENILAIAN DALAM FILE UPLOAD
        df_kegiatan_ = df['ID Kegiatan Penilaian'].unique()
        if len(df_kegiatan_) > 1 :
            self._errors['import_file'] = self.error_class([f'Satu file upload hanya digunakan untuk satu jenis kegiatan penilaian penilaian. Periksa kolom <b>ID Kegiatan Penilaian (Kol.C) </b>'])
            return self._errors['import_file']

        for idx, dt in df['ID Kegiatan Penilaian'].items():
            check_db = models.KegiatanPenilaianModel.objects.filter(pk = dt)
            if not check_db.exists():
                self._errors['import_file'] = self.error_class([f'Kegiatan penilaian [{dt}] tidak tersedia pada database. Periksa kolom <b>ID Kegiatan Penilaian [KOLOM C] Baris {idx+1}</b>.'])
                return self._errors['import_file']

        kegiatan_penilaian = models.KegiatanPenilaianModel.objects.filter(pk = df['ID Kegiatan Penilaian'][0]).first()

        check_indikator = list(models.IndikatorKegiatanPenilaian.objects.filter(kegiatan_penilaian = kegiatan_penilaian.id).values_list('indikator_penilaian__nama_indikator', flat=True))
        data_indikator = check_indikator
        check_catatan_personal = [f'Catatan Personal {indikator}' for indikator in check_indikator]
        check_indikator = [f'Penilaian Indikator {indikator}' for indikator in check_indikator]
    
        for check in check_indikator:
            if check not in df.columns:
                self._errors['import_file'] = self.error_class([f'Format template tidak sesuai (Indikator Penilaian [{check}] tidak match / tidak tersedia pada file upload). Silahkan gunakan template yang telah disediakan.'])
                return self._errors['import_file']
            
        for check in check_catatan_personal:
            if check not in df.columns:
                self._errors['import_file'] = self.error_class([f'Format template tidak sesuai (Catatan Personal [{check}] tidak match / tidak tersedia pada file upload). Silahkan gunakan template yang telah disediakan.'])
                return self._errors['import_file']

        df.drop(columns=df.columns[0], axis=1, inplace=True)
        
        ### PENGECEKAN ISIAN ###
        df_null = df[df.isna().any(axis=1)]
        for idx, i in df_null.iterrows():
            null_cols = []
            for e in i[i.isna()].index:
                if 'Catatan personal' in e:
                    null_cols.append(str(e).capitalize())
            base_errors.append(f'Nilai kosong pada <b>Baris {idx+1}</b> ditemukan. Periksa kolom <b>({", ".join(null_cols)})</b>')
        pprint(base_errors)
        
        # Cek ID Alokasi Mitra dengan data file upload sesuai atau tidak
        for idx, dt in df.iterrows():
            id_alokasi = dt['ID Alokasi Mitra']
            kode_petugas = dt['Kode Petugas']
            nama_petugas = dt['Nama Petugas']
            survei = dt['Survei']
            jabatan = dt['Jabatan']

            db_check = AlokasiPetugas.objects.filter(
                petugas__kode_petugas = kode_petugas,
                survey__nama = survei,
                role__jabatan = jabatan,
            )
            
            if db_check.exists() == False :
                base_errors.append(f'Data alokasi petugas: <b>[{kode_petugas}] {nama_petugas} - {survei} - {jabatan}</b> tidak tersedia pada Database. Harap periksa baris <b>{idx+1}</b>')
                continue
            else:
                db_check_data = db_check.first()
                role_permitted = list(kegiatan_penilaian.role_permitted.values_list('id', flat=True))

                if db_check_data.role.id not in role_permitted:
                    base_errors.append(f'Role petugas <b>[{kode_petugas}] {nama_petugas} - {jabatan}</b> tidak sesuai dengan <b>role permitted</b> untuk kegiatan penilaian {kegiatan_penilaian.nama_kegiatan} <b>(Role yang diizinkan hanya {", ".join(role_permitted)})</b>. Harap periksa baris <b>{idx+1}</b>')
                    continue

            if str(db_check.first().id) != str(id_alokasi) :
                base_errors.append(f'Data alokasi petugas: <b>[{kode_petugas}] {nama_petugas} - {survei} - {jabatan}</b> tidak sesuai dengan ID Alokasi Petugas. Harap periksa baris <b>{idx+1}</b>')
               

        # Cek ID Kegiatan Penilaian Mitra dengan data file upload sesuai atau tidak
        for idx, dt in df.iterrows():
            id_alokasi = dt['ID Kegiatan Penilaian']
            dt_kegiatan = dt['Kegiatan Penilaian']

            db_check = models.KegiatanPenilaianModel.objects.filter(
                            pk = id_alokasi,
                            nama_kegiatan = dt_kegiatan
                        )
            
            if db_check.exists() == False :
                base_errors.append(f'Data Kegiatan Penilaian: <b>[{dt_kegiatan}]</b> tidak tersedia pada Database. Harap periksa baris <b>{idx+1}</b>')
                continue
     

        # Cek duplikasi Data pada master file
        df_data_mitra = df[headers[2:]]
        duplicated_petugas = df_data_mitra[df_data_mitra.duplicated()]['Nama Petugas']
        for idx, row in duplicated_petugas.items():
            base_errors.append(f'Duplikasi data petugas: <b>{row}</b> dengan beban tugas yang sama ditemukan. Harap periksa baris <b>{idx+1}</b>')

        # Pengecekan tipe data dari nilai pada master file
        # Numerik Value

        if len(base_errors) > 0:
            self._errors['import_file'] = self.error_class(base_errors)
            return self._errors['import_file'] 
        
        for idx, data in df[check_indikator].iterrows():
            for idx2, row in data.items():
                if row.isnumeric() == False:
                    base_errors.append(f'Indikator penilaian <b>{idx2}</b> untuk petugas <b> [{df["Kode Petugas"][idx]}] {df["Nama Petugas"][idx]} </b> hanya dapat diisikan digit numerik. Harap periksa baris <b>{idx+1} kolom {idx2}</b>')
                else:
                    if (int(row) > 100) or (int(row) < 0) :
                        base_errors.append(f'Indikator penilaian <b>{idx2}</b> untuk petugas <b> [{df["Kode Petugas"][idx]}] {df["Nama Petugas"][idx]} </b> hanya dapat diisikan <b>nilai 0-100</b>. Harap periksa baris <b>{idx+1} kolom {idx2}</b>')

        if len(base_errors) > 0:
            self._errors['import_file'] = self.error_class(base_errors)
            return self._errors['import_file'] 
    
        # FORMATING DICTIONARY

        id_indikator = []
        for col_new, col_old in zip(data_indikator, check_indikator):
            db_query = models.IndikatorPenilaian.objects.filter(nama_indikator = col_new ).first()
            id_indikator.append(db_query.id)
            df.rename(columns = {col_old:db_query.id}, inplace = True)
            df.rename(columns = {f"Catatan Personal {col_new}": f"catatan_{db_query.id}"}, inplace = True)

        df_dict = []

        for idx, data in df.iterrows():

            for id in id_indikator:
                row_db =  {}

                penilaian = models.IndikatorKegiatanPenilaian.objects.filter(kegiatan_penilaian = kegiatan_penilaian.id, indikator_penilaian = id).first()
                row_db['petugas'] = data['ID Alokasi Mitra']
                row_db['penilaian'] = penilaian.id
                row_db['nilai'] = data[id]
                row_db['catatan'] = data[f'catatan_{id}']
                
                df_dict.append(row_db)

        
        self.cleaned_data = df_dict
        return self.cleaned_data
    