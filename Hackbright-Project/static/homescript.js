"use strict"



// var map;

// function initMap() {

//       map = new google.maps.Map(document.getElementById('map'), {
//         center: pos,
//         zoom: 10
//       });
    


if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(function(position) {
        var pos = {
          lat: position.coords.latitude,
          lng: position.coords.longitude
        };

        $('#location').val(JSON.stringify(pos))

      })

        
  

  function handleLocationError(browserHasGeolocation, infoWindow, pos) {
    infoWindow.setPosition(pos);
    infoWindow.setContent(browserHasGeolocation ?
                          'Error: The Geolocation service failed.' :
                          'Error: Your browser doesn\'t support geolocation.');
    infoWindow.open(map);
  }
}







  

  







// var infoWindow;

//         infoWindow.setPosition(pos);
//         infoWindow.setContent('You are here.');
//         infoWindow.open(map);
//         map.setCenter(pos);
//       }, function() {
//         handleLocationError(true, infoWindow, map.getCenter());
//       });
//     } else {
//       // Browser doesn't support Geolocation
//       handleLocationError(false, infoWindow, map.getCenter());
//     }


