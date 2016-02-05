 $(document).ready(function() {
    $("#filtroNombre").keyup(function(e){
        e.preventDefault()
        $.ajax({
            url: 'listadoMarcas',
            type: 'get',
            dataType: "json",
            data : {
                nombre : $("#filtroNombre").val(),
                csrfmiddlewaretoken: '{{ csrf_token }}'
            },
             success : function(json) {
                 alert("hola")
                 alert(json)
             },
            error : function(xhr,errmsg,err) {

            }
        });
    });
 });