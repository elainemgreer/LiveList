"use strict"


var map;
function initMap() {

if (navigator.geolocation) {
navigator.geolocation.getCurrentPosition(function(position) {
   var currentpos = {
       lat: position.coords.latitude,
       lng: position.coords.longitude
   };
   var map = new google.maps.Map(document.getElementById('map'), {
       // center: ,
       zoom: 14,
   });

   var contentString = 'Your location';
   var infowindow = new google.maps.InfoWindow({
       content: contentString
   });

   var marker = new google.maps.Marker({
        position: currentpos,
        map: map,
        title: 'marker with infoWindow'
   });}
   marker.addListener('click', function() {
       infowindow.open(map, marker);

//Handle errors if browser doesn't support geolocation

}, function() {
     handleLocationError(true, infoWindow, map.getCenter());
});

} else {
    // Browser doesn't support Geolocation
    handleLocationError(false, infoWindow, map.getCenter());
}
}

function handleLocationError(browserHasGeolocation, infoWindow, pos) {
infoWindow.setPosition(pos);
infoWindow.setContent(browserHasGeolocation ?
                    'Error: The Geolocation service failed.' :
                    'Error: Your browser doesn\'t support geolocation.');
}


