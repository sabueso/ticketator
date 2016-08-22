    //some docs: http://stackoverflow.com/questions/28576002/ajax-jquery-django (about: jdjangp +jquery + models +json)
    $(document).ready(function() {
    
    //we catch the values rendered by Django template
    var idTicket = document.getElementById("idTicket").value;
    
    // deprecated: Django test function
    // $('.botonazo').click(function(){
    //     $.ajax({
    //         type: "GET",
    //         dataType: "json",
    //         url: "/tickets/get_comments/{{form_ticket.instance.id}}",
    //         success: function(data) {
    //                     var dataparsed = JSON.parse(data);
    //                     //console.log(data);
    //                     //alert(data.length);
    //                     $( ".comment_box" ).empty();
    //                     $.each(dataparsed, function(i, item){
    //                         $(".comment_box").append(
    //                         '<div class="mail_list">'+
    //                         '<div class="right">'+
    //                         '<h3>'+'user_pending'+'</h3>'+
    //                         '<p>'+ item.fields.comment +'</p>'+
    //                         '</div>'+
    //                         '</div>'    
    //                         );
    //                     });
    //                 }
    //          });
    // });


    function update_comments_new()
    {
        $.ajax({
            type: "GET",
            dataType: "json",
            url: "/tickets/get_comments/"+idTicket+"",
            success: function(data) {
                        var dataparsed = (data);
                        //console.log(data);
                        //alert(data.length);
                        $( ".comment_box" ).empty();
                        $.each(dataparsed, function(i, item){
                            $(".comment_box").append(
                            '<div id="comment" class="col-md-12 col-sm-12 col-xs-12 form-group">'+
                            '<img alt="Avatar" class="avatar" src="/static/media/'+item.avatar_data+'">'+
                            '<span class="pull-right" style="margin-top: 10px;">'+item.date_data+'</span>'+
                            '<h5>'+item.human_name+'</h5>'+
                            '<div class="well">'+
                            '<p class="message">'+item.comment_data+'</p>'+
                            '</div>'+
                            '</div>'
                            

                             );
                        });
                        
                    }
             });
    }



    // AJAX POST
    $('.add-message').click(function(){
      //console.log('am i called');
        $.ajax({
            type: "POST",
            url: "/tickets/add_comment/"+idTicket+"",
            dataType: "json",
            data: { "message_text": $("#message_data").val() },
            success: function(data) {
		                  $("#message_data").val("");
                          //location.reload();
                          update_comments_new();
                    }
            });
    });



    // CSRF code
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
