$(document).ready(function () {
    var next = "?next=" + document.location.pathname;
    //$('#loader').show();

    var oTableCasos = $('#dt-casos').DataTable(options_datatable_casos());
    var oTableEjecucion = $('#dt-ejecucion').DataTable(options_datatable_ejecucin());

    $('#filtro_caso_activo').change(function(){
        oTableCasos.draw();
    });

    init_actions(oTableCasos, oTableEjecucion);
});


/**
* Datatable casos de prueba
*/
function options_datatable_casos(){
    var url_grupos = $('#dt-casos').data('url');
    var url_agregar = $('#dt-casos').data('url_agregar');
    var proyecto_id = $('#dt-casos').data('id');
    var ciclo_id = $('#dt-casos').data('ciclo_id');

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
            {"data": "codigo"},
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
                return data;
            }},
            {targets: [1], render: function (data, type, row) {
                return data;
            }},
            {targets: [2], render: function (data, type, row) {
                return data;
            }},
            {targets: [3], 'class': "text-right", render: function (data, type, row) {
                var url =  url_agregar + row.id;
                url = url.replace('/0/', '/'+ciclo_id+'/');
                return $.validator.format('<a class="item-add-caso" href="javascript:void(0);" data-url="{0}"><i class="fas fa-plus"></i> {1}</a>', url, 'Agregar');
            }}

        ],
        initComplete: function (settings, json) {
        },
        "stateSave": true,
        fnStateSaveParams: function(oSettings, oData){

        },
        fnStateLoadParams: function(oSettings, oData){

        }
    };
};

function init_actions(oTableCasos, oTableEjecucion){
    $(document).on('click', '.item-add-caso', function(e){
        var url = $(this).data('url');
        $.get(url, {}, function(res){
            if (res.status == 'error'){
                mensaje_error(res.message);
            }else{
                mensaje_exito(res.message);
            }
            oTableEjecucion.draw(false); //false para no cambiar de página
        });
    });

    $(document).on('click', '.item-view-evidencia', function(e){
       $('#imagepreview').attr('src', $(this).attr('src'));
       $('#imagemodal').modal('show');
    });
};


/**
* Datatable casos de prueba
*/
function options_datatable_ejecucin(){
    var url_grupos = $('#dt-ejecucion').data('url');
    var proyecto_id = $('#dt-ejecucion').data('id');
    var ciclo_id = $('#dt-ejecucion').data('ciclo_id');
    var url_ejecutar = $('#dt-ejecucion').data('url_ejecutar');

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
                d.ciclo_id = ciclo_id;
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
            {"data": "caso_prueba__codigo"},
            {"data": "caso_prueba__nombre"},
            {"data": "comentario"},
            {"data": "evidencia"},
            {"data": "estado"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                orderable: true,
                targets: [0,1,2],
                class: '',
            },
            {targets: [0], render: function (data, type, row) {
                return data;
            }},
            {targets: [1], render: function (data, type, row) {
                return data;
            }},
            {targets: [2], render: function (data, type, row) {
                return data;
            }},
            {targets: [3], render: function (data, type, row) {
                if (data){
                    return $.validator.format('<a class="item-view-evidencia" src="{0}"><img src="{1}" width="128" /></a>', data, data);
                }
                return '';
            }},
             {targets: [4], render: function (data, type, row) {

                 if (data === 'Aprobada'){
                     return $.validator.format('<span class="badge badge-success">{0}</span>', data);
                 }else if(data === 'Fallo') {
                     return $.validator.format('<span class="badge badge-danger">{0}</span>', data);
                 }else if(data === 'Bloqueada') {
                     return $.validator.format('<span class="badge badge-warning">{0}</span>', data);
                 } else {
                     return $.validator.format('<span class="badge badge-secondary">{0}</span>', data);
                 }

            }},
            {targets: [5], 'class': "text-right", render: function (data, type, row) {
                var url =  url_ejecutar + row.id;
                return $.validator.format('<a class="item-add-caso-ejecutar" href="{0}"><i class="fas fa-cogs"></i> {1}</a>', url, '');
            }}

        ],
        initComplete: function (settings, json) {
        },
        "stateSave": true,
        fnStateSaveParams: function(oSettings, oData){

        },
        fnStateLoadParams: function(oSettings, oData){

        }
    };
};