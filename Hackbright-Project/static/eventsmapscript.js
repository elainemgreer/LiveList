"use strict"

var eventsToGet = $('#eventlist').html()
var pos = $('#position').html()
var pos2 = $('#position2').html()

function initMap() {

var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 15,
    center: new google.maps.LatLng(currentuserlat, currentuserlng),
    styles: [
  {
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#f5f5f5"
      }
    ]
  },
  {
    "elementType": "labels.icon",
    "stylers": [
      {
        "visibility": "off"
      }
    ]
  },
  {
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#616161"
      }
    ]
  },
  {
    "elementType": "labels.text.stroke",
    "stylers": [
      {
        "color": "#f5f5f5"
      }
    ]
  },
  {
    "featureType": "administrative.land_parcel",
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#bdbdbd"
      }
    ]
  },
  {
    "featureType": "poi",
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#eeeeee"
      }
    ]
  },
  {
    "featureType": "poi",
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#757575"
      }
    ]
  },
  {
    "featureType": "poi.park",
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#e5e5e5"
      }
    ]
  },
  {
    "featureType": "poi.park",
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#9e9e9e"
      }
    ]
  },
  {
    "featureType": "road",
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#ffffff"
      }
    ]
  },
  {
    "featureType": "road.arterial",
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#757575"
      }
    ]
  },
  {
    "featureType": "road.highway",
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#dadada"
      }
    ]
  },
  {
    "featureType": "road.highway",
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#616161"
      }
    ]
  },
  {
    "featureType": "road.local",
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#9e9e9e"
      }
    ]
  },
  {
    "featureType": "transit.line",
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#e5e5e5"
      }
    ]
  },
  {
    "featureType": "transit.station",
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#eeeeee"
      }
    ]
  },
  {
    "featureType": "water",
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#c9c9c9"
      }
    ]
  },
  {
    "featureType": "water",
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#9e9e9e"
      }
    ]
  }
]
  });


var locations = events
console.log(locations)

var currentmarker = new google.maps.Marker({
    position: new google.maps.LatLng(currentuserlat, currentuserlng),
    map: map,
    icon: {
      path: fontawesome.markers.MAP_PIN,
      scale: 0.5,
      strokeWeight: 1.0,
      strokeColor: '#ffc815',
      strokeOpacity: 0.5,
      fillColor: '#ffc815',
      fillOpacity: .8,
      },
  });

var currentcontentString = 'You are here';

var currentinfowindow = new google.maps.InfoWindow({
 content: currentcontentString
 });
  
currentinfowindow.open(map, currentmarker);
 
google.maps.event.addListener(currentmarker, 'mouseover', function() {
});   

var infowindow = new google.maps.InfoWindow();

var marker, i;
var markers = new Array();

for (i = 0; i < locations.length; i++) {  
  marker = new google.maps.Marker({
    position: new google.maps.LatLng(locations[i][2], locations[i][3]),
    animation: google.maps.Animation.DROP,
    map: map,
    icon: {
        path: fontawesome.markers.MAP_PIN,
        scale: 0.4,
        strokeWeight: 0.6,
        strokeColor: '#585858',
        strokeOpacity: 0.8,
        fillColor: '#585858',
        fillOpacity: 0.9,
    },
  });

  markers.push(marker);

  markers.push(currentmarker);


  google.maps.event.addListener(marker, 'mouseover', (function(marker, i) {
    return function() {
      infowindow.setContent('<div id="content">' + "EVENT: " + locations[i][0] + '<br>' + 
  "VENUE: " + locations[i][1] + '<br>' +  "DATE: " + locations[i][5] + '<br>' + "URL: " + "<a href=" + locations[i][7] + ">Buy Tickets</a>")

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

