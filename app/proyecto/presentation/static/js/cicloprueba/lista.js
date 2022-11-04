$(document).ready(function () {
    var next = "?next=" + document.location.pathname;
    //$('#loader').show();

    var oTableCiclos = $('#dt-ciclos').DataTable(options_datatable_ciclos());

    $('#filtro_ciclo_activo').change(function () {
        oTableCiclos.draw();
    });

    init_actions();
});


/**
* Datatable casos de prueba
*/
function options_datatable_ciclos(){
    var url_grupos = $('#dt-ciclos').data('url');
    var url_detalle = $('#dt-ciclos').data('url_detalle');
    var proyecto_id = $('#dt-ciclos').data('id');

    return {
        "order": [[0, "desc"]],
        "responsive": true,
        "autoWidth": false,
        "destroy": true,
        "deferRender": true,
        "language": {url: getUrl('static/plugins/datatables/es.txt')},
        "processing": true,
        "serverSide": true,
        ajax: {
            url: url_grupos,
            type: 'POST',
            data: function ( d ) {
                d.proyecto_id = proyecto_id;
                d.filtro_activo = $('#filtro_ciclo_activo').val();
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
            {"data": "id"},
        ],
        columnDefs: [
            {
                orderable: true,
                targets: [0,1,2],
                class: '',
            },
            {targets: [0], render: function (data, type, row) {
                var url =  url_detalle + row.id;
                return $.validator.format('<a href="{0}"><i class="fas fa-users"></i> {1}</a>', url, data);
                return data;
            }},
            {targets: [1], render: function (data, type, row) {
                return data;
            }},
            {targets: [3], 'class': "text-right", render: function (data, type, row) {
                var html =
                '<div class="dropdown show dropdown-grupo" data-id="'+ row.id +'" data-activo="' + row.activo + '"> \
                  <a class="btn btn-link btn-xs dropdown-toggle" href="#" role="button" id="dropdownMenuLink" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"> \
                    <i class="fas fa-ellipsis-h"></i> \
                  </a> \
                  <div class="dropdown-menu" aria-labelledby="dropdownMenuLink"> \
                    <a class="dropdown-item item-ciclo-ejecutar" href="javascript:void(0);">' + ('Ejecutar') + '</a> \
                  </div> \
                </div>';
                return html;
            }}

        ],
        initComplete: function (settings, json) {
        },
        "stateSave": true,
        fnStateSaveParams: function(oSettings, oData){
            oData.filtro_activo = $('#filtro_ciclo_activo').val();
        },
        fnStateLoadParams: function(oSettings, oData){
            $('#filtro_ciclo_activo').val(oData.filtro_activo);
        }
    };
};

function init_actions(){
    $(document).on('click', '.item-ciclo-ejecutar', function(e){

        var div = $(this).parents('div.dropdown-grupo');

        var id = $(div).data('id');
        var url_ejecutar = $('#dt-ciclos').data('url_ejecutar');
        console.log(url_ejecutar);
        $(this).attr('href', url_ejecutar + id);
    });
}