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
window.setInterval(function () {
	$("#map-interface").zIndex(1000);
}, 500);
//loading the ui map.This is the function that loads when the opens the page 
function initMap() {

	geocoder = new google.maps.Geocoder();

	infowindow = new google.maps.InfoWindow();

	// Instantiate a directions service.
	directionsService = new google.maps.DirectionsService;

	directionsDisplay = new google.maps.DirectionsRenderer({
		map: map
	})

	//the current location 
	// var dublin = { lat: 53.349424, lng: -6.260452};

	var dublin = {
		lat: 53.349424,
		lng: -6.363448826171867
	};


	//showing the map
	map = new google.maps.Map(
		document.getElementById('map'), {
			center: dublin,
			zoom: 12,
			bounds_changed: function () {

				$("#map-interface").zIndex(5000);
			},
			idle: function () {

				$("#map-interface").zIndex(5000);
			},
			zoom_changed: function () {

				$("#map-interface").zIndex(5000);
			},
			styles: [{
					"featureType": "administrative.land_parcel",
					"elementType": "all",
					"stylers": [{
						"visibility": "off"
					}]
				},
				{
					"featureType": "landscape.man_made",
					"elementType": "all",
					"stylers": [{
						"visibility": "off"
					}]
				},
				{
					"featureType": "poi",
					"elementType": "labels",
					"stylers": [{
						"visibility": "off"
					}]
				},
				{
					"featureType": "poi",
					"elementType": "labels.text",
					"stylers": [{
						"visibility": "on"
					}]
				},
				{
					"featureType": "poi.park",
					"elementType": "geometry.fill",
					"stylers": [{
						"lightness": "-18"
					}]
				},
				{
					"featureType": "poi.park",
					"elementType": "labels.text.fill",
					"stylers": [{
						"visibility": "on"
					}]
				},
				{
					"featureType": "road",
					"elementType": "labels",
					"stylers": [{
							"visibility": "simplified"
						},
						{
							"lightness": 20
						}
					]
				},
				{
					"featureType": "road.highway",
					"elementType": "geometry",
					"stylers": [{
						"hue": "#f49935"
					}]
				},
				{
					"featureType": "road.highway",
					"elementType": "labels",
					"stylers": [{
						"visibility": "simplified"
					}]
				},
				{
					"featureType": "road.arterial",
					"elementType": "geometry",
					"stylers": [{
						"hue": "#fad959"
					}]
				},
				{
					"featureType": "road.arterial",
					"elementType": "labels",
					"stylers": [{
						"visibility": "off"
					}]
				},
				{
					"featureType": "road.local",
					"elementType": "geometry",
					"stylers": [{
						"visibility": "simplified"
					}]
				},
				{
					"featureType": "road.local",
					"elementType": "labels",
					"stylers": [{
						"visibility": "simplified"
					}]
				},
				{
					"featureType": "transit",
					"elementType": "all",
					"stylers": [{
						"visibility": "off"
					}]
				},
				{
					"featureType": "transit",
					"elementType": "geometry.fill",
					"stylers": [{
						"lightness": "0"
					}]
				},
				{
					"featureType": "water",
					"elementType": "all",
					"stylers": [{
							"hue": "#a1cdfc"
						},
						{
							"saturation": 30
						},
						{
							"lightness": 49
						}
					]
				},
				{
					"featureType": "water",
					"elementType": "geometry.fill",
					"stylers": [{
						"lightness": "-16"
					}]
				}
			],
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
		navigator.geolocation.getCurrentPosition(function () {}, function () {});
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
		}, {
			timeout: 10000
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
	var latlng = {
		lat: parseFloat(lat),
		lng: parseFloat(lng)
	};
	geocoder.geocode({
		location: latlng
	}, function (results, status) {
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