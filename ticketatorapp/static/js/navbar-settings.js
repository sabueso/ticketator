//Store settings for mantain collapsed the side-navbar
$().ready(function() {

// var tckstorage = localStorage;


// // //Startup check
// if (tckstorage['bar-colapsed'] === "true")
//   	{
// 	$('body').toggleClass('nav-md nav-sm',0);
// 	}



// //Toggle status
// function set_bar()
// {
// 	if (tckstorage['bar-colapsed'] === "true")
// 	{
// 		tckstorage.setItem('bar-colapsed', false);
// 		console.log(tckstorage.getItem('bar-colapsed'));
// 	}
// 	else
// 	{
// 		tckstorage.setItem('bar-colapsed', true);
// 		console.log(tckstorage.getItem('bar-colapsed'));
// 	}
// }


// //Click event
// $('.nav').on("click", "#menu_toggle", function(){
// 	 set_bar();
// 	 console.log(tckstorage);

// });


try {
    var userid_data = document.getElementById("idUser").value;
}
catch (e) {}

console.log(userid_data)


function set_navbar(final_value)
{
 $.ajax({
        type: "POST",
        url: "/settings/user/set_togglenavbar/",
        dataType: "json",
        data: { "submited_user_id": userid_data },
        success: function(data) {
                //console.log("Post set_percentage: " + final_value);
                notif('info','Success','Navbar toggled');
                }
        });
 }


$('.nav').on("click", "#menu_toggle", function(){
	 set_navbar();
	// console.log(tckstorage);

});

    // CSRF magic
    function getCookie(name) {
        var cookieValue = null;
        var i = 0;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (i; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});