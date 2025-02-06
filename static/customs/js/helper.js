var swalWithBootstrapButtons = Swal.mixin({
    customClass: {
      confirmButton: 'btn btn-primary'},
    buttonsStyling: true
})

function reset_administrative(all, level=null, except_keldes = null){
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

function preview_excel(table_id, field_file_id, len_coloumn){
    var input = $('#'+field_file_id).get(0).files[0]
    readXlsxFile(input).then(function(data){
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

function clearFormValidation(form){
    $(form + ' .form-control').each(function(i, obj) {
        $(obj).removeClass('is-invalid')
        $(obj).trigger('change')
    });

    $(form + ' .form-select').each(function(j, objs) {
        $(objs).removeClass('is-invalid')
        $(objs).trigger('change')
    });
    
    $('.invalid-feedback').each(function(i, obj) {
        $(obj).html('')
    });
}