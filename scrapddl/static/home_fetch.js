function fetch_home_section(section, container_class){
    var url = section + "-home" ;
    $.get( url, function( data ) {
        $( container_class ).html( data );
    });
}