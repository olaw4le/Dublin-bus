// remove line from map
function removeLineFromMap() {
	if (directionsRenderer) {
		directionsRenderer.setDirections({
			routes: []
		});
	}
	// First, remove any existing markers from the map.
	if (allMarkers) {
		for (var i = 0; i < allMarkers.length; i++) {
			allMarkers[i].setMap(null);
		}
	}
}
//clear any markers on the map 
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

			route_number += (x[0] + " " + headSign) + ",";

			// populate routeNames
			routeNames[x[0] + " " + headSign] = key;
		}

		//turning the into an array
		route_number = route_number.trim().split(",");

		//getting unqiue value of all the stops number
		route_number = route_number.filter(function (item, pos) {
			return route_number.indexOf(item) == pos;
		});
	});

	$("#estimator-route").autocomplete({
		source: function (request, response) {
			var matcher = new RegExp("^" + $.ui.autocomplete.escapeRegex(request.term), "i");
			response($.grep(route_number, function (item) {
				return matcher.test(item);
			}));

		},
		close: () => {
			$("#estimator-route").blur();
			stops();
		},
		change: () => {
			stops()
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
	// disable select
	$("#estimator-origin").prop('disabled', true);

	// getting the value of the selected route
	sel_route = $("#estimator-route").val();

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

				for (var key2 in routes) {

					for (var key3 in routes[key2]) {
						console.log(key3)

						var x = Object.values(routes[key2])
						console.log("x = ", x)
						var y = JSON.stringify(x);
						console.log("y =", y)
						y = y.replace(/[[\]]/g, '')
						y = y.replace(/['"]+/g, '')
 
						if (y != ""){
						list += (key3 + " " + y) + ",";}
					}
				}

				//turning the into an array
				list = list.trim().split(",");
				result = list

				console.log(list)

				//popuplating the sub route select list
				for (var i = 0; i < list.length; i++) {
					To += "<option>  " + list[i] + "</option>";
					stop_list.push(list[i])
				}
				$("#estimator-origin").html(To);
			}
		}
	}).done(() => {
		//enable select
		$("#estimator-origin").prop('disabled', false);
	});
}

var index;


