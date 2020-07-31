// remove line from map
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
function clearMarkers() {
    if (directionsDisplay != null) {
        directionsDisplay.setMap(null);
        directionsDisplay = null;
    }
}


$(document).ready(function () {

    // Remove routes when navigating to another tab
    $(document).on("click.routes", "#routeplanner-nav, #allroutes-nav, #tourist-nav, #allroutes-tab, #tourist-tab, #routeplanner-tab, #leap-nav, #realtime-nav,#realtime-tab,#leap-tab",
        removeLineFromMap);

    // clear markers when navigating to another tab
    $(document).on("click.routes", "#routeplanner-nav, #allroutes-nav, #tourist-nav, #allroutes-tab, #tourist-tab, #routeplanner-tab, #leap-nav, #realtime-nav,#realtime-tab,#leap-tab",
        clearMarkers);


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


//initialise variables
var routes = "";
var route_number = "";
var stop_name = "";
var stations = "";
var routes = ""
var allMarkers = [];
// an object to hold key-pair values <headsign>:<route_id> - similar to a python dict
var routeNames = {};


$(function () {
    var jqxhr = $.getJSON("static/new_ordered_stops.json", null, function (data) {
        stations = data;

        for (var key in stations) {
            var x = key.split("_");
            route_number += (x[0] + " " + stations[key].headsign) + ",";

            // extract the headsign
            var headSign = stations[key].headsign;

            route_number += (x[0]+" "+ headSign)+ ",";

            // populate routeNames
            routeNames[x[0]+" "+ headSign] = key;
        }

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


//getting the value of the selected  route
var sel_route = "";
var direction = ""
var stop_list = [];

// function to populate the origin and destination
function stops() {
    var To = "<option value=0>-- Select -- </option>";

    // getting the value of the selected route
    sel_route = $("#estimator-route").val();

    //console.log("route", sel_route)

    $.getJSON("static/new_ordered_stops.json", null, function (data) {
        stations = data;
        var key;
        //getting the value of the selected route
        var list = ''

        for (key in stations) {
            var x = key.split("_");
            var y = (x[0] + " " + stations[key].headsign)


            if (sel_route == y) {


                routes = stations[key].stops
                direction = key.charAt(key.length - 1);
                //console.log("direction", direction)


                for (var key2 in routes) {

                    for (var key3 in routes[key2]) {

                        var x = Object.values(routes[key2])
                        var y = JSON.stringify(x);
                        y = y.replace(/[[\]]/g, '')
                        y = y.replace(/['"]+/g, '')


                        list += (key3 + " " + y) + ",";
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
}
        }
    })

}


var index;

// function to populate the remaining destination stop
function destination() {
    var To = "<option value=0>-- Select --</option>";

    starting_stop = $("#estimator-origin").val();
    index = stop_list.indexOf(String(starting_stop)) //finding the index of the selected stop
    //console.log(index)
    destination_list = stop_list.slice(index + 1) //displaying the stops after the selected stops 

    //console.log(destination_list)

    for (var i = 0; i < destination_list.length; i++) {
        To += "<option>" + destination_list[i] + "</option>";

    }
    // populating the inner html with the destination
    $("#estimator-destination").html(To)
}


function origin_marker() {
    var origin_stop = $("#estimator-origin").val()
    var x = origin_stop.split(" ");
    origin_stop = x[0]

    var route = $("#estimator-route").val();
    var x = route.split(" ");
    route = x[0]


    $.ajax({
        type: "POST",
        url: "list_latlng/",
        data: { route: route }
    })

        .done(function (response) {
            //console.log("successfully posted");
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

// calculate route
function calcRoute() {
    var route = $("#estimator-route").val();
    var x = route.split(" ");
    route = x[0]
    var start = $("#estimator-origin").val();
    var x = start.split(" ");
    start = x[0]
    var end = $("#estimator-destination").val()
    var x = end.split(" ");
    end = x[0]

    $.ajax({
        type: "POST",
        url: "list_latlng/",
        data: { route: route }
    })

        .done(function (response) {

            var x = JSON.parse(response)

            var start_latlng = { lat: x[start].lat, lng: x[start].lng };
            var end_latlng = { lat: x[end].lat, lng: x[end].lng };

            var request = {
                origin: start_latlng,
                destination: end_latlng,
                travelMode: google.maps.TravelMode.DRIVING
            };
            directionsService = new google.maps.DirectionsService;

            directionsDisplay = new google.maps.DirectionsRenderer({
                map: map
            })
            directionsService.route(request, function (result, status) {
                if (status == google.maps.DirectionsStatus.OK) {
                    directionsDisplay.setDirections(result);
                }
                removeLineFromMap()
            });
        })
};

// event listner to porpulate the route dropdown list)
$("#estimator-route").on('keyup click change hover', stops);
$("#estimator-route").change(origin_marker);
$("#estimator-origin").change(destination);


// go button for tab 2 to show and hide results
$(function () {

    $('#stop-to-stop-go').on('click', function () {

// clear old fare and prediction values each time user clicks go
        $('#stop-to-stop-fare').html("");
        $("#stop-to-stop-estimate").html("");

        // show error if user doesn't complete all fields in form
        if ($('#estimator-route').val() == "" || $("#estimator-origin option:selected").text() == '-- Select --'
            || $("#estimator-destination option:selected").text() == '-- Select --') {
            $('#stop-to-stop-incomplete-form-error').show();
        } else {
            $(".spinner-border").show();

            calcRoute();
            removeLineFromMap();
            makeStatsRequest();

            //  use different date and time values depending on size of screen
            if ($(window).width() < 992) {
                datetimeValue = $("#datetime-tab2").val();
                //console.log("datetime value mobile: " + datetimeValue);
                var arr = datetimeValue.split('T');
                date = arr[0];
                //console.log("mobile date: " + date);
                time = arr[1];
                //console.log("mobile time: " + time);
            } else {
                var date = $("#datepicker-tab2").val();
                //console.log("desktop date: " + date);
                time = $('#timepicker-tab2').val();
                //console.log("desktop time: " + time);

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
            route = x[0]
            origin = $("#estimator-origin").val();
            var x = origin.split(" ");
            origin = x[0]
            destination = $("#estimator-destination").val();
            var x = destination.split(" ");
            destination = x[0]

            // send post request
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

                // response returned from post request
                .done(function (response) {

                    $('.fare-accordion').show();

                    // display fare to user and display 'unavailable' when no fare given
                    var fare = response.fare;

                    // if fare has found flag 'True', append fares to list
                    if (fare["found"]) {
                        for (const key in fare) {
                            if (key != "url" && key != "route" && key != "found") {
                                if (key == "Adult Cash" || key == "Adult Leap"){
                                    $('#cash-and-leap-tab2').append('<li>' + key + " Fare: " + "€" + fare[key] + "</li>");
                                } else {
                                    $('#fare-result-tab2').append('<li>' + key + " Fare: " + "€" + fare[key] + "</li>");
                                }
                            }
                        }
                    } else {
                        // else append unavailable
                        $('#fare-result-tab2').append('<li>' + "Unavailable" + '</li>');
                    }

                    console.log("successfully posted");

                    // hide spinner and show estimate
                    $(".spinner-border").hide();
                    $("#stop-to-stop-estimate").html(response.result + " minutes");
                });


            // show results
            $(".form-area").hide();
            if ($(window).width() < 992) {
                $("#map-interface").animate({ top: "350px" }, 'fast');
            }
            $("#stop-to-stop-results").show();

            // set the value of the html for the summary results using the html id
            $("#origin-tab2").html("Stop " + $("#estimator-origin").val());
            $("#destination-tab2").html("Stop " + $("#estimator-destination").val());
        }
    });

    // add on click to edit-journey button to hide results and show journey planner
    $('#edit-journey-tab2').on('click', function () {
        $(".form-area").show();
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

    // diff date and time values depending on screen size
    if ($(window).width() < 992) {
        datetimeValue = $("#datetime-tab2-results").val();
        var arr = datetimeValue.split('T');
        date = arr[0];
        time = arr[1];
    } else {
        var date = $("#datepicker-tab2-results-date").val();
        time = $('#datepicker-tab2-results-time').val();

        // use date and time here to make properly formatted datetimeValue for mobile
        datetimeValue = date + 'T' + time;
    }

    // populate the values of the date and time pickers
    $(".datetime").val(datetimeValue);
    $("#datepicker-tab2-results-date").val(date);
    $("#datepicker-tab2-results-time").val(time);

    var timeSplit = time.split(':');
    var timeSeconds = (+timeSplit[0]) * 60 * 60 + (+timeSplit[1]) * 60;

    // send post request again when user changes date and time
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
    }).done(function (response) {
        //console.log("successfully posted");
        $(".spinner-border").hide();
        $("#stop-to-stop-estimate").show();
        $("#stop-to-stop-estimate").html(response.result + " minutes");
        // request new data for graphs when date & time changes
        makeStatsRequest();

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


// function for reading in the parameters used for generating the graphs
function getSearchParams() {
    var routeName = $("#estimator-route").val();
    // find the route number using the routeName
    console.log(routeName);
    var route = routeNames[routeName].split("_");

    var originName = $("#estimator-origin").val();
    var origin = originName.split(" ")[0];
    var destinationName = $("#estimator-destination").val();
    var destination = destinationName.split(" ")[0];

    var params = new Object();
    params["route"] = route[0];
    params["direction"] = route[1];
    params["start"] = origin;
    params["end"] = destination;

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

    // hide any error messages from the previous search
    $("#no-data-error").hide()

    // make the request
    $.ajax({
        type: "POST",
        url: "get_stats/",
        data: { date: params.date, time: params.time, route: params.route, direction: params.direction, end: params.end, start: params.start }
    })

        // when response received
        .done(function (response) {
            var data = JSON.parse(response);

        if (data.hourly != "none" ) {
            var infoObject = new Object();
            infoObject["data"] = data.hourly;
            infoObject["route"] = params.route;
            infoObject["start"] = params.start;
            infoObject["end"] = params.end;

            updateTextInfo(infoObject);
            drawBarChart(data.hourly);
        } else {
            chartDataError();
        }
    })
}


// display a textual description of the data contained in the graph
function updateTextInfo(data) {

    //$("#results-route-number").html(data.route);
    //$("#results-route-stops").html(data.start + '-' + data.end);


    // get the 95% journey time for this time group
    var keys = Object.keys(data.data)
    var current_time = keys[Math.floor(keys.length / 2)];
    var journey_time = data.data[current_time];
    var fastest_time = current_time;

    for (var key in data.data) {
        var t = data.data[key];
        if (t < journey_time) {
            // ignore journey times of 0 minute - this is missing data
            if (t != 0) {
                fastest_time = key;
            }
        }
    }

    // if there's a faster time than the 'search time' add that to the description
    if (current_time === fastest_time) {
        $("#results-description").html("At " + current_time + " 95% of journeys take less than " + journey_time + " minutes.");
    } else {
        var timeDelta = journey_time - data.data[fastest_time];
        $("#results-description").html("At " + current_time + " 95% of journeys take less than " + journey_time + " minutes. This journey is up to "  + timeDelta + " minutes faster at " + fastest_time + ".");
    }

}


function DataSet(data) {
    // formats the passed data as an object w/ instance variables to be passed
    // to the Chart() object constructor
    this.label = "Journey Duration";

    // allow function to handle datasets of non-fixed size - central datapoint is assumed to be current
    var length = Object.keys(data).length;
    var midpoint = Math.floor(length / 2);
    this.backgroundColor = new Array();
    this.borderColor = new Array();
    for (var i = 0; i < length; i++) {
        if ( i == midpoint ) {
            this.backgroundColor.push("rgba(64, 204, 219, 0.8)");
            this.borderColor.push("rgb(64, 204, 219)");
        } else {
            this.backgroundColor.push("rgba(184, 202, 204, 0.8)");
            this.borderColor.push("rgb(184, 202, 204)");
        }
    }
    this.borderWidth = 1;
    this.barPercentage = 0.95;     // sets the relative width of bars in a bar chart
    this.categoryPercentage = 1;   // sets the relative width of bars in a bar chart

    var arr = new Array();

    Object.keys(data).forEach(function (item) {
        arr.push(data[item]);
    })

    this.data = arr;
}


function drawBarChart(data) {

    // get the chart container from the info.html page
    var ctx = $("#results-canvas");
    var bars = [];
    var labels = Object.keys(data);

    bars =  new DataSet(data);

    // check if a chart already exists in the container div;
    // if so just update the existing chart with new data
    // else create a new chart element in the container div

    if (ctx.firstChild) {
        someChart.config.data = {
            datasets: [bars],
            labels: Object.keys(data)
        }
    } else {
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
    }
    return someChart;

}

function chartDataError(){
    // display an error message when no data historical data associated with the searched time...
    var msg = "Oh no! There appears to be no Historical data for this route at this time! Maybe try a different time?";
    $("#no-data-error").text(msg);
    $("#no-data-error").show();
    $("#results-chart").hide();
}


$('#stop-to-stop-go').on('click',makeStatsRequest)