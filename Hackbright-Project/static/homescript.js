"use strict"


var map;

function initMap() {

// all dealing with POS must happen INSIDE this function, which must happen INSIDE initmap function!!!
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(function(position) {
        var pos = {
          lat: position.coords.latitude,
          lng: position.coords.longitude
        };

        $('#location').val(JSON.stringify(pos))


        //create map and set to user's position
        map = new google.maps.Map(document.getElementById('map'), {
        center: pos,
        zoom: 10

      });

      //set infowindow content
      var contentString = 'You are here!';
      var infowindow = new google.maps.InfoWindow({
       content: contentString
       });

      //set marker
      var marker = new google.maps.Marker({
        position: pos,
        map: map,
        title: 'marker with infoWindow'
   });

      //event listener so infowindow opens on user click
      marker.addListener('click', function() {
               infowindow.open(map, marker);


      })
})


     
   




  

  function handleLocationError(browserHasGeolocation, infoWindow, pos) {
    infoWindow.setPosition(pos);
    infoWindow.setContent(browserHasGeolocation ?
                          'Error: The Geolocation service failed.' :
                          'Error: Your browser doesn\'t support geolocation.');
    infoWindow.open(map);
  }

}}




  

  



