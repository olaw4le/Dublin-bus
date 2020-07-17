
// .ready waits for DOM to be loaded before executing this function
$(document).ready(function () {

    // function to populate datetime inputs with current date and time
    var currentDateTime = function () {
        var d = new Date();
        var month = ((d.getMonth()+1) < 10) ? "0" + (d.getMonth()+1) : (d.getMonth()+1);
        var date = (d.getDate()  < 10) ? "0" + d.getDate() : d.getDate();
        var datestring = d.getFullYear() + "-" + month + "-" + date + "T" + ("0" + d.getHours()).slice(-2) + ":" + ("0" + d.getMinutes()).slice(-2);
        console.log("full date " + datestring);
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
        $('.nav-bottom').removeClass("active");
        navId = $(this).attr('id');
        $('#' + navId).addClass("active");

        // show map on input view of tourist map
        if (navId === "tourist-nav" && $(window).width() < 992) {
            $("#map-interface").css("top", "400px");

        } else {
            $("#map-interface").css("top", "0px")
        }
    });
});
;

// Show interface if hidden when window resized and change button to say show map
$(window).resize(function () {

    if ($(window).width() <= 992){
          if ($('#tourist-nav').hasClass("active")) {
            $("#map-interface").css("top", "400px");
        }
    }
    if ($(window).width() >= 992) {
        $("#map-interface").show();
        $("#show-map").html("Show Map");
        $("#map-interface").css("top", "");

        // if ($('#tourist-nav').hasClass("active")) {
        //     $("#map-interface").css("top", "");
        // }
    }
});




