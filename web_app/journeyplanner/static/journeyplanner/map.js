// code for map from https://developers.google.com/maps/documentation/javascript/tutorial
var map;
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
var current = {lat: 53.3155395,lng: -6.4161858 };
    
//using google map autocomplete for the address          
var input1 = document.getElementById('origin');
var input2= document.getElementById("destination");
var options = { componentRestrictions: {country: "ie"},types: ['geocode']};
origin = new google.maps.places.Autocomplete(input1,options);
destination = new google.maps.places.Autocomplete(input2,options);

          
//showing the map
map = new google.maps.Map(
document.getElementById('map'), {center: current, zoom: 16});
	
          
// marker for the current location 
var current1 = new google.maps.Marker({
position:current,
map: map,
title: "You are here!"});
          
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
	

// function to create a marker for the bus station nearby from the user location 
function createMarker(place) {
var marker = new google.maps.Marker({
          map: map,
          icon:"http://maps.google.com/mapfiles/ms/micons/bus.png",
          position: place.geometry.location
        });

google.maps.event.addListener(marker, 'click', function() {
infowindow.setContent(place.name);
infowindow.open(map, this);
        });
      }
		
    
//the starting location   
var starting_lat; 
var starting_lng;
    
// destination location 
var ending_lat;
var ending_lng;



// The routes function that shows the route 
function routes() {
    var markerArray = [];
              
    //getting the lat and lng of the input address 
    var starting = origin.getPlace();
    var ending= destination.getPlace();
        
    //starting address latitude
    starting_lat = starting.geometry.location.lat();
    starting_lng= starting.geometry.location.lng();
        
    //destination address longitude   
     ending_lat=ending.geometry.location.lat();
     ending_lng=ending.geometry.location.lng();
        
         
    // Create a map and center it on Manhattan.
    var map = new google.maps.Map(document.getElementById('map'), {
    //          zoom: 14,
              center: {lat: starting_lat, lng: starting_lng}
            });
        
    // Create a renderer for directions and bind it to the map.
    var directionsRenderer = new google.maps.DirectionsRenderer({map: map});
    
    // Instantiate an info window to hold step text.
    var stepDisplay = new google.maps.InfoWindow;
    
    // Display the route between the initial start and end selections.
     calculateAndDisplayRoute( directionsRenderer, directionsService, markerArray, stepDisplay, map);}
            
            
            
            
    // calculating and showing the bus routes
    function calculateAndDisplayRoute(directionsRenderer, directionsService, markerArray, stepDisplay, map) {
        
    // First, remove any existing markers from the map.
    for (var i = 0; i < markerArray.length; i++) {
              markerArray[i].setMap(null);}
    
    // Retrieve the start and end locations and create a DirectionsRequest using
        
     // Bus directions.
     directionsService.route({
    origin: document.getElementById('origin').value,
    destination: document.getElementById('destination').value,
              travelMode: 'TRANSIT',
              transitOptions: {
                modes: ['BUS'],
      } }, 
        function(response, status) {
        // Route the directions and pass the response to a function to create
         
        // markers for each step.
         if (status === 'OK') {
        //  document.getElementById('warnings-panel').innerHTML =
        //             '<b>' + response.routes[0].warnings + '</b>';
         directionsRenderer.setDirections(response);
         showSteps(response, markerArray, stepDisplay, map);
          } else {
                window.alert('Directions request failed due to ' + status);
              }
            });
          }
    
    
     function showSteps(directionResult, markerArray, stepDisplay, map) {
     // For each step, place a marker, and add the text to the marker's infowindow.
     // Also attach the marker to an array so we can keep track of it and remove it
     // when calculating new routes.
    var myRoute = directionResult.routes[0].legs[0];
    for (var i = 0; i < myRoute.steps.length; i++) {
         var marker = markerArray[i] = markerArray[i] || new google.maps.Marker;
              marker.setMap(map);
              marker.setPosition(myRoute.steps[i].start_location);
              attachInstructionText(
                  stepDisplay, marker, myRoute.steps[i].instructions, map);}}
         
    
     function attachInstructionText(stepDisplay, marker, text, map) {
       google.maps.event.addListener(marker, 'click', function() {
    // Open an info window when the marker is clicked on, containing the text
    // of the step.
        stepDisplay.setContent(text);
        stepDisplay.open(map, marker);
            });
          }	  
          
// when the user click the go button, the route function runs 
$(function(){
  $('#go').on('click', function(){
     routes();
  });
});

