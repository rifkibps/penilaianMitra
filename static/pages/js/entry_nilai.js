let generate_kegiatan_penilaian = (url, csrf) => {
    return $("#list_kegiatan_penilaian").DataTable(
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
                {"data": 'kegiatan_survey__nama_kegiatan'},
                {"data": 'kegiatan_survey__survey__nama'},
                {"data" : 'tgl_penilaian'},
                {"data": 'status'},
                {"data" : 'status_penilaian'},
                {"data" : 'aksi'},
            ],
            lengthMenu: [5, 25, 50, 100,'All'],
            columnDefs: [ {
                'targets': [5], /* column index */
                'orderable': false, /* true or false */
                'className': "text-center"
            },
            {
                'targets': [2, 3, 4], /* column index */
                'className': "text-center"
            }
            ],
            bLengthChange: false,
            bFilter: false,
        }, ...settingDatatables()
    }
);
}

let generate_penilaian = (url, csrf) => {
    return $("#list-penilaian").DataTable(
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
                        "kegiatan_penilaian": $('#kegiatan_penilaian').val(),
                        "search_mitra": $('#search-mitra-datatable').val(),
                    })
                },
                "type": "POST"
            },
            columns :[
                {"data": 'kegiatan_penilaian'},
                {"data": 'wilayah'},
                {"data" : 'nama'},
                {"data": 'role'},
                {"data" : 'rerata'},
                {"data" : 'state'},
                {"data" : 'aksi'},
            ],
            lengthMenu: [5, 25, 50, 100,'All'],
            columnDefs: [ {
                'targets': [6], /* column index */
                'orderable': false, /* true or false */
                'className': "text-center"
            },
            {
                'targets': [3, 4, 5], /* column index */
                'className': "text-center"
            }
            ],
            bLengthChange: false,
            bFilter: false,
        }, ...settingDatatables()
    }
);
}

let generate_ranking_global = (url, csrf) => {
    return $('#ranking-global').DataTable({
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
                    "search_mitra": $('#search-mitra').val(),
                })
            },
        },
        columns :[
            {"data": 'wilayah'},
            {"data" : 'petugas'},
            {"data" : 'rerata'},
            {"data" : 'rank'},
        ],
        columnDefs: [ {
            'targets': [2,3], /* column index */
            'className': "text-center"
        }],
        bLengthChange: false,
        bPaginate: false,
        bFilter: false,
    });
}

let entryPenilaianRequest = (url, csrf, id1, id2) => {
    $.ajax({
        url: url,
        type: "POST",   
        dataType: "json",
        data :  {'id_kegiatan' : id1, 'id_alokasi' : id2},
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": csrf,
        },
        success: (response) => {
            $('#field_id_penilai').html(response.data.penilai_opts)
            $('#field_role_penilai').html(response.data.role_penilai_opts)
            $('#field_kegiatan_penilaian').html(response.data.kegiatan_opts)
            $('#field_survey').html(response.data.survei_opts)
            $('#field_mitra').html(response.data.petugas_opts)
            $('#field_role_petugas').html(response.data.role_petugas_opts)

            $('#table_form_penilaian tbody').html(response.data.tbody)
            $('#card-form-penilaian').removeClass('d-none')
        },
        error: (error) => {
            console.log(error);
        }
    });
}

let check_submit_penilaian = (csrf) => {
    var serializedData = $('#formPenilaianPetugas').serialize();
    $.ajax({
        type: 'POST',
        url: $('#formPenilaianPetugas').attr('action'),
        data: serializedData,
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": csrf,
        },
        success: (response) => {
            if (response.status == 'success'){
                Swal.fire(
                        'Data berhasil disimpan',
                        response.messages,
                        'success'
                )
                table2.ajax.reload();
            }
        },
        error: (response) => {
            console.log(response)
        }
    })
}

let pushValuePenilaian = (id) => {
    $('#kegiatan_penilaian').val(id)
    table2.draw()
}

$('#search-mitra').on("keyup", () => {
    table3.draw()
})

$('#search-mitra-datatable').on("keyup", () => {
    table2.draw()
})

$('#refresh-rank').on("click", () => {
    table3.draw()
})




$('#close-card-form').on('click', () => {
    $('.form-select').val('')
    $('#table_form_penilaian tbody').html('')
    $('#card-form-penilaian').addClass('d-none')
})