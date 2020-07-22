/*
$(document).ready(function () {

    $('#leap-login-button').on('click', function () {

        console.log("inside leap click");
        $('#leap-login-container').hide();
        $('#leap-overview-container').show();
        $('#leap-detailed-container').show();
    })

    $('#leap-logout').on('click', function () {
        $('#leap-login-container').show();
        $('#leap-overview-container').hide();
        $('#leap-detailed-container').hide();

    }); 



});
*/

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
