$(document).ready(function () {

    $('#leap-login-button').on('click', function () {

        $('.spinner-border').show();

        console.log("inside leap click");
        leap_login();
        $('#leap-login-container').hide();
        
        
        
    })

    $('#leap-logout').on('click', function () {
        $('#leap-logout').hide();
        $('#leap-login-container').show();
        $('#leap-overview-container').hide();
        $('#leap-detailed-container').hide();

        // clear the entered username & password
        $("#leap-user").val("");
        $("#leap-password").val("");

    }); 



});


// login to leap api & return card overview
function leap_login(){

    // get the entred username & password
    var this_user = $("#leap-user").val();
    var this_passwd = $("#leap-password").val();

    // request to get the bus time table, this should be done in the django app
    $.ajax({
        type:"POST",
        url:"leap_login/",
        data:{user:this_user, passwd:this_passwd}
    })

        .done(function(response){

            $('.spinner-border').hide();
            $('#leap-detailed-container').show();
            $('#leap-overview-container').show();
            $('#leap-logout').show();
            var overviewData = JSON.parse(response);
            console.log(overviewData);

            displayOverview(overviewData);
        })
}


// display the overview information on the leap.html page
function displayOverview(overviewData) {

    $("#card-name").html(overviewData.cardName);
    var a = $("#card-balance").html("€" + overviewData.cardBalance);
    var a = $("#card-type").html(overviewData.cardType);
    var a = $("#card-number").html(overviewData.cardNumber);
    var a = $("#card-expiry").html(overviewData.cardExpiry);

}
