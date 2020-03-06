"use strict"

var allButtonsOnPage = document.querySelectorAll('.button');

allButtonsOnPage.forEach(function(button) {
  button.addEventListener('click', function() {
    id = this.id
    
    const formInputs = {
      'event_id': id
    }

    $.post('/saveevents', formInputs, (res) => {
      console.log('Event has been saved!');
    })
  });
});


$('.button').on('click',function() {
  $(this).find("i").toggleClass("far fas selected-heart border-heart");
  });


var eventsToGet = $('#eventlist').html()

console.log(events)


function initMap() {

 
var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 15,
  });

var locations = events
console.log(locations)

var infowindow = new google.maps.InfoWindow();

var marker, i;
var markers = new Array();

for (i = 0; i < locations.length; i++) {  
  marker = new google.maps.Marker({
    position: new google.maps.LatLng(locations[i][2], locations[i][3]),
    animation: google.maps.Animation.DROP,
    map: map
  });

  markers.push(marker);


  google.maps.event.addListener(marker, 'click', (function(marker, i) {
    return function() {
      infowindow.setContent('<div id="content">' + "EVENT: " + locations[i][0] + '<br>' + 
  "VENUE: " + locations[i][1] + '<br>' +  "DATE: " + locations[i][5] + '<br>' + "TIME: " +
  locations[i][6] + "<br>" + "URL: " + "<a href=" + locations[i][7] + ">Buy Tickets</a>")

  infowindow.open(map, marker);
 }
})(marker, i)); 


function AutoCenter() {
  //  Create a new viewpoint bound
  var bounds = new google.maps.LatLngBounds();
  //  Go through each...
  $.each(markers, function (index, marker) {
  bounds.extend(marker.position);
  });
  //  Fit these bounds to the map
  map.fitBounds(bounds);
}
AutoCenter(); 

  }
}

