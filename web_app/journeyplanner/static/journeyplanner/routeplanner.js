
$(document).ready(function () {

  // flatpickr date https://flatpickr.js.org/options/
  $("#datepicker-tab1").flatpickr({
    altInput: true,
    altFormat: "F j, Y",
    dateFormat: 'yy-m-d',
    defaultDate: new Date(),
    minDate: "today"
  });

  // flatpickr time
  $('#timepicker-tab1').flatpickr({
    enableTime: true,
    defaultDate: new Date().getHours() + ":" + new Date().getMinutes(),
    dateFormat: 'H:i',
    noCalendar: true,
    time_24hr: true,
    minTime: "05:00",
    minuteIncrement: 1
  });

});

//using google map autocomplete for the address          
var input1 = document.getElementById('origin');
var input2 = document.getElementById("destination");
var options = { componentRestrictions: { country: "ie" }, types: ['geocode'] };
origin = new google.maps.places.Autocomplete(input1, options);
destination = new google.maps.places.Autocomplete(input2, options);

// function to create a marker for the bus station nearby from the user location 
function createMarker(place) {
  var marker = new google.maps.Marker({
    map: map,
    icon: "http://maps.google.com/mapfiles/ms/micons/bus.png",
    position: place.geometry.location
  });

  google.maps.event.addListener(marker, 'click', function () {
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
  var ending = destination.getPlace();

  //starting address latitude
  starting_lat = starting.geometry.location.lat();
  starting_lng = starting.geometry.location.lng();

  //destination address longitude   
  ending_lat = ending.geometry.location.lat();
  ending_lng = ending.geometry.location.lng();


  // Create a map and center it on starting point
  var map = new google.maps.Map(document.getElementById('map'), {
    //          zoom: 14,
    center: { lat: starting_lat, lng: starting_lng }
  });

  // Create a renderer for directions and bind it to the map.
  var directionsRenderer = new google.maps.DirectionsRenderer({ map: map });

  // Instantiate an info window to hold step text.
  var stepDisplay = new google.maps.InfoWindow;

  // Display the route between the initial start and end selections.
  calculateAndDisplayRoute(directionsRenderer, directionsService, markerArray, stepDisplay, map);
}


// calculating and showing the bus routes
function calculateAndDisplayRoute(directionsRenderer, directionsService, markerArray, stepDisplay, map) {

  // First, remove any existing markers from the map.
  for (var i = 0; i < markerArray.length; i++) {
    markerArray[i].setMap(null);
  }

  // Retrieve the start and end locations and create a DirectionsRequest using
  // Bus directions.
  directionsService.route({
    origin: document.getElementById('origin').value,
    destination: document.getElementById('destination').value,
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

        staringAddress = response.routes[0].legs[0].start_address;

        endingAddress = response.routes[0].legs[0].end_address;

        //trimming the origin address
        startingAddress = response.routes[0].legs[0].start_address;
        address1 = startingAddress.split(',');
        address1 = address1[0];

        //trimming the destination address
        endingAddress = response.routes[0].legs[0].end_address;
        address2 = endingAddress.split(',');
        address2 = address2[0];

        //getting the value of the user selected time
        // var time = $("#datetime-tab1").val();

        // var dateArr, date, dateElements, year, month, date, time, dateToDisplay;

        // dateArr = time.split('T');
        // date = dateArr[0];
        // dateElements = date.split('-');
        // year = dateElements[0];
        // month = dateElements[1];
        // date = dateElements[2];
        // dateToDisplay = date + "-" + month + "-" + year;

        // time = dateArr[1];

        $("#origin-tab1").html(address1);
        $("#destination-tab1").html(address2);
        // $("#datetime-tab").html(dateToDisplay + ", " + time);


        journeysteps = response.routes[0].legs[0].steps;

        var direction_text = $("#direction");

        for (var i = 0; i < journeysteps.length; i++) {
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

          var bus_details = []; //array to store each bus journey 
          var journey_steps = {}; //array for each bus steps in the journey

          // going through the repsone recieved from google
          var travelMode = journeysteps[i].travel_mode;


          //picture
          var bus = ("<img src=static/journeyplanner/icons/com.nextbus.dublin.jpg width=20 height=20>");
          var walking = ("<img src=static/journeyplanner/icons/walking.png width=20 height=20>");
          var road = ("<img src=static/journeyplanner/icons/road.png width=20 height=20>");

          // going through the object to get the travel mode details 

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
            distance = journeysteps[i].distance.text;
            //duration=journeysteps[i].duration.text
            instruction = journeysteps[i].instructions;
            Route_number = journeysteps[i].transit.line.short_name;
            arrival_stop = journeysteps[i].transit.arrival_stop.name;
            departure_stop = journeysteps[i].transit.departure_stop.name;
            num_stops = journeysteps[i].transit.num_stops;
            departure_latlng = journeysteps[i].start_location.lat() + ',' + journeysteps[i].start_location.lng();
            arrival_latlng = journeysteps[i].end_location.lat() + ',' + journeysteps[i].start_location.lng();

            //trimming the instruction text
            instruction = instruction.split(',');
            instruction = instruction[0];



            journey_steps["route_number"] = Route_number;
            journey_steps["arrival_stop"] = arrival_stop;
            journey_steps["departure_stop"] = departure_stop;
            journey_steps["num_stops"] = num_stops;
            journey_steps["departure_latlng"] = departure_latlng;
            journey_steps["arrival_latlng"] = arrival_latlng;

            // Append the dictionary made for each bus
            bus_details.push(journey_steps);

            //turning the list into a json
            bus_details = JSON.stringify(bus_details);

            // sending a post request to the server
            $.ajax({
              type: "POST",
              url: "planner/",
              data: { bus_details },
              sucess: function () {
                alert("successfully posted")

              }
            })

            direction_text.append('<li>' + bus + '&nbsp;&nbsp;' + instruction + '</p><p>' + road + '&nbsp;&nbsp;<b>Route:&nbsp;</b>' + Route_number + '&nbsp;&nbsp;<b>Stops:&nbsp;</b>' + num_stops + '&nbsp;stops&nbsp;&nbsp;<b>Duration:</b>' + duration + '</li>');

          };
        };

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

  $('#go').on('click', function () {
    var time, date, datetimeValue;
    // use different variables for date and time depending on screen size
      if ($(window).width() < 992) {
        datetimeValue = $("#datetime-tab1").val();
        var arr = datetimeValue.split('T');
        date = arr[0];
        console.log("mobile date: " + date);
        time = arr[1];
      } else {
        var date = $("#datepicker-tab1").val();
        console.log("desktop date: " + date);
        time = $('#timepicker-tab1').val();
        console.log("desktop time: " + time);

        // use date and time here to make properly formatted datetimeValue for mobile
        datetimeValue = date + 'T' + time;
      }
      // show date and time inputs on desktop results page for better user experience
      // default date and time are those selected by user on input page
      $("#datepicker-tab1-results-date").flatpickr({
        altInput: true,
        altFormat: "F j, Y",
        dateFormat: 'yy-m-d',
        defaultDate: date,
        minDate: "today",
        onClose: function (selectedDates, dateStr, instance) {
          // sendDateTimeChangePostRequest();
          console.log("on close date tab1");
      },
      });

      $('#datepicker-tab1-results-time').flatpickr({
        enableTime: true,
        defaultDate: time,
        dateFormat: 'H:i',
        noCalendar: true,
        time_24hr: true,
        minTime: "05:00",
        minuteIncrement: 1,
        onClose: function (selectedDates, dateStr, instance) {
          // sendDateTimeChangePostRequest();
          console.log("on close time tab1");
      },
      });

    
    $(".datetime").val(datetimeValue);

    // convert time to seconds since midnight
    console.log("time: " + time);
    var timeSplit = time.split(':');
    var timeSeconds = (+timeSplit[0]) * 60 * 60 + (+timeSplit[1]) * 60;
    console.log(timeSeconds);

    // show results and routes
    routes();
    $(".form-area").hide();
    if ($(window).width() < 992) {
      $("#map-interface").css("top", "300px");
    }
    $("#route-results").show();


  });

  // add on click to edit-journey button to hide results and show journey planner
  $('#edit-journey').on('click', function () {
    $(".form-area").show();
    $("#map-interface").css("top", "0px");
    $("#route-results").hide();
  });
});



