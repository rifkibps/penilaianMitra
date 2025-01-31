var swalWithBootstrapButtons = Swal.mixin({
    customClass: {
      confirmButton: 'btn btn-primary'},
    buttonsStyling: true
})

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