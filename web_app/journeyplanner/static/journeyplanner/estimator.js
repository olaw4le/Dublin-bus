  // add on click to edit-journey button to hide results and show journey planner
  $('#edit-journey-time-planner').on('click', function () {
    $(".form-area").show();
    $("#journey-time-results").hide();
  });

  // when the user click the go button, the route function runs and the results div shows
$(function () {
    $('#stop-to-stop-go').on('click', function () {
        console.log("in go click");
      $("#stop-to-stop-input").hide();
      $("#journey-time-results").show();
    });
  
    // add on click to edit-journey button to hide results and show journey planner
    $('#stop-to-stop-edit').on('click', function () {
      $(".form-area").show();
      $("#journey-time-results").hide();
    });
  
  
  });