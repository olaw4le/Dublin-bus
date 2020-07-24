var dublin = { lat: 53.349424, lng: -6.363448826171867 };

$(document).ready(function () {

    // remove tourist markers when user navigates to different tab using name spacing
    $(document).off('click.tourist');
    $(document).on('click.tourist', "#routeplanner-tab, #allroutes-tab, #tourist-tab, #tourist-nav, #routeplanner-nav, #allroutes-nav", function () {
        clearAllTouristMarkers(markers);
        removeLineFromTouristMap();
    });
    map.panTo(dublin)

    // hide destination box initially
    $('#destination-tourist').hide();

    // initialise all tooltips
    $(function () {
        $('[data-toggle="tooltip"]').tooltip()
    })

    // flatpickr date https://flatpickr.js.org/options/
    $("#datepicker-tourist").flatpickr({
        altInput: true,
        altFormat: "F j, Y",
        dateFormat: 'yy-m-d',
        defaultDate: new Date(),
        minDate: "today"
    });

    // flatpickr time
    $('#timepicker-tourist').flatpickr({
        enableTime: true,
        defaultDate: new Date().getHours() + ":" + new Date().getMinutes(),
        dateFormat: 'H:i',
        noCalendar: true,
        time_24hr: true,
        minuteIncrement: 1
    });

    var input1 = document.getElementById("origin-tourist");
    var options = { componentRestrictions: { country: "ie" }, types: ['geocode'] };
    origin = new google.maps.places.Autocomplete(input1, options);
    // hide error when content of origin input box changed
    $("#origin-tourist").on("input", function () {
        $('.geo-error').hide();
    });


    // call the geolocation function when button is clicked
    $('#geolocation-tourist').on('click', function () {
        getGeolocation('origin-tourist');
        $('.geo-spinner').show();
    });
});

// https://developers.google.com/maps/documentation/javascript/places


var markers = {};
var destination_latlng;
var name;
var infowindow;
var directionsRenderer;
var markerArray = [];

// loop through checkboxes and display markers on map using data attribute
$(".tourist-check").change(function () {
    if (this.checked) {
        var type = $(this).attr("data-type");
        console.log(type);

        // show spinner for clicked checkbox
        $('#' + type + '-spin').show();

        var request = {
            location: dublin,
            radius: '50000',
            type: type
        };

        service = new google.maps.places.PlacesService(map);
        service.nearbySearch(request, function (results, status) {
            callback(results, status, type)
        });

        // hide markers when checkbox un-checked
    } else if (!this.checked) {
        var type = $(this).attr("data-type");
        var typeMarkers = markers[type];
        clearMarkers(typeMarkers);

    }
});

//callback function which calls function to create markers
function callback(results, status, type) {
    if (status == google.maps.places.PlacesServiceStatus.OK) {
        $('#' + type + '-spin').hide();
        markers[type] = []
        for (var i = 0; i < results.length; i++) {
            var icon = results[i].icon
            var rating = results[i].rating;
            createMarker(results[i], icon, markers[type], rating);
        }
    }
}

// clear markers for a specific Place Type from map when checkbox un-checked
function clearMarkers(markers) {
    $.each(markers, function (index) {
        markers[index].setMap(null);
    });
}

// function to clear markers of all Place Types from tourist map
function clearAllTouristMarkers(markers) {
    for (var type in markers) {
        clearMarkers(markers[type]);
    }
}

function removeLineFromTouristMap() {
    if (directionsRenderer) {
        directionsRenderer.setDirections({ routes: [] });
    }
}

