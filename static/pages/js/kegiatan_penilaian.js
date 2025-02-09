// KEGIATAN PENILAIAN
let generate_kegiatan_penilaian = (url, csrf) => {
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
                            "survei_filter": $('#survei-select-filter').val(),
                            "status_filter": $('#status-select-filter').val(),
                            "role_filter": $('#role-select-filter').val(),
                        })
                    },
                    "type": "POST"
                },
                columns :[
                    {"data": 'kegiatan_survey__nama_kegiatan'},
                    {"data": 'kegiatan_survey__nama_kegiatan'},
                    {"data" : 'tgl_penilaian'},
                    {"data": 'role_permitted__jabatan'},
                    {"data": 'role_penilai_permitted__jabatan'},
                    {"data" : 'status'},
                    {"data" : 'aksi'},
                ],
                lengthMenu: [5, 25, 50, 100,'All'],
                columnDefs: [ {
                    'targets': [6], /* column index */
                    'orderable': false, /* true or false */
                    'className': "text-center"
                },
                {
                    "targets": 0,
                    "data": null,
                    "defaultContent": "",
                    "render": (data, type, row, meta) => {
                        return meta.row + 1;
                    }
                }],
                }, ...settingDatatables()
        }
    );
}

let editKegiatanPenilaian = (url, csrf, target_url, e) => {
    $('#submitformKegiatanPenilaianPetugas').html('Update Data')
    $('#formKegiatanPenilaianPetugas').attr('action', target_url)
    $.ajax({
        url: url,
        type: "POST",
        dataType: "json",
        data : {
            'id' : e
        },
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": csrf,
        },
        success: (data) => {
            for (const [key, value] of Object.entries(data.instance)) {
                $('#id_'+key).val(value)
                if (key == 'role_permitted'){
                    $('#id_'+key).val(value)
                }
            }
            $('.nav-tabs a[href="#input-tab"]').tab('show');
            table.ajax.reload();
        },
        error: (error) => {
            console.log(error);
        }
    });
}

let check_submit_kegiatan_penilaian = (csrf) => {
    clearFormValidation('#formKegiatanPenilaianPetugas')
    let serializedData = $('#formKegiatanPenilaianPetugas').serialize();

    $('.invalid-feedback').html('')
    $('.is_invalid').removeClass('is_invalid')

    $.ajax({
        type: 'POST',
        url: $('#formKegiatanPenilaianPetugas').attr('action'),
        data: serializedData,
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": csrf,
        },
        success: (response) => {
            if (response.status == 'failed'){
                Swal.fire(
                    'Terjadi Kesalahan!',
                    response.message,
                    'info'
                )
            }else{
                $('#messages-content').html(response["message"])
                $('#msgs-upload').removeClass('alert-danger')
                $('#msgs-upload').addClass('alert-success')
                $('#msgs-upload').removeClass('d-none')
                table.ajax.reload();
                resetForm()
                clearFormValidation('#formKegiatanPenilaianPetugas')
                $('.nav-tabs a[href="#kegiatan-penilaian-preview"]').tab('show');
            }
        },
        error: (response) => {
            var errors = response["responseJSON"]["error"]
            for (const [key, value] of Object.entries(errors)) {
                var msgs = '<ul>'
                value.forEach((item, index) => {
                    msgs += '<li>'+item+'</li>'
                    });
                msgs += '</ul>'
                $('#id_'+ key).addClass('is-invalid');
                $('#msg-id_'+key).html(msgs)
            }    
        }
    })
}

let resetFormKegiatanPenilain = (url) => {
    $('#formKegiatanPenilaianPetugas')[0].reset();
    $('.was-validated').removeClass('was-validated')
    $('#submitformKegiatanPenilaianPetugas').html('Kirim Data')
    $('#formKegiatanPenilaianPetugas').attr('action', url)
}

$('#survei-select-filter').bind("keyup change", () => {
    table.draw()
})

$('#status-select-filter').bind("keyup change", () => {
    table.draw()
})

$('#role-select-filter').bind("keyup change", () => {
    table.draw()
})

$('#reset-filter').on('click', () => {
    $('#survei-select-filter').prop('selectedIndex',0);
    $('#status-select-filter').prop('selectedIndex',0);
    $('#role-select-filter').prop('selectedIndex',0);
    table.draw();
})

$('#redraw-table').on('click', () => {
    table.draw();
})

$('#ResetformKegiatanPenilaianPetugas').on('click', (e) => {
    resetForm()
})


// INDIKATOR KEGIATAN PENILAIAN





