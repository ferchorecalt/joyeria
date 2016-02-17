 $(document).ready(function() {

     $("#filtroNombre").keyup(function(e){
        e.preventDefault();
        llamadoAjax();
     });

     $("#marcasPorPagina").change(function(){
        llamadoAjax();
     });

     function llamadoAjax() {
         var nombre= $("#filtroNombre").val();
         var cantidad= $("#marcasPorPagina").val();
         $.ajax({
             url: 'listadoMarcas',
             type: 'get',
             dataType: "json",
             data: {
                 nombre: nombre,
                 cantidad: cantidad,
                 csrfmiddlewaretoken: '{{ csrf_token }}'
             },
             success: function (marcas) {
                 var myNode = document.getElementById("tablaMarcas");
                 myNode.innerHTML = '';
                 var nuevoHtml = "<thead><tr><th><a href='?sort=nombred'><i class='fa fa-sort-desc fa-2x'></i></a>Nombre</th><th>Editar</th><th>Eliminar</th></tr></thead>" +
                     "<tbody>";
                 for (var i = 0; i < marcas.length; i++) {
                     nuevoHtml = nuevoHtml.concat("<tr>");
                     nuevoHtml = nuevoHtml.concat("<td>" + marcas[i].fields.nombre + "</td>");
                     nuevoHtml = nuevoHtml.concat("<td><a href='editarMarca/"+marcas[i].pk+"'><p><span class='glyphicon glyphicon-pencil'></span></p></a></td>");
                     nuevoHtml = nuevoHtml.concat("<td><a href='eliminarMarca/"+marcas[i].pk+"' onclick='return confirm('Seguro que desea eliminar la marca? " +
                         "Eliminara tambien los articulos que de ella dependen')'><p><span class='glyphicon glyphicon-remove'></span></p>" +
                         "</a></td>");
                     //$.each(marcas[i].fields, function(k, v) {
                     //    alert(k + ' is ' + v);
                     //});
                     nuevoHtml = nuevoHtml.concat("</tr>");
                 }
                 document.getElementById("tablaMarcas").innerHTML = nuevoHtml;
             },
             error: function (xhr, errmsg, err) {

             }
         });
     }
 });