// create markers
function createMarker(place, icon, markerList, rating) {
    ending_lat = place.geometry.location.lat();
    ending_lng = place.geometry.location.lng();

    var icon = {
        url: icon,
        scaledSize: new google.maps.Size(30, 30),
    }
    var marker = new google.maps.Marker({
        map: map,
        icon: icon,
        position: place.geometry.location,
    });

    markerList.push(marker);

    console.log(place.name);


    // show name of place when mouse hovers over  marker
    google.maps.event.addListener(marker, 'mouseover', (function (placeName, rating) {
        return function () {
            console.log("inside event: " + placeName);
            infowindow.setContent(placeName + "<br>Rating: " + rating);
            infowindow.open(map, this);
        }
    })(place.name, rating));

    // populate destination input box with location clicked on map
    google.maps.event.addListener(marker, 'click', (function (placeName, ending_lat, ending_lng) {
        return function () {
            destination_latlng = new google.maps.LatLng(ending_lat, ending_lng);
            name = placeName;
            $('#destination-tourist').val(placeName);
            $('#destination-tourist').show();
            $('#tourist-destination-error').hide();
        }
    })(place.name, ending_lat, ending_lng));
}


infoWindow = new google.maps.InfoWindow;

var ending_lat;
var ending_lng;
var starting_lat;
var starting_lng;




// show route on map
function routes_tourist() {

    // clear tourist markers from map
    clearAllTouristMarkers(markers);


    if (!geolocation) {
        //getting the lat and lng of the input address 
        var starting = origin.getPlace();

        //starting address latitude
        var starting_lat = starting.geometry.location.lat();
        var starting_lng = starting.geometry.location.lng();
    }

    // center map at starting point
    var center = new google.maps.LatLng(starting_lat, starting_lng);
    // map.panTo(center);

    // Create a renderer for directions and bind it to the map.
    directionsRenderer = new google.maps.DirectionsRenderer({ map: map, preserveViewport: true });

    // Instantiate an info window to hold step text.
    var stepDisplay = new google.maps.InfoWindow;

    // Display the route between the initial start and end selections.
    calculateAndDisplayRoute(directionsRenderer, directionsService, markerArray, stepDisplay, map);
}


