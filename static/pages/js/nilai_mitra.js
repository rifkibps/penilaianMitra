var region_code = ''

let destroy_datatable = () => {
    if ( $.fn.DataTable.isDataTable('#basic-datatable-2') ) {
        $('#basic-datatable-2').DataTable().destroy();
    }
    
    var thead_def = `<tr>
            <th>ID Mitra</th>
            <th>Kec.</th>
            <th>Mitra</th>
            <th>Jabatan</th>
            <th>Kegiatan Penilaian</th>
            <th>Penilaian Indikator</th>
        </tr>`
      
    var tbody_def = `<tr class="text-center">
            <td colspan="6">Silahkan Pilih Kegiatan Survei dan Penilaian</td>
        </tr>`

    $('#basic-datatable-2 thead').html(thead_def);
    $('#basic-datatable-2 tbody').html(tbody_def);
}

let generate_master_penilaian = (url, csrf) => {
    return $("#basic-datatable").DataTable(
    {
        ...{
            processing: true,
            serverSide: true,
            ajax: {
                "url": url,
                "headers": {
                    "X-Requested-With": "XMLHttpRequest",
                    "X-CSRFToken": csrf,
                },
                "data": (d) => {
                    return $.extend({}, d, {
                        "role_filter": $('#role-select-filter').val(),
                        "survei_filter": $('#survei-select-filter').val(),
                        "kegiatan_filter": $('#kegiatan-select-filter').val(),
                        "mitra_filter": $('#mitra-select-filter').val(),
                        "pegawai_filter": $('#pegawai-select-filter').val(),
                        "region_code" : region_code
                    })
                },
                "type": "POST"
            },
            columns :[
                {"data": 'petugas__petugas__nama_petugas'},
                {"data": 'petugas__petugas__adm_id__region'},
                {"data": 'petugas__petugas__nama_petugas'},
                {"data": 'petugas__role__jabatan'},
                {"data" : 'detail_nilai__indikator_penilaian__kegiatan_penilaian__kegiatan_survey__nama_kegiatan'},
                {"data" : 'detail_nilai__indikator_penilaian__indikator_penilaian__nama_indikator'},
                {"data" : 'detail_nilai__nilai'},
                {"data" : 'detail_nilai__catatan'},
                {"data" : 'penilai__pegawai__name'},
            ],
            columnDefs: [
            {
                "targets": 0,
                "data": null,
                "defaultContent": "",
                "render": (data, type, row, meta) => {
                    return meta.row + 1;
                }
            }]
        }, ...settingDatatables()
    }
);
}

let edit_penilaian_request = (url, csrf, e) => {
    $.ajax({
        url: url,
        type: "POST",
        dataType: "json",
        data : {
            'id_penilaian' : e,
        },
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": csrf,
        },
        success: (data) => {
            if (data.status == 'success'){
                var opt_kegiatan = '<option value="">-- Pilih Kegiatan --</option><option value="'+ data.data_kegiatan.id +'" selected>'+data.data_kegiatan.kegiatan_survey__nama_kegiatan + '</option>'
                var opt_mitra = '<option value="">-- Pilih Petugas --</option><option value="'+ data.data_mitra.id +'" selected>['+data.data_mitra.petugas__kode_petugas + '] '+ data.data_mitra.petugas__nama_petugas+' | ' +data.data_mitra.role__jabatan + '</option>'
                var opt_penilai = '<option value="">-- Pilih Penilai --</option><option value="'+ data.data_penilai.id +'" selected>['+data.data_penilai.pegawai__nip + '] '+ data.data_penilai.pegawai__name+' | ' +data.data_penilai.role__jabatan + '</option>'
                $('#field_mitra').html(opt_mitra)
                $('#field_penilai').html(opt_penilai)
                $('#field_kegiatan').html(opt_kegiatan)
                $('#field_survey').val(data.data_mitra.sub_kegiatan__survey__id)
                
                var tbody_rows = ''
                if(data.nilai_mitra.length > 0){
                    for (let i = 0; i < data.nilai_mitra.length; i++) {
                        tbody_rows += `<tr>
                            <td>`+(i+1)+`.</td>
                            <td>`+data.nilai_mitra[i]['detail_nilai__indikator_penilaian__indikator_penilaian__nama_indikator'] +`</td>
                            <td>
                                <input type="number" class="form-control d-inline" name="nilai_indikator_`+data.nilai_mitra[i]['detail_nilai__indikator_penilaian'] +`" placeholder="Isikan nilai" alt="Isikan nilai" min="`+data.nilai_mitra[i]['detail_nilai__indikator_penilaian__n_min'] +`" max="`+data.nilai_mitra[i]['detail_nilai__indikator_penilaian__n_max'] +`" onkeyup="if(this.value > `+data.nilai_mitra[i]['detail_nilai__indikator_penilaian__n_max'] +` || this.value < `+data.nilai_mitra[i]['detail_nilai__indikator_penilaian__n_min'] +`) this.value = null;" value="`+data.nilai_mitra[i]['detail_nilai__nilai'] +`">   
                            </td>
                            <td>
                                <textarea class="form-control" name="catatan_indikator_`+data.nilai_mitra[i]['detail_nilai__indikator_penilaian'] +`" cols="30" rows="5">`+data.nilai_mitra[i]['detail_nilai__catatan'] +`</textarea>
                            </td>
                        </tr>`
                    }
                }else{
                    tbody_rows = '<tr><td colspan="4" class="text-center">Kegiatan Penilaian Belum Memiliki Indiktor Penilaian/ Kegiatan sedang Tidak Aktif</td></tr>'
                }
                $('#form-indikator-nilai tbody').html(data.opt)
                $('.nav-tabs a[href="#input-tab"]').tab('show');
            }
        },
        error: (error) => {
            console.log(error);
        }
    });
}

