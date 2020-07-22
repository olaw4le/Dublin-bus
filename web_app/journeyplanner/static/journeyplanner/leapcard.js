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