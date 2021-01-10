function initMap(){
    var myPos = {lat:37.983810, lng: 23.727539};
    var mapOptions = {
        zoom: 8,
        center: myPos,
        mapTypeId: 'satellite'
    };
    
    var map = new google.maps.Map(document.getElementById('map'), mapOptions);

    var events = '{{events}}';
    
    new google.maps.Marker({
       position: myPos,
        map,
        title: hello
    });


}

function myFunction() {
    new google.maps.Marker({
        position: {lat:40.000, lng: 35.000},
        map,
        title: marker
    });
}

