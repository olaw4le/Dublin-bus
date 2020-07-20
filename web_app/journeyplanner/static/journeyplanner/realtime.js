var routes = "";
var stop_number = "";
var stop_name = "";
var latitude = "";
var longitude = "";



$(function() {
    //jquery to acess the json file
var jqxhr = $.getJSON("static/bus_ routes_routes_stops.json", null, function (data) {
    stations = data.bus;
    // going through the list of objects in the json file
    for (var i = 0; i < stations.length; i++) {
         routes += stations[i].routes + " ";
         stop_number += stations[i].stopid + " ";
         stop_name += stations[i].shortname +stations[i].stopid+ " ";
                    }
    //turning the into an array
    stop_number = stop_number.trim().split(" ");
    stop_name=  stop_name.trim().split(" ");
    
    //getting unqiue value of all the stops number
    stop_number = stop_number.filter(function (item, pos) {
                        return stop_number.indexOf(item) == pos;
                    });

    
    $("#Stop-number").autocomplete({
        source: function (request, response) {
            var matcher = new RegExp("^" + $.ui.autocomplete.escapeRegex(request.term), "i");
            response($.grep(stop_number, function (item) {
                return matcher.test(item);
            }));
        }
    });


})


})

// getting the real time bus info
function bustime(){
    var url= 'https://data.smartdublin.ie/cgi-bin/rtpi/realtimebusinformation?stopid=124&format=json'

    var stopnumber=$("#Stop-number").val()
        
    var tableRows = ""
    // request to get the bus time table, this should be done in the django app
    $.ajax({
        type:"POST",
        url:"real_time/",
        data:{stopnumber:stopnumber}
      })

      .done(function(response){
          var x=JSON.parse(response)
          businfo= x.results
          tableRows += "<tr><th>Route Number</th><th>Destination</th><th>Due time</th></tr>"

          for (var i = 0; i < businfo.length; i++) {
           var route_number= businfo[i].route;
           var origin= businfo[i].origin
           var destination= businfo[i].destination;
           var due_time= businfo[i].duetime;

           console.log(route_number)
           console.log(destination)
           console.log(due_time)

      tableRows += "<tr><td>" + route_number + "</td><td>" + destination + "</td><td>" + due_time + "mins"+ "</td></tr>";


              }
     $("#real-time-table").html(tableRows)
            
            
            })}


$("#real-time-button").click(bustime)
    

