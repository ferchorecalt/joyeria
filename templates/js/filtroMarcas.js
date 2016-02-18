 $(document).ready(function() {

     var page=1;
     var orden="nombre";
     habYdeshabBotones(page, $("#cantidadPaginas").val());

     $("#filtroNombre").keyup(function(e){
        e.preventDefault();
        page=1;
        llamadoAjax();
     });

     $("#marcasPorPagina").change(function(){
        llamadoAjax();
     });

     $("#tablaMarcas").on("click","#ordenarPorNombre",function(){
         if($("#ordenarPorNombre").attr('name').indexOf("ASC")>-1)
             orden="-nombre";
         else orden="nombre";
         llamadoAjax();
     });

     $("#previa").click(function(){
         if(page!=1){
            page = page -1;
            llamadoAjax();
         }
     });

     $("#siguiente").click(function(){
         var cantidadPaginas = $("#cantidadPaginas").val();
         if(page<cantidadPaginas){
            page = page +1;
            llamadoAjax();
         }
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
                 page: page,
                 orden: orden,
                 csrfmiddlewaretoken: '{{ csrf_token }}'
             },
             success: function (data) {
                 $("#infoPagActual").text("Pagina "+data["page"]+" de "+data["cantPaginas"]);
                 habYdeshabBotones(data["page"],data["cantPaginas"]);
                 var marcas = JSON.parse(data["marcas"]);
                 var myNode = document.getElementById("tablaMarcas");

                 if(marcas.length == 0){
                     $("#tablaMarcas").hide();
                     $("#infoPagActual").text("Ninguna marca posee '"+nombre+"' en su nombre");
                 }
                 else{
                     $("#tablaMarcas").show();
                     $("#tablaMarcas").css('visibility', 'visible');
                     myNode.innerHTML = '';
                     var nuevoHtml = "<thead><tr>";

                     if(data["orden"]=="nombre")
                         nuevoHtml = nuevoHtml.concat("<th><button class='btn btn-warning btn-sm' id='ordenarPorNombre' name='ASC'><i class='fa fa-sort-asc fa-2x'></i></button>Nombre</th>");
                     else nuevoHtml = nuevoHtml.concat("<th><button class='btn btn-warning btn-sm' id='ordenarPorNombre' name='DESC'><i class='fa fa-sort-desc fa-2x'></i></button>Nombre</th>");

                     nuevoHtml = nuevoHtml.concat("<th>Editar</th><th>Eliminar</th></tr></thead>" +
                         "<tbody>");
                     for (var i = 0; i < marcas.length; i++) {
                         nuevoHtml = nuevoHtml.concat("<tr>");
                         nuevoHtml = nuevoHtml.concat("<td>" + marcas[i].fields.nombre + "</td>");
                         nuevoHtml = nuevoHtml.concat("<td><a href='editarMarca/"+marcas[i].pk+"'><p><span class='glyphicon glyphicon-pencil'></span></p></a></td>");
                         nuevoHtml = nuevoHtml.concat("<td><a href='eliminarMarca/"+marcas[i].pk+"'" +
                             " onclick='return confirm('Seguro que desea eliminar la marca? Eliminara tambien los articulos que de ella dependen')'>" +
                             "<p><span class='glyphicon glyphicon-remove'></span></p>" +
                             "</a></td>");
                         //$.each(marcas[i].fields, function(k, v) {
                         //    alert(k + ' is ' + v);
                         //});
                         nuevoHtml = nuevoHtml.concat("</tr>");
                     }

                     document.getElementById("tablaMarcas").innerHTML = nuevoHtml;
                 }


             },
             error: function (xhr, errmsg, err) {

             }
         });
     }
 });

 function habYdeshabBotones(numPage, cantPaginas){
     if(numPage=="1")
         $("#previa").hide();
     else{
         $("#previa").show();
         $("#previa").css('visibility', 'visible');
     }

     if(numPage==cantPaginas)
         $("#siguiente").hide();
     else{
         $("#siguiente").show();
         $("#siguiente").css('visibility', 'visible');
     }
 }