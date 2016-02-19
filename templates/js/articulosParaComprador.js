 $(document).ready(function() {
      var page=1;

     $("#previa1").click(function(){
         if(page!=1){
            page = page -1;
            llamadoAjax();
         }
         $("#titulo").focus();
     });

     $("#siguiente1").click(function(){
         var cantidadPaginas = $("#cantidadPaginas").val();
         if(page<cantidadPaginas){
            page = page +1;
            llamadoAjax();
         }
         $("#titulo").focus();
     });

     $("#previa2").click(function(){
         if(page!=1){
            page = page -1;
            llamadoAjax();
         }
         $("#titulo").focus();
     });

     $("#siguiente2").click(function(){
         var cantidadPaginas = $("#cantidadPaginas").val();
         if(page<cantidadPaginas){
            page = page +1;
            llamadoAjax();
         }
         $("#titulo").focus();
     });

     function llamadoAjax() {
         $.ajax({
             url: 'articulosParaComprador',
             type: 'get',
             dataType: "json",
             data: {
                 page: page,
                 csrfmiddlewaretoken: '{{ csrf_token }}'
             },
             success: function (data) {
                 $("#infoPagActual").text("Pagina " + data["page"] + " de " + data["cantPaginas"]);
                 $("#infoPagActual2").text("Pagina " + data["page"] + " de " + data["cantPaginas"]);
                 habYdeshabBotones(data["page"], data["cantPaginas"]);
                 var marcas = JSON.parse(data["marcas"]);
                 var myNode = document.getElementById("datosMarcas");
                 if (marcas.length == 0) {
                     $("#datosMarcas").hide();
                     $("#infoPagActual1").text("Ningun articulo posee tales filtros");
                     $("#infoPagActual2").text("Ningun articulo posee tales filtros");
                 }
                 else {
                     $("#datosMarcas").show();
                     $("#datosMarcas").css('visibility', 'visible');
                     myNode.innerHTML = '';
                     var nuevoHtml = "";
                     for (var i = 0; i < marcas.length; i++) {
                         nuevoHtml = nuevoHtml.concat("<div class='collection-section wow bounceInLeft' data-wow-delay='0.4s'><div class='container'><div class='collection-main' id='bordeadaPuntos'>" +
                        "<div class='col-md-4 collection-text'>");
                         nuevoHtml = nuevoHtml.concat("<h2>"+marcas[i].nombre+"</h2>");
                         nuevoHtml = nuevoHtml.concat("<h4><img src='"+marcas[i].imagen+"' alt='imagen de marca "+marcas[i].nombre+"' width='270' height='130'> </h4>");
                         nuevoHtml = nuevoHtml.concat("<p>"+marcas[i].descripcion+"</p>");
                         nuevoHtml = nuevoHtml.concat("<a class='read' href='singleMarca/"+marcas[i].pk+"'>Detalles de la Marca</a>");
                         nuevoHtml = nuevoHtml.concat("</div>");
                         nuevoHtml = nuevoHtml.concat("<div class='col-md-8 collection-images' id='bordeada'>");
                         nuevoHtml = nuevoHtml.concat("<h3>Coleccion "+marcas[i].nombre+"</h3>");
                         if(marcas[i].articulos.length>0){
                             for (var j = 0; j < marcas[i].articulos.length; j++) {
                                 nuevoHtml = nuevoHtml.concat("<div class='col-md-4 collection-images-grid'>");
                                 nuevoHtml = nuevoHtml.concat("<img src='"+marcas[i].articulos[j].imagen.url+"' style='margin-top: 30px;' alt='imagen de articulo "+j+" de "+marcas[i].nombre+" width='200' height='150'>");
                                 nuevoHtml = nuevoHtml.concat("<h4>"+marcas[i].articulos[j].modelo+"</h4>");
                                 nuevoHtml = nuevoHtml.concat("<a class='read one' href='single/"+ marcas[i].articulos[j].id+"'> Leer mas</a></div>");
                             }
                         }else{
                             nuevoHtml = nuevoHtml.concat("No existen articulos de la marca por el momento.");
                         }
                         nuevoHtml = nuevoHtml.concat("</div><div class='clearfix'></div></div></div>");
                     }
                     document.getElementById("datosMarcas").innerHTML = nuevoHtml;
                 }


             },
             error: function (xhr, errmsg, err) {

             }
         });
     }
 });

 function habYdeshabBotones(numPage, cantPaginas){
     if(numPage=="1"){
         $("#previa1").hide();
         $("#previa2").hide();
     }
     else{
         $("#previa1").show();
         $("#previa1").css('visibility', 'visible');
         $("#previa2").show();
         $("#previa2").css('visibility', 'visible');
     }

     if(numPage==cantPaginas){
         $("#siguiente1").hide();
         $("#siguiente2").hide();
     }
     else{
         $("#siguiente1").show();
         $("#siguiente1").css('visibility', 'visible');
         $("#siguiente2").show();
         $("#siguiente2").css('visibility', 'visible');
     }
 }