// function to populate the remaining destination stop
function destination_stops() {
	var To = "<option value=0>-- Select --</option>";

	//getting unqiue value of all the stops number
	stop_list = stop_list.filter(function (item, pos) {
		return stop_list.indexOf(item) == pos;
	});

	starting_stop = $("#estimator-origin").val();
	index = stop_list.indexOf(String(starting_stop)) //finding the index of the selected stop
	destination_list = stop_list.slice(index + 1) //displaying the stops after the selected stops 

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
			data: {
				route: route
			}
		})

		.done(function (response) {
			var x = JSON.parse(response)
			var bounds = new google.maps.LatLngBounds();

			for (key in x) {
				var marker = new google.maps.Marker({
					position: new google.maps.LatLng(x[key].lat, x[key].lng),
					map: map,
					title: key,
				});

				loc = new google.maps.LatLng(marker.position.lat(), marker.position.lng());
				bounds.extend(loc);

				allMarkers.push(marker)


			}

			map.fitBounds(bounds);
			map.panToBounds(bounds);
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
	var end_stop = $("#estimator-destination").val()
	var end = $("#estimator-destination").val()
	var x = end.split(" ");
	end = x[0]

	$.ajax({
			type: "POST",
			url: "list_latlng/",
			data: {
				route: route
			}
		})
		.done(function (response) {

			var x = JSON.parse(response)

			var start_latlng = {
				lat: x[start].lat,
				lng: x[start].lng
			};
			var end_latlng = {
				lat: x[end].lat,
				lng: x[end].lng
			};

			var marker1 = new google.maps.Marker({
				position: new google.maps.LatLng(start_latlng),
				map: map,
				title: 'Origin',
				icon: 'http://maps.google.com/mapfiles/ms/icons/yellow-dot.png'
			});

			var marker2 = new google.maps.Marker({
				position: new google.maps.LatLng(end_latlng),
				map: map,
				title: 'Destination',
				icon: 'http://maps.google.com/mapfiles/ms/icons/green-dot.png'
			});

			allMarkers.push(marker1)
			allMarkers.push(marker2)

			list = destination_list.splice(0, destination_list.length - 2)

			index = list.indexOf(String(end_stop)) //finding the index of the selected stop
			destination_list = list.slice(0, index + 1) //displaying the stops after the selected stops 
			destination_list.pop()

			var bounds = new google.maps.LatLngBounds();
			for (key in destination_list) {
				var y = destination_list[key].split(" ");
				start = y[0]

				try {
					var stop_latlng = {
						lat: x[start].lat,
						lng: x[start].lng
					};
				} catch (err) {
					stop_latlng = null
				}

				var marker = new google.maps.Marker({
					position: new google.maps.LatLng(stop_latlng),
					map: map,
					title: 'stop ' + start,
					icon: 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png'
				});

				loc = new google.maps.LatLng(marker.position.lat(), marker.position.lng());
				bounds.extend(loc);

				allMarkers.push(marker)
			}

			map.fitBounds(bounds);
			map.panToBounds(bounds);


		})
};

// event listner to porpulate the route dropdown list)
$("#estimator-route").on('keyup click change hover focus', stops);
$("#estimator-route").change(origin_marker);
$("#estimator-route").change(removeLineFromMap);
$("#estimator-origin").change(destination_stops);

// go button for tab 2 to show and hide results
$(function () {

	$('#stop-to-stop-go').on('click', function () {

		// clear old fare and prediction values each time user clicks go
		$('#cash-and-leap-tab2').html("");
		$('#fare-result-tab2').html("");
		$("#stop-to-stop-estimate").html("");

		// hide results and fare initially 
		$('.fare-accordion').hide();
		$('#results-card').hide();
		$('#results-chart').hide();

		// show error if user doesn't complete all fields in form
		if ($('#estimator-route').val() == "" || $("#estimator-origin option:selected").text() == '-- Select --' ||
			$("#estimator-destination option:selected").text() == '-- Select --') {
			$('#stop-to-stop-incomplete-form-error').show();
		} else {
			$(".spinner-border").show();

			// calculate the route and hide line from map
			calcRoute();
			removeLineFromMap();

			//  use different date and time values depending on size of screen
			if ($(window).width() < 992) {
				datetimeValue = $("#datetime-tab2").val();
				var arr = datetimeValue.split('T');
				date = arr[0];
				time = arr[1];
			} else {
				var date = $("#datepicker-tab2").val();
				time = $('#timepicker-tab2').val();
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
					$('#results-card').show();

					// display fare to user and display 'unavailable' when no fare given
					var fare = response.fare;

					// if fare has found flag 'True', append fares to list
					if (fare["found"]) {
						for (const key in fare) {
							if (key != "url" && key != "route" && key != "found") {
								if (key == "Adult Cash" || key == "Adult Leap") {
									$('#cash-and-leap-tab2').append('<li>' + key + " Fare: " + "€" + fare[key] + "</li>");
								} else {
									$('#fare-result-tab2').append('<li>' + key + " Fare: " + "€" + fare[key] + "</li>");
								}
							}
						}
					} else {
						// else append unavailable
						$('#fare-result-tab2').append('<li>' + "Fare currently unavailable" + '</li>');
					}

					// hide spinner and show estimate
					$("#estimate-loader").hide();
					$("#stop-to-stop-estimate").html(response.result);
					if (response.result === "Currently unavailable") {
						$('#graph-loader').hide();
					} else {
						makeStatsRequest();
					}
				});


			// show results
			$(".form-area").hide();
			if ($(window).width() < 992) {
				$("#map-interface").css(
					"top", "350px");
			}
			$("#stop-to-stop-results").show();

			// set the value of the html for the summary results using the html id
			$("#origin-tab2").html("Stop " + $("#estimator-origin").val());
			$("#destination-tab2").html("Stop " + $("#estimator-destination").val());
		}
	});

	// add on click to edit-journey button to hide results and show journey planner
	$('#edit-journey-tab2').on('click', function () {
		clearMarkers()
		$(".form-area").show();
		$("#stop-to-stop-results").hide();
		$('.fare-accordion').hide();
		$('#cash-and-leap-tab2').html("");
		$('#fare-result-tab2').html("");

	});
	// call post request function when mobile datetime value changed
	$("#datetime-tab2-results").on("change", function () {
		sendDateTimeChangePostRequest();
	});
});


