"use strict"


function initMap() {
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 11
    });
    setMarkers(map);
}

// Data for the markers consisting of a name, a LatLng and a zIndex for the
// order in which these markers should display on top of each other.

var locations = {{ events | tojson }};

console.log(locations)
 

function setMarkers(map) {
    // Adds markers to the map.
    for (var i = 0; i < stores.length; ++i) {
        var store = stores[i];
        var marker = new google.maps.Marker({
            position: {
                lat: store[1],
                lng: store[2]
            },
            map: map,
            animation: google.maps.Animation.DROP,
            title: store[0],
            zIndex: store[3],
        });
        attachStoreTitle(marker);
    }
}

// Attaches an info window to a marker with the provided message. When the
// marker is clicked, the info window will open with the secret message.
function attachStoreTitle(marker, storeName) {
    var infowindow = new google.maps.InfoWindow({
        content: marker.title
    });

    marker.addListener('click',
        function() {
            infowindow.open(marker.get('map'), marker);
        });
}
