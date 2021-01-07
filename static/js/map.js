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
        title: hello,
    });

    alert(5+6);



}
document.getElementById("test2").addEventListener("onclick", myFunction);

function myFunction() {
    document.write("hello");
}

