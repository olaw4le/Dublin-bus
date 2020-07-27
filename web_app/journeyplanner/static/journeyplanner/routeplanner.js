$(document).ready(function () {

  // load twitter to display the twitter widget whenever this tab is clicked
  if (typeof twttr != 'undefined') {
    twttr.widgets.load();
  }

  // .off ensures onclicks are not added multiple times
  $(document).off("click.routes");

  // Remove routes on map when navigating to another tab
  $(document).on("click.routes", "#routeplanner-nav, .edit-journey, #allroutes-nav, #tourist-nav, #allroutes-tab, #tourist-tab, #routeplanner-tab",
    removeLineFromMap);

  // initialise tooltip for info regarding geolocation
  $(function () {
    $('[data-toggle="tooltip"]').tooltip()
  })

  // call geolocation function when button clicked
  $('#geolocation-routeplanner').on('click', function () {
    getGeolocation('origin');
    $('.geo-spinner').show();
  });

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
var origin;
var destination;

// prevent the enter button working on the autocomplete dropdown
// this is done to prevent the geolocation button underneath being selected when enter is clicked
$(".form-control").keydown(function (e) {
  if (e.keyCode == 13) {
    return false;
  }
});

// wait until google is loaded
function WhenGoogleLoadedDo(fnt) {
  if (typeof google != 'undefined')
    fnt();
  else
    setTimeout(function () {
      (function (fnt) {
        WhenGoogleLoadedDo(fnt)
      })(fnt)
    }, 500);
}

WhenGoogleLoadedDo(() => {
  origin = new google.maps.places.Autocomplete(input1, options);
  destination = new google.maps.places.Autocomplete(input2, options);
});

$("#origin").on("input", function () {
  $('.geo-error').hide();
});


// function to create a marker for the bus station nearby from the user location 
// function createMarker(place) {
//   var marker = new google.maps.Marker({
//     map: map,
//     icon: "http://maps.google.com/mapfiles/ms/micons/bus.png",
//     position: place.geometry.location
//   });

//   google.maps.event.addListener(marker, 'click', function () {
//     infowindow.setContent(place.name);
//     infowindow.open(map, this);
//   });
// }


//the starting location   
var starting_lat;
var starting_lng;

// destination location 
var ending_lat;
var ending_lng;
var directionsRenderer;
var allMarkers = [];

function removeLineFromMap() {
  if (directionsRenderer) {
    directionsRenderer.setDirections({ routes: [] });
  }
  // First, remove any existing markers from the map.
  console.log(allMarkers);
  if (allMarkers) {
    for (var i = 0; i < allMarkers.length; i++) {
      allMarkers[i].setMap(null);
    }
  }
}

// The routes function that shows the route 
function routes() {
  var markerArray = [];

  //getting the lat and lng of the input address 
  var starting = origin.getPlace();
  var ending = destination.getPlace();

  // display error to user if valid starting location not entered
  if (!starting) {
    $('.invalid-location-error').show();
    return false;
  } else {
    //starting address latitude
    starting_lat = starting.geometry.location.lat();
    starting_lng = starting.geometry.location.lng();
  }
  // display error to user if valid ending location not entered
  if (!ending) {
    $('.invalid-location-error').show();
    return false;
  } else {
    //destination address longitude   
    ending_lat = ending.geometry.location.lat();
    ending_lng = ending.geometry.location.lng();
  }

  // Create a map and center it on starting point

  // map.panTo(center);

  // Create a renderer for directions and bind it to the map.
  directionsRenderer = new google.maps.DirectionsRenderer({ map: map, preserveViewport: true });

  // Instantiate an info window to hold step text.
  var stepDisplay = new google.maps.InfoWindow;

  // Display the route between the initial start and end selections.
  calculateAndDisplayRoute(directionsRenderer, directionsService, markerArray, stepDisplay, map);
  return true;
}


// calculating and showing the bus routes
function calculateAndDisplayRoute(directionsRenderer, directionsService, markerArray, stepDisplay, map) {



  // Retrieve the start and end locations and create a DirectionsRequest using
  // Bus directions.
  directionsService.route({
    origin: document.getElementById('origin').value,
    destination: document.getElementById('destination').value,
    travelMode: 'TRANSIT',
    transitOptions: {
      modes: ['BUS'],
      routingPreference: 'FEWER_TRANSFERS',
      // departure_time: "17:44:2"
    }
  },

    // showing the response received in a text format 
    function (response, status) {
      console.log(response)

      // markers for each step.
      if (status === 'OK') {

        map.fitBounds(response.routes[0].bounds);
        if ($(window).width() >= 992) {
          map.panBy(-600, 0);
          map.setZoom(map.getZoom() - 1);
        }
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
        $("#destination-tab1").html(address2);

        // get date and time details to fill into summary results
        var date, dateElements, year, month, date, time, dateToDisplay;


        if ($(window).width() < 992) {
          datetimeValue = $("#datetime-tab1").val();
          var arr = datetimeValue.split('T');
          date = arr[0];
          time = arr[1];
        } else {
          date = $("#datepicker-tab1").val();
          time = $('#timepicker-tab1').val();
    
          // use date and time here to make properly formatted datetimeValue for mobile
          datetimeValue = date + 'T' + time;
        }

        dateElements = date.split('-');
        year = dateElements[0];
        month = dateElements[1];
        date = dateElements[2];
        dateToDisplay = date + "-" + month + "-" + year;

        // display information to user
        $("#origin-tab1").html(address1);
        $("#destination-tab1").html(address2);
        $(".datetime-results-tab1").html(dateToDisplay + ", " + time);


        journeysteps = response.routes[0].legs[0].steps;

        var direction_text = $("#direction");
        var journey_list = []
        var bus_details = []; //array to store each bus journey 


        var datetimeValue = $("#datetime-tab1").val();
        var arr = datetimeValue.split('T');
        var date1 = arr[0];
        var input_time = arr[1];


        // convert time to seconds since midnight
        // console.log("time: "+ input_time);
        var timeSplit = input_time.split(':');
        var timeSeconds = (+timeSplit[0]) * 60 * 60 + (+timeSplit[1]) * 60;



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
        var list = []
        var list1 = []



        //  // going through the repsone recieved from google
        //  var travelMode = journeysteps[i].travel_mode;

        var journeyTime = 0;
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
            var data = JSON.stringify(journey_steps);
          }
        }

        var data = JSON.stringify(list);

        console.log("data", list)


        var prediction = 0;
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
          
            // parse the response
            response = JSON.parse(response)

            // hide the spinner and show the results
            $('.prediction-spinner').hide();
            $('.results-card').show();
            $('#journey-planner-fare').show();

            let fare = response.fare;
            console.log("Fare")
            console.log(fare)
            $('#fare-result-tab1').html("");
            fare.forEach(element => {
              console.log(element["fare"] )
              if (element["fare"] != null) {
                $('#fare-result-tab1').append('<li>' + element["route"] + ": " + element["fare"] + "</li>");
                console.log(element["fare"] + element["route"])
              } else {
                console.log("inside else if");
                $('#fare-result-tab1').append('<li>' + element["route"] + ": Unavailable" + '</li>');
              }
            });



            // get prediction from dict returned
            response = response.prediction;
            
            // prediction1 = JSON.parse(response)
            prediction1 = response
            console.log("prediction")
            console.log(prediction1)

            function bus_time(k) {

              return prediction1[k]
            }

            var number = 0

            // adding the predicted time to the total time
            for (var j = 0; j < prediction1.length; j++) {

              journeyTime += parseInt(prediction1[j])
              console.log(journeyTime)
            }


            var b = input_time.split(':');
            var theFutureTime = moment().hour(b[0]).minute(b[1]).add(journeyTime, 'minutes').format("HH:mm");
            console.log(theFutureTime)
            // setting the total time and predicted arrival time in the html

            $("#duration-val").html(journeyTime + ' mins')
            $("#journey-time").html(input_time + ' - ' + theFutureTime)



            for (var i = 0; i < journeysteps.length; i++) {



              console.log('number', number)
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

                direction_text.append('<li>' + walking + '&nbsp;&nbsp;' + instruction + '</p><p>' + road + '&nbsp;&nbsp;<b> Duration:</b>&nbsp;' + duration + '</li>');

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

                direction_text.append('<li><p>' + bus + '&nbsp;&nbsp;' + instruction + '</p><p>' + road + '<b> Route:&nbsp;</b>' + Route_number + '&nbsp;&nbsp;<b>Stops: </b>' + num_stops + '<b>Duration: </b>' + bus_time(number) + " mins" + '</p></li>');

                number += 1
              }


            }

            console.log(number)
          })

        //showing the response on the map. 	 
        directionsRenderer.setDirections(response);

        // google.maps.event.addListener(directionsRenderer, 'directions_changed', function() {
        //   console.log("changed")
        //   map.panBy(-600, 0);
        //   map.setZoom(map.getZoom() - 1);
        // });
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
    allMarkers.push(marker);
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

    $('.prediction-spinner').show();
    $('.results-card').hide();

    removeLineFromMap();


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
 
    $(".datetime").val(datetimeValue);

    // convert time to seconds since midnight
    console.log("time: " + time);
    var timeSplit = time.split(':');
    var timeSeconds = (+timeSplit[0]) * 60 * 60 + (+timeSplit[1]) * 60;
    console.log(timeSeconds);

    // show results and routes
    var success = routes();
    if (success) {

      $(".form-area").hide();
      if ($(window).width() < 992) {
        $("#map-interface").animate({ top: "400px" }, 400);
      }
      $("#route-results").show();
    }

    // remove line from map when user clicks go
    removeLineFromMap();


  });

  // add on click to edit-journey button to hide results and show journey planner
  $('.edit-journey').on('click', function () {
    $(".form-area").show();
    if ($(window).width() < 992) {
      $("#map-interface").css("top", "0px");
    }
    $("#route-results").hide();
  });


});
