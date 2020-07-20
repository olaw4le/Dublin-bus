$(document).ready(function () {

    // Remove routes when navigating to another tab
  $(document).on("click.routes", "#routeplanner-nav, #allroutes-nav, #tourist-nav, #allroutes-tab, #tourist-tab, #routeplanner-tab",
  removeLineFromMap);


    // flatpickr date https://flatpickr.js.org/options/
    $("#datepicker-tab2").flatpickr({
        altInput: true,
        altFormat: "F j, Y",
        dateFormat: 'yy-m-d',
        defaultDate: new Date(),
        minDate: "today"
    });

    // flatpickr time
    $('#timepicker-tab2').flatpickr({
        enableTime: true,
        defaultDate: new Date().getHours() + ":" + new Date().getMinutes(),
        dateFormat: 'H:i',
        noCalendar: true,
        time_24hr: true,
        minTime: "05:00",
        minuteIncrement: 1
    });

});

var routes = "";
var route_number = "";
var stop_name = "";
var stations = "";
var routes = ""
var allMarkers = [];

$(function() {
    var jqxhr = $.getJSON("static/journeyplanner/ordered_stops_main.json", null, function (data) {
        stations = data;

        for (var key in stations) {
            route_number += key + " ";
        }

        //turning the into an array
        route_number = route_number.trim().split(" ");
    });

    $("#estimator-route").autocomplete({
        source: function (request, response) {
            var matcher = new RegExp("^" + $.ui.autocomplete.escapeRegex(request.term), "i");
            response($.grep(route_number, function (item) {
                return matcher.test(item);
            }));
        }
    });

});


function removeLineFromMap() {
    if (directionsRenderer) {
      directionsRenderer.setDirections({ routes: [] });
    }
    // First, remove any existing markers from the map.
    console.log(allMarkers);
    if(allMarkers) {
      for (var i = 0; i < allMarkers.length; i++) {
        allMarkers[i].setMap(null);
      }
    }
  }





  
// function to populate the sub_routes list			
function route_list() {

    sel = $("#estimator-route").val();
    console.log(sel)

    //getting the value of the selected route
    var list = ''

    //jquery to open the json file 
    $.getJSON("static/journeyplanner/ordered_stops_main.json", null, function (data) {
        stations = data;

        // populating the sub route select list 
        var To = "<option value=0>Sub Route</option>";
        for (var key in stations) {


            if (sel.toString() == key.toString()) {

                routes = stations[key]

                for (var key2 in routes) {
                    console.log(key2)
                    list += key2 + " ";
                }
            }
        }

        //turning the into an array
        list = list.trim().split(" ");
        result=list

        //popuplating the sub route select list
        for (var i = 0; i < list.length; i++) {
            To += "<option  value=" + list[i] + ">" + list[i] + "</option>";
        }

        document.getElementById("estimator-sub").innerHTML = To;

    });
}

//getting the value of the selected sub route
var sel_sub = "";
var direction= ""
var stop_list=[];

// function to populate the origin and destination
function stops() {
    var To = "<option value=0>Stops</option>";

    // getting the value of the selected sub-route
    sel_sub = $("#estimator-sub").val();

    // going through the sub-routes the selected route has 
    for (key in routes) {
   
        // if the user selected sub-route is found 
        if (sel_sub == key) {

            // the stops the selected sub-routes goes through
            bus_stops = routes[key].stops;

            direction = routes[key].direction


            // poppulating the origin and destination with the stops
            for (var i = 0; i < bus_stops.length; i++) {
                To += "<option  value=" + bus_stops[i] + ">" + bus_stops[i] + "</option>";

                stop_list.push(bus_stops[i])

            }

            // populating the inner html
          $("#estimator-origin").html(To) 

        }
    }  
}
var index;
    // function to populate the remaining destination stop
    function destination(){
        var To = "<option value=0>Stops</option>";

        starting_stop=$("#estimator-origin").val()
        index = stop_list.indexOf(+starting_stop) //finding the index of the selected stop
        destination_list=stop_list.slice(index + 1) //displaying the stops after the selected stops 

        console.log(destination_list)

        for (var i = 0; i < destination_list.length; i++) {
            To += "<option  value=" + destination_list[i] + ">" + destination_list[i] + "</option>";

        }

           // populating the inner html with the destination
           $("#estimator-destination").html(To)
    }


