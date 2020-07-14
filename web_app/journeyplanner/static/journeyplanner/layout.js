
// .ready waits for DOM to be loaded before executing this function
$(document).ready(function () {

    // function to populate datetime inputs with current date and time
    var currentDateTime = function () {
        var d = new Date();
        var datestring = d.getFullYear() + "-" + "0" + (d.getMonth() + 1) + "-" + "0" + d.getDate() + "T" + ("0" + d.getHours()).slice(-2) + ":" + ("0" + d.getMinutes()).slice(-2);
        return datestring;
    }

    // All nav items that load the interface pane have this class
    // When clicked the ID of the clicked element is checked and the
    // appropriate html is loaded and put in the interface
    $(".load-interface").click(function () {
        $('.nav-bottom').removeClass("active");
        navIdFull = $(this).attr('id');
        navId = navIdFull.split("-")[0];

        $("#map-interface-content").load("/" + navId, function () {
            console.log("id: " + navIdFull);
            console.log("id bottom: " + '#' + navId + '-nav');
            $('#' + navId + '-nav').addClass("active");
            $(".datetime").val(currentDateTime());
        });
    });

    // Load routeplanner by default when page is loaded
    $("#map-interface-content").load("/routeplanner", function () {
        $(".datetime").val(currentDateTime());
    });

    // show active link in bottom nav bar
    $('.nav-bottom').on('click', function () {
        $('#map').off('click');
        $('#map-interface').off('click');
        $('.nav-bottom').removeClass("active");
        navId = $(this).attr('id');
        $('#' + navId).addClass("active");

        // show map on input view of tourist map
        if (navId === "tourist-nav" && $(window).width() < 992) {
            $("#map-interface").css("top", "500px");
            $('#map').on('click', function () {
                $("#map-interface").css("top", "700px");
            });
            $('#map-interface').on('click', function () {
                $("#map-interface").css("top", "400px");
            });
        } else {
            $("#map-interface").css("top", "0px")
        }
    });
});
;

// Show interface if hidden when window resized and change button to say show map
$(window).resize(function () {
    if ($(window).width() >= 992) {
        $("#map-interface").show();
        $("#show-map").html("Show Map");
        $("#map-interface").css("top", "");

        if ($('#tourist-nav').hasClass("active")) {
            $("#map-interface").css("top", "0px");
        }
    }
});




