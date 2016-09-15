    $(document).ready(function() {

    //some docs: http://stackoverflow.com/questions/28576002/ajax-jquery-django (about: jdjangp +jquery + models +json)
    //we catch the values rendered by Django template
    var idTicket = document.getElementById("idTicket").value;
    var idPercentage = document.getElementById("idPercentage").value;

    //Update the percentage via ajax call
    function update_percentage(final_value)
    {
     $.ajax({
            type: "POST",
            url: "/tickets/set_percentage/"+idTicket+"/range/",
            dataType: "json",
            data: { "range_value": final_value },
            success: function(data) {
                    //console.log("Post update_percentage: " + final_value);
                    notif('info','Success','Percentage updated');
                    }
            });
     }

    //Catch the value on the range slider
    var $range = $(".range_base_ticket");+
    $(".range_base_ticket").ionRangeSlider({
          type: "single",
          min: 0,
          max: 100,
          step: 10,
          from: idPercentage,
          max_interval: 0,
          onFinish: function (data) {
                    //Log final value for test purpouses
                    var raw_value = data.from;
                    //console.log("Value: " + raw_value);
                    update_percentage(raw_value);
                }

        });

    var slider = $(".range_base_ticket").data("ionRangeSlider");



    //Catch the value on the range slider and set it when no instance is definded (new tickets only)
    var $range = $(".range_base_ticket_for_submit");+
    $(".range_base_ticket_for_submit").ionRangeSlider({
          type: "single",
          min: 0,
          max: 100,
          step: 10,
          from: idPercentage,
          max_interval: 0,
          onFinish: function (data) {
                    //Log final value for test purpouses
                    var raw_value = data.from;
                    //console.log("Value: " + raw_value);
                    if($('#id_ticket-percentage').val())
                    {   
                        $('#id_ticket-percentage').val(raw_value)
                    }
                    else
                    {
                        $('#ticketform').append('<input type="hidden" id="id_ticket-percentage" name="ticket-percentage" value="'+raw_value+'">');
                    }
                    
                    //update_percentage(raw_value);
                }

        });

    var slider = $(".range_base_ticket_for_submit").data("ionRangeSlider");


    //Create all divs with updated data
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
                            '<div class="comment-toolbar pull-right">'+
                            '<input type="hidden" id="idPMessage" name="idPMessage" value="'+item.id+'">'+
                            '<a href="#" class="del-message" onClick="return false;">Delete comment</a>'+
                            '</div>'+
                            '</div>'+
                            '</div>'
                             );
                        });
                        
                    }
             });
    }


    function notif(type, title, text){
    new PNotify({
                    title: ''+title+'',
                    text: ''+text+'',
                    type: ''+type+'',
                    styling: 'bootstrap3',
                    nonblock: true,
                    hide: true,
                    delay: 2000,
                });
    }



    //Post new message
    $('.add-message').click(function(){
      //console.log('am i called');
        $.ajax({
            type: "POST",
            url: "/tickets/add_comment/"+idTicket+"",
            dataType: "json",
            data: { "message_text": $("#message_data").val() },
            success: function(data) {
		                    $("#message_data").val("");
                            //console.log(data);
                            notif('info','Success','Message added');
                            update_comments_new();

                    },
            error: function(xhr, status, error) {
                            //$("#message_data").val("");
                            var json = JSON.parse(xhr.responseText);
                            var error_message = json.message;
                            notif('error','Oops!',error_message);
                    }
            });
    });

    //Post delete meessage
    //With ON class we can keep changes in new dinamically created objects!
    $('.comment_box').on("click", ".del-message", function(){
        //var idActualMessage = $(".del-message").closest("#idPMessage").attr("value");
        var idActualMessage = $(this).closest("div#comment").find("input[name='idPMessage']").val();
        $.ajax({
            type: "POST",
            url: "/tickets/del_comment/",
            dataType: "json",
            data: { "message_id": idActualMessage, "ticket_id": idTicket},
            success: function(data) {
                            update_comments_new();
                    },
            error: function(xhr, status, error) {
                        //$("#message_data").val("");
                            var json = JSON.parse(xhr.responseText);
                            var error_message = json.message;
                            notif('error','Oops!',error_message);
                    }
            });
    });


    //Update all microtask table
    function update_microtasks()
    {
        $.ajax({
            type: "GET",
            dataType: "json",
            url: "/tickets/get_microtasks/"+idTicket+"",
            success: function(data) {
                        var dataparsed = (data);
                        //console.log(data);
                        //alert(data.length);
                        $("#tblmicrotasks").empty();
                        $.each(dataparsed, function(i, item){
                            $("#tblmicrotasks").append(
                                    '<tr>'+
                                      '<td>'+item.id+'</td>'+
                                      '<td>'+
                                        '<a>'+item.subject_data+'</a>'+
                                        '<br>'+
                                        '<small>Created 01.01.2015</small>'+
                                      '</td>'+
                                      '<td>'+item.body_data+'</td>'+
                                      '<td class="project_progress">'+
                                        '<div class="progress progress_sm">'+
                                          '<div data-transitiongoal="'+item.percentage_data+'" role="progressbar" class="progress-bar bg-green" style="width: '+item.percentage_data+'%;" aria-valuenow="'+item.percentage_data+'"></div>'+
                                        '</div>'+
                                        '<small>'+item.percentage_data+'% Complete</small>'+
                                      '</td>'+
                                      '<td>'+
                                        '<span class="label" style="background-color:#'+item.state_color_data+'"><font color="black">'+item.state_data+'</font></span>'+
                                      '</td>'+
                                      '<td id="buttons">'+
                                        '<input type="hidden" id="idmk" name="idmk" value="'+item.id+'">'+
                                        '<a class="btn btn-info btn-xs edit-mk" href="#"><i class="fa fa-pencil"></i> Edit </a>'+
                                        '<a class="btn btn-danger btn-xs del-mk" href="#"><i class="fa fa-trash-o"></i> Delete </a>'+
                                      '</td>'+
                                    '</tr>'
                             );
                        });
                        
                    }
             });
    }



    //Microtask percentage
    var PercentageNewMK = 0 ;
    //Catch the value on the range slider
    var $range = $(".range_new_mk");+
    $(".range_new_mk").ionRangeSlider({
          type: "single",
          min: 0,
          max: 100,
          step: 10,
          from: 0,
          max_interval: 0,
          onFinish: function (data) {
                PercentageNewMK = data.from;
                },
          onUpdate: function (data) {
               PercentageNewMK = data.from;
          }

        });

    var slider_new = $(".range_new_mk").data("ionRangeSlider");



    //Post new microtask
    $('.add-microtask').click(function(){
        //console.log('am i called');
        //Try if ID exists and instance the variable
        //var ActualMK = $(this).closest("#microtask_modal").find("input[name='idmk']").val();
        var ActualMK = $(this).closest(".modal-footer").find("input[name='idmk']").val();
        $.ajax({
            type: "POST",
            url: "/tickets/add_microtask/"+idTicket+"",
            dataType: "json",
            data: { "id_mk": ActualMK,
                    "subject_text": $("#subject_mk").val(),
                    "body_text": $("#body_mk").val(),
                    "state_id": $("#state_mk").val(),
                    "percentage_num": PercentageNewMK },
            success: function(data) {
                            $("#subject_mk").val("");
                            $("#body_mk").val("");
                            //$("#state_mk option:first-child").attr("selected", "selected");
                            //$("#state_mk option:first").val();
                            //$("#state_mk").val('');
                            $("#state_mk").val($("#state_mk option:first").val());
                            slider_new.update({ from: 0 });
                            $('.modal-footer').find('[name="idmk"]').remove();
                            //console.log(data);
                            notif('info','Success','Message added');
                            $('#microtask_modal').modal('toggle');
                            update_microtasks();
                    },
             error: function(xhr, status, error) {
                             //$("#message_data").val("");
                             var json = JSON.parse(xhr.responseText);
                             var error_message = json.message;
                             notif('error','Oops!',error_message);
                     }
            });
    });






    //Edit microtasks modal


    function edit_microtask(mk_id)

    {
        $.ajax({
            type: "GET",
            dataType: "json",
            url: "/tickets/get_microtask/"+mk_id+"",
            success: function(data)
                {
                    
                    var dataparsed = (data);
                        $('#microtask_modal').find('[name="subject_mk"]').val(data.subject_data);
                        $('#microtask_modal').find('[name="body_mk"]').val(data.body_data);
                        $('#microtask_modal').find('[name="state_mk"]').val(data.state_data_id);
                        slider_new.update({ from: data.percentage_data });
                        $('.modal-footer').append('<input type="hidden" id="idmk" name="idmk" value="'+mk_id+'">');
                        $('#microtask_modal').modal('show');
                        


                }

        })
    }


    $('#tblmicrotasks ').on("click", ".edit-mk", function(){
      //console.log('am i called');
     var idActualMK = $(this).closest("td#buttons").find("input[name='idmk']").val();
     edit_microtask(idActualMK);

    });



    //Delete microtask by ID
        $('#tblmicrotasks').on("click", ".del-mk", function(){
        //var idActualMessage = $(".del-message").closest("#idPMessage").attr("value");
        var ActualMK = $(this).closest("td#buttons").find("input[name='idmk']").val();
        $.ajax({
            type: "POST",
            url: "/tickets/del_microtask/",
            dataType: "json",
            data: { "mk_id": ActualMK, "ticket_id": idTicket},
            success: function(data) {
                            update_microtasks();
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
