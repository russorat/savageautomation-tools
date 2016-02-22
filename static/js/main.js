$(document).ready(function(){
	$(".google-button").hover(function() {
		$(this).attr("src","/static/images/google-signin-long/Red-signin-Long-hover-44dp.png");
	    }, function() {
		$(this).attr("src","/static/images/google-signin-long/Red-signin-Long-base-44dp.png");
	});
  $(".google-button").mousedown(function() {
		$(this).attr("src","/static/images/google-signin-long/Red-signin-Long-press-44dp.png");
	});
  $(".google-button").mouseup(function() {
		$(this).attr("src","/static/images/google-signin-long/Red-signin-Long-hover-44dp.png");
	});

  $(".google-button-small").hover(function() {
		$(this).attr("src","/static/images/google-signin-small/Red-signin-Small-hover-44dp.png");
	    }, function() {
		$(this).attr("src","/static/images/google-signin-small/Red-signin-Small-base-44dp.png");
	});
  $(".google-button-small").mousedown(function() {
		$(this).attr("src","/static/images/google-signin-small/Red-signin-Small-press-44dp.png");
	});
  $(".google-button-small").mouseup(function() {
		$(this).attr("src","/static/images/google-signin-small/Red-signin-Small-hover-44dp.png");
	});
});
