let generate_master_survey = (url, csrf) => {
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
                {"data": 'nama'},
                {"data": 'nama'},
                {"data" : 'tgl_mulai'},
                {"data":  'deskripsi'},
                {"data":  'state'},
                {"data" : 'aksi'},
            ],
            lengthMenu: [5, 25, 50, 100,'All'],
            columnDefs: [ {
                'targets': [5], /* column index */
                'orderable': false, /* true or false */
            },
            {
                "targets": 0,
                "data": null,
                "defaultContent": "",
                "render": (data, type, row, meta)  => {
                    return meta.row + 1;
                }
            }],
        }, ...settingDatatables()
    }
    );
}

let edit_survey_request = (url, csrf, target_url, e) => {
    $('#formMasterSurvei').attr('action', target_url)
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
            "X-CSRFToken": csrf,
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

let submit_form_survey = (csrf) => {
    var serializedData = $("#formMasterSurvei").serialize();
    $('.invalid-feedback').html('')
    $('.is_invalid').removeClass('is_invalid')
    $.ajax({
        type: 'POST',
        url: $("#formMasterSurvei").attr('action'),
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
            $('.nav-tabs a[href="#survey-preview"]').tab('show');
            resetForm()
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

let confirmSubmitFile = (url, csrf, formData) => {
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
            data.append("import_file",formData)
            $.ajax({
                type: 'POST',
                url: url,
                data: data,
                processData: false,
                contentType: false,
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                    "X-CSRFToken": csrf,
                },
                success: (response) => {
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

let reset_form_survey = (url) => {
    $('#formMasterSurvei')[0].reset();
    $('.was-validated').removeClass('was-validated')
    $('#submitFormPetugas').html('Kirim Data')
    $('#formMasterSurvei').attr('action', url)
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

$('#btn-submit-file').on('click', () => {
    $('#nav-item-import').removeClass('d-none')
    $('#import-modal').modal('toggle')
    $('.nav-tabs a[href="#import-tab"]').tab('show');
})

$('#reset-filter').on('click', () => {
    $('#status-select-filter').prop('selectedIndex',0);
    table.draw();
})