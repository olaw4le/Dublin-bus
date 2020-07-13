$(document).ready(function () {

    // https://developers.google.com/maps/documentation/javascript/places
    var dublin = { lat: 53.3155395, lng: -6.4161858 };
    // var touristIcons = {
    //     restaurant: {
    //         icon: "<img src=static/journeyplanner/icons/com.nextbus.dublin.jpg width=20 height=20>"
    //     }
    // }

    // loop through checkboxes and display markers on map using data attr
    $(".tourist-check").change(function () {
        if (this.checked) {
            var type = $(this).attr("data-type");

            var request = {
                location: dublin,
                radius: '50000',
                type: type
            };

            service = new google.maps.places.PlacesService(map);
            service.nearbySearch(request, callback);

        }
    });


    function callback(results, status) {
    console.log(status)
    if (status == google.maps.places.PlacesServiceStatus.OK) {
        for (var i = 0; i < results.length; i++) {
            createMarker(results[i]);
            // var marker = new google.maps.Marker({
            //     position: results[i],
            //     icon: touristIcons[type].icon,
            //     map:map


        }
    }
}
});

