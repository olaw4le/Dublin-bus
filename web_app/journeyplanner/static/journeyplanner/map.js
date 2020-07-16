// code for map from https://developers.google.com/maps/documentation/javascript/tutorial
var map;
var service;
var infowindow;
var directionsService
var origin;
var destination;
var directionsRenderer;
var markerArray;

//loading the ui map.This is the function that loads when the opens the page 
function initMap() {

    // Instantiate a directions service.
    directionsService = new google.maps.DirectionsService;

    //the current location 
    var current = { lat: 53.3155395, lng: -6.4161858 };

    // //using google map autocomplete for the address          
    // var input1 = document.getElementById('origin');
    // var input2 = document.getElementById("destination");
    // var options = { componentRestrictions: { country: "ie" }, types: ['geocode'] };
    // origin = new google.maps.places.Autocomplete(input1, options);
    // destination = new google.maps.places.Autocomplete(input2, options);


    //showing the map
    map = new google.maps.Map(
        document.getElementById('map'), { center: current, zoom: 16 });


    // marker for the current location 
    var current1 = new google.maps.Marker({
        position: current,
        map: map,
        title: "You are here!"
    });

    infowindow = new google.maps.InfoWindow();

    // request to find the nearest bus station 
    var request = {
        location: current,
        radius: '500',
        type: ['transit_station']
    };

    service = new google.maps.places.PlacesService(map);
    service.nearbySearch(request, callback);
}

function callback(results, status) {
    if (status == google.maps.places.PlacesServiceStatus.OK) {
        for (var i = 0; i < results.length; i++) {
            createMarker(results[i]);
        }
    }
}

// Removes the markers from the map, but keeps them in the array.
function clearMarkers() {
    setMapOnAll(null);
  }

$("#nav-tab").click(clearMarkers)
$("#leap-tab").click(clearMarkers)
$("#tourist-tab").click(clearMarkers)

