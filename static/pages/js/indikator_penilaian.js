let generate_indikator_penilaian = (url, csrf) => {
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
                "type": "POST"
            },
            columns :[
                {"data": 'nama_indikator'},
                {"data": 'nama_indikator'},
                {"data": 'deskripsi_penilaian'},
                {"data" : 'aksi'},
            ],
            lengthMenu: [5, 25, 50, 100, 250],
            columnDefs: [ {
                'targets': [3], /* column index */
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

let edit_indikator = (url, csrf, target_url, e) => {
    $('#formKegiatanPenilaianPetugas').attr('action', target_url)
    $('#submitformIndikatorPenilaianPetugas').html('Update Data')

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
            if (data.status == 'success'){
                for (const [key, value] of Object.entries(data.instance)) {
                    $('#id_'+key).val(value)
                }
                $('.nav-tabs a[href="#input-tab"]').tab('show');
                table.ajax.reload();
            }else{
                Swal.fire(
                    'Terjadi Kesalahan!',
                     data.message,
                    'info'
                )
            }
            
        },
        error: (error) => {
            console.log(error);
        }
    });
}

let check_submit = (csrf) => {
    clearFormValidation('#formKegiatanPenilaianPetugas')
    var serializedData = $('#formKegiatanPenilaianPetugas').serialize();
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
            $('#messages-content').html(response["message"])
            $('#msgs-upload').removeClass('alert-danger')
            $('#msgs-upload').addClass('alert-success')
            $('#msgs-upload').removeClass('d-none')
            table.ajax.reload();
            $('.nav-tabs a[href="#indikator-penilaian-preview"]').tab('show');
            $('#formKegiatanPenilaianPetugas')[0].reset();
            clearFormValidation('#formKegiatanPenilaianPetugas')
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

let resetFormIndikatorPenilaian = (url) => {
    $('#formKegiatanPenilaianPetugas')[0].reset();
    $('.was-validated').removeClass('was-validated')
    $('#submitformIndikatorPenilaianPetugas').html('Kirim Data')
    $('#formKegiatanPenilaianPetugas').attr('action', url)
}

$('#ResetformIndikatorPenilaianPetugas').on('click', (e) => {
    resetForm()
})
