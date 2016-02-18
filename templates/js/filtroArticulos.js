 $(document).ready(function() {

     var page=1;
     var orden="modelo";
     habYdeshabBotones(page, $("#cantidadPaginas").val());

     $("#filtroMarca").keyup(function(e){
        e.preventDefault();
        page=1;
        llamadoAjax();
     });

     $("#filtroModelo").keyup(function(e){
        e.preventDefault();
        page=1;
        llamadoAjax();
     });

     $("#filtroDescripcion").keyup(function(e){
        e.preventDefault();
        page=1;
        llamadoAjax();
     });

     $("#articulosPorPagina").change(function(){
        llamadoAjax();
     });

     $("#tablaArticulos").on("click","#ordenarPorNombre",function(){
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
         var filtroMarca= $("#filtroMarca").val();
         var filtroModelo= $("#filtroModelo").val();
         var filtroDescripcion= $("#filtroDescripcion").val();
         var cantidad= $("#articulosPorPagina").val();
         $.ajax({
             url: 'listadoArticulos',
             type: 'get',
             dataType: "json",
             data: {
                 filtroMarca: filtroMarca,
                 filtroModelo: filtroModelo,
                 filtroDescripcion: filtroDescripcion,
                 cantidad: cantidad,
                 page: page,
                 orden: orden,
                 csrfmiddlewaretoken: '{{ csrf_token }}'
             },
             success: function (data) {
                 $("#infoPagActual").text("Pagina "+data["page"]+" de "+data["cantPaginas"]);
                 habYdeshabBotones(data["page"],data["cantPaginas"]);
                 var articulos = JSON.parse(data["articulos"]);
                 var myNode = document.getElementById("tablaArticulos");

                 if(articulos.length == 0){
                     $("#tablaArticulos").hide();
                     $("#infoPagActual").text("Ningun articulo posee '"+filtro+"' en su "+tipoFiltro);
                 }
                 else{
                     $("#tablaArticulos").show();
                     $("#tablaArticulos").css('visibility', 'visible');
                     myNode.innerHTML = '';
                     var nuevoHtml = "<thead><tr>";

                     //if(data["orden"]=="nombre")
                     //    nuevoHtml = nuevoHtml.concat("<th><button class='btn btn-warning btn-sm' id='ordenarPorNombre' name='ASC'><i class='fa fa-sort-asc fa-2x'></i></button>Nombre</th>");
                     //else nuevoHtml = nuevoHtml.concat("<th><button class='btn btn-warning btn-sm' id='ordenarPorNombre' name='DESC'><i class='fa fa-sort-desc fa-2x'></i></button>Nombre</th>");

                     nuevoHtml = nuevoHtml.concat("<th><button class='btn btn-warning btn-sm' id='ordenarPorMarca' name='ASC'><i class='fa fa-sort-asc fa-2x' id='iconoOrdenMarca'></i></button> Marca</th>" +
                                                  "<th><button class='btn btn-warning btn-sm' id='ordenarPorModelo' name='ASC'><i class='fa fa-sort-asc fa-2x' id='iconoOrdenModelo'></i></button>Modelo</th>" +
                                                  "<th><button class='btn btn-warning btn-sm' id='ordenarPorDescripcion' name='ASC'><i class='fa fa-sort-asc fa-2x' id='iconoOrdenDescripcion'></i></button>Descripcion</th>" +
                                                  "<th><button class='btn btn-warning btn-sm' id='ordenarPorFecha' name='ASC'><i class='fa fa-sort-asc fa-2x' id='iconoOrdenFecha'></i></button>Fecha</th>" +
                                                  "<th>Imagen</th><th>Editar</th><th>Eliminar</th></tr></thead><tbody>");
                     for (var i = 0; i < articulos.length; i++) {
                         nuevoHtml = nuevoHtml.concat("<tr>");
                         nuevoHtml = nuevoHtml.concat("<td>" + articulos[i].fields.articulo_marca.nombre + "</td>");
                         nuevoHtml = nuevoHtml.concat("<td>" + articulos[i].fields.modelo + "</td>");
                         nuevoHtml = nuevoHtml.concat("<td>" + articulos[i].fields.descripcion + "</td>");
                         nuevoHtml = nuevoHtml.concat("<td>" + articulos[i].fields.fecha + "</td>");
                         //EN LO SIGUIENTE HARCODEO EL /IMAGENES.. VER SI SE PUEDE CORREGIR
                         nuevoHtml = nuevoHtml.concat("<td> <img src='/imagenes/"+articulos[i].fields.imagen+"' alt='imagen del articulo "+i+"' width='200' height='100'> </td>");
                         nuevoHtml = nuevoHtml.concat("<td><a href='editarArticulo/"+articulos[i].pk+"'><p><span class='glyphicon glyphicon-pencil'></span></p></a></td>");
                         nuevoHtml = nuevoHtml.concat("<td><a href='eliminarArticulo/"+articulos[i].pk+"' onclick='return confirm('Seguro que desea eliminar al articulo?')'><p><span class='glyphicon glyphicon-remove'></span></p></a></td>");
                         nuevoHtml = nuevoHtml.concat("</tr>");
                     }
                     document.getElementById("tablaArticulos").innerHTML = nuevoHtml;
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