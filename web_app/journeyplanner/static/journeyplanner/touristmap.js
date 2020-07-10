$(document).ready(function () {

    // https://developers.google.com/maps/documentation/javascript/places
    var dublin = { lat: 53.3155395, lng: -6.4161858 };

    var request = {
        location: dublin,
        radius: '50000',
        type: ['supermarket']
    };

    service = new google.maps.places.PlacesService(map);
    service.nearbySearch(request, callback);


});

function callback(results, status) {
    console.log(status)
    if (status == google.maps.places.PlacesServiceStatus.OK) {
        for (var i = 0; i < results.length; i++) {
            createMarker(results[i]);
        }
    }
}