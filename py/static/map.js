var map;

var TRANSIT = 'TRANSIT'
var WALKING = 'WALKING'
var directionsService;
var directionsDisplays = []


function initMap() {
    var uluru = {lat: -25.363, lng: 131.044};
    directionsService = new google.maps.DirectionsService()
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 4,
        center: uluru
    });
    $("div#info").bind("DOMSubtreeModified",function(){
        $("div.adp-warnbox").remove();
    });
    /*var marker = new google.maps.Marker({
        position: uluru,
        map: map
    });*/
}


function load_path_url(response){
    var json = jQuery.parseJSON(response);
    var url = "https://www.google.ru/maps/dir/"
    for (var i = 0; i < json.length; i++){
        url += json[i].lat + ',' + json[i].lng + '/';
    }
    url += "data=!3m1!4b1!4m2!4m1!3e2?hl=ru";
    document.location.href = url;
}


function add_path_to_map(from, to, type, num){
    /*alert(from.lat)
    alert(from.lng)*/
    directionsDisplays[num] = new google.maps.DirectionsRenderer()
    directionsDisplays[num].setMap(map)
    //document.getElementBy("adp-warnbox").style.display='none'
    var request = {
        origin: new google.maps.LatLng(from.lat, from.lng),
        destination: new google.maps.LatLng(to.lat, to.lng),
        travelMode: type
    };
    directionsService.route(request, function(result, status) {
        if (status == 'OK') {
            //directionsDisplays[num].setPanel(document.getElementById('info'))
            //directionsDisplays[num].setDirections(result);
            var line = result.routes[0].overview_path

            var Path = new google.maps.Polyline({
                path: line,
                geodesic: true,
                strokeColor: '#FF0000',
                strokeOpacity: 1.0,
                strokeWeight: 2
            });
            Path.setMap(map)

        }
        else{
            alert(status);
        }
    });
    //alert("sosipisos");
}


function display_path(response){
    alert(response)
    var json = jQuery.parseJSON(response);
    markers = []
    for (var i = 1; i < json.length; i++){
        //alert("http://maps.google.com/mapfiles/kml/pal3/icon"+(i-1)+".png")
        add_path_to_map(json[i - 1], json[i], json[i - 1].type, i - 1);
        markers[i - 1] = new google.maps.Marker({
            position: new google.maps.LatLng(json[i-1].lat, json[i-1].lng),
            label: ''+i,
            map: map
        })
       // display_photo(json[i - 1]);
    }
    var marker = new google.maps.Marker({
            position: new google.maps.LatLng(json[json.length-1].lat, json[json.length-1].lng),
            label: ''+json.length,
            map: map
        })

    map.setCenter(marker.getPosition());
}
//data=!3m1!4b1!4m2!4m1!3e0
//data=!3m1!4b1!4m2!4m1!3e2

function display_photo(point){
    var contentString =
        //'<div id="content">'+
        '<img src="'+point.href+'"width="100" height="111">'
        //+'</div>';
   // alert(contentString);
    var infowindow = new google.maps.InfoWindow({
        content: contentString
    });
    var marker = new google.maps.Marker({
        position: new google.maps.LatLng(point.lat, point.lng),
        icon: undefined,
        map: map
    });
    var image = {
        url: point.href,
        // This marker is 20 pixels wide by 32 pixels high.
        size: new google.maps.Size(1, 1),
        // The origin for this image is (0, 0).
        origin: new google.maps.Point(0, 0),
        // The anchor for this image is the base of the flagpole at (0, 32).
        anchor: new google.maps.Point(0, 0),
    };
    marker.setIcon(image)
    map.setCenter(marker.getPosition());
    map.setZoom(12)
    //marker.addListener('click', function() {
    infowindow.open(map, marker);
    //});
}