// calculating and showing the bus routes
function calculateAndDisplayRoute(directionsRenderer, directionsService, markerArray, stepDisplay, map) {

    // Retrieve the start and end locations and create a DirectionsRequest using
    // Bus directions.
    directionsService.route({
        origin: document.getElementById('origin-tourist').value,
        destination: destination_latlng,
        travelMode: 'TRANSIT',
        transitOptions: {
            modes: ['BUS'],
            routingPreference: 'FEWER_TRANSFERS',
        }
    },

        // showing the response received in a text format 
        function (response, status) {

            // markers for each step.
            if (status === 'OK') {

                //trimming the origin address
                startingAddress = response.routes[0].legs[0].start_address;
                address1 = startingAddress.split(',');
                address1 = address1[0];

                //trimming the destination address
                endingAddress = response.routes[0].legs[0].end_address;
                address2 = endingAddress.split(',');
                address2 = address2[0];

                // fill journey details into summary results
                $("#origin-tab1").html(address1);
                $("#destination-tab1").html(name);

                journeysteps = response.routes[0].legs[0].steps;

                var direction_text = $("#direction-tourist");

                
           // the route distance
           var distance = '';
  
           // the route instruction example (walk , take bus)
           var instruction = '';
  
           // the departing stop
           var departure_stop = '';
  
           // the arival stop	
           var arrival_stop = '';
  
           // the number of stops between arrival and departing stop
           var num_stops = '';
  
           // the walking duration , we will predict the bus one 
           var duration = '';
  
           // the bus number user take
           var Route_number = '';
  
           var arrival_latlng;
           var departure_latlng;
           var list=[]
           var list1=[]

           var datetimeValue = $("#datetime-tourist").val();
          var arr = datetimeValue.split('T');
          var date1 = arr[0];
          var input_time = arr[1];

          // convert time to seconds since midnight
          // console.log("time: "+ input_time);
          var timeSplit = input_time.split(':');
          var timeSeconds = (+timeSplit[0]) * 60 * 60 + (+timeSplit[1]) * 60;




  
  
  
          //  // going through the repsone recieved from google
          //  var travelMode = journeysteps[i].travel_mode;
  
          var journeyTime=0;
          for (var i = 0; i < journeysteps.length; i++) {
            
            // going through the repsone recieved from google
            var travelMode = journeysteps[i].travel_mode;
  
            // going through the object to get the travel mode details 
  
            if (travelMode == "WALKING") {
  
              duration = journeysteps[i].duration.text;
  
              journeyTime += parseInt(duration[0])
  
  
              console.log(journeyTime)
  
              //trimming the instruction text
              instruction = instruction.split(',');
              instruction = instruction[0];
  
  
            }
  
            else if (travelMode == "TRANSIT") {
              var journey_steps = {}; //dictionary for each bus steps in the journey
              distance = journeysteps[i].distance.text;
              //duration=journeysteps[i].duration.text
              instruction = journeysteps[i].instructions;
              Route_number = journeysteps[i].transit.line.short_name;
              arrival_stop = journeysteps[i].transit.arrival_stop.name;
              departure_stop = journeysteps[i].transit.departure_stop.name;
              num_stops = journeysteps[i].transit.num_stops;
              arrival_latlng = journeysteps[i].transit.arrival_stop.location.lat() + ',' + journeysteps[i].transit.arrival_stop.location.lng();
              departure_latlng = journeysteps[i].transit.departure_stop.location.lat() + ',' + journeysteps[i].transit.departure_stop.location.lng();
  
              //trimming the instruction text
              instruction = instruction.split(',');
              instruction = instruction[0];
  
  
  
              journey_steps["route_number"] = Route_number;
              journey_steps["arrival_stop"] = arrival_stop;
              journey_steps["departure_stop"] = departure_stop;
              journey_steps["num_stops"] = num_stops;
              journey_steps["departure_latlng"] = departure_latlng;
              journey_steps["arrival_latlng"] = arrival_latlng;


              list.push(journey_steps)
              list1.push(Route_number)

              //turning the data to sent into json
              var data = JSON.stringify(journey_steps);}
            }

            var data = JSON.stringify(list);

            console.log("data",list)
  
    
              var prediction=0;
              // sending a post request to the server
              $.ajax({
                type: "POST",
                url: "planner/",
                data: {
                  data,
                  date: date1,
                  time: timeSeconds,
                
                }
                
              })
             
                .done(function (response) {
                  prediction1 = JSON.parse(response)
                  console.log(prediction1) 

                  function bus_time(k){
             
                    return prediction1[k]
                    }

                    var number=0

                // adding the predicted time to the total time
                for (var j = 0; j < prediction1.length; j++){
              
                journeyTime+= parseInt(prediction1[j])
                console.log(journeyTime)
                    }
                  

                var b = input_time.split(':');
                var theFutureTime = moment().hour(b[0]).minute(b[1]).add(journeyTime,'minutes').format("HH:mm");
                console.log(theFutureTime)
// setting the total time and predicted arrival time in the html

                $("#duration-val-tourist").html(journeyTime +' mins')
                $("#journey-time").html(input_time+' - '+theFutureTime)

                

            for (var i = 0; i < journeysteps.length; i++) {

            var bus = ("<img src=static/journeyplanner/icons/com.nextbus.dublin.jpg width=25 height=25>");
            var walking = ("<img src=static/journeyplanner/icons/walking.png width=25 height=25>");
            var road = ("<img src=static/journeyplanner/icons/road.png width=25 height=25>");
                   
            // going through the repsone recieved from google
            var travelMode = journeysteps[i].travel_mode;
  
                  if (travelMode == "WALKING") {
                    
  
                    distance = journeysteps[i].distance.text;
                    duration = journeysteps[i].duration.text;
                    instruction = journeysteps[i].instructions;
        
                    //trimming the instruction text
                    instruction = instruction.split(',');
                    instruction = instruction[0];
        
                    direction_text.append('<li>' + walking + '&nbsp;&nbsp;' + instruction + '</p><p>' + road + '&nbsp;&nbsp;<b>Duration:</b>&nbsp;' + duration + '</li>');
        
                  }
        
                  else if (travelMode == "TRANSIT") {
                    var journey_steps = {}; //dictionary for each bus steps in the journey
                    distance = journeysteps[i].distance.text;


                    instruction = journeysteps[i].instructions;
                    Route_number = journeysteps[i].transit.line.short_name;
                    arrival_stop = journeysteps[i].transit.arrival_stop.name;
                    departure_stop = journeysteps[i].transit.departure_stop.name;
                    num_stops = journeysteps[i].transit.num_stops;
                    arrival_latlng = journeysteps[i].transit.arrival_stop.location.lat() + ',' + journeysteps[i].transit.arrival_stop.location.lng();
                    departure_latlng = journeysteps[i].transit.departure_stop.location.lat() + ',' + journeysteps[i].transit.departure_stop.location.lng();
      
                    //trimming the instruction text
                    instruction = instruction.split(',');
                    instruction = instruction[0];


                    
    


                    

                     
                      
                    direction_text.append('<li>' + bus + '&nbsp;&nbsp;' + instruction + '</p><p>' + road + '&nbsp;&nbsp;<b>Route:&nbsp;</b>' + Route_number + '&nbsp;&nbsp;<b>Stops:&nbsp;</b>' + num_stops + '&nbsp;stops&nbsp;&nbsp;<b>Duration:&nbsp</b>' +bus_time(number)+" mins"+'</li>');
   
                    number +=1
                }
                
              
              }
                
                console.log(number)
                }) 


                //showing the response on the map. 	 
                directionsRenderer.setDirections(response);
                showSteps(response, markerArray, stepDisplay, map);
            }
            else {
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
            stepDisplay, marker, myRoute.steps[i].instructions, map);
    }
}

function attachInstructionText(stepDisplay, marker, text, map) {
    google.maps.event.addListener(marker, 'click', function () {
        // Open an info window when the marker is clicked on, containing the text
        // of the step.
        stepDisplay.setContent(text);
        stepDisplay.open(map, marker);
    });
}


// when the user click the go button, the route function runs and the results div shows
$(function () {

    $('#go-tourist').on('click', function () {

        // display error if user does not select a destination on map
        if ($("#destination-tourist").is(":hidden")) {

            $('#tourist-destination-error').show();
        } else {

            var time, dateValue
            // use different variables for date and time depending on screen size
            if ($(window).width() < 992) {
                var dateValue = $("#datetime-tourist").val();
                var arr = dateValue.split('T');
                date = arr[0];
                time = arr[1];
            } else {
                dateValue = $("#datepicker-tourist").val();
                time = $('#timepicker-tourist').val();

                // show date and time inputs on desktop results page for better user experience
                // default date and time are those selected by user on input page
                $("#datepicker-tourist-results-date").flatpickr({
                    altInput: true,
                    altFormat: "F j, Y",
                    dateFormat: 'yy-m-d',
                    defaultDate: dateValue,
                    minDate: "today"
                });

                $('#datepicker-tourist-results-time').flatpickr({
                    enableTime: true,
                    defaultDate: time,
                    dateFormat: 'H:i',
                    noCalendar: true,
                    time_24hr: true,
                    minuteIncrement: 1
                });
            }

            // convert time to seconds since midnight
            var timeSplit = time.split(':');
            var timeSeconds = (+timeSplit[0]) * 60 * 60 + (+timeSplit[1]) * 60;

            // show results and routes
            routes_tourist();
            $(".form-area").hide();
            $("#checkbox-card").hide();
            if ($(window).width() < 992) {
                $("#map-interface").animate({ top: "400px" }, 400);
            }
            $("#route-results-tourist").show();

        }



    });

    // add on click to edit-journey button to hide results and show journey planner
    $('.edit-journey').on('click', function () {
        $("#checkbox-card").show();
        $(".form-area").show();
        if ($(window).width() < 992) {
            $("#map-interface").animate({ top: "400px" }, 400);
        }
        $("#route-results-tourist").hide();
    });
});



