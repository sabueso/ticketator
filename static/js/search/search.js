$().ready(function() {

	//PNotify for events (add messages, range change, etc)
    function notif(type, title, text){
    new PNotify({
                    title: ''+title+'',
                    text: ''+text+'',
                    type: ''+type+'',
                    styling: 'bootstrap3',
                    nonblock: true,
                    buttons: {
                            sticker: false,
                            },
                    hide: true,
                    delay: 1000,
                });
    }


    function render_search_results(data)
    {
        				var dataparsed = (data);
                        //console.log(data);
                        //alert(data.length);
                        $( "#tbodysearch" ).empty();
                        $.each(dataparsed, function(i, item){
                            $("#tbodysearch").append(

									'<tr class="odd gradeX">'+
                              	   	'<td class="text-center" style="vertical-align:middle"><a href="/tickets/edit-dev/'+item.id+'">'+item.id+'</a></td>'+
                              	 	'<td class="text-center" style="vertical-align:middle"><a href="/tickets/edit-dev/'+item.id+'">'+item.subject_data+'</a></td>'+
                                    '<td class="text-center" style="vertical-align:middle"><span class="label" style="background-color:#'+item.state_color_data+'><font color="black">'+item.state_data+'</font></span></td>'+
                                    '<td class="text-center" style="vertical-align:middle">'+item.queue_shortcode+'</td>'+
                              	   	'<td class="text-center" style="vertical-align:middle">'+item.create_user+'</td>'+
                                    '<td class="text-center" style="vertical-align:middle">'+item.date+'</td>'+
                                    '<td class="text-center" style="vertical-align:middle">'+item.assigned_user_data+'</td>'+
                                  	'<td class="project_progress">'+item.percentage_data+'</td>'+
                                  	'<td class="text-center" style="vertical-align:middle">'+item.assigned_prio+'</td>'

                              	 	)
                        		});

                             
					}
                        




	//Send search data
    $('#search-btn').click(function(){
      //console.log('am i called');
        $.ajax({
            type: "POST",
            url: "/search/",
            dataType: "json",
            data: { 
                    "subject_text": $("#subject").val(),
                    "body_text": $("#body").val(),
                    "assigned_id": $("#id_assigned_user").val(),
                    "creator_id": $("#id_create_user").val(),
                   },
            success: function(data) {
		                    //$("#message_data").val("");
                            console.log(data);
                            notif('info','Success','Message added');
                            render_search_results(data);
                            //update_comments_new();
                            },
            error: function(xhr, status, error) {
                            //$("#message_data").val("");
                            var json = JSON.parse(xhr.responseText);
                            var error_message = json.message;
                            notif('error','Oops!',error_message);
                            }
            });
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


