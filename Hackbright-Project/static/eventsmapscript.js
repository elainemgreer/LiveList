"use strict"


var eventsToGet = $('#eventlist').html()
var pos = $('#position').html()
var pos2 = $('#position2').html()
console.log(pos)
console.log(currentuserlat)
console.log(currentuserlng)

console.log(events)


function initMap() {

 
var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 15,
    center: new google.maps.LatLng(currentuserlat, currentuserlng),
  });

var locations = events
console.log(locations)


var currentmarker = new google.maps.Marker({
    position: new google.maps.LatLng(currentuserlat, currentuserlng),
    map: map
  });

var currentcontentString = 'You are here!';

var currentinfowindow = new google.maps.InfoWindow({
 content: currentcontentString
 });
  
currentinfowindow.open(map, currentmarker);
 
google.maps.event.addListener(currentmarker, 'click', function() {
});   

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

  markers.push(currentmarker);

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