function origin_marker(){
    var origin_stop=$("#estimator-origin").val()
    var route=$("#estimator-route").val();
    
    
    $.ajax({
        type:"POST",
        url:"list_latlng/",
        data:{route:route}
      })

      .done(function(response){
          console.log("successfully posted");
          var x=JSON.parse(response)

          for (key in x) { 
           var marker = new google.maps.Marker({
              position: new google.maps.LatLng(x[key].lat, x[key].lng),
              map: map,
              title:key, 
            });
            allMarkers.push(marker)
         
            }

            for (var i in allMarkers ){


            google.maps.event.addListener(allMarkers[i],'click',function() {
                $('#estimator-origin').val(this.getTitle());
                $('#estimator-origin').show();
              });}



      });
}

function initMap2() {
    directionsService = new google.maps.DirectionsService;
   
    directionsDisplay = new google.maps.DirectionsRenderer({
        map: map
    });
    calcRoute();
    removeLineFromMap();
}


 // calculate route
 function calcRoute() {
 var route=$("#estimator-route").val();
var start=$("#estimator-origin").val();
var end= $("#estimator-destination").val()
    $.ajax({
        type:"POST",
        url:"list_latlng/",
        data:{route:route}
      })

      .done(function(response){
          console.log("successfully posted");
         var x=JSON.parse(response)

         var start_latlng = {lat:x[start].lat,lng: x[start].lng};
         var end_latlng = {lat:x[end].lat, lng:x[end].lng};
         var request = {
             origin: start_latlng,
             destination: end_latlng,
             travelMode: google.maps.TravelMode.DRIVING
         };
     
         directionsService.route(request, function(result, status) {
             if (status == google.maps.DirectionsStatus.OK) {
                 directionsDisplay.setDirections(result);
                 console.log(result)
             }
         });


      })
      removeLineFromMap()

};

// event listner to porpulate the route dropdown list)
$("#estimator-route").on('keyup click change hover', route_list);

// event listner to populate the origin and destination 
$("#estimator-sub").change(stops);

$("#estimator-route").change(origin_marker);
$("#estimator-origin").change(destination);


