
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
        $('.hide-slide-menu').removeClass("active");
        navIdFull = $(this).attr('id');
        navId = navIdFull.split("-")[0];

        $("#map-interface-content").load("/" + navId, function () {
            $('#' + navId + '-tab').addClass("active");
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
        // $('.nav-bottom').removeClass("active");
        navId = $(this).attr('id');
        $('#' + navId).addClass("active");
        navIdForTab = navId.split("-")[0];
        $('#' + navIdForTab + '-tab').addClass("active");

        // show map on input view of tourist map
        if ((navId === "tourist-nav" || navId === "allroutes-nav") && $(window).width() < 992) {
            $("#map-interface").animate({ top: "400px" }, 400);

        } else {
            $("#map-interface").css("top", "0px")
        }
    });


    $("#hide-menu").on('click', function(){
        $("#hide-menu").hide();
        $(".hide-slide-menu, #hide-menu").hide();
        $("#show-menu").fadeIn(10);
        $("#tab-menu").animate({
            "max-width": "30px",
            "width": "30px"
          }, 200);
    });
    $("#show-menu").on('click', function(){
        $("#show-menu").hide();
        $("#hide-menu").show();
        $("#tab-menu").animate({
            "max-width": "150px",
            "width": "150px"
          }, 200, () => $(".hide-slide-menu, #hide-menu").show());
    });

});
;

// Show interface if hidden when window resized and change button to say show map
$(window).resize(function () {

    if ($(window).width() <= 992){
          if ($('#tourist-nav').hasClass("active") || $('#allroutes-nav').hasClass("active")) {
            $("#map-interface").css("top", 400);
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




