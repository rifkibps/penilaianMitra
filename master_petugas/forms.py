from django import forms

from . import models
from . import utils
import pandas as pd
from io import BytesIO
from django.db.models import Q

from master_survey.models import SurveyModel, SubKegiatanSurvei
from master_pegawai.models import MasterPegawaiModel
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from pprint import pprint

class MasterPetugasForm(forms.ModelForm):
    
    class Meta:
        model = models.MasterPetugas
        fields = "__all__"

        attrs_input = {
            'class' : 'form-control',
            'placeholder': '...'
        }

        widgets = {
            'adm_id': forms.Select(
                attrs = attrs_input | {'class' : 'form-select ', 'id' : 'id_adm_id_id'}
            ),
            'kode_petugas': forms.TextInput(
                attrs = attrs_input | {'autofocus': 'autofocus'}
            ),
            'jk': forms.Select(
                attrs = attrs_input | {'class' : 'form-select'}
            ),
            'nama_petugas': forms.TextInput(
                attrs = attrs_input | {'autofocus': 'autofocus'}
            ),
            'nik': forms.TextInput(
                attrs = attrs_input
            ),
            'npwp': forms.TextInput(
                attrs = attrs_input
            ),
            'tgl_lahir': forms.DateInput(
                attrs = attrs_input | {'type': 'date'}
            ),
            'pendidikan': forms.Select(
                attrs = attrs_input | {'class' : 'form-select'}
            ),
            'pekerjaan': forms.TextInput(
                attrs = attrs_input
            ),
            'agama': forms.Select(
                attrs = attrs_input | {'class' : 'form-select'}
            ),
            'email': forms.EmailInput(
                attrs = attrs_input
            ),
            'no_telp': forms.TextInput(
                attrs = attrs_input
            ),
            'alamat': forms.Textarea(
                attrs = attrs_input | {'rows' : 50}
            ),
            'status': forms.Select(
                attrs = attrs_input | {'class' : 'form-select'}
            ),
            'bank': forms.Select(
                attrs = attrs_input | {'class' : 'form-select'}
            ),
            'rekening': forms.TextInput(
                attrs = attrs_input
            ),
            'pemilik_rek': forms.TextInput(
                attrs = attrs_input
            ),
        }

    def clean(self):
        form_data = self.cleaned_data
        data_not_cleaned = self.data

        if form_data.get('kode_petugas') is not None or len(form_data.get('kode_petugas')) > 0:
            # Validasi Kode Petugas
            if form_data['kode_petugas'].isnumeric() == False or len(form_data['kode_petugas']) != 12:
                self._errors['kode_petugas'] = self.error_class(['Format Kode Petugas/Sobat ID harus berupa angka 12 digit.'])
            else:
                check_code = models.MasterPetugas.objects.filter(kode_petugas=form_data['kode_petugas'])
                if check_code.exists():
                    if len(data_not_cleaned.get('id')) > 0:
                        if check_code.first().id != int(data_not_cleaned.get('id')):
                            self._errors['kode_petugas'] = self.error_class(['Kode Petugas telah terdaftar pada database'])
                    else:
                            self._errors['kode_petugas'] = self.error_class(['Kode Petugas telah terdaftar pada database'])
        
        if form_data.get('nik') is not None:
            # Validasi NIK
            if form_data['nik'].isnumeric() == False or len(form_data['nik']) != 16:
                self._errors['nik'] = self.error_class(['Format NIK harus berupa angka 16 digit.'])
            else:
                check_kk = models.MasterPetugas.objects.filter(nik=form_data['nik'])
                if check_kk.exists():
                    if len(data_not_cleaned.get('id')) > 0:
                        if check_kk.first().id != int(data_not_cleaned.get('id')):
                            self._errors['nik'] = self.error_class(['No KK telah terdaftar pada database'])
                    else:
                        self._errors['nik'] = self.error_class(['No KK telah terdaftar pada database'])
        
        if form_data.get('npwp') is not None:
            if form_data['npwp'].isnumeric() == False or len(form_data['npwp']) != 15:
                self._errors['npwp'] = self.error_class(['Format NPWP harus berupa angka 15 digit.'])
            else:
                check_npwp = models.MasterPetugas.objects.filter(npwp=form_data['npwp'])
                if check_npwp.exists():
                    if len(data_not_cleaned.get('id')) > 0:
                        if check_npwp.first().id != int(data_not_cleaned.get('id')):
                            self._errors['npwp'] = self.error_class(['No NPWP telah terdaftar pada database'])
                    else:
                        self._errors['npwp'] = self.error_class(['No NPWP telah terdaftar pada database'])
        
        if form_data.get('no_telp') is not None:
            if form_data['no_telp'].isnumeric() == False or len(form_data['no_telp']) != 13:
                self._errors['no_telp'] = self.error_class(['Format No Hp harus berupa angka 13 digit. Contoh:6285712345678'])
        
        if form_data.get('email') is not None:
            check_email = models.MasterPetugas.objects.filter(email=form_data['email'].strip())
            if check_email.exists():
                if len(data_not_cleaned.get('id')) > 0:
                    if check_email.first().id != int(data_not_cleaned.get('id')):
                        self._errors['email'] = self.error_class(['Email telah terdaftar pada database'])
                else:
                    self._errors['email'] = self.error_class(['Email telah terdaftar pada database'])

        if form_data.get('bank') is not None or form_data.get('rekening') is not None or form_data.get('pemilik_rek') is not None:
            if (form_data.get('bank') is not None and form_data.get('rekening') is not None and form_data.get('pemilik_rek') is not None) is False:
                if form_data.get('rekening') is None:
                    self._errors['rekening'] = self.error_class(['Nomor rekening tidak terisi lengkap'])
                elif form_data.get('pemilik_rek') is None:
                    self._errors['pemilik_rek'] = self.error_class(['Nama pemilik rekening tidak terisi lengkap'])
                else:
                    self._errors['bank'] = self.error_class(['Rincian Bank tidak terisi lengkap'])
            else:
                if form_data['rekening'].isnumeric() == False or (len(form_data['rekening']) > 16 or len(form_data['rekening']) < 10):
                    self._errors['rekening'] = self.error_class(['Nomor rekening harus berupa angka dengan maksimal 10 - 16 digit.'])
                else:
                    check_rekening = models.MasterPetugas.objects.filter(rekening=form_data['rekening'])
                    if check_rekening.exists():
                        if len(data_not_cleaned.get('id')) > 0:
                            if check_rekening.first().id != int(data_not_cleaned.get('id')):
                                self._errors['rekening'] = self.error_class(['Rekening telah terdaftar pada database'])
                        else:
                            self._errors['rekening'] = self.error_class(['Rekening telah terdaftar pada database'])

        return self.cleaned_data
    
