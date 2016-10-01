//Store settings for mantain collapsed the side-navbar
$().ready(function() {

var tckstorage = localStorage;


//Startup check

if (tckstorage['bar-colapsed'] === "true")
 	{
	$('body').toggleClass('nav-md nav-sm');
 	}



//Toggle status
function set_bar()
{
	if (tckstorage['bar-colapsed'] === "true")
	{
		tckstorage.setItem('bar-colapsed', false);
		console.log(tckstorage.getItem('bar-colapsed'));
	}
	else
	{
		tckstorage.setItem('bar-colapsed', true);
		console.log(tckstorage.getItem('bar-colapsed'));
	}
}


//Click event
$('.nav').on("click", "#menu_toggle", function(){
     //console.log('TOGGLE');
     //tckstorage.setItem('bar-colapsed', true);
	 // var idActualMK = $(this).closest("td#buttons").find("input[name='idmk']").val();
	 // edit_microtask(idActualMK);
	 set_bar();
	 console.log(tckstorage);

});

});