let get_data_penilaian_by_survei = (data, field_target, url, csrf) => {
    $.ajax({
        url: url,
        type: "POST",   
        dataType: "json",
        data : data,
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": csrf,
        },
        success: (data) => {
            let option = '<option value="">-- Pilih Penilaian --</option>'
            for (let i = 0; i < data.instance.length; i++) {
                option += '<option value="'+ data.instance[i]['id'] +'">'+ data.instance[i]['kegiatan_survey__nama_kegiatan'] +'</option>'
            }
            $(field_target).html(option)
        },
        error: (error) => {
            console.log(error);
        }
    });
}

let preview_excel_nilai = (table_id, field_file_id) => {
    let input = $('#'+field_file_id).get(0).files[0]
    readXlsxFile(input).then((data) => {
        let i = 0
        $('#'+table_id+' tbody').html('') 
        data.map((row, index) =>{
            if (i==1){
                let throws = '<tr>'
                for (let key of row){
                    throws += '<th>' + key + '</th>'
                }
                throws += '</tr>'
                $('#'+table_id+' thead').html(throws) 
            }
            if (i>1){
                let tdrows = '<tr>'
                let isnull = 0
                for (let key of row){
                    if ( key == null ){
                        isnull += 1
                    }
                    tdrows += '<td>' + key + '</td>'
                }
                tdrows += '</tr>'
                if (isnull < data[1].length) {
                    $('#'+table_id+' tbody').append(tdrows) 
                }
            }
            i++
        })
        return true

    })
}

let ExportToExcel = (type, fn, dl) => {
    let elt = document.getElementById('basic-datatable-2');
    let wb = XLSX.utils.table_to_book(elt, { sheet: "Nilai Mitra" });
    return dl ?
        XLSX.write(wb, { bookType: type, bookSST: true, type: 'base64' }):
        XLSX.writeFile(wb, fn || ('Data Nilai Mitra per Indikator.' + (type || 'xlsx')));
}

let confirm_submit_file = (url, csrf, formDataTarget) => {
    swalWithBootstrapButtons.fire({
        title: 'Are you sure?',
        text: "Apakah anda yakin ingin mengupload data mitra?",
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: 'Yes, upload it!',
        cancelButtonText: 'No, cancel!',
        reverseButtons: true
      }).then((result) => {
        if (result.isConfirmed) {
            var data = new FormData();
            data.append("import_file",formDataTarget)
            $.ajax({
                url: url,
                type: "POST",   
                data: data,
                processData: false,
                contentType: false,
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                    "X-CSRFToken": csrf,
                },
                success: (response) =>  {
                    if (response.status == 'error'){
                        var content_msgs = '<strong>Terjadi kesalahan</strong> saat import data: <ol class="px-3 font-12">'
                        for (let i = 0; i < response.messages.length; i++) {
                            content_msgs += '<li>'+ response.messages[i] +'</li>'
                        }
                        
                        $('#messages-content').html(content_msgs)
                        $('#msgs-upload').removeClass('alert-success')
                        $('#msgs-upload').addClass('alert-danger')
                        $('#msgs-upload').removeClass('d-none')
                    }else{
                        var content_msgs = response.messages
                        
                        $('#messages-content').html(content_msgs)
                        $('#msgs-upload').removeClass('alert-danger')
                        $('#msgs-upload').addClass('alert-success')
                        $('#msgs-upload').removeClass('d-none')
                        table.ajax.reload();
                    }
                },
                error: (xhr, status, error) => {
                    return console.log(xhr.responseText['messages'])
                }
            })
        } else if (
          result.dismiss === Swal.DismissReason.cancel
        ) {
          swalWithBootstrapButtons.fire(
            'Cancelled',
            'Data successfully cancelled',
            'error'
          )
        }
    }) 
}

