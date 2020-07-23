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

function getSearchParams() {
    //var d = $("#date-picker").val();
    //var t = $("#time-picker").val();
    // 2020-07-23T17:09
    var params = new Object();
        params["route"] = $("#estimator-route").val();
        params["start"] = $("#estimator-origin").val();
        params["end"] = $("#estimator-destination").val();
        params["dt"] = $("#datetime-tab2").val();

    return params;
}


function makePredictionRequest() {

    var params = getSearchParams()

    // request to get the bus time table, this should be done in the django app
    $.ajax({
        type:"POST",
        url:"leap_login/",
        data:{user:this_user, passwd:this_passwd}
    })
}


function updateTextInfo() {
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
    console.log(bars)
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
                            stacked: false,
                            display: true,
                            gridLineWidth: 0,
                            minorTickInterval: null
                        }],
                        xAxes: [{
                            stacked: false,
                            display: true,
                            gridLineWidth: 0,
                        }]
                    }
                }
    });
    return someChart;

}


// var sampleData = [{x: "2016-12-25", y: 4}, {x: "2016-12-26", y: 20}, {x: "2016-12-27", y: 10}, {x: "2016-12-28", y: 7}, {x: "2016-12-29", y: 3}];
var sampleData = {"13:30": 4, "14:00": 20, "14:30": 10, "15:00": 7, "15:30": 3};

drawBarChart(sampleData)