$(document).ready(function () {

    $('#leap-login-button').on('click', function () {

        console.log("inside leap click");
        $('#leap-login-container').hide();
        $('#leap-overview-container').show();
        $('#leap-detailed-container').show();
    })
});