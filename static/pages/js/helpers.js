let swalWithBootstrapButtons = Swal.mixin({
    customClass: {
      confirmButton: 'btn btn-primary'},
    buttonsStyling: true
})

let settingDatatables = () => {
    return {
        keys: !0,
        language: {
            paginate: {
            previous: "<i class='mdi mdi-chevron-left'>",
            next: "<i class='mdi mdi-chevron-right'>",
            },
            lengthMenu : "Menampilkan _MENU_",
            search: "Cari data ",
        },
        drawCallback: () => {
            $(".dataTables_paginate > .pagination").addClass("pagination-rounded");
        },
    }
}

let reset_administrative = (all, level=null, except_keldes = null) => {
    if (all){
        $('#filter_kabkot').html('<option value="">-- Pilih Kab/Kota --</option>')
        $('#filter_kec').html('<option value="">-- Pilih Kecamatan --</option>')
        $('#filter_keldes').html('<option value="">-- Pilih Desa --</option>')
    }else{
        if (level == 'filter_prov'){
            $('#filter_kabkot').html('<option value="">-- Pilih Kab/Kota --</option>')
            $('#filter_kec').html('<option value="">-- Pilih Kecamatan --</option>')
            $('#filter_keldes').html('<option value="">-- Pilih Desa --</option>')
        }else if (level == 'filter_kabkot'){
            $('#filter_kec').html('<option value="">-- Pilih Kecamatan --</option>')
            $('#filter_keldes').html('<option value="">-- Pilih Desa --</option>')
        }else if (level == 'filter_kec'){
            if (!except_keldes) return false
            $('#filter_keldes').html('<option value="">-- Pilih Desa --</option>')
        }
    }
}

let preview_excel = (table_id, field_file_id, len_coloumn) => {
    var input = $('#'+field_file_id).get(0).files[0]
    readXlsxFile(input).then((data) => {
        var i = 0
        $('#'+table_id+' tbody').html('') 
        data.map((row, index) =>{
            if (i==1){
                var throws = '<tr>'
                for (var key of row.slice(0, len_coloumn)){
                    throws += '<th>' + key + '</th>'
                }
                throws += '</tr>'
                $('#'+table_id+' thead').html(throws) 
            }

            if (i>1){
                var tdrows = '<tr>'
                var isnull = 0
                for (var key of row.slice(0, len_coloumn)){
                    if ( key == null ){
                        isnull += 1
                    }
                    tdrows += '<td>' + key + '</td>'
                }
                tdrows += '</tr>'
                if (isnull < len_coloumn) {
                    $('#'+table_id+' tbody').append(tdrows) 
                }
            }
            i++
        })
        return true
    })
}

let clearFormValidation = (form) => {
    $(form + ' .form-control').each((i, obj) => {
        $(obj).removeClass('is-invalid')
        $(obj).trigger('change')
    });

    $(form + ' .form-select').each((j, objs) => {
        $(objs).removeClass('is-invalid')
        $(objs).trigger('change')
    });
    
    $('.invalid-feedback').each((i, obj) => {
        $(obj).html('')
    });
}
 
let delete_general_request = (ask, url, csrf, e, table) => {
    swalWithBootstrapButtons.fire({
        title: 'Are you sure?',
        text: ask,
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: 'Yes, delete it!',
        cancelButtonText: 'No, cancel!',
        reverseButtons: false
      }).then((result) => {
        if (result.isConfirmed) {
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
                        Swal.fire(
                            'Deleted!',
                            data.message,
                            'success'
                            )
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
    }) 
}

let fetch_administrative = (url, csrf, e) => {
    var code = $(e).val()
    var id = $(e).attr('id')
    
    reset_administrative(false, id, true)
    if (code.length == 0) return false
    region_code = code
    if (id == 'filter_keldes') return table.draw()

    $.ajax({
        url: url,
        type: "POST",   
        dataType: "json",
        data :  {'code' : code},
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": csrf,
        },
        success: (data) => {
            if (data.status == 'success'){
                if (code.length == 2){
                    $('#filter_kabkot').html(data.adm)
                } else if (code.length == 4){
                    $('#filter_kec').html(data.adm)
                } else {
                    $('#filter_keldes').html(data.adm)
                }
                table.draw()
            }
        },
        error: (error) => {
            console.log(error);
        }
    }); 
}

$(document).on('change', '.form-control, .form-select', () => {
    if ($(this).hasClass('is-invalid')){
        $(this).removeClass('is-invalid')
    }
});