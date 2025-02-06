// KEGIATAN PENILAIAN

$('#survei-select-filter').bind("keyup change", function (){
    table.draw()
})

$('#status-select-filter').bind("keyup change", function (){
    table.draw()
})

$('#role-select-filter').bind("keyup change", function (){
    table.draw()
})

$('#reset-filter').on('click', function (){
    $('#survei-select-filter').prop('selectedIndex',0);
    $('#status-select-filter').prop('selectedIndex',0);
    $('#role-select-filter').prop('selectedIndex',0);
    table.draw();
})

$('#redraw-table').on('click', function (){
    table.draw();
})

$('#ResetformKegiatanPenilaianPetugas').on('click', function(e){
    resetForm()
})

// INDIKATOR PENILAIAN

$('#ResetformIndikatorPenilaianPetugas').on('click', function(e){
    resetForm()
})

$('#formKegiatanPenilaianPetugas').on('submit', function(e){
    e.preventDefault()
    clearFormValidation('#formKegiatanPenilaianPetugas')

    var serializedData = $(this).serialize();
    $('.invalid-feedback').html('')
    $('.is_invalid').removeClass('is_invalid')
    $.ajax({
        type: 'POST',
        url: $(this).attr('action'),
        data: serializedData,
        success: function (response) {
            $('#messages-content').html(response["message"])
            $('#msgs-upload').removeClass('alert-danger')
            $('#msgs-upload').addClass('alert-success')
            $('#msgs-upload').removeClass('d-none')
            table.ajax.reload();
            $('.nav-tabs a[href="#indikator-penilaian-preview"]').tab('show');
            $('#formKegiatanPenilaianPetugas')[0].reset();
            clearFormValidation('#formKegiatanPenilaianPetugas')
        },
        error: function (response) {
            var errors = response["responseJSON"]["error"]
            for (const [key, value] of Object.entries(errors)) {
                var msgs = '<ul>'
                value.forEach(function (item, index) {
                    msgs += '<li>'+item+'</li>'
                    });
                msgs += '</ul>'
                $('#id_'+ key).addClass('is-invalid');
                $('#msg-id_'+key).html(msgs)
            }    
        }
    })
})

// INDIKATOR KEGIATAN PENILAIAN

$('#kegiatan-select-filter').bind("keyup change", function (){
    table.draw()
})

$('#indikator-select-filter').bind("keyup change", function (){
    table.draw()
})

$('#ResetformIndikatorKegiatanPenilaianPetugas').on('click', function(e){
    resetForm()
})

$('#formKegiatanIndikatorPenilaianPetugas').on('submit', function(e){
    e.preventDefault()
    clearFormValidation('#formKegiatanIndikatorPenilaianPetugas')

    var serializedData = $(this).serialize();
    $('.invalid-feedback').html('')
    $('.is_invalid').removeClass('is_invalid')
    $.ajax({
        type: 'POST',
        url: $(this).attr('action'),
        data: serializedData,
        success: function (response) {
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
        error: function (response) {
            var errors = response["responseJSON"]["error"]
            for (const [key, value] of Object.entries(errors)) {
                var msgs = '<ul>'
                value.forEach(function (item, index) {
                    msgs += '<li>'+item+'</li>'
                    });
                msgs += '</ul>'
                $('#id_'+ key).addClass('is-invalid');
                $('#msg-id_'+key).html(msgs)
            }    
        }
    })
})

$('#reset-filter').on('click', function (){
    $('#kegiatan-select-filter').prop('selectedIndex',0);
    $('#indikator-select-filter').prop('selectedIndex',0);
    table.draw();
})

$('#redraw-table').on('click', function (){
    table.draw();
})