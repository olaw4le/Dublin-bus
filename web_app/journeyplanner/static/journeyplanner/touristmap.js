$(document).ready(function () {

    // https://developers.google.com/maps/documentation/javascript/places
    var dublin = { lat: 53.3155395, lng: -6.4161858 };
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
                console.log(results[i]);
                console.log(results[i].icon);
                var icon = results[i].icon
                createMarker(results[i], type, icon, markers[type]);
            }
            console.log(markers[type]);
            console.log(markers);
        }
    }


    function clearMarkers(markers) {
        $.each(markers , function(index) { 
            console.log(index);
            markers[index].setMap(null);
          });
    }
});

// create markers
function createMarker(place, type, icon, markerList) {
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

    google.maps.event.addListener(marker, 'click', function () {
        infowindow.setContent(place.name);
        infowindow.open(map, this);
    });
}

