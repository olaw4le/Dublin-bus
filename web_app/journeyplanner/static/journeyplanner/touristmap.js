$(document).ready(function () {

    // flatpickr date https://flatpickr.js.org/options/
  $( "#datepicker-tourist" ).flatpickr({
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
    minTime: "05:00",
    minuteIncrement: 1
  });

    // https://developers.google.com/maps/documentation/javascript/places
    var dublin = { lat: 53.3155395, lng: -6.4161858 };

    // geolocation for tourists origin
    infoWindow = new google.maps.InfoWindow;
    var geocoder = new google.maps.Geocoder();


    // HTML5 geolocation from https://developers.google.com/maps/documentation/javascript/geolocation
    // if (navigator.geolocation) {
    //     navigator.geolocation.getCurrentPosition(function (position) {
    //         var pos = {
    //             lat: position.coords.latitude,
    //             lng: position.coords.longitude
    //         };

    //         // call geocoder function to convert coordinates to place name
    //         var address = geocodeLatLng(geocoder, pos.lat, pos.lng);
    // $('#origin-tourist').val(address);

    //         // center map at users location
    //         map.setCenter(pos);
    //     }, function () {
    //         handleLocationError(true, infoWindow, map.getCenter());
    //     });
    // } else {
    //     // Browser doesn't support Geolocation
    //     handleLocationError(false, infoWindow, map.getCenter());
    // }

    // function handleLocationError(browserHasGeolocation, infoWindow, pos) {
    //     infoWindow.setPosition(pos);
    //     infoWindow.setContent(browserHasGeolocation ?
    //         'Error: The Geolocation service failed.' :
    //         'Error: Your browser doesn\'t support geolocation.');
    //     infoWindow.open(map);

    // };








    var markers = {};
    // loop through checkboxes and display markers on map using data attr
    $(".tourist-check").change(function () {
        if (this.checked) {
            var type = $(this).attr("data-type");

            var request = {
                location: dublin,
                radius: '50000',
                type: type
            };

            console.log(type);
            service = new google.maps.places.PlacesService(map);
            service.nearbySearch(request, function (results, status) {
                callback(results, status, type)
            });

            // hide markers when checkbox un-checked
        } else if (!this.checked) {
            console.log("unchecked");
            var type = $(this).attr("data-type");
            var typeMarkers = markers[type];
            clearMarkers(typeMarkers);

        }
    });


    function callback(results, status, type) {
        console.log(status)
        if (status == google.maps.places.PlacesServiceStatus.OK) {

            markers[type] = []
            for (var i = 0; i < results.length; i++) {
                var icon = results[i].icon
                var rating = results[i].rating;
                console.log(results[i]);
                createMarker(results[i], type, icon, markers[type], rating);
            }
        }
    }


    function clearMarkers(markers) {
        $.each(markers, function (index) {
            console.log(index);
            markers[index].setMap(null);
        });
    }


    // create markers
    function createMarker(place, type, icon, markerList, rating) {
        var lat = place.geometry.location.lat();
        var lng = place.geometry.location.lng();

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

        // show name of place when mouse hovers over  marker
        google.maps.event.addListener(marker, 'mouseover', function () {
            infowindow.setContent(place.name + "<br>Rating: " + rating);
            infowindow.open(map, this);
        });


        // populate destination input box with location clicked on map
        google.maps.event.addListener(marker, 'click', function () {
            // convert lat and long to address using geocoder
            var address = geocodeLatLng(geocoder, lat, lng, "dest");
            console.log(address);
            $('#destination-tourist').val(address);

        });
    }

    // function to geocode coordinates into address
    function geocodeLatLng(geocoder, lat, lng, dest="") {
        var latlng = { lat: parseFloat(lat), lng: parseFloat(lng) };
        geocoder.geocode({ location: latlng }, function (results, status) {
            if (status === "OK") {
                if (results[0]) {
                    // populate origin input box with address 
                    // $('#origin-tourist').val(results[0].formatted_address);
                    if (dest === "dest") {
                        $('#destination-tourist').val(results[0].formatted_address);
                    } else {
                        $('#origin-tourist').val(results[0].formatted_address);
                    }
                    // var address = results[0].formatted_address;
                    // console.log(results[0].formatted_address);
                    // return address;
                } else {
                    window.alert("No results found");
                }
            } else {
                window.alert("Geocoder failed due to: " + status);
            }
        })
    };

});