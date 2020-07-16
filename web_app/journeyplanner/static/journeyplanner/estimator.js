$(document).ready(function () {

    // flatpickr date https://flatpickr.js.org/options/
    $("#datepicker-tab2").flatpickr({
        altInput: true,
        altFormat: "F j, Y",
        dateFormat: 'yy-m-d',
        defaultDate: new Date(),
        minDate: "today"
    });

    // flatpickr time
    $('#timepicker-tab2').flatpickr({
        enableTime: true,
        defaultDate: new Date().getHours() + ":" + new Date().getMinutes(),
        dateFormat: 'H:i',
        noCalendar: true,
        time_24hr: true,
        minTime: "05:00",
        minuteIncrement: 1
    });

});

//the code from w3 school 
function autocomplete(inp, arr) {
    /*the autocomplete function takes two arguments,
     the text field element and an array of possible autocompleted values:*/
    var currentFocus;
    /*execute a function when someone writes in the text field:*/
    inp.addEventListener("input", function (e) {
        var a,
            b,
            i,
            val = this.value;
        /*close any already open lists of autocompleted values*/
        closeAllLists();
        if (!val) {
            return false;
        }
        currentFocus = -1;
        /*create a DIV element that will contain the items (values):*/
        a = document.createElement("DIV");
        a.setAttribute("id", this.id + "autocomplete-list");
        a.setAttribute("class", "autocomplete-items");
        /*append the DIV element as a child of the autocomplete container:*/
        this.parentNode.appendChild(a);
        /*for each item in the array...*/
        for (i = 0; i < arr.length; i++) {
            /*check if the item starts with the same letters as the text field value:*/
            if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
                /*create a DIV element for each matching element:*/
                b = document.createElement("DIV");
                /*make the matching letters bold:*/
                b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
                b.innerHTML += arr[i].substr(val.length);
                /*insert a input field that will hold the current array item's value:*/
                b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
                /*execute a function when someone clicks on the item value (DIV element):*/
                b.addEventListener("click", function (e) {
                    /*insert the value for the autocomplete text field:*/
                    inp.value = this.getElementsByTagName("input")[0].value;
                    /*close the list of autocompleted values,
  (or any other open lists of autocompleted values:*/
                    closeAllLists();
                });
                a.appendChild(b);
            }
        }
    });
    /*execute a function presses a key on the keyboard:*/
    inp.addEventListener("keydown", function (e) {
        var x = document.getElementById(this.id + "autocomplete-list");
        if (x) x = x.getElementsByTagName("div");
        if (e.keyCode == 40) {
            /*If the arrow DOWN key is pressed,
increase the currentFocus variable:*/
            currentFocus++;
            /*and and make the current item more visible:*/
            addActive(x);
        } else if (e.keyCode == 38) {
            //up
            /*If the arrow UP key is pressed,
decrease the currentFocus variable:*/
            currentFocus--;
            /*and and make the current item more visible:*/
            addActive(x);
        } else if (e.keyCode == 13) {
            /*If the ENTER key is pressed, prevent the form from being submitted,*/
            e.preventDefault();
            if (currentFocus > -1) {
                /*and simulate a click on the "active" item:*/
                if (x) x[currentFocus].click();
            }
        }
    });
    function addActive(x) {
        /*a function to classify an item as "active":*/
        if (!x) return false;
        /*start by removing the "active" class on all items:*/
        removeActive(x);
        if (currentFocus >= x.length) currentFocus = 0;
        if (currentFocus < 0) currentFocus = x.length - 1;
        /*add class "autocomplete-active":*/
        x[currentFocus].classList.add("autocomplete-active");
    }
    function removeActive(x) {
        /*a function to remove the "active" class from all autocomplete items:*/
        for (var i = 0; i < x.length; i++) {
            x[i].classList.remove("autocomplete-active");
        }
    }
    function closeAllLists(elmnt) {
        /*close all autocomplete lists in the document,
except the one passed as an argument:*/
        var x = document.getElementsByClassName("autocomplete-items");
        for (var i = 0; i < x.length; i++) {
            if (elmnt != x[i] && elmnt != inp) {
                x[i].parentNode.removeChild(x[i]);
            }
        }
    }
    /*execute a function when someone clicks in the document:*/
    document.addEventListener("click", function (e) {
        closeAllLists(e.target);
    });
}