class AlokasiForm(forms.ModelForm):
    
    class Meta:

        model = models.AlokasiPetugas
        fields = [
            'sub_kegiatan',
            'petugas', 
            'pegawai', 
            'role',
        ]

        labels = {
            'petugas': 'Nama Petugas', 
            'pegawai': 'Nama Pegawai', 
            'sub_kegiatan': 'Nama Kegiatan',
            'role': 'Jabatan',
        }

        attrs_input = {
            'class' : 'form-control',
            'required': 'required',
            'placeholder': '...'
        }

        widgets = {
            'petugas': forms.Select(
                attrs = attrs_input | {'class' : 'form-select', 'id': 'id_petugas_id'}
            ),
            'pegawai': forms.Select(
                attrs = attrs_input | {'class' : 'form-select', 'id': 'id_pegawai_id'}
            ),
            'sub_kegiatan': forms.Select(
                attrs = attrs_input | {'class' : 'form-select', 'id' : 'id_sub_kegiatan_id'}
            ),
            'role': forms.Select(
                attrs = attrs_input | {'class' : 'form-select',  'id' : 'id_role_id'}
            ),
        }

class RoleForm(forms.ModelForm):
    
    class Meta:

        model = models.RoleMitra
        fields = [
            'jabatan',
        ]

        labels = {
            'jabatan': 'Nama Jabatan'
        }

        attrs_input = {
            'class' : 'form-control',
            'required': 'required',
            'placeholder': '...'
        }

        widgets = {
            'jabatan': forms.TextInput(
                attrs = attrs_input
            ),
        }

