$(function () {
    initDataTable();
});

function initDataTable(){
    table = $('#lista').DataTable({
        "processing": true,
        "serverSide": true,
        "stateSave": true,
        "language": {url: getUrl('static/plugins/datatables/es.txt')},
        "order": [[0, "asc"], [1, "asc"], [2, "asc"]],
        "ajax": {
            "url": url_notificaion_usuario_lista_paginador,
            "type": "POST",
            "error": function (error) {
                mensaje_error(error.responseText);
            }
        },
        "columns": [
            {"data": "notificacion__asunto", render: function ( data, type, row ) {
                return '<a href="'+basehref+'/seguridad/notificacion-usuario/detalle/' + row.id +'">' + data + '</a>';
            }},
            {"data": "notificacion__created_at", render: function ( data, type, row ) {
                return '<span class="time">' + data + '</span>';
            }},
            {"data": "estado", render: function ( data, type, row ) {
                let estado = data=='P'?'Pendiente':data=='V'?'Visto':'Leído';
                return estado;
            }},
        ],
        "language": {"url": "/static/plugins/datatables/es.js"}
    });
}

