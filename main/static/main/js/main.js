$(document).ready(function(){
    $('.menu_bar').click(function(){
        $('header').toggleClass('active');
        $('main').toggleClass('main');
    })
    $('#menu_close').click(function(){
    	if (document.getElementById('navheader').className == "active") {
	        $('header').toggleClass('active');
	        $('main').toggleClass('main');
        }
    })
})

