$(document).ready(function () {
    var next = "?next=" + document.location.pathname;
    //$('#loader').show();



    $(document).on('click', '.item-grupo-activar', function(e){

        var div = $(this).parents('div.dropdown-grupo');
        var activo = $(div).data('activo');
        var mensaje = activo ? 'desactivar' : 'activar';

        alert_confirm('Cambiar de estado', '¿Estas seguro de ' + mensaje + ' el grupo de trabajo?', 'warning' ).then((result) => {
            if (result.isConfirmed) {

                var id = $(div).data('id');
                var url_activar_grupo = $('#dt-casos').data('url_activar_grupo');
                var url_desactivar_grupo = $('#dt-casos').data('url_desactivar_grupo');
                var url = activo ? url_desactivar_grupo : url_activar_grupo;
                $.get(url + id, {}, function(res){
                    if (res.status == 'error'){
                        mensaje_error(res.message);
                    }else{
                        mensaje_exito(res.message);
                    }
                    oTableCasos.draw(false); //false para no cambiar de página
                });

            }
        });
    });

});