let filter_penilaian_by_survey = (url, csrf) => {
    var thead_def = `<tr>
        <th>ID Mitra</th>
        <th>Mitra</th>
        <th>Jabatan</th>
        <th>Kegiatan Penilaian</th>
        <th>Penilaian Indikator</th>
    </tr>`

    var tbody_def = `<tr class="text-center">
        <td colspan="6">Silahkan Pilih Kegiatan Survei dan Penilaian</td>
    </tr>`
    
    if ($('#nilai-mitra-filter-survey').val() == '') {
        if ( $.fn.DataTable.isDataTable('#basic-datatable-2') ) {
            $('#basic-datatable-2').DataTable().destroy();
        }
        $('#basic-datatable-2 thead').html(thead_def);
        $('#basic-datatable-2 tbody').html(tbody_def);
        $('#nilai-mitra-filter-kegiatan').html('<option value="">Pilih Penilaian</option>');
        return
    }

    var data = {'survey_id' : $('#nilai-mitra-filter-survey').val()}
    get_data_penilaian_by_survei(data, '#nilai-mitra-filter-kegiatan',  url, csrf)
}

let get_penilai_by_kegiatan = (url, csrf) => {
    if ($('#filter-kegiatan-template').val().length == 0) return false
    $('#filter-penilai-template').html('')
    $.ajax({
        url: url,
        type: "POST",   
        dataType: "json",
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": csrf,
        },
        data :  {
            'sub_kegiatan' : $('#filter-kegiatan-template').find(':selected').attr('data-subkegiatan'),
            'kegiatan_penilaian' : $('#filter-kegiatan-template').val(),
        },
        success: (response) => {
            if (response.status == 'success') $('#filter-penilai-template').html(response.data)
        },
        error: (error) => {
            console.log(error);
        }
    });
}

let resetForm = () => {
    $('#formPenilaianPetugas')[0].reset();
    $('.was-validated').removeClass('was-validated')
    $('#submitformPenilaianPetugas').html('Kirim Data')
    $('#form-indikator-nilai tbody').html('')
}

let select_mitra = (url, csrf) => {
    var id_petugas = $('#field_mitra').val()
    var id_penilai = $('#field_penilai').val()
    var id_kegiatan = $('#field_kegiatan').val()
    if (id_petugas.length == 0 || id_penilai.length == 0 || id_kegiatan.length == 0) return false

    $.ajax({
        url: url,
        type: "POST",   
        dataType: "json",
        data :  {'id_petugas' : id_petugas, 'id_penilai' : id_penilai, 'id_kegiatan' : id_kegiatan},
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": csrf,
        },
        success: (data) => {
            var tbody_rows = ''
            if(data.nilai_mitra.length > 0){
                for (let i = 0; i < data.nilai_mitra.length; i++) {
                    tbody_rows += `<tr>
                        <td>`+(i+1)+`.</td>
                        <td>`+data.nilai_mitra[i]['detail_nilai__indikator_penilaian__indikator_penilaian__nama_indikator'] +`</td>
                        <td>
                            <input type="number" class="form-control d-inline" name="nilai_indikator_`+data.nilai_mitra[i]['detail_nilai__indikator_penilaian'] +`" placeholder="Isikan nilai" alt="Isikan nilai" min="`+data.nilai_mitra[i]['detail_nilai__indikator_penilaian__n_min'] +`" max="`+data.nilai_mitra[i]['detail_nilai__indikator_penilaian__n_max'] +`" onkeyup="if(this.value > `+data.nilai_mitra[i]['detail_nilai__indikator_penilaian__n_max'] +` || this.value < `+data.nilai_mitra[i]['detail_nilai__indikator_penilaian__n_min'] +`) this.value = null;" value="`+data.nilai_mitra[i]['detail_nilai__nilai'] +`">   
                        </td>
                        <td>
                            <textarea class="form-control" name="catatan_indikator_`+data.nilai_mitra[i]['detail_nilai__indikator_penilaian'] +`" cols="30" rows="5">`+data.nilai_mitra[i]['detail_nilai__catatan'] +`</textarea>
                        </td>
                    </tr>`
                }
            }else{
                tbody_rows = '<tr><td colspan="4" class="text-center">Kegiatan Penilaian Belum Memiliki Indiktor Penilaian/ Kegiatan sedang Tidak Aktif</td></tr>'
            }
            $('#form-indikator-nilai tbody').html(data.opt)
        },
        error: (error) => {
            console.log(error);
        }
    });

}

