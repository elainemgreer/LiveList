
"use strict"


var map;
function initMap() {

      // var map = new google.maps.Map(document.getElementById('map'), {
      // // zoom: 50,
      // // center: new google.maps.LatLng(51.530616, -0.123125),
      // // mapTypeId: google.maps.MapTypeId.ROADMAP
      var map = new google.maps.Map(document.getElementById('map'), {
          center: {lat: 40.674, lng: -73.945},
          zoom: 12,
          // styles: [
          //   {elementType: 'geometry', stylers: [{color: '#242f3e'}]},
          //   {elementType: 'labels.text.stroke', stylers: [{color: '#242f3e'}]},
          //   {elementType: 'labels.text.fill', stylers: [{color: '#746855'}]},
          //   {
          //     featureType: 'administrative.locality',
          //     elementType: 'labels.text.fill',
          //     stylers: [{color: '#d59563'}]
          //   },
          //   {
          //     featureType: 'poi',
          //     elementType: 'labels.text.fill',
          //     stylers: [{color: '#d59563'}]
          //   },
          //   {
          //     featureType: 'poi.park',
          //     elementType: 'geometry',
          //     stylers: [{color: '#263c3f'}]
          //   },
          //   {
          //     featureType: 'poi.park',
          //     elementType: 'labels.text.fill',
          //     stylers: [{color: '#6b9a76'}]
          //   },
          //   {
          //     featureType: 'road',
          //     elementType: 'geometry',
          //     stylers: [{color: '#38414e'}]
          //   },
          //   {
          //     featureType: 'road',
          //     elementType: 'geometry.stroke',
          //     stylers: [{color: '#212a37'}]
          //   },
          //   {
          //     featureType: 'road',
          //     elementType: 'labels.text.fill',
          //     stylers: [{color: '#9ca5b3'}]
          //   },
          //   {
          //     featureType: 'road.highway',
          //     elementType: 'geometry',
          //     stylers: [{color: '#746855'}]
          //   },
          //   {
          //     featureType: 'road.highway',
          //     elementType: 'geometry.stroke',
          //     stylers: [{color: '#1f2835'}]
          //   },
          //   {
          //     featureType: 'road.highway',
          //     elementType: 'labels.text.fill',
          //     stylers: [{color: '#f3d19c'}]
          //   },
          //   {
          //     featureType: 'transit',
          //     elementType: 'geometry',
          //     stylers: [{color: '#2f3948'}]
          //   },
          //   {
          //     featureType: 'transit.station',
          //     elementType: 'labels.text.fill',
          //     stylers: [{color: '#d59563'}]
          //   },
          //   {
          //     featureType: 'water',
          //     elementType: 'geometry',
          //     stylers: [{color: '#17263c'}]
          //   },
          //   {
          //     featureType: 'water',
          //     elementType: 'labels.text.fill',
          //     stylers: [{color: '#515c6d'}]
          //   },
          //   {
          //     featureType: 'water',
          //     elementType: 'labels.text.stroke',
          //     stylers: [{color: '#17263c'}]
          //   }
          // ]
        });
    
      

  

    var locations = {{ event_locations | tojson }}; 
    console.log(locations)



    // var map = new google.maps.Map(document.getElementById('map'), {
    //   zoom: 10,
    //   // center: new google.maps.LatLng(51.530616, -0.123125),
    //   mapTypeId: google.maps.MapTypeId.ROADMAP
    // });

    var infowindow = new google.maps.InfoWindow();

    var marker, i;
    var markers = new Array();

    for (i = 0; i < locations.length; i++) {  
      marker = new google.maps.Marker({
        position: new google.maps.LatLng(locations[i][2], locations[i][3]),
        map: map
      });

      markers.push(marker);

      google.maps.event.addListener(marker, 'click', (function(marker, i) {
        return function() {
          infowindow.setContent(locations[i][0], locations[i][1]);
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

  





