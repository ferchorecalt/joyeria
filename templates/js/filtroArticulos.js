 $(document).ready(function() {

     var page=1;
     var orden="articulo_marca__nombre";
     var ordenMarca="ASC";
     var ordenModelo="ASC";
     var ordenDescripcion="ASC";
     var ordenFecha="ASC";
     //document.getElementById('filtroFechaDesde').value= "";
     //document.getElementById('filtroFechaHasta').value = "";
     $("#filtroFechaDesde").val(new Date(2016,00,01).toISOString().substring(0, 10));
     $("#filtroFechaHasta").val(new Date().toISOString().substring(0, 10));
     var viendoFiltros=true;
     habYdeshabBotones(page, $("#cantidadPaginas").val());

     $("#modoFiltros").click(function(){
        if(viendoFiltros){
            viendoFiltros=false;
            $("#filtros").hide();
            $("#textoModoFiltros").text("Ver Filtros");
        }else{
            viendoFiltros=true;
            $("#filtros").show();
            $("#filtros").css("visibility","visible");
            $("#textoModoFiltros").text("Ocultar Filtros");
        }
     });

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
        page=1;
        llamadoAjax();
     });

     $("#filtroFechaDesde").change(function(e){
         e.preventDefault();
         page=1;
         llamadoAjax();
     });

     $("#filtroFechaHasta").change(function(e){
         e.preventDefault();
         page=1;
         llamadoAjax();
     });

     $("#tablaArticulos").on("click","#ordenarPorMarca",function(){
         if($("#ordenarPorMarca").attr('name').indexOf("ASC")>-1){
             orden="-articulo_marca__nombre";
             ordenMarca="DESC";
         }
         else{
             orden="articulo_marca__nombre";
             ordenMarca="ASC";
         }
         llamadoAjax();
     });

     $("#tablaArticulos").on("click","#ordenarPorModelo",function(){
         if($("#ordenarPorModelo").attr('name').indexOf("ASC")>-1){
             orden="-modelo";
             ordenModelo="DESC";
         }
         else{
             orden="modelo";
             ordenModelo="ASC";
         }
         llamadoAjax();
     });

     $("#tablaArticulos").on("click","#ordenarPorDescripcion",function(){
         if($("#ordenarPorDescripcion").attr('name').indexOf("ASC")>-1){
             orden="-descripcion";
             ordenDescripcion="DESC";
         }
         else{
             orden="descripcion";
             ordenDescripcion="ASC";
         }
         llamadoAjax();
     });

     $("#tablaArticulos").on("click","#ordenarPorFecha",function(){
         if($("#ordenarPorFecha").attr('name').indexOf("ASC")>-1){
             orden="-fecha";
             ordenFecha="DESC";
         }
         else{
             orden="fecha";
             ordenFecha="ASC";
         }
         llamadoAjax();
     });

     $("#previa").click(function(){
         if(page!=1){
            page = page -1;
            llamadoAjax();
         }
         $("#ordenarPorMarca").focus();
     });

     $("#siguiente").click(function(){
         var cantidadPaginas = $("#cantidadPaginas").val();
         if(page<cantidadPaginas){
            page = page +1;
            llamadoAjax();
         }
         $("#ordenarPorMarca").focus();
     });

     function llamadoAjax() {
         var filtroMarca= $("#filtroMarca").val();
         var filtroModelo= $("#filtroModelo").val();
         var filtroDescripcion= $("#filtroDescripcion").val();
         var filtrofechaDesde= $("#filtrofechaDesde").val();
         var filtroFechaHasta= $("#filtroFechaHasta").val();
         var cantidad= $("#articulosPorPagina").val();
         $.ajax({
             url: 'listadoArticulos',
             type: 'get',
             dataType: "json",
             data: {
                 filtroMarca: filtroMarca,
                 filtroModelo: filtroModelo,
                 filtroDescripcion: filtroDescripcion,
                 filtrofechaDesde: filtrofechaDesde,
                 filtroFechaHasta: filtroFechaHasta,
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
                     $("#infoPagActual").text("Ningun articulo posee tales filtros");
                 }
                 else{
                     $("#tablaArticulos").show();
                     $("#tablaArticulos").css('visibility', 'visible');
                     myNode.innerHTML = '';
                     var nuevoHtml = "<thead><tr>";
                     nuevoHtml = nuevoHtml.concat("<th><button class='btn btn-warning btn-sm' id='ordenarPorMarca' name='"+ordenMarca+"'><i class='fa fa-sort-"+ordenMarca.toLocaleLowerCase()+" fa-2x' id='iconoOrdenMarca'></i></button> Marca</th>" +
                                                  "<th><button class='btn btn-warning btn-sm' id='ordenarPorModelo' name='"+ordenModelo+"'><i class='fa fa-sort-"+ordenModelo.toLocaleLowerCase()+" fa-2x' id='iconoOrdenModelo'></i></button>Modelo</th>" +
                                                  "<th><button class='btn btn-warning btn-sm' id='ordenarPorDescripcion' name='"+ordenDescripcion+"'><i class='fa fa-sort-"+ordenDescripcion.toLocaleLowerCase()+" fa-2x' id='iconoOrdenDescripcion'></i></button>Descripcion</th>" +
                                                  "<th><button class='btn btn-warning btn-sm' id='ordenarPorFecha' name='"+ordenFecha+"'><i class='fa fa-sort-"+ordenFecha.toLocaleLowerCase()+" fa-2x' id='iconoOrdenFecha'></i></button>Fecha</th>" +
                                                  "<th>Imagen</th><th>Editar</th><th>Eliminar</th></tr></thead><tbody>");
                     for (var i = 0; i < articulos.length; i++) {
                         nuevoHtml = nuevoHtml.concat("<tr>");
                         nuevoHtml = nuevoHtml.concat("<td><a href='singleMarca/"+articulos[i].id_marca+"'>" + articulos[i].nombre_marca + "</a></td>");
                         nuevoHtml = nuevoHtml.concat("<td>" + articulos[i].modelo + "</td>");
                         nuevoHtml = nuevoHtml.concat("<td>" + articulos[i].descripcion + "</td>");
                         nuevoHtml = nuevoHtml.concat("<td>" + articulos[i].fecha + "</td>");
                         nuevoHtml = nuevoHtml.concat("<td> <img src='"+articulos[i].imagen+"' alt='imagen del articulo "+i+"' width='200' height='100'> </td>");
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