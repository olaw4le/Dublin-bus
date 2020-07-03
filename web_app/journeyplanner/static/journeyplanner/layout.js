
// .ready waits for DOM to be loaded before executing this function
$(document).ready(function () {



    // function to populate datetime inputs with current date and time
    var currentDateTime = function(){
        var d = new Date();
        var datestring = d.getFullYear() + "-" + "0" + (d.getMonth()+1) + "-" + "0" + d.getDate() + "T" + ("0" + d.getHours()).slice(-2) + ":" + ("0" + d.getMinutes()).slice(-2);
        console.log("full date " + datestring);
        $(".datetime").val(datestring);
    }

    // All nav items that load the interface pane have this class
    // When clicked the ID of the clicked element is checked and the
    // appropriate html is loaded and put in the interface
    $(".load-interface").click(function() {
        navId = $(this).attr('id');
        navId = navId.split("-")[0];
        console.log(navId);
        
        $("#map-interface-content").load("/" + navId);
    });

    // Load routeplanner by default when page is loaded
    $("#map-interface-content").load("/routeplanner", function () {
        currentDateTime();
    });

    
// show and hide map
    // $("#show-map").click(function () {

    //     // Toggle display of map-interface 
    //     $("#map-interface").toggle();

    //     // Change text on show/hide map button
    //     if ($("#map-interface").is(":hidden")){
    //         $("#show-map").html("Hide Map");
    //     } else {
    //         $("#show-map").html("Show Map");
    //     }
    // });

    // show active link in bottom nav bar
    $('.nav-bottom').on('click', function(){
        $('.nav-bottom').removeClass("active");
        navId = $(this).attr('id');
        console.log(navId);
        $('#' + navId).addClass("active");
        $("#map-interface").css("top", "0px");
    });

});
;

// Show interface if hidden when window resized and change button to say show map
$(window).resize(function () {
    if ($(window).width() >= 992) {
        $("#map-interface").show();
        $("#show-map").html("Show Map");
        $("#map-interface").css("top", "");
    }
});