class MasterPetugasFormUpload(forms.Form):
    import_file = forms.FileField(allow_empty_file=False, validators=[FileExtensionValidator(allowed_extensions=['xlsx'])], label="Import File Mitra", widget=forms.FileInput(
                    attrs={'class': "form-control"}))
    
    def clean(self):
        try:
            data = self.cleaned_data.get('import_file').read()
            df = pd.read_excel(BytesIO(data), skiprows=1, usecols='A:R', dtype='str')
            headers = utils.get_verbose_fields(models.MasterPetugas, exclude_pk=True)
            headers = ['No'] + headers
        except:
            self._errors['import_file'] = self.error_class(['Format template tidak sesuai. Silahkan gunakan template yang telah disediakan.'])
            return self._errors['import_file']

        df.dropna(axis=0, how='all', inplace=True)

        if [str(x).lower() for x in df.columns] != [str(x).lower() for x in headers]:
            self._errors['import_file'] = self.error_class(['Format template tidak sesuai. Silahkan gunakan template yang telah disediakan.'])
            return self._errors['import_file']
            
        # Validate Non Values
        base_errors = []
        df.columns = headers
        df.drop(columns=df.columns[0], axis=1, inplace=True)

        df_required = df.drop(['NPWP', 'Jenis Bank', 'Nomor Rekening', 'Pemilik Rekening'], axis=1)
        df_null = df_required[df_required.isna().any(axis=1)]
        for idx, i in df_null.iterrows():
            null_cols = ', '.join(str(e).capitalize() for e in i[i.isna()].index)
            base_errors.append(f'Nilai kosong pada <b>Baris {idx+1}</b> ditemukan. Periksa kolom <b>({null_cols})</b>')
        
        # Validasi untuk  Categoric value
        # Get option choices
        adm = models.AdministrativeModel.objects.values_list('code', flat=True)
        for idx, row in df['Kode Desa'].items():
            if len(row.split(']')) == 2:
                code = row.split(']')[0].replace('[', '')
                if code in adm:
                    df.loc[idx, 'Kode Desa'] = code
                    continue
            base_errors.append(f'<b>Kode Desa</b> Kode Desa tidak ditemukan pada database. Harap periksa baris <b>{idx+1}</b>')

        choices_status = dict(models.MasterPetugas._meta.get_field('status').choices)
        for idx, row in df['Status Mitra'].items():
            if row not in choices_status.values():
                base_errors.append(f'<b>Status Mitra</b> hanya dapat diisi {", ".join(choices_status.values())}. Harap periksa baris <b>{idx+1}</b>')
        df['Status Mitra'] = df['Status Mitra'].replace(list(choices_status.values()), list(choices_status.keys()))

        choices_jk = dict(models.MasterPetugas._meta.get_field('jk').choices)
        for idx, row in df['Jenis Kelamin'].items():
            if row not in choices_jk.values():
                base_errors.append(f'<b>Jenis Kelamin</b> hanya dapat diisi {", ".join(choices_jk.values())}. Harap periksa baris <b>{idx+1}</b>')
        df['Jenis Kelamin'] = df['Jenis Kelamin'].replace(list(choices_jk.values()), list(choices_jk.keys()))

        choices_pendidikan = dict(models.MasterPetugas._meta.get_field('pendidikan').choices)
        for idx, row in df['Pendidikan Terakhir'].items():
            if row not in choices_pendidikan.values():
                base_errors.append(f'<b>Pendidikan Terakhir</b> hanya dapat diisi {", ".join(choices_pendidikan.values())}. Harap periksa baris <b>{idx+1}</b>')
        df['Pendidikan Terakhir'] = df['Pendidikan Terakhir'].replace(list(choices_pendidikan.values()), list(choices_pendidikan.keys()))

        choices_agama = dict(models.MasterPetugas._meta.get_field('agama').choices)
        for idx, row in df['Agama'].items():
            if row not in choices_agama.values():
                base_errors.append(f'<b>Agama</b> hanya dapat diisi {", ".join(choices_agama.values())}. Harap periksa baris <b>{idx+1}</b>')
        df['Agama'] = df['Agama'].replace(list(choices_agama.values()), list(choices_agama.keys()))
        
        choices_bank = dict(models.MasterPetugas._meta.get_field('bank').choices)
        choices_bank_err = False
        for idx, row in df['Jenis Bank'].items():
            if pd.isna(row) is False:
                if row not in choices_bank.values():
                    base_errors.append(f'<b>Jenis Bank</b> hanya dapat diisi {", ".join(choices_bank.values())}. Harap periksa baris <b>{idx+1}</b>')
                    choices_bank_err = True
                    
        if choices_bank_err is False:
            df['Jenis Bank'] = df['Jenis Bank'].replace(list(choices_bank.values()), list(choices_bank.keys()))

        df['Tanggal Lahir'] = pd.to_datetime(df['Tanggal Lahir'], format='%d/%m/%Y')

        # Insert coloumn id to dataframe
        df.insert(loc=0, column='id', value='')

        # Convert verbose name as header of table to field_name
        field_names = utils.get_name_fields(models.MasterPetugas, exclude_pk = False)
        df.columns = field_names

        # Cek duplikasi Data pada master file
        duplicated_petugas = df[df.duplicated('kode_petugas')].kode_petugas
        for idx, row in duplicated_petugas.items():
            base_errors.append(f'Duplikasi Kode Petugas: <b>{row}</b> ditemukan. Harap periksa baris <b>{idx+1}</b>')
        
        duplicated_nik = df[df.duplicated('nik')].nik
        for idx, row in duplicated_nik.items():
            base_errors.append(f'Duplikasi NIK: <b>{row}</b> ditemukan. Harap periksa baris <b>{idx+1}</b>')
        
        duplicated_npwp = df[df.duplicated('npwp')].npwp
        for idx, row in duplicated_npwp.items():
            base_errors.append(f'Duplikasi NPWP: <b>{row}</b> ditemukan. Harap periksa baris <b>{idx+1}</b>')
                
        duplicated_email = df[df.duplicated('email')].email
        for idx, row in duplicated_email.items():
            base_errors.append(f'Duplikasi Email: <b>{row}</b> ditemukan. Harap periksa baris <b>{idx+1}</b>')
        
        duplicated_rekening = df[df.duplicated('rekening')].rekening
        for idx, row in duplicated_rekening.items():
            base_errors.append(f'Duplikasi Rekening: <b>{row}</b> ditemukan. Harap periksa baris <b>{idx+1}</b>')

        # Cek duplikasi Data pada Database
        dt_petugas_sort = {
            'kode_petugas' : [],
            'nik' : [],
            'npwp' : [],
            'email' : [],
            'rekening' : [],
        }

        db_petugas = models.MasterPetugas.objects.values_list('kode_petugas', 'nik', 'npwp', 'email', 'rekening')
        for dt in list(db_petugas):
            dt_petugas_sort['kode_petugas'].append(dt[0])
            dt_petugas_sort['nik'].append(dt[1])
            dt_petugas_sort['npwp'].append(dt[2])
            dt_petugas_sort['email'].append(dt[3])
            dt_petugas_sort['rekening'].append(dt[4])

        for idx, row in df['kode_petugas'].items():
            if row in dt_petugas_sort['kode_petugas']:
                base_errors.append(f'<b>Kode Petugas: [{row}]</b> telah tersedia pada database. Harap periksa baris <b>{idx+1}</b>')
      
        for idx, row in df['nik'].items():
            if row in dt_petugas_sort['nik']:
                base_errors.append(f'<b>NIK Petugas: [{row}]</b> telah tersedia pada database. Harap periksa baris <b>{idx+1}</b>')
      
        for idx, row in df['npwp'].items():
            if row in dt_petugas_sort['npwp']:
                base_errors.append(f'<b>NPWP Petugas: [{row}]</b> telah tersedia pada database. Harap periksa baris <b>{idx+1}</b>')
        
        for idx, row in df['email'].items():
            if row in dt_petugas_sort['email']:
                base_errors.append(f'<b>Email petugas: [{row}]</b> telah tersedia pada database. Harap periksa baris <b>{idx+1}</b>')
      
        for idx, row in df['rekening'].items():
            if row in dt_petugas_sort['rekening']:
                base_errors.append(f'<b>Rekening petugas: [{row}]</b> telah tersedia pada database. Harap periksa baris <b>{idx+1}</b>')

        if len(base_errors) > 0:
            self._errors['import_file'] = self.error_class(base_errors)
            return self._errors['import_file'] 

        for col in ['npwp', 'bank', 'rekening', 'pemilik_rek']:
            df[col] = df[col].fillna('')

        for column in df.columns:
            if column in ['jk', 'pendidikan', 'agama', 'status', 'bank', models.MasterPetugas._meta.pk.name]:
                continue
            
            obj_field = models.MasterPetugas._meta.get_field(column)
            max_field = obj_field.max_length
            vname_field = obj_field.verbose_name
            
            index = df[df[column].astype(str).str.len() > max_field].index.tolist()
            rows = [idx+1 for idx in index]

            if len(rows) > 0:
                msg = f'Kesalahan pada kolom {vname_field}<ul>'
                for row in rows:
                    msg += f'<li>Kolom {vname_field} pada baris {row} memiliki panjang lebih dari {max_field} karakter</li>'
                msg += '</ul>'
                base_errors.append(msg)
       
        if len(base_errors) > 0:
            self._errors['import_file'] = self.error_class(base_errors)
            return self._errors['import_file'] 
        
        self.cleaned_data = df.to_dict()

        return self.cleaned_data