// post request sent again when date and time changed on results page
function sendDateTimeChangePostRequest() {

	// show and hide appropriate info 
	$('#results-card').hide();
	$("#stop-to-stop-estimate").hide();
	$("#estimate-loader").show();
	$('#results-chart').hide();

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
		$('#results-card').show();
		$("#estimate-loader").hide();
		$("#stop-to-stop-estimate").html(response.result);
		$("#stop-to-stop-estimate").show();
		// request new data for graphs when date & time changes
		console.log(response.result)
		if (response.result === "Currently unavailable") {
			$('#graph-loader').hide();
		} else {
			makeStatsRequest();
		}
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

	// diff date and time values depending on screen size
	if ($(window).width() < 992) {
		datetimeValue = $("#datetime-tab2-results").val();
		var arr = datetimeValue.split('T');
		params["date"] = arr[0];
		params["time"] = arr[1];
	} else {
		params["date"] = $("#datepicker-tab2-results-date").val();
		params["time"] = $('#datepicker-tab2-results-time').val();
	}

	return params;
}


// function for requesting graph data from web server
function makeStatsRequest() {

	// red the search parameters
	var params = getSearchParams();

	// hide any error messages from the previous search
	$("#no-data-error").hide();
	$('#graph-loader').show();
	// make the request
	$.ajax({
			type: "POST",
			url: "get_stats/",
			data: {
				date: params.date,
				time: params.time,
				route: params.route,
				direction: params.direction,
				end: params.end,
				start: params.start
			}
		})

		// when response received
		.done(function (response) {
			var data = JSON.parse(response);

			if (data.hourly != "none") {
				var infoObject = new Object();
				infoObject["data"] = data.hourly;
				infoObject["route"] = params.route;
				infoObject["start"] = params.start;
				infoObject["end"] = params.end;

				updateTextInfo(infoObject);
				drawBarChart(data.hourly);
				$('#results-chart').show();
			} else {
				chartDataError();
			}

			$('#graph-loader').hide();
		});
}


// display a textual description of the data contained in the graph
function updateTextInfo(data) {

	// get the 95% journey time for this time group
	var keys = Object.keys(data.data);
	var current_time = keys[Math.floor(keys.length / 2)];
	var journey_time = "dummy";
	var fastest_time;

	for (var key in data.data) {
		var t = data.data[key];
		if (journey_time === "dummy") {
			if (data.data[key] > 0) {
				journey_time = data.data[key];
				fastest_time = key;
			}
		} else if (t < journey_time) {
			// ignore journey times of 0 minute - this is missing data
			if (t > 0) {
				journey_time = data.data[key];
				fastest_time = key;
			}
		}
	}

	// if there's a faster time than the 'search time' add that to the description
	if (data.data[current_time] == 0) {
		$("#results-description").html("Unfortunately there is no historical data for buses at this time, however 95% of journey at " + fastest_time + " take less than " + data.data[fastest_time] + " minutes .");

	} else if (current_time === fastest_time) {
		$("#results-description").html("At " + current_time + " 95% of journeys take less than " + data.data[current_time] + " minutes.");
	} else {
		var timeDelta = data.data[current_time] - data.data[fastest_time];
		$("#results-description").html("At " + current_time + " 95% of journeys take less than " + data.data[current_time] + " minutes. This journey is up to " + timeDelta + " minute faster at " + fastest_time + ".");
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
		if (i == midpoint) {
			this.backgroundColor.push("rgba(64, 204, 219, 0.8)");
			this.borderColor.push("rgb(64, 204, 219)");
		} else {
			this.backgroundColor.push("rgba(184, 202, 204, 0.8)");
			this.borderColor.push("rgb(184, 202, 204)");
		}
	}
	this.borderWidth = 1;
	this.barPercentage = 0.95; // sets the relative width of bars in a bar chart
	this.categoryPercentage = 1; // sets the relative width of bars in a bar chart

	var arr = new Array();

	Object.keys(data).forEach(function (item) {
		arr.push(data[item]);
	})

	this.data = arr;
}


function drawBarChart(data) {

	// get the chart container from the info.html page
	var container = $("#chart-container");
	var bars = [];
	var labels = Object.keys(data);

	bars = new DataSet(data);

	// check if a chart already exists in the container div;
	// if so just update the existing chart with new data
	// else create a new chart element in the container div

	container.empty();
	$('<canvas id="results-canvas"></canvas>').prependTo(container);

	var ctx = $("#results-canvas");

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

function chartDataError() {
	// display an error message when no data historical data associated with the searched time...
	$("#no-data-error").show();
	$("#results-chart").hide();
}

//$('#stop-to-stop-go').on('click', makeStatsRequest)