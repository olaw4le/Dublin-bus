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

//jquery to acess the json file
var jqxhr = $.getJSON("static/journeyplanner/ordered_stops_main.json", null, function (data) {
    stations = data;

    for (var key in stations) {
        route_number += key + " ";
    }

    //turning the into an array
    route_number = route_number.trim().split(" ");

    console.log(route_number)

    // using auto complete for the all the bus stop, if i use jquery it wont work
    autocomplete(document.getElementById("estimator-route"), route_number);
});

//getting the value of the selected route
var sel = ""

// function to populate the sub_routes list			
function route_list() {

    //getting the value of the selected route
    sel = $("#estimator-route").val();

    var list = ''

    //jquery to open the json file 
    $.getJSON("static/journeyplanner/ordered_stops_main.json", null, function (data) {
        stations = data;

        // populating the sub route select list 
        var To = "<option value=0>Sub Route</option>";
        for (var key in stations) {

            if (sel == key) {
                routes = stations[key]

                for (var key2 in routes) {
                    list += key2 + " ";
                }
            }
        }

        //turning the into an array
        list = list.trim().split(" ");

        //popuplating the sub route select list
        for (var i = 0; i < list.length; i++) {
            To += "<option  value=" + list[i] + ">" + list[i] + "</option>";
        }

        document.getElementById("estimator-sub").innerHTML = To;

    });
}

//getting the value of the selected sub route
var sel_sub = "";

// function to populate the origin and destination
function stops() {
    var To = "<option value=0>Routes</option>";

    // getting the value of the selected sub-route
    sel_sub = $("#estimator-sub").val();

    // going through the sub-routes the selected route has 
    for (key in routes) {

        // if the user selected sub-route is found 
        if (sel_sub == key) {

            // the stops the selected sub-routes goes through
            bus_stops = routes[key].stops;

            // poppulating the origin and destination with the stops
            for (var i = 0; i < bus_stops.length; i++) {
                To += "<option  value=" + bus_stops[i] + ">" + bus_stops[i] + "</option>";

            }
            // populating the inner html
            document.getElementById("estimator-origin").innerHTML = To;
            document.getElementById("estimator-destination").innerHTML = To;

        }
    }
    console.log(sel_sub)
}

// event listner to porpulate the route dropdown list
$("#estimator-route").change(route_list);
// event listner to populate the origin and destination 
$("#estimator-sub").change(stops);

// go button for tab 2 to show and hide results
$(function () {
  
    $('#stop-to-stop-go').on('click', function () {
        var datetimeValue = $("#datetime-tab2").val();
        var arr = datetimeValue.split('T');
        var date = arr[0];
        var time = arr[1];
     
        console.log("date: " + date);
        console.log("time: "+ time);

        // convert time to seconds since midnight
        console.log("time: "+ time);
        var timeSplit = time.split(':');
        var timeSeconds = (+timeSplit[0]) * 60 * 60 + (+timeSplit[1]) * 60;
        console.log(timeSeconds); 

        // show results
        $(".form-area").hide();
        $("#map-interface").css("top", "400px");
        $("#stop-to-stop-results").show();
  
    });
  
    // add on click to edit-journey button to hide results and show journey planner
    $('#edit-journey-tab2').on('click', function () {
        console.log("inside edit-journey-results");
      $(".form-area").show();
      $("#map-interface").css("top", "0px");
      $("#stop-to-stop-results").hide();
    });
  
  
  });