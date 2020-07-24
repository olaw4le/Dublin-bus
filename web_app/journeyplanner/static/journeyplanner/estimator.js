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

// function to populate the sub_routes list			
function route_list() {

            routes = stations[key].stops
            direction=key.charAt(key.length-1);
            console.log("direction",direction)
            
           

            for (var key2 in routes) {

                for (var key3 in routes[key2]){

        // populating the sub route select list 
        var To = "<option value=0>-- Select --</option>";
        for (var key in stations) {


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

        document.getElementById("estimator-sub").innerHTML = To;
  }
    };


//getting the value of the selected sub route
var sel_sub = "";
var direction = ""
var stop_list = [];

// function to populate the origin and destination
function stops() {
    var To = "<option value=0>-- Select --</option>";

    // getting the value of the selected sub-route
    sel_sub = $("#estimator-sub").val();

    // going through the sub-routes the selected route has 
    for (key in routes) {

        // if the user selected sub-route is found 
        if (sel_sub == key) {

        $("#estimator-origin").html(To) ;
    
        }}
    }





var index;

// function to populate the remaining destination stop
function destination() {
    var To = "<option value=0>-- Select --</option>";

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
    makeStatsRequest();

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
            || $("#estimator-destination option:selected").text() == 'Select stop:') {
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

    });
}


// code for creating journey time graphs //

//  1.  read the search params from the html
//      date, time, route, start & end stops
//  2.  request the predictions data from the server
//      matching search params to database data wil happen serverside
//  3.  wait for the data to return
//
//  4.  create a bar chart with the returned data...
//

// define the colours to use when drawing & filling charts & graphs
var borderColours = ["rgb(184, 202, 204)", "rgb(64, 204, 219)"];
var fillColours = ["rgba(102, 255, 255, 0.5)", "rgba(64, 204, 219, 0.8)"];


// function for reading in the parameters used for generating the graphs
function getSearchParams() {
    var params = new Object();
        params["route"] = $("#estimator-route").val();
        params["direction"] = "1";                           // placeholder values !!!
        params["start"] = $("#estimator-origin").val();
        params["end"] = $("#estimator-destination").val();

        // get the date & time
        if ($(window).width() < 992) {
            // if used on mobile
            var datetimeValue = $("#datetime-tab2").val();
            var arr = datetimeValue.split('T');
            params["date"] = arr[0];
            params["time"] = arr[1];
        } else {
            // for other devices...
            params["date"] = $("#datepicker-tab2").val();
            params["time"] = $('#timepicker-tab2').val();
        }

    return params;
}


// function for requesting graph data from web server
function makeStatsRequest() {

    // red the search parameters
    var params = getSearchParams()

    // make the request
    $.ajax({
        type:"POST",
        url:"get_stats/",
        data:{date:params.date, time:params.time, route:params.route, direction:params.direction, end:params.end, start:params.start}
    })

    // when response received
    .done(function(response){
        var data = JSON.parse(response);

        var infoObject = new Object();
            infoObject["data"] = data;
            infoObject["route"] = params.route;
            infoObject["start"] = params.start;
            infoObject["end"] = params.end;

        updateTextInfo(infoObject);
        drawBarChart(data);
        })
}


// display a textual description of the data contained in the graph
function updateTextInfo(data) {

    //$("#results-route-number").html(data.route);
    //$("#results-route-stops").html(data.start + '-' + data.end);


    // get the 95% journey time for this time group
    var day_time = Object.keys(data.data)[2];
    var journey_time = data.data[day_time];
    var fastest_time = day_time;

    for (var key in data.data) {
        if (data.data[key] < journey_time) {
            fastest_time = key
        }
    }

    // if there's a faster time than the 'search time' add that to the description
    if (day_time == fastest_time) {
        $("#results-description").html("At " + day_time + " 95% of journeys take less than " + journey_time + " minutes.");
    } else {
        var timeDelta = journey_time - data.data[day_time];
        $("#results-description").html("At " + day_time + " 95% of journeys take less than " + journey_time + " minutes. You could expect to save "  + timeDelta + "minutes by making this trip at " + fastest_time + "instead.");
    }

}


function DataSet(data) {
    // formats the passed data as an object w/ instance variables to be passed
    // to the Chart() object constructor
    this.label = "Journey Duration";
    // this.fill = fill;
    this.backgroundColor = [fillColours[0], fillColours[0], fillColours[1], fillColours[0], fillColours[0]];
    this.borderColor = [borderColours[0], borderColours[0], borderColours[1], borderColours[0], borderColours[0]];
    this.borderWidth = 1;
    this.barPercentage = 0.95;     // sets the relative width of bars in a bar chart
    this.categoryPercentage = 1;   // sets the relative width of bars in a bar chart

    var arr = new Array();

    Object.keys(data).forEach( function(item) {
            arr.push(data[item]);
        })

    this.data = arr;
}

function drawBarChart(data) {

    // get the chart container from the info.html page
    var ctx = document.getElementById("results-canvas");
    var bars = [];
    var labels = Object.keys(data);

    bars =  new DataSet(data);
    var someChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    datasets: [bars],
                    labels: Object.keys(data),
                    },
                options: {
                    responsive: true,
                    legend: {
                        display: false
                    },
                    scales: {
                        yAxes: [{
                            scaleLabel: {
                                labelString: "Travel Time (Minutes)",
                                display: true
                            },
                            stacked: false,
                            display: true,
                            gridLineWidth: 0,
                            minorTickInterval: null,
                            ticks: {
                                beginAtZero: true
                            }
                        }],
                        xAxes: [{
                            stacked: false,
                            display: true,
                            gridLineWidth: 0,
                            gridLines: {
                                display: false
                            }
                        }]
                    }
                }
    });
    return someChart;

}