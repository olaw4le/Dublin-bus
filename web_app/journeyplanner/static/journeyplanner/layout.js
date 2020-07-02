
// .ready waits for DOM to be loaded before executing this function
$(document).ready(function () {

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
    $("#map-interface-content").load("/routeplanner");
    // .getScript(name of script);


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


    // Collapse mobile nav bar when menu item is clicked
    $('.navbar-nav>a').on('click', function(){
        $('.navbar-collapse').collapse('hide');
    });

    // show active link in bottom nav bar
    $('.nav-bottom').on('click', function(){
        $('.nav-bottom').removeClass("active");
        navId = $(this).attr('id');
        console.log(navId);
        $('#' + navId).addClass("active");
    });
});
;
// bootstrap datetime picker
$(function () {
    $('#datetimepicker1').datetimepicker({
        icons: {
			time: 'far fa-clock',
			date: 'far fa-calendar',
			up: 'fas fa-arrow-up',
			down: 'fas fa-arrow-down'
		}
    });
});


// Show interface if hidden when window resized and change button to say show map
$(window).resize(function () {
    if ($(window).width() >= 992) {
        $("#map-interface").show();
        $("#show-map").html("Show Map");
    }
});



