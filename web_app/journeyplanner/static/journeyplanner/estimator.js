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
        minuteIncrement: 1
    });

});

var routes = "";
var route_number = "";
var stop_name = "";
var stations = "";
var routes = ""
var allMarkers = [];

$(function () {
    var jqxhr = $.getJSON("static/new_ordered_stops.json", null, function (data) {
        stations = data;

        for (var key in stations) {
            var x = key.split("_");
            route_number += (x[0]+" "+stations[key].headsign)+ ",";
        }
        console.log(route_number)

        //turning the into an array
        route_number = route_number.trim().split(",");
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
    if (allMarkers) {
        for (var i = 0; i < allMarkers.length; i++) {
            allMarkers[i].setMap(null);
        }
    }
}

//getting the value of the selected  route
var sel_route = "";
var direction = ""
var stop_list = [];

// function to populate the origin and destination
function stops() {
    var To = "<option value=0>Stops</option>";

    // getting the value of the selected route
    sel_route= $("#estimator-route").val();

    console.log("route",sel_route)

    $.getJSON("static/new_ordered_stops.json", null, function (data) {
       stations = data;
       var key;
     //getting the value of the selected route
      var list = ''

       for (key in stations) {
        var x = key.split("_");
        var y= (x[0]+" "+stations[key].headsign)
        
           
        if (sel_route ==y) {
            

            routes = stations[key].stops
            direction=key.charAt(key.length-1);
            console.log("direction",direction)
            
           

            for (var key2 in routes) {

                for (var key3 in routes[key2]){

                   var x=Object.values(routes[key2])
                   var y = JSON.stringify(x);
                   y= y.replace(/[[\]]/g,'')
                   y=y.replace(/['"]+/g, '')


                   list += (key3+" "+y)+ ",";


                 
                 
    
                }            
            }

        //turning the into an array
        list = list.trim().split(",");
        result = list
        

        //popuplating the sub route select list
        for (var i = 0; i < list.length; i++) {
            To += "<option>  " + list[i] + "</option>";
            stop_list.push(list[i])
        }


        $("#estimator-origin").html(To) ;
    
        }}
    })

}



var index;

// function to populate the remaining destination stop
function destination() {
    var To = "<option value=0>Stops</option>";

    starting_stop = $("#estimator-origin").val();
    index = stop_list.indexOf(String(starting_stop)) //finding the index of the selected stop
    console.log(index)
    destination_list = stop_list.slice(index + 1) //displaying the stops after the selected stops 

    console.log(destination_list)
    

    for (var i = 0; i < destination_list.length; i++) {
        To += "<option>" + destination_list[i] + "</option>";

    }

    // populating the inner html with the destination
    $("#estimator-destination").html(To)
}


function origin_marker() {
    var origin_stop = $("#estimator-origin").val()
    var x = origin_stop.split(" ");
    origin_stop=x[0]
    
    var route = $("#estimator-route").val();
    var x = route.split(" ");
    route=x[0]


    $.ajax({
        type: "POST",
        url: "list_latlng/",
        data: { route: route}
    })

        .done(function (response) {
            console.log("successfully posted");
            var x = JSON.parse(response)

            for (key in x) {
                var marker = new google.maps.Marker({
                    position: new google.maps.LatLng(x[key].lat, x[key].lng),
                    map: map,
                    title: key,
                });
                allMarkers.push(marker)

            }


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
    var route = $("#estimator-route").val();
    var x = route.split(" ");
    route=x[0]
    var start = $("#estimator-origin").val();
    var x = start.split(" ");
    start=x[0]
    var end = $("#estimator-destination").val()
    var x = end.split(" ");
    end=x[0]

    $.ajax({
        type: "POST",
        url: "list_latlng/",
        data: { route: route }
    })

        .done(function (response) {
            console.log("successfully posted");
            var x = JSON.parse(response)

            var start_latlng = { lat: x[start].lat, lng: x[start].lng };
            var end_latlng = { lat: x[end].lat, lng: x[end].lng };
            var request = {
                origin: start_latlng,
                destination: end_latlng,
                travelMode: google.maps.TravelMode.DRIVING
            };

            directionsService.route(request, function (result, status) {
                if (status == google.maps.DirectionsStatus.OK) {
                    directionsDisplay.setDirections(result);
                    console.log(result)
                }
            });


        })
    removeLineFromMap()

};

// event listner to porpulate the route dropdown list)
$("#estimator-route").on('keyup click change hover', stops);
$("#estimator-route").change(origin_marker);
$("#estimator-origin").change(destination);


// go button for tab 2 to show and hide results
$(function () {

    $('#stop-to-stop-go').on('click', function () {

        // show error if user doesn't complete all fields
        if ($('#estimator-route').val() == "" || $("#estimator-sub option:selected").text() ==
            'Select route:' || $("#estimator-origin option:selected").text() == 'Select stop:' 
            || $("#estimator-origin option:selected").text() == 'Stops' ||
            $("#estimator-destination option:selected").text() == 'Stops' ||
            $("#estimator-destination option:selected").text() == 'Select stop:') {
            $('#stop-to-stop-incomplete-form-error').show();
        } else {
            $(".spinner-border").show();

            initMap2();
            removeLineFromMap();

            if ($(window).width() < 992) {
                datetimeValue = $("#datetime-tab2").val();
                console.log("datetime value mobile: " + datetimeValue);
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
                },
            });

            $('#datepicker-tab2-results-time').flatpickr({
                enableTime: true,
                defaultDate: time,
                dateFormat: 'H:i',
                noCalendar: true,
                time_24hr: true,
                minuteIncrement: 1,
                onClose: function (selectedDates, dateStr, instance) {
                    sendDateTimeChangePostRequest();
                },
            });


            $(".datetime").val(datetimeValue);

            // convert time to seconds since midnight
            var timeSplit = time.split(':');
            var timeSeconds = (+timeSplit[0]) * 60 * 60 + (+timeSplit[1]) * 60;


            // sending a post request to the server
            route = $("#estimator-route").val();
            var x = route.split(" ");
            route=x[0]
            origin = $("#estimator-origin").val();
            var x = origin.split(" ");
            origin=x[0]
            destination = $("#estimator-destination").val();
            var x = destination.split(" ");
            destination=x[0]

            console.log("route",route)
            console.log("origin",origin)
            console.log("destination",destination)
            console.log("direction",direction)
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
                });


            // show results
            $(".form-area").hide();
            if ($(window).width() < 992) {
                $("#map-interface").animate({ top: "400px" }, 'fast');
            }
            $("#stop-to-stop-results").show();

            // set the value of the html for the summary results using the html id
            $("#origin-tab2").html("Stop " + $("#estimator-origin").val());
            $("#destination-tab2").html("Stop " + $("#estimator-destination").val());

        }





    });

    // add on click to edit-journey button to hide results and show journey planner
    $('#edit-journey-tab2').on('click', function () {
        console.log("inside edit-journey-results");
        $(".form-area").show();
        // $("#map-interface").css("top", "0px");
        $("#stop-to-stop-results").hide();
    });

    // call post request function when mobile datetime value changed
    $("#datetime-tab2-results").on("change", function () {
        sendDateTimeChangePostRequest();
    });

});


// post request sent again when date and time changed on results page
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

    // populate the values of the date and time pickers
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
            route: route[0],
            origin: origin[0],
            destination: destination[0],
            direction: direction
        }
    }).done(function (result) {
        console.log("successfully posted");
        $(".spinner-border").hide();
        $("#stop-to-stop-estimate").show();
        $("#stop-to-stop-estimate").html(result + " minutes");

    });
}