function ExportToExcel(type, fn, dl) {
    var elt = document.getElementById('basic-datatable-2');
    var wb = XLSX.utils.table_to_book(elt, { sheet: "Nilai Mitra" });
    return dl ?
        XLSX.write(wb, { bookType: type, bookSST: true, type: 'base64' }):
        XLSX.writeFile(wb, fn || ('Data Nilai Mitra per Indikator.' + (type || 'xlsx')));
}

function resetForm(){
    $('#formPenilaianPetugas')[0].reset();
    $('.was-validated').removeClass('was-validated')
    $('#submitformPenilaianPetugas').html('Kirim Data')
    $('#form-indikator-nilai tbody').html('')
}

$('#formPenilaianPetugas').on('submit', function(e){
    e.preventDefault()
    var serializedData = $(this).serialize();
    
    $.ajax({
        type: 'POST',
        url: $(this).attr('action'),
        data: serializedData,
        success: function (response) {
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
        error: function (response) {
            var errors = response["responseJSON"]["error"]
            var msgs = '<ul>'
            for (const [key, value] of Object.entries(errors)) {
                value.forEach(function (item, index) {
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

$('#mitra-select-filter, #pegawai-select-filter, #kegiatan-select-filter, #survei-select-filter, #role-select-filter').bind("keyup change", function (){
    table.draw()
})

$('#reset-filter').on('click', () => {
    region_code = ''
    $('#mitra-select-filter, #pegawai-select-filter, #kegiatan-select-filter, #survei-select-filter, #role-select-filter, .region-adm').prop('selectedIndex',0);
    reset_administrative(true)
    table.draw();
})

$('#reset-filter-2').on('click', function (){
    $('#role-select-filter-2').prop('selectedIndex',0);
    get_data_tables_nilai({
        'kegiatan_penilaian' : $('#nilai-mitra-filter-kegiatan').val()
    })
})

$('#btn-submit-file').on('click', function(){
    $('#nav-item-import').removeClass('d-none')
    $('#import-modal').modal('toggle')
    $('.nav-tabs a[href="#import-tab"]').tab('show');
})

$('#nilai-mitra-filter-kegiatan').on("change", function(){
    get_data_tables_nilai({
        'kegiatan_penilaian' : $('#nilai-mitra-filter-kegiatan').val()
    })
})

$('#redraw-table').on('click', function (){
    table.draw();
})

$('#redraw-table-2').on('click', function (){
    get_data_tables_nilai({
        'kegiatan_penilaian' : $('#nilai-mitra-filter-kegiatan').val()
    })
})

$('#ResetformPenilaianPetugas').on('click', function(e){
    resetForm()
    $('#field_mitra').val('')
    $('#field_penilai').val('')
    $('#field_kegiatan').val('')
})

$('#role-select-filter-2').on('change', function(){
    get_data_tables_nilai({
        'kegiatan_penilaian' : $('#nilai-mitra-filter-kegiatan').val(),
        'filter_role_nilai_mitra' : $(this).val()
    })
})

