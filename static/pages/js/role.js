let generate_role_petugas = (url, csrf) => {
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
            lengthMenu: [5, 25, 50, 100,'All'],
            columns :[
                {"data": 'jabatan'},
                {"data": 'jabatan'},
                {"data" : 'aksi'},
            ], 
            columnDefs: [
                {
                'targets': [2], /* column index */
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
                }
            ],
        }, ...settingDatatables()
    }
);
}

let edit_role = (url, csrf, target_url, e) => {
    $('#formRolePetugas').attr('action', target_url)
    $('#submitformRolePetugas').html('Update Data')
    
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
            }else{
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

let form_submit = (csrf) => {
    var serializedData = $('#formRolePetugas').serialize();
    $('.invalid-feedback').html('')
    $('.is_invalid').removeClass('is_invalid')
    
    $.ajax({
        url: $('#formRolePetugas').attr('action'),
        type: 'POST',
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
            resetForm()
            table.ajax.reload();

            $('.nav-tabs a[href="#rolepetugas-preview"]').tab('show');
        },
        error: (response) => {
            var errors = response["responseJSON"]["error"]
            for (const [key, value] of Object.entries(errors)) {
                var msgs = '<ul>'
                value.forEach((item, index)  => {
                    msgs += '<li>'+item+'</li>'
                    });
                msgs += '</ul>'
                $('#id_'+ key).addClass('is-invalid');
                $('#msg-id_'+key).html(msgs)
            }    
            
        }
    })
}

let resetFormTarget = (url) => {
    $('#formRolePetugas')[0].reset();
    $('.was-validated').removeClass('was-validated')
    $('#submitformRolePetugas').html('Kirim Data')
    $('#formRolePetugas').attr('action', url)
}

$('#redraw-table').on('click', () => {
    table.draw();
})

$('#ResetformRolePetugas').on('click', (e) => {
    resetForm()
})