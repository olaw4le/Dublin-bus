$(document).ready(function () {


});


// login to leap api & return card overview
function leap_login(){

    // get the entred username & password
    var this_user = $("leap-user").val()
    var this_passwd = $("leap-password").val()

    // request to get the bus time table, this should be done in the django app
    $.ajax({
        type:"POST",
        url:"leap_login/",
        data:{user:this_user, passwd:this_passwd}
      })

      .done(function(response){
          var x = JSON.parse(response)
          return x }

}
