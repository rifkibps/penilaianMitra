let generate_indikator_kegiatan_penilaian = (url, csrf) => {
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
                        "kegiatan_filter": $('#kegiatan-select-filter').val(),
                        "indikator_filter": $('#indikator-select-filter').val(),
                    })
                },
                "type": "POST"
            },
            columns :[
                {"data": 'kegiatan_penilaian__kegiatan_survey__nama_kegiatan'},
                {"data": 'kegiatan_penilaian__kegiatan_survey__nama_kegiatan'},
                {"data": 'indikator_penilaian__nama_indikator'},
                {"data": 'scale'},
                {"data" : 'aksi'},
            ],
            lengthMenu: [5, 25, 50, 100,'All'],
            columnDefs: [ {
                'targets': [4], /* column index */
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

let edit_indikator_kegiatan_request = (url, csrf, target_url, e) => {
        $('#formKegiatanIndikatorPenilaianPetugas').attr('action', target_url)
        $('#submitformIndikatorKegiatanPenilaianPetugas').html('Update Data')

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
                if (data.status == 'failed'){
                    Swal.fire(
                        'Terjadi Kesalahan!',
                         data.message,
                        'info'
                    )
                } else {
                    for (const [key, value] of Object.entries(data.instance)) {
                        $('#id_'+key).val(value)
                    }
                    $('.nav-tabs a[href="#input-tab"]').tab('show');
                    table.ajax.reload();
                }

            },
            error: (error) => {
                console.log(error);
            }
        });
}

let check_submit = (csrf) => {
    clearFormValidation('#formKegiatanIndikatorPenilaianPetugas')
    let serializedData = $('#formKegiatanIndikatorPenilaianPetugas').serialize();

    $('.invalid-feedback').html('')
    $('.is_invalid').removeClass('is_invalid')
    $.ajax({
        type: 'POST',
        url: $('#formKegiatanIndikatorPenilaianPetugas').attr('action'),
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
                $('#messages-content').html(response.message)
                $('#msgs-upload').removeClass('alert-danger')
                $('#msgs-upload').addClass('alert-success')
                $('#msgs-upload').removeClass('d-none')
                table.ajax.reload();
                $('.nav-tabs a[href="#indikator-penilaian-preview"]').tab('show');
                $('#formKegiatanIndikatorPenilaianPetugas')[0].reset();
                clearFormValidation('#formKegiatanIndikatorPenilaianPetugas')
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

let resetFormIndikatorPenilaianParent = (url) => {
    $('#formKegiatanIndikatorPenilaianPetugas')[0].reset();
    $('.was-validated').removeClass('was-validated')
    $('#submitformIndikatorKegiatanPenilaianPetugas').html('Kirim Data')
    $('#formKegiatanIndikatorPenilaianPetugas').attr('action', url)
}

$('#kegiatan-select-filter').bind("keyup change", () => {
    table.draw()
})

$('#indikator-select-filter').bind("keyup change", () => {
    table.draw()
})

$('#ResetformIndikatorKegiatanPenilaianPetugas').on('click', (e) => {
    resetForm()
})

$('#reset-filter').on('click', () => {
    $('#kegiatan-select-filter').prop('selectedIndex',0);
    $('#indikator-select-filter').prop('selectedIndex',0);
    table.draw();
})

$('#redraw-table').on('click', () => {
    table.draw();
})