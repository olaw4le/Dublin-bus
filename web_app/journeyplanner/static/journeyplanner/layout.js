
// .ready waits for DOM to be loaded before executing this function
$(document).ready(function () {

    // loading html into tabs on dekstop view

    // .load() sends a get request and fills the html will the result of the request
    $("#map-interface-content").load("/routeplanner");
    // .getScript(name of script);

    $("#routeplanner-tab").click(function() {
        $("#map-interface-content").load("/routeplanner");
        console.log("HLKSDFFGSDGDFKLGJDLFGKJ");
        // .getScript(name of script);
    });

    $("#all-routes-tab").click(function() {
        $("#map-interface-content").load("/allroutes");
        console.log("allrotues");
    });

    $("#leap-tab").click(function() {
        $("#map-interface-content").load("/leap");
        console.log("leap");
    });

    $("#disruptions-tab").click(function() {
        $("#map-interface-content").load("/disruptions");
        console.log("disruptions");
    });

    $("#tourist-tab").click(function() {
        $("#map-interface-content").load("/tourist");
        console.log("tourist");
    });

    // loading html into from hamburger menu on mobile view

    $("#routeplanner-nav").click(function() {
        $("#map-interface-content").load("/routeplanner");
        console.log("HLKSDFFGSDGDFKLGJDLFGKJ");
        // .getScript(name of script);
    });

    $("#all-routes-nav").click(function() {
        $("#map-interface-content").load("/allroutes");
        console.log("allrotues");
    });

    $("#leap-nav").click(function() {
        $("#map-interface-content").load("/leap");
        console.log("leap");
    });

    $("#disruptions-nav").click(function() {
        $("#map-interface-content").load("/disruptions");
        console.log("disruptions");
    });

    $("#tourist-nav").click(function() {
        $("#map-interface-content").load("/tourist");
        console.log("tourist");
    });



// show and hide map
    $("#show-map").click(function () {

        // Toggle display of map-interface 
        $("#map-interface").toggle();

        // Change text on show/hide map button
        if ($("#map-interface").is(":hidden")){
            $("#show-map").html("Hide Map");
        } else {
            $("#show-map").html("Show Map");
        }
    });

    // Show interface if hidden when window resized and change button to say show map
    $(window).resize(function () {
        if ($(window).width() >= 992) {
            $("#map-interface").show();
            $("#show-map").html("Show Map");
        }
    });
});

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



