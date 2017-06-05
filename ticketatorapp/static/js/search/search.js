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
                          if (item.percentage_data <= 30 && item.percentage_data >= 0){
                            var colorback = 'bg-red'
                          }
                          if (item.percentage_data <= 60 && item.percentage_data >= 40){
                            var colorback = 'bg-orange'
                          }
                          if (item.percentage_data <= 100 && item.percentage_data >= 70){
                            var colorback = 'bg-green'
                          }
                            $("#tbodysearch").append(

									          '<tr class="odd gradeX">'+
                              	   	'<td class="text-center" style="vertical-align:middle"><a href="/tickets/view/'+item.id+'">'+item.id+'</a></td>'+
                              	 	  '<td class="text-center" style="vertical-align:middle"><a href="/tickets/view/'+item.id+'">'+item.subject_data+'</a></td>'+
                                    '<td class="text-center" style="vertical-align:middle"><span class="label" style="background-color:#'+item.state_color_data+'"><font color="black">'+item.state_data+'</font></span></td>'+
                                    '<td class="text-center" style="vertical-align:middle">'+item.queue_shortcode+'</td>'+
                              	   	'<td class="text-center" style="vertical-align:middle">'+item.create_user+'</td>'+
                                    '<td class="text-center" style="vertical-align:middle">'+item.date+'</td>'+
                                    '<td class="text-center" style="vertical-align:middle">'+item.assigned_user_data+'</td>'+
                                    '<td class="project_progress"><div class="progress progress_sm"><div aria-valuenow="'+item.percentage_data+'" style="width: '+item.percentage_data+'%" class="progress-bar '+colorback+'"role="progressbar" data-transitiongoal="'+item.percentage_data+'"></div></div><div class="percentage_range" <small>'+item.percentage_data+'%</small></div></td>'+
                                    '<td class="text-center" style="vertical-align:middle">'+item.priority+'</td>'

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
                    "status_id": $("#id_status").val(),
                   },
            success: function(data) {
		                    //$("#message_data").val("");
                            console.log(data)
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