var routes = "";
var route_number = "";
var stop_name = "";
var stations = "";
var routes = ""

function clearMarkers() {
    setMapOnAll(null);
  }


<<<<<<< HEAD
$(function () {
||||||| 94a350c
$(function() {
=======
$(function() {
    
 clearMarkers()
>>>>>>> tab1

    var jqxhr = $.getJSON("static/journeyplanner/ordered_stops_main.json", null, function (data) {
        stations = data;

        for (var key in stations) {
            route_number += key + " ";
        }

        //turning the into an array
        route_number = route_number.trim().split(" ");
    });

    $("#estimator-route").autocomplete({
        source: function (request, response) {
            var matcher = new RegExp("^" + $.ui.autocomplete.escapeRegex(request.term), "i");
            response($.grep(route_number, function (item) {
                return matcher.test(item);
            }));
        }
    });

});

  
// function to populate the sub_routes list			
function route_list() {

    sel = $("#estimator-route").val();
    console.log(sel)

    //getting the value of the selected route
    var list = ''

    //jquery to open the json file 
    $.getJSON("static/journeyplanner/ordered_stops_main.json", null, function (data) {
        stations = data;

        // populating the sub route select list 
        var To = "<option value=0>Sub Route</option>";
        for (var key in stations) {


            if (sel.toString() == key.toString()) {

                routes = stations[key]

                for (var key2 in routes) {
                    console.log(key2)
                    list += key2 + " ";
                }
            }
        }

        //turning the into an array
        list = list.trim().split(" ");
        result=list

        //popuplating the sub route select list
        for (var i = 0; i < list.length; i++) {
            To += "<option  value=" + list[i] + ">" + list[i] + "</option>";
        }

        document.getElementById("estimator-sub").innerHTML = To;

    });
}

//getting the value of the selected sub route
var sel_sub = "";
<<<<<<< HEAD
var direction = ""
||||||| 94a350c
var direction= ""
=======
var direction= ""
var stop_list=[];
>>>>>>> tab1

// function to populate the origin and destination
function stops() {
    var To = "<option value=0>Stops</option>";

    // getting the value of the selected sub-route
    sel_sub = $("#estimator-sub").val();

    // going through the sub-routes the selected route has 
    for (key in routes) {
   
        // if the user selected sub-route is found 
        if (sel_sub == key) {

            // the stops the selected sub-routes goes through
            bus_stops = routes[key].stops;

            direction = routes[key].direction


            // poppulating the origin and destination with the stops
            for (var i = 0; i < bus_stops.length; i++) {
                To += "<option  value=" + bus_stops[i] + ">" + bus_stops[i] + "</option>";

                stop_list.push(bus_stops[i])

            }

            // populating the inner html
<<<<<<< HEAD
            $("#estimator-origin").html(To)
            $("#estimator-destination").html(To);
||||||| 94a350c
          $("#estimator-origin").html(To) 
          $("#estimator-destination").html(To);
=======
          $("#estimator-origin").html(To) 
>>>>>>> tab1

        }
<<<<<<< HEAD
        // else if(sel_sub != key){
        //     // the stops the selected sub-routes goes through
        //          bus_stops = routes.stops;
        //          direction= routes.direction

        //          // poppulating the origin and destination with the stops
        //         for (i in bus_stops) {
        //             To += "<option  value=" + bus_stops[i] + ">" + bus_stops[i] + "</option>";

        //         }
        //         // populating the inner html
        //         $("#estimator-origin").html(To);
        //         $("#estimator-destination").html(To);


        //     }
||||||| 94a350c
        // else if(sel_sub != key){
        //     // the stops the selected sub-routes goes through
        //          bus_stops = routes.stops;
        //          direction= routes.direction
    
        //          // poppulating the origin and destination with the stops
        //         for (i in bus_stops) {
        //             To += "<option  value=" + bus_stops[i] + ">" + bus_stops[i] + "</option>";
    
        //         }
        //         // populating the inner html
        //         $("#estimator-origin").html(To);
        //         $("#estimator-destination").html(To);
    
    
        //     }
=======
    }  
}
var index;
    // function to populate the remaining destination stop
    function destination(){
        var To = "<option value=0>Stops</option>";

        starting_stop=$("#estimator-origin").val()
        console.log(starting_stop)
        console.log(stop_list) 
        index = stop_list.indexOf(+starting_stop) //finding the index of the selected stop
        destination_list=stop_list.slice(index + 1) //displaying the stops after the selected stops 

        console.log(destination_list)

        for (var i = 0; i < destination_list.length; i++) {
            To += "<option  value=" + destination_list[i] + ">" + destination_list[i] + "</option>";

        }

           // populating the inner html with the destination
           $("#estimator-destination").html(To)
        

>>>>>>> tab1


    }
<<<<<<< HEAD

||||||| 94a350c
    
=======


function origin_marker(){
    var origin_stop=$("#estimator-origin").val()
    var route=sel= $("#estimator-route").val();
    
    
    $.ajax({
        type:"POST",
        url:"list_latlng/",
        data:{route:route}
      })

      .done(function(response){
          console.log("successfully posted");
          var x=JSON.parse(response)

          var map = new google.maps.Map(document.getElementById("map"), {
            zoom: 14,
            center:{ lat: 53.350140, lng: -6.266155 }
          })

          for (key in x) { 
           var marker = new google.maps.Marker({
              position: new google.maps.LatLng(x[key].lat, x[key].lng),
              map: map,
              title: "Stop" + key,
              

             
            });
            }
      });
>>>>>>> tab1
}


// event listner to porpulate the route dropdown list)
$("#estimator-route").on('keyup click change hover', route_list);

// event listner to populate the origin and destination 
$("#estimator-sub").change(stops);

<<<<<<< HEAD
var route, origin, destination;

||||||| 94a350c
=======
$("#estimator-route").change(origin_marker);
$("#estimator-origin").change(destination);


>>>>>>> tab1
// go button for tab 2 to show and hide results
$(function () {

    $('#stop-to-stop-go').on('click', function () {

        if ($(window).width() < 992) {
            datetimeValue = $("#datetime-tab2").val();
            console.log("datetime value mobile: " + datetimeValue );
            var arr = datetimeValue.split('T');
            date = arr[0];
            console.log("mobile date: " + date);
            time = arr[1];
            console.log("mobile time: " + time);
        } else {
            var date = $("#datepicker-tab2").val();
            console.log("desktop date: " + date);
            time = $('#timepicker-tab2').val();
            console.log("desktop time: " + time);

            // use date and time here to make properly formatted datetimeValue for mobile
            datetimeValue = date + 'T' + time;
            console.log("datetimevalue test: " + datetimeValue);
        }
        // show date and time inputs on desktop results page for better user experience
        // default date and time are those selected by user on input page
        $("#datepicker-tab2-results-date").flatpickr({
            altInput: true,
            altFormat: "F j, Y",
            dateFormat: 'yy-m-d',
            defaultDate: date,
            minDate: "today",
            onClose: function (selectedDates, dateStr, instance) {
                sendDateTimeChangePostRequest();
                console.log("craoissant day");
            },
        });

        $('#datepicker-tab2-results-time').flatpickr({
            enableTime: true,
            defaultDate: time,
            dateFormat: 'H:i',
            noCalendar: true,
            time_24hr: true,
            minTime: "05:00",
            minuteIncrement: 1,
            onClose: function (selectedDates, dateStr, instance) {
                sendDateTimeChangePostRequest();
                console.log("craoissant time");
            },
        });


        $(".datetime").val(datetimeValue);

        // convert time to seconds since midnight
        // console.log("time: "+ input_time);
        console.log("time: " + time);
        var timeSplit = time.split(':');
        var timeSeconds = (+timeSplit[0]) * 60 * 60 + (+timeSplit[1]) * 60;
        console.log(timeSeconds);

        // sending a post request to the server
        route = $("#estimator-route").val();
        origin = $("#estimator-origin").val();
        destination = $("#estimator-destination").val();
        $.ajax({
            type: "POST",
            url: "prediction/",
            data: {
                date: date,
                time: timeSeconds,
                route: route,
                origin: origin,
                destination: destination,
                direction: direction
            }
        })

            .done(function (result) {
                console.log("successfully posted");
                $(".spinner-border").hide();
                $("#stop-to-stop-estimate").html(result + " minutes");
                // console.log(result);

            });

<<<<<<< HEAD
        // show results
||||||| 94a350c
    // show results
=======

    // show results
>>>>>>> tab1
        $(".form-area").hide();
        if ($(window).width() < 992) {
            $("#map-interface").css("top", "400px");
        }
        $("#stop-to-stop-results").show();

        //getting the value of the user selected time
        //var time = $("#datetime-tab2").val();


        // var dateArr, date, dateElements, year, month, date, time, dateToDisplay;

        // dateArr = time.split('T');
        // date = dateArr[0];
        // dateElements = date.split('-');
        // year = dateElements[0];
        // month = dateElements[1];
        // date = dateElements[2];
        // dateToDisplay = date + "-" + month + "-" + year;

        // time = dateArr[1];

        // set the value of the html for the results using the html id
        $("#origin-tab2").html("Stop " + $("#estimator-origin").val());
        $("#destination-tab2").html("Stop " + $("#estimator-destination").val());
        // $("#datetime-tab").html(dateToDisplay + ", " + time)




    });

    // add on click to edit-journey button to hide results and show journey planner
    $('#edit-journey-tab2').on('click', function () {
        console.log("inside edit-journey-results");
        $(".form-area").show();
        $("#map-interface").css("top", "0px");
        $("#stop-to-stop-results").hide();
    });

// call post request function when mobile datetime value changed
    $("#datetime-tab2-results").on("change", function () {
        sendDateTimeChangePostRequest();
    });




});



// these need to be the results ids??? 

function sendDateTimeChangePostRequest() {

    $("#stop-to-stop-estimate").hide();
    $(".spinner-border").show();

    if ($(window).width() < 992) {
        datetimeValue = $("#datetime-tab2-results").val();
        var arr = datetimeValue.split('T');
        date = arr[0];
        console.log("mobile date: " + datetimeValue);
        time = arr[1];
    } else {
        var date = $("#datepicker-tab2-results-date").val();
        console.log("desktop date: " + date);
        time = $('#datepicker-tab2-results-time').val();
        console.log("desktop time: " + time);

        // use date and time here to make properly formatted datetimeValue for mobile
        datetimeValue = date + 'T' + time;
    }
    $(".datetime").val(datetimeValue);
    $("#datepicker-tab2-results-date").val(date);
    $("#datepicker-tab2-results-time").val(time);


    var timeSplit = time.split(':');
    var timeSeconds = (+timeSplit[0]) * 60 * 60 + (+timeSplit[1]) * 60;
    console.log(timeSeconds);

    $.ajax({
        type: "POST",
        url: "prediction/",
        data: {
            date: date,
            time: timeSeconds,
            route: route,
            origin: origin,
            destination: destination,
            direction: direction
        }
    }).done(function (result) {
        console.log("successfully posted");
        $(".spinner-border").hide();
        $("#stop-to-stop-estimate").show();
        $("#stop-to-stop-estimate").html(result + " minutes");
        // console.log(result);

    });
}