// go button for tab 2 to show and hide results
$(function () {

    $('#stop-to-stop-go').on('click', function () {

        initMap2(); 
        removeLineFromMap();      

        if ($(window).width() < 992) {
            datetimeValue = $("#datetime-tab2").val();
            console.log("datetime value mobile: " + datetimeValue );
            var arr = datetimeValue.split('T');
            date = arr[0];
            console.log("mobile date: " + date);
            time = arr[1];
            console.log("mobile time: " + time);
        } else {
            var date = $("#datepicker-tab2").val();
            console.log("desktop date: " + date);
            time = $('#timepicker-tab2').val();
            console.log("desktop time: " + time);

            // use date and time here to make properly formatted datetimeValue for mobile
            datetimeValue = date + 'T' + time;
            console.log("datetimevalue test: " + datetimeValue);
        }
        // show date and time inputs on desktop results page for better user experience
        // default date and time are those selected by user on input page
        $("#datepicker-tab2-results-date").flatpickr({
            altInput: true,
            altFormat: "F j, Y",
            dateFormat: 'yy-m-d',
            defaultDate: date,
            minDate: "today",
            onClose: function (selectedDates, dateStr, instance) {
                sendDateTimeChangePostRequest();
                console.log("craoissant day");
            },
        });

        $('#datepicker-tab2-results-time').flatpickr({
            enableTime: true,
            defaultDate: time,
            dateFormat: 'H:i',
            noCalendar: true,
            time_24hr: true,
            minTime: "05:00",
            minuteIncrement: 1,
            onClose: function (selectedDates, dateStr, instance) {
                sendDateTimeChangePostRequest();
                console.log("craoissant time");
            },
        });


        $(".datetime").val(datetimeValue);

        // convert time to seconds since midnight
        // console.log("time: "+ input_time);
        console.log("time: " + time);
        var timeSplit = time.split(':');
        var timeSeconds = (+timeSplit[0]) * 60 * 60 + (+timeSplit[1]) * 60;
        console.log(timeSeconds);

        // sending a post request to the server
        route = $("#estimator-route").val();
        origin = $("#estimator-origin").val();
        destination = $("#estimator-destination").val();
        $.ajax({
            type: "POST",
            url: "prediction/",
            data: {
                date: date,
                time: timeSeconds,
                route: route,
                origin: origin,
                destination: destination,
                direction: direction
            }
        })

            .done(function (result) {
                console.log("successfully posted");
                $(".spinner-border").hide();
                $("#stop-to-stop-estimate").html(result + " minutes");
                // console.log(result);

            });


    // show results
        $(".form-area").hide();
        if ($(window).width() < 992) {
            $("#map-interface").css("top", "400px");
        }
        $("#stop-to-stop-results").show();

        //getting the value of the user selected time
        //var time = $("#datetime-tab2").val();


        // var dateArr, date, dateElements, year, month, date, time, dateToDisplay;

        // dateArr = time.split('T');
        // date = dateArr[0];
        // dateElements = date.split('-');
        // year = dateElements[0];
        // month = dateElements[1];
        // date = dateElements[2];
        // dateToDisplay = date + "-" + month + "-" + year;

        // time = dateArr[1];

        // set the value of the html for the results using the html id
        $("#origin-tab2").html("Stop " + $("#estimator-origin").val());
        $("#destination-tab2").html("Stop " + $("#estimator-destination").val());
        // $("#datetime-tab").html(dateToDisplay + ", " + time)




    });

    // add on click to edit-journey button to hide results and show journey planner
    $('#edit-journey-tab2').on('click', function () {
        console.log("inside edit-journey-results");
        $(".form-area").show();
        $("#map-interface").css("top", "0px");
        $("#stop-to-stop-results").hide();
    });

// call post request function when mobile datetime value changed
    $("#datetime-tab2-results").on("change", function () {
        sendDateTimeChangePostRequest();
    });




});



// these need to be the results ids??? 

function sendDateTimeChangePostRequest() {

    $("#stop-to-stop-estimate").hide();
    $(".spinner-border").show();

    if ($(window).width() < 992) {
        datetimeValue = $("#datetime-tab2-results").val();
        var arr = datetimeValue.split('T');
        date = arr[0];
        console.log("mobile date: " + datetimeValue);
        time = arr[1];
    } else {
        var date = $("#datepicker-tab2-results-date").val();
        console.log("desktop date: " + date);
        time = $('#datepicker-tab2-results-time').val();
        console.log("desktop time: " + time);

        // use date and time here to make properly formatted datetimeValue for mobile
        datetimeValue = date + 'T' + time;
    }
    $(".datetime").val(datetimeValue);
    $("#datepicker-tab2-results-date").val(date);
    $("#datepicker-tab2-results-time").val(time);


    var timeSplit = time.split(':');
    var timeSeconds = (+timeSplit[0]) * 60 * 60 + (+timeSplit[1]) * 60;
    console.log(timeSeconds);

    $.ajax({
        type: "POST",
        url: "prediction/",
        data: {
            date: date,
            time: timeSeconds,
            route: route,
            origin: origin,
            destination: destination,
            direction: direction
        }
    }).done(function (result) {
        console.log("successfully posted");
        $(".spinner-border").hide();
        $("#stop-to-stop-estimate").show();
        $("#stop-to-stop-estimate").html(result + " minutes");
        // console.log(result);

    });
}
