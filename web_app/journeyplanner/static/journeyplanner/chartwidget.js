// code for creating journey time graphs //

//  1.  read the search params from the html
//      date, time, route, start & end stops
//  2.  request the predictions data from the server
//      matching search params to database data wil happen serverside
//  3.  wait for the data to return
//
//  4.  create a bar chart with the returned data...
//

// define the colours to use when drawing & filling charts & graphs
var borderColours = ["rgb(184, 202, 204)", "rgb(64, 204, 219)"];
var fillColours = ["rgba(102, 255, 255, 0.5)", "rgba(64, 204, 219, 0.8)"];


// function for reading in the parameters used for generating the graphs
function getSearchParams() {
    var params = new Object();
        params["route"] = $("#estimator-route").val();
        params["direction"] = "1";                           // placeholder values !!!
        params["start"] = $("#estimator-origin").val();
        params["end"] = $("#estimator-destination").val();

        // get the date & time
        if ($(window).width() < 992) {
            // if used on mobile
            var datetimeValue = $("#datetime-tab2").val();
            var arr = datetimeValue.split('T');
            params["date"] = arr[0];
            params["time"] = arr[1];
        } else {
            // for other devices...
            params["date"] = $("#datepicker-tab2").val();
            params["time"] = $('#timepicker-tab2').val();
        }

    return params;
}


// function for requesting graph data from web server
function makeStatsRequest() {

    // red the search parameters
    var params = getSearchParams()

    // make the request
    $.ajax({
        type:"POST",
        url:"get_stats/",
        data:{date:params.date, time:params.time, route:params.route, direction:params.direction, end:params.end, start:params.start}
    })

    // when response received
    .done(function(response){
        var data = JSON.parse(response);

        var infoObject = new Object();
            infoObject["data"] = data;
            infoObject["route"] = params.route;
            infoObject["start"] = params.start;
            infoObject["end"] = params.end;

        updateTextInfo(infoObject);
        drawBarChart(data);
        })
}


// display a textual description of the data contained in the graph
function updateTextInfo(data) {

    //$("#results-route-number").html(data.route);
    //$("#results-route-stops").html(data.start + '-' + data.end);


    // get the 95% journey time for this time group
    var day_time = Object.keys(data.data)[2];
    var journey_time = data.data[day_time];
    var fastest_time = day_time;

    for (var key in data.data) {
        if (data.data[key] < journey_time) {
            fastest_time = key
        }
    }

    // if there's a faster time than the 'search time' add that to the description
    if (day_time == fastest_time) {
        $("#results-description").html("At " + day_time + " 95% of journeys take less than " + journey_time + " minutes.");
    } else {
        var timeDelta = journey_time - data.data[day_time];
        $("#results-description").html("At " + day_time + " 95% of journeys take less than " + journey_time + " minutes. You could expect to save "  + timeDelta + "minutes by making this trip at " + fastest_time + "instead.");
    }

}


function DataSet(data) {
    // formats the passed data as an object w/ instance variables to be passed
    // to the Chart() object constructor
    this.label = "Journey Duration";
    // this.fill = fill;
    this.backgroundColor = [fillColours[0], fillColours[0], fillColours[1], fillColours[0], fillColours[0]];
    this.borderColor = [borderColours[0], borderColours[0], borderColours[1], borderColours[0], borderColours[0]];
    this.borderWidth = 1;
    this.barPercentage = 0.95;     // sets the relative width of bars in a bar chart
    this.categoryPercentage = 1;   // sets the relative width of bars in a bar chart

    var arr = new Array();

    Object.keys(data).forEach( function(item) {
            arr.push(data[item]);
        })

    this.data = arr;
}

function drawBarChart(data) {

    // get the chart container from the info.html page
    var ctx = document.getElementById("results-canvas");
    var bars = [];
    var labels = Object.keys(data);

    bars =  new DataSet(data);
    var someChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    datasets: [bars],
                    labels: Object.keys(data),
                    },
                options: {
                    responsive: true,
                    legend: {
                        display: false
                    },
                    scales: {
                        yAxes: [{
                            scaleLabel: {
                                labelString: "Travel Time (Minutes)",
                                display: true
                            },
                            stacked: false,
                            display: true,
                            gridLineWidth: 0,
                            minorTickInterval: null,
                            ticks: {
                                beginAtZero: true
                            }
                        }],
                        xAxes: [{
                            stacked: false,
                            display: true,
                            gridLineWidth: 0,
                            gridLines: {
                                display: false
                            }
                        }]
                    }
                }
    });
    return someChart;

}


// var sampleData = [{x: "2016-12-25", y: 4}, {x: "2016-12-26", y: 20}, {x: "2016-12-27", y: 10}, {x: "2016-12-28", y: 7}, {x: "2016-12-29", y: 3}];
//var sampleData = {"13:30": 4, "14:00": 20, "14:30": 10, "15:00": 7, "15:30": 3};

//drawBarChart(sampleData)