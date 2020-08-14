$(document).ready(function () {

	$('#leap-login-button').on('click', function () {

		$('.spinner-border').show();


		leap_login();
		$('#leap-login-container').hide();


	})

	$('#leap-logout').on('click', function () {
		$('#leap-logout').hide();
		$('#leap-login-container').show();
		$('#leap-overview-container').hide();
		$('#leap-detailed-container').hide();
		$('#leap-error').hide();

		// clear the entered username & password
		$("#leap-user").val("");
		$("#leap-password").val("");

	});


});


// login to leap api & return card overview
function leap_login() {

	// get the entred username & password
	var this_user = $("#leap-user").val();
	var this_passwd = $("#leap-password").val();

	// request to get the bus time table, this should be done in the django app
	$.ajax({
			type: "POST",
			url: "leap_login/",
			data: {
				user: this_user,
				passwd: this_passwd
			}
		})

		.done(function (response) {

			$('.spinner-border').hide();
			var overviewData = JSON.parse(response);

			displayOverview(overviewData);
		})
}


// display the overview information on the leap.html page
function displayOverview(overviewData) {

	// code 00 represents a successful response
	if (overviewData.code == "00") {
		$("#card-name").html(overviewData.cardName);
		var a = $("#card-balance").html("€" + overviewData.cardBalance);
		var a = $("#card-type").html(overviewData.cardType);
		var a = $("#card-number").html(overviewData.cardNumber);
		var a = $("#card-expiry").html(overviewData.cardExpiry);

		$('#leap-detailed-container').show();
		$('#leap-overview-container').show();
		$('#leap-logout').show();
	} else {
		// error handling
		$("#leap-error").html(overviewData.msg)
		$('#leap-error').show();
		$('#leap-login-container').show();
		// clear the entered username & password
		$("#leap-user").val("");
		$("#leap-password").val("");

	}

}