// code for map from https://developers.google.com/maps/documentation/javascript/tutorial
var map;
var service;
var infowindow;
var directionsService
var origin;
var destination;
var directionsRenderer;
var markerArray;
var geocoder;
var geolocation = false;

//loading the ui map.This is the function that loads when the opens the page 
function initMap() {

    geocoder = new google.maps.Geocoder();

    // Instantiate a directions service.
    directionsService = new google.maps.DirectionsService;

    directionsDisplay = new google.maps.DirectionsRenderer({
        map: map})

    //the current location 
    var dublin = { lat: 53.3155395, lng: -6.4161858 };

    //showing the map
    map = new google.maps.Map(
        document.getElementById('map'), {
        center: dublin,
        zoom: 12,
        mapTypeControlOptions: {
            style: google.maps.MapTypeControlStyle.HORIZONTAL_BAR,
            position: google.maps.ControlPosition.TOP_RIGHT
        }
    });
}

// function to get users geolocation
function getGeolocation(inputID) {
    geolocation = true;
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            var pos = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };

            starting_lat = pos.lat;
            starting_lng = pos.lng;


            // call geocoder function to convert coordinates to place name
            geocodeLatLng(geocoder, pos.lat, pos.lng, inputID);

        }, function () {
            handleLocationError(true, infoWindow, map.getCenter());
        });
    } else {
        // Browser doesn't support Geolocation
        handleLocationError(false, infoWindow, map.getCenter());
    }

    function handleLocationError(browserHasGeolocation, infoWindow, pos) {
        $('.geo-error').show();
        $('.geo-spinner').hide();
        infoWindow.setPosition(pos);
        infoWindow.setContent(browserHasGeolocation ?
            'Error: The Geolocation service failed.' :
            'Error: Your browser doesn\'t support geolocation.');
        infoWindow.open(map);
    };


}

// function to geocode geolocation coordinates into address
function geocodeLatLng(geocoder, lat, lng, inputID) {
    var latlng = { lat: parseFloat(lat), lng: parseFloat(lng) };
    geocoder.geocode({ location: latlng }, function (results, status) {
        if (status === "OK") {
            if (results[0]) {
                // populate origin input with geolocation 
                $('#' + inputID).val(results[0].formatted_address);
                $('.geo-spinner').hide();
            } else {
                window.alert("No results found");
            }
        } else {
            window.alert("Geocoder failed due to: " + status);
        }
    })
};

