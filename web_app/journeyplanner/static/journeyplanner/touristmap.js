// initialise center of map for both desktop and mobile screens
var dublin = {
	lat: 53.349424,
	lng: -6.363448826171867
};
var mobileDublin = {
	lat: 53.350152,
	lng: -6.260416
};

$(document).ready(function () {

	// remove tourist markers when user navigates to different tab using name spacing
	$(document).off('click.tourist');
	$(document).on('click.tourist', "#routeplanner-tab, .edit-journey, #allroutes-tab, #tourist-tab, #tourist-nav, #routeplanner-nav, #allroutes-nav, #leap-nav, #realtime-nav,#realtime-tab,#leap-tab", function () {
		clearAllTouristMarkers(markers);
		removeLineFromTouristMap();
	});

	// center the map and set the zoom
	map.panTo(dublin)
	map.setZoom(12);

	// on mobile, pan to a slightly different coordinate in dublin
	if ($(window).width() <= 992) {
		map.panTo(mobileDublin);
	}

	// hide destination box initially
	$('#destination-tourist').hide();

	// initialise tooltip for geolocation information
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

	// use autocomplete for origin and destination
	var input1 = document.getElementById("origin-tourist");

	//setting the autocomplete to dublin only
	var bound = new google.maps.LatLngBounds(new google.maps.LatLng(52.999804, -6.841221), new google.maps.LatLng(53.693045, -5.914218));

	var options = {
		componentRestrictions: {
			country: "ie"
		},
		types: ['geocode'],
		bounds: bound,
		strictBounds: true,
	};

	origin = new google.maps.places.Autocomplete(input1, options);

	// hide error when content of origin input box changed
	$("#origin-tourist").on("input", function () {
		$('.geo-error').hide();
	});


	// call the geolocation function when button is clicked
	$('#geolocation-tourist').on('click', function (e) {
		e.preventDefault(); //prevent this button from causing the form error handling
		getGeolocation('origin-tourist');
		$('.geo-spinner').show();
	});
});

// use the Google Place API to display tourist attractions on the map
// https://developers.google.com/maps/documentation/javascript/places
var markers = {};
var destination_latlng;
var name;
var infowindow;
var directionsRenderer;
var markerArray = [];

// prevent the enter button working on the autocomplete dropdown
// this is done to prevent the geolocation button underneath being selected when enter is clicked
$(".form-control").keydown(function (e) {
	if (e.keyCode == 13) {
		return false;
	}
});