class AlokasiPetugasFormUpload(forms.Form):
    import_file = forms.FileField(allow_empty_file=False,validators=[FileExtensionValidator(allowed_extensions=['xlsx'])], label="Import Alokasi Petugas", widget=forms.FileInput(
                              attrs={'class': "form-control"}))
    
    def clean(self):
        def check_db(dataframe, col, data_list, base_errors):
            for idx, row in dataframe[col].items():
                if pd.isna(row) is False:
                    id = [dt[1] for dt in data_list if dt[0] == row]
                    if len(id) > 0 :
                        dataframe.loc[idx, col] = id[0]
                    else:
                        base_errors.append(f'<b>{col} [{row}]</b> tidak tersedia pada database. Harap periksa baris <b>{idx+1}</b>')

            return dataframe
        
        try:
            data = self.cleaned_data.get('import_file').read()
            df = pd.read_excel(BytesIO(data), skiprows=1, usecols='A:E', dtype='str')
            df.dropna(axis=0, how='all', inplace=True)
        except:
            self._errors['import_file'] = self.error_class(['Format template tidak sesuai. Silahkan gunakan template yang telah disediakan.'])
            return self._errors['import_file']

        headers = utils.get_verbose_fields(models.AlokasiPetugas, exclude_pk=True)
        headers = ['No'] + headers

        if [str(x).lower() for x in df.columns] != [str(x).lower() for x in headers]:
            self._errors['import_file'] = self.error_class(['Format template tidak sesuai. Silahkan gunakan template yang telah disediakan.'])
            return self._errors['import_file']
            
        # Validate Non Values
        base_errors = []
        df.columns = headers
        df.drop(columns=df.columns[0], axis=1, inplace=True)

        df_null = df[df.isna().any(axis=1)]
        for idx, rows in df_null.iterrows():
            null_cols = [e for e in rows[rows.isna()].index]
            if 'Pegawai (Organik)' in null_cols and 'Petugas (Mitra)' in null_cols:
                base_errors.append(f'Kolom "Pegawai (Organik)" atau "Petugas (Mitra)" salah satunya tidak boleh kosong. Harap periksa <b>Baris {idx+1}</b>.')
            else:
                for col in ['Pegawai (Organik)', 'Petugas (Mitra)']:
                    if col in null_cols:
                        null_cols.remove(col)

                if len(null_cols) > 0:
                    str_cols = ', '.join(null_cols)
                    base_errors.append(f'Nilai kosong pada <b>Baris {idx+1}</b> ditemukan. Periksa kolom <b>({str_cols})</b>')
        
        for idx, row in df['Petugas (Mitra)'].items():
            if pd.isna(row) is False:
                if len(row.split(']')) == 2:
                    code = row.split(']')[0].replace('[', '')
                    df.loc[idx, 'Petugas (Mitra)'] = code

        for idx, row in df['Pegawai (Organik)'].items():
            if pd.isna(row) is False:
                if len(row.split(']')) == 2:
                    code = row.split(']')[0].replace('[', '')
                    df.loc[idx, 'Pegawai (Organik)'] = code

        # Validasi untuk non numerik value
        # Get option choices
        data_pegawai = list(MasterPegawaiModel.objects.values_list('nip', 'id'))
        data_mitra = list(models.MasterPetugas.objects.filter(~Q(status = 1), ~Q(status = 3)).values_list('kode_petugas', 'id'))
        data_survei = list(SubKegiatanSurvei.objects.values_list('nama_kegiatan', 'id'))
        data_role = list(models.RoleMitra.objects.values_list('jabatan', 'id'))

        check_db(df, 'Pegawai (Organik)', data_pegawai, base_errors)
        check_db(df, 'Petugas (Mitra)', data_mitra, base_errors)
        check_db(df, 'Kegiatan Survei', data_survei, base_errors)  
        check_db(df, 'Jabatan Petugas', data_role, base_errors)
        
        # Insert coloumn id to dataframe
        df.insert(loc=0, column='id', value='')

        # Convert verbose name as header of table to field_name
        field_names = utils.get_name_fields(models.AlokasiPetugas, exclude_pk = False)
        df.columns = field_names

        # Cek duplikasi Data pada master file    
        duplicated_petugas = df[df.duplicated()].petugas
        for idx, row in duplicated_petugas.items():
            if pd.isna(row) is False:
                base_errors.append(f'Duplikasi Petugas (Mitra): <b>{row}</b> dengan beban tugas yang sama ditemukan. Harap periksa baris <b>{idx+1}</b>')
        
        duplicated_pegawai = df[df.duplicated()].pegawai
        for idx, row in duplicated_pegawai.items():
            if pd.isna(row) is False:
                base_errors.append(f'Duplikasi pegawai (organik): <b>{row}</b> dengan beban tugas yang sama ditemukan. Harap periksa baris <b>{idx+1}</b>')

        if len(base_errors) > 0:
            self._errors['import_file'] = self.error_class(base_errors)
            return self._errors['import_file'] 
        
        # Cek duplikasi Data pada database
        for idx, row in df.iterrows():
            check_exist_data = models.AlokasiPetugas.objects.filter(sub_kegiatan = row['sub_kegiatan'])
            check_exist_data = check_exist_data.filter(pegawai = row['pegawai']) if pd.isna(row['petugas']) else check_exist_data.filter(petugas = row['petugas'])
            if check_exist_data.exists():
                exist_data = check_exist_data.first()
                duplicate_str = f'Data Petugas (Mitra): <b>[{exist_data.petugas.kode_petugas}] {exist_data.petugas.nama_petugas}' if pd.isna(row['pegawai']) else f'Data Pegawi (Organik): <b>[{exist_data.pegawai.nip}] {exist_data.pegawai.name}'
                base_errors.append(f'{duplicate_str} | {exist_data.sub_kegiatan.nama_kegiatan} sebagai {exist_data.role.jabatan}</b> dengan beban tugas yang sama telah tersedia pada database. Harap periksa baris <b>{idx+1}</b>')

        if len(base_errors) > 0:
            self._errors['import_file'] = self.error_class(base_errors)
            return self._errors['import_file'] 
        
        self.cleaned_data = df.to_dict()
        return self.cleaned_data
    