let get_alocation_by_survey = (url, csrf) => {
    $.ajax({
        url: url,
        type: "POST",   
        dataType: "json",
        data :  {'survey_id' : $('#field_survey').val(), 'penilaian_id' : $(this).val()},
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": csrf,
        },
        success: (data) => {
            var opt_mitra = '<option value="">-- Pilih Petugas --</option>'
            var opt_penilai = '<option value="">-- Pilih Penilai --</option>'
            for (let i = 0; i < data.instance.length; i++) {
                opt_mitra += '<option value="'+ data.instance[i]['id'] +'">['+ data.instance[i]['petugas__kode_petugas'] +'] '+ data.instance[i]['petugas__nama_petugas'] + ' | ' + data.instance[i]['role__jabatan']  + ' </option>'
            }
            for (let i = 0; i < data.instance_2.length; i++) {
                opt_penilai += '<option value="'+ data.instance_2[i]['id'] +'">['+ data.instance_2[i]['pegawai__nip'] +'] '+ data.instance_2[i]['pegawai__name'] + ' | ' + data.instance_2[i]['role__jabatan']  + ' </option>'
            }
            $('#field_mitra').html(opt_mitra)
            $('#field_penilai').html(opt_penilai)
        },
        error: (error) => {
            console.log(error);
        }
    });
}

let get_template_upload = (url) => {
    if ($('#filter-kegiatan-template').val().length == 0 || $('#filter-penilai-template').val().length == 0) return false
    let kegiatan = $('#filter-kegiatan-template').val()
    let penilai = $('#filter-penilai-template').val()
    return window.location.replace(url + "?kegiatan=" + kegiatan + "&penilai=" + penilai);
}

$('#formPenilaianPetugas').on('submit', (e) => {
    e.preventDefault()
    let serializedData = $(this).serialize();
    $.ajax({
        type: 'POST',
        url: $(this).attr('action'),
        data: serializedData,
        success: (response) =>  {
            if (response.status == 'success'){
                $('#messages-content').html(response.messages)
                $('#msgs-upload').removeClass('alert-danger')
                $('#msgs-upload').addClass('alert-success')
                $('#msgs-upload').removeClass('d-none')
                
            }else{
                Swal.fire(
                    'Terjadi Kesalahan!',
                    response.messages,
                    'info'
                )
            }
            
            table.ajax.reload();
        },
        error: (response) =>  {
            var errors = response["responseJSON"]["error"]
            var msgs = '<ul>'
            for (const [key, value] of Object.entries(errors)) {
                value.forEach((item, index) => {
                    msgs += '<li>'+item+'</li>'
                });
            }   
            msgs += '</ul>'
            $('#messages-content').html(msgs)
            $('#msgs-upload').addClass('alert-danger')
            $('#msgs-upload').removeClass('alert-success')
            $('#msgs-upload').removeClass('d-none')
        }
    })
})

$('#mitra-select-filter, #pegawai-select-filter, #kegiatan-select-filter, #survei-select-filter, #role-select-filter').bind("keyup change", () =>{
    table.draw()
})

$('#reset-filter').on('click', () => {
    region_code = ''
    $('#mitra-select-filter, #pegawai-select-filter, #kegiatan-select-filter, #survei-select-filter, #role-select-filter, .region-adm').prop('selectedIndex',0);
    reset_administrative(true)
    table.draw();
})

$('#reset-filter-2').on('click', () =>{
    $('#role-select-filter-2').prop('selectedIndex',0);
    get_data_tables_nilai({
        'kegiatan_penilaian' : $('#nilai-mitra-filter-kegiatan').val()
    })
})

$('#btn-submit-file').on('click', () => {
    $('#nav-item-import').removeClass('d-none')
    $('#import-modal').modal('toggle')
    $('.nav-tabs a[href="#import-tab"]').tab('show');
})

$('#nilai-mitra-filter-kegiatan').on("change", () => {
    get_data_tables_nilai({
        'kegiatan_penilaian' : $('#nilai-mitra-filter-kegiatan').val()
    })
})

$('#redraw-table').on('click', () =>{
    table.draw();
})

$('#redraw-table-2').on('click', () =>{
    get_data_tables_nilai({
        'kegiatan_penilaian' : $('#nilai-mitra-filter-kegiatan').val()
    })
})

$('#ResetformPenilaianPetugas').on('click', (e) => {
    resetForm()
    $('#field_mitra').val('')
    $('#field_penilai').val('')
    $('#field_kegiatan').val('')
})

$('#role-select-filter-2').on('change', () => {
    get_data_tables_nilai({
        'kegiatan_penilaian' : $('#nilai-mitra-filter-kegiatan').val(),
        'filter_role_nilai_mitra' : $(this).val()
    })
})

