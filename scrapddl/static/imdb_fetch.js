function fetch_imdb_rating(slug, title, container_class){
    var url = "imdb/" + slug + "/?title=" + title ;
    $.get( url, function( data ) {
        $( container_class + slug ).html( data );
    });
}