// loop through checkboxes and display markers on map using data attribute
$(".tourist-check").change(function () {

	// center to correct area of map depending on screen size 
	if ($(window).width() <= 992) {
		map.panTo(mobileDublin);
		map.setZoom(13);
	} else {
		map.panTo(dublin);
		map.setZoom(13);
		map.panBy(300, 0);
	}

	if (this.checked) {
		var type = $(this).attr("data-type");

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
		clearTouristMarkers(typeMarkers);

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
function clearTouristMarkers(markers) {
	$.each(markers, function (index) {
		markers[index].setMap(null);
	});
}

// clear markers of all Place Types from tourist map
function clearAllTouristMarkers(markers) {
	for (var type in markers) {
		clearTouristMarkers(markers[type]);
	}
}

// remove route line and all markers from tourist map
function removeLineFromTouristMap() {
	if (directionsRenderer) {
		directionsRenderer.setDirections({
			routes: []
		});
	}
	if (markerArray) {
		for (var i = 0; i < markerArray.length; i++) {
			markerArray[i].setMap(null);
		}
	}
}

// create markers, add event listeners to show info window on hover and on-clicks
// use IIFE to ensure the correct information is associated with each on-click event
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

	// show name of place and rating when mouse hovers over marker
	google.maps.event.addListener(marker, 'mouseover', (function (placeName, rating) {
		return function () {
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

// initialise info window and some variables
infoWindow = new google.maps.InfoWindow;
var ending_lat;
var ending_lng;
var starting_lat;
var starting_lng;


//function to covert the date time into timestamp
function timestamp() {
	var pickedDate = $("#datepicker-tourist").val()
	var pickedTime = $('#dtimepicker-tourist').val()
	var x = (pickedDate + ' ' + pickedTime)
	var departureTime;

	// making sure the date chosen isnt less than the current date 
	if (Date.parse(x) < Date.now()) {
		departureTime = Date.now();
	} else {
		departureTime = Date.parse(x);
	}

	return departureTime
	// return departureTime + 3600000; // 1 hour time zoon difference 

}

// show route on map
function routes_tourist() {

	// clear tourist markers from map
	clearAllTouristMarkers(markers);
	var starting = origin.getPlace();

	if (!geolocation) {
		//getting the lat and lng of the input address 
		// display error to user if valid starting location not entered
		if (!starting) {
			$('.invalid-location-error').show();
			return false;
		} else {
			//starting address latitude
			var starting_lat = starting.geometry.location.lat();
			var starting_lng = starting.geometry.location.lng();
		}
	}

	// Create a renderer for directions and bind it to the map.
	directionsRenderer = new google.maps.DirectionsRenderer({
		map: map,
		preserveViewport: true
	});

	// Instantiate an info window to hold step text.
	var stepDisplay = new google.maps.InfoWindow;

	// Display the route between the initial start and end selections.
	calculateAndDisplayRoute(directionsRenderer, directionsService, markerArray, stepDisplay, map);
	return true;
}


// calculating and showing the bus routes
function calculateAndDisplayRoute(directionsRenderer, directionsService, markerArray, stepDisplay, map) {
	var userTime = timestamp()

	// Retrieve the start and end locations and create a DirectionsRequest using
	// Bus directions.
	directionsService.route({
		origin: document.getElementById('origin-tourist').value,
		destination: destination_latlng,
		travelMode: 'TRANSIT',
		transitOptions: {
			modes: ['BUS'],
			routingPreference: 'FEWER_TRANSFERS',
			departureTime: new Date(userTime)
		}
	},

		// showing the response received in a text format 
		function (response, status) {

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
				$("#origin-tourist-summary").html(address1);
				$("#destination-tourist-summary").html(name);

				// fill date and time details into summary results
				if ($(window).width() < 992) {
					datetimeValue = $("#datetime-tourist").val();
					var arr = datetimeValue.split('T');
					date = arr[0];
					time = arr[1];
				} else {
					date = $("#datepicker-tourist").val();
					time = $('#timepicker-tourist').val();

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
				$(".datetime-results-tourist").html(dateToDisplay + ", " + time);

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
				var list = []
				var list1 = []

				var datetimeValue = $("#datetime-tourist").val();
				var arr = datetimeValue.split('T');
				var date1 = arr[0];
				var input_time = arr[1];

				// convert time to seconds since midnight
				var timeSplit = input_time.split(':');
				var timeSeconds = (+timeSplit[0]) * 60 * 60 + (+timeSplit[1]) * 60;

				var journeyTime = 0;
				for (var i = 0; i < journeysteps.length; i++) {

					// going through the repsone recieved from google
					var travelMode = journeysteps[i].travel_mode;

					// going through the object to get the travel mode details 

					if (travelMode == "WALKING") {
						duration = journeysteps[i].duration.text;
						journeyTime += parseInt(duration)

						//trimming the instruction text
						instruction = instruction.split(',');
						instruction = instruction[0];

					} else if (travelMode == "TRANSIT") {
						var journey_steps = {}; //dictionary for each bus steps in the journey
						distance = journeysteps[i].distance.text;
						duration = journeysteps[i].duration.text
						x = duration.split(" ")
						duration = x[0]
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
						journey_steps["duration"] = duration;

						list.push(journey_steps)
						list1.push(Route_number)

						//turning the data to sent into json
						var data = JSON.stringify(journey_steps);
					}
				}

				var data = JSON.stringify(list);

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

					// response returned from post request
					.done(function (response) {

						response = JSON.parse(response)

						// hide spinner when post request is done
						$('.prediction-spinner').hide();
						$('.results-card').show();
						$('.fare-accordion').show();

						// extract the fare from the response
						let fare = response.fare;

						// clear the fare each time a new fare is shown
						$('#fare-result-tourist').html("");
						$('#total-fares-tourist').html("");

						// initialise total cash and leap fares
						var total_cash = 0;
						var total_leap = 0;

						// keep track of whether a fare for every bus was added to the total
						var all_fares_included = true;

						// loop through all fare dictionaries in the list returned
						fare.forEach(element => {
							if (element["found"]) {
								$('#fare-result-tourist').append('<li>' + "Route " + element["route"] + ":" + "</li>");
								// append all price related items to list
								for (const key in element) {
									if (key != "url" && key != "route" && key != "found") {
										$('#fare-result-tourist').append('<li>' + key + ": " + "€" + element[key] + "</li>");
									}
									// parse from a string to a float and add to cash or leap total
									if (key == "Adult Cash") {
										amount = parseFloat(element[key]);
										total_cash += amount;

									}
									if (key == "Adult Leap") {
										element[key] = parseFloat(element[key]);
										total_leap += element[key];
									}
								}
								//add new line
								$('#fare-result-tourist').append('<br>');
							} else {

								// if all fares not included, show a message to the user 
								all_fares_included = false;
								$('#fare-result-tourist').append('<li>' + "Route " + element["route"] + ":" + '</li>');
								$('#fare-result-tourist').append('<li>' + "Unavailable" + '</li>');
								$('#fare-result-tourist').append('<br>');
							}
						});

						// cap leap total at €6
						if (total_leap > 6) {
							total_leap == 6.00
						}

						// use regex to remove leading 0 for values below €10
						total_leap = "" + total_leap.toFixed(2);
						total_leap = total_leap.replace(/^0+/, '');
						total_cash = "" + total_cash.toFixed(2);
						total_cash = total_cash.replace(/^0+/, '');

						// append totals to list and display to user
						// if all fares included display to user with no error message
						if (all_fares_included) {
							$('#total-fares-tourist').append('<li>' + "Total Cash Fare: €" + total_cash + '</li>');
							$('#total-fares-tourist').append('<li>' + "Total Leap Fare: €" + total_leap + '</li>');
						} else {
							// if all fares unavailable show total as unavailable
							if (total_cash == 0) {
								$('#total-fares-tourist').append('<li>' + "Total Cash Fare: Unavailable" + '</li>');
							}
							if (total_leap == 0) {
								$('#total-fares-tourist').append('<li>' + "Total Leap Fare: Unavailable" + '</li>');
							} else {
								// else show totals that are available along with error message
								$('#total-fares-tourist').append('<li>' + "Total Cash Fare: €" + total_cash + '</li>');
								$('#total-fares-tourist').append('<li>' + "Total Leap Fare: €" + total_leap + '</li>');
								$('.fare-total-message').show();
							}
						}

						prediction1 = response.prediction;

						//function to get each predcition in the list returned
						function bus_time(k) {

							return prediction1[k]
						}

						var number = 0

						// adding the predicted time to the total time
						for (var j = 0; j < prediction1.length; j++) {
							journeyTime += parseInt(prediction1[j])
						}
						var format = journeyTime

						//coverting the time in hours and minutes
						function timeConvert(n) {
							var num = n;
							var hours = (num / 60);
							var rhours = Math.floor(hours);
							var minutes = (hours - rhours) * 60;
							var rminutes = Math.round(minutes);
							return rhours + "hour " + rminutes + " mins";
						}

						// show the total durtion in the right format
						if (format >= 60) {
							format = timeConvert(format)
						} else {
							format = journeyTime + ' mins'
						}

						var b = input_time.split(':');
						var theFutureTime = moment().hour(b[0]).minute(b[1]).add(journeyTime, 'minutes').format("HH:mm");

						// setting the total time and predicted arrival time in the html

						$("#duration-val-tourist").html(format)
						$("#journey-time").html(input_time + ' - ' + theFutureTime)


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

								direction_text.append('<li>' + walking + '  ' + instruction + '</p><p>' + road + '  <b>Duration:</b> ' + duration + '</li>');

							} else if (travelMode == "TRANSIT") {
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


								direction_text.append('<li><p>' + bus + '  ' + instruction + '</p><p>' + road + '<b> Route: </b>' + Route_number + '  <b>Stops: </b>' + num_stops + '<b> Duration: </b>' + bus_time(number) + " mins" + '</p></li>');

								number += 1
							}
						}
					})
				//showing the response on the map. 	 
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

		// hide no directions error and show summary results
		$('#tourist-summary-results').show();
		$('.no-directions-error').hide();

		// show loader while prediction is loading
		$('.prediction-spinner').show();
		$('.results-card').hide();

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
			}

			// convert time to seconds since midnight
			var timeSplit = time.split(':');
			var timeSeconds = (+timeSplit[0]) * 60 * 60 + (+timeSplit[1]) * 60;

			// show results and routes
			var tourist_success = routes_tourist();
			if (tourist_success) {
				$(".form-area").hide();
				$("#checkbox-card").hide();
				if ($(window).width() < 992) {
					$("#map-interface").css(
						"top", "350");
				}
				$("#route-results-tourist").show();
			}
		}
	});

	// add on click to edit-journey button to hide results and show journey planner
	$('.edit-journey').on('click', function () {

		// hide the fare and error messages when the user clicks back
		$('.no-directions-error').hide();
		$('.fare-accordion').hide();

		// pan to correct place on map depending on screen size
		if ($(window).width() <= 992) {
			map.panTo(mobileDublin);
			map.setZoom(13);
		} else {
			map.panTo(dublin);
			map.setZoom(13);
			map.panBy(300, 0);
		}

		// when the user clicks 'back' show the markers again of the checked check-box
		$('.tourist-check').each(function (index, obj) {
			if (this.checked) {
				var type = $(this).attr("data-type");

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
			}
		});

		$("#checkbox-card").show();
		$(".form-area").show();
		// show half map on mobile screens
		if ($(window).width() < 992) {
			$("#map-interface").css(
				"top", "350");
		}
		$("#route-results-tourist").hide();
		$('#direction-tourist').empty()
	});
});