$(document).ready(function () {
    var next = "?next=" + document.location.pathname;

    $('#filtro_activo').change(function(){
        oTable.draw();
    });

    $('#loader').show();
    var oTable = $('#lista').DataTable(default_options_datatable());

    $(document).on('click', '.item-espacio-activar', function(e){

        var div = $(this).parents('div.dropdown-espacio');
        var activo = $(div).data('activo');
        var mensaje = activo ? 'desactivar' : 'activar';

        alert_confirm('Cambiar de estado', '¿Estas seguro de ' + mensaje + ' el espacio de trabajo?', 'warning' ).then((result) => {
            if (result.isConfirmed) {

                var id = $(div).data('id');
                var url = activo ? url_desactivar : url_activar;
                $.get(url + id, {}, function(res){
                    if (res.status == 'error'){
                        mensaje_error(res.message);
                    }else{
                        mensaje_exito(res.message);
                    }
                    oTable.draw(false); //false para no cambiar de página
                });

            }
        });
    });
});

function default_options_datatable(){
    return {
        "order": [[0, "desc"]],
        "responsive": true,
        "autoWidth": false,
        "destroy": true,
        "deferRender": true,
        "language": {url: getUrl('static/plugins/datatables/es.js')},
        "processing": true,
        "serverSide": true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: function ( d ) {
                d.filtro_activo = $('#filtro_activo').val();
            },
            //dataSrc: "",
            cache: false,
            error: function(err){
                if (err.responseJSON && err.responseJSON.message){
                    var msg = err.responseJSON.message;
                    alert(msg);
                }
                console.log(err);
                if (err.status == 401){
                    window.location = window.location;
                }
            }
        },
        columns: [
            {"data": "nombre"},
            {"data": "descripcion"},
            {"data": "activo"},
            {"data": "created_by"},
            {"data": "created_at"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                orderable: true,
                targets: [0,1,2],
                class: '',
            },
            {targets: [0], render: function (data, type, row) {
                var url =  url_editar + row.id;
                return '<a href="'+(url)+'">' + data + '</a>';
            }},
            {targets: [1], render: function (data, type, row) {
                return data;
            }},
            {targets: [2], render: function (data, type, row) {
                var html = [
                '<span class="label label-' + (data ? 'success' : 'danger') + '">',
                (data ? 'SI' : 'NO'),
                '</span>'];
                return html.join('');
            }},
            {targets: [5], 'class': "text-right", render: function (data, type, row) {
                var html =
                '<div class="dropdown show dropdown-espacio" data-id="'+ row.id +'" data-activo="' + row.activo + '"> \
                  <a class="btn btn-link btn-xs dropdown-toggle" href="#" role="button" id="dropdownMenuLink" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"> \
                    <i class="fas fa-th-list"></i> \
                  </a> \
                  <div class="dropdown-menu" aria-labelledby="dropdownMenuLink"> \
                    <a class="dropdown-item item-espacio-activar" href="javascript:void(0);">' + (row.activo ? 'Desactivar' : 'Activar') + '</a> \
                  </div> \
                </div>';
                return html;
            }}

        ],
        "stateSave": true,
        fnStateSaveParams: function(oSettings, oData){
            oData.filtro_activo = $('#filtro_activo').val();
        },
        fnStateLoadParams: function(oSettings, oData){
            $('#filtro_activo').val(oData.filtro_activo);
        }
    };
};