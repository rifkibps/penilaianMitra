let generate_kegiatan_survey = (url, csrf) => {
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
                "type": "POST",
                "data": (d) => {
                    return $.extend({}, d, {
                        "state_filter": $('#status-select-filter').val(),
                    })
                },
            },
            columns :[
                {"data": 'nama_kegiatan'},
                {"data": 'nama_kegiatan'},
                {"data" : 'survey__nama'},
                {"data":  'survey__tgl_mulai'},
                {"data":  'status'},
                {"data" : 'aksi'},
            ],
            lengthMenu: [5, 25, 50, 100,'All'],
            columnDefs: [ {
                'targets': [5], /* column index */
                'orderable': false, /* true or false */
            }, {
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

let edit_kegiatan_request = (url, csrf, target_url, e) => {
    $('#formSubKegiatan').attr('action', target_url)
    $('#submitFormSurvei').html('Update Data')
    $.ajax({
        url: url,
        type: "POST",
        dataType: "json",
        data : {
            'id' : e
        },
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken":csrf,
        },
        success: (data) => {
            for (const [key, value] of Object.entries(data.instance)) {
                $('#id_'+key).val(value)
            }
            $('.nav-tabs a[href="#input-tab"]').tab('show');
        },
        error: (error) => {
            console.log(error);
        }
    });
}

let submit_form_kegiatan = (csrf) => {
    var serializedData = $("#formSubKegiatan").serialize();
    $('.invalid-feedback').html('')
    $('.is_invalid').removeClass('is_invalid')
    $.ajax({
        type: 'POST',
        url: $("#formSubKegiatan").attr('action'),
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
            $('.nav-tabs a[href="#subkegiatan-preview"]').tab('show');
            resetForm()
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

let resetFormKegiatan = (url) => {
    $('#formSubKegiatan')[0].reset();
    $('.was-validated').removeClass('was-validated')
    $('#submitFormPetugas').html('Kirim Data')
    $('#formSubKegiatan').attr('action', url)
}

$('#status-select-filter').bind("keyup change", () => {
    table.draw()
})

$('#ResetFormSurvei').on('click', (e) => {
    resetForm()
})

$('#redraw-table').on('click', () => {
    table.draw();
})

$('#reset-filter').on('click', () => {
    $('#status-select-filter').prop('selectedIndex',0);
    table.draw();
})