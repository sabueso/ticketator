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

    //Now
    var now = moment().format("DD/MM/YYYY HH:mm:ss a");

    //Date picker
    $('#id_ticket-date').daterangepicker({
        "singleDatePicker": true,
        "timePicker": true,
        "timePicker24Hour": true,
        "showCustomRangeLabel": false,
        "autoUpdateInput": true,
        "format": 'DD/MM/YYYY H:mm:ss',

    });


    if($('#id_ticket-date').length != 0) {
        $('#id_ticket-date').data('daterangepicker').setEndDate(now);
    }

    //some docs: http://stackoverflow.com/questions/28576002/ajax-jquery-django (about: jdjangp +jquery + models +json)
    //we catch the values rendered by Django template
    var idTicket_data = document.getElementById("idTicket").value;
    var idPercentage_data = document.getElementById("id_ticket-percentage").value;
    var count_microtask_data = document.getElementById("count_microtask").value;
    var path = window.location.pathname.split("/")[2];

    function update_percentage_input(percentage_value)
    {
    var raw_value = percentage_value;
    if($('#id_ticket-percentage').val())
       {
        $('#id_ticket-percentage').val(raw_value)
       }
    else
       {
        $('#ticketform').append('<input type="hidden" id="id_ticket-percentage" name="ticket-percentage" value="'+raw_value+'">');
       }
    }

    //Update the global percentage via ajax call
    function set_percentage(final_value)
    {
     $.ajax({
            type: "POST",
            url: "/tickets/set_percentage/"+idTicket_data+"/range/",
            dataType: "json",
            data: { "range_value": final_value },
            success: function(data) {
                    //console.log("Post set_percentage: " + final_value);
                    notif('info','Success','Percentage updated');
                    }
            });
     }

    //Get the global percentage to use it as value for the slider
    function get_percentage(ticket_id)
    {
     $.ajax({
            type: "GET",
            async: false,
            url: "/tickets/get_percentage/"+ticket_id+"",
            dataType: "json",
            success: function(data) {
                    //console.log(data);
                    dataparsed = (data.percentage_data);
                    //console.log(dataparsed.percentage_data);
                    }

            });
            return dataparsed
     }

    //Catch the value on the range slider
    var $range = $(".range_base_ticket");+
    $(".range_base_ticket").ionRangeSlider({
          type: "single",
          keyboard: true,
          //disable: true,
          min: 0,
          max: 100,
          step: 10,
          from: idPercentage_data,
          max_interval: 0,
          onFinish: function (data) {
                    //Log final value for test purpouses
                    var raw_value = data.from;
                    //console.log("Value: " + raw_value);
                    set_percentage(raw_value);
                    update_percentage_input(data.from)
                }

        });
    var slider_for_existing = $(".range_base_ticket").data("ionRangeSlider");


    //Define if existing ticket load needs to disable the range slider because the existence
    //of microtasks

    if (count_microtask_data != 0 || path == "view")
    {
        slider_for_existing.update({disable: true});
    }
    //console.log(count_microtask_data);



    //Catch the value on the range slider and set it when no instance is definded (new tickets only)
    var $range = $(".range_base_ticket_for_submit");+
    $(".range_base_ticket_for_submit").ionRangeSlider({
          type: "single",
          keyboard: "true",
          min: 0,
          max: 100,
          step: 10,
          from: idPercentage_data,
          max_interval: 0,
          onFinish: function (data) {
                    //Log final value for test purpouses
                    // var raw_value = data.from;
                    update_percentage_input(data.from)
                    // //console.log("Value: " + raw_value);
                    // if($('#id_ticket-percentage').val())
                    // {
                    //     $('#id_ticket-percentage').val(raw_value)
                    // }
                    // else
                    // {
                    //     $('#ticketform').append('<input type="hidden" id="id_ticket-percentage" name="ticket-percentage" value="'+raw_value+'">');
                    // }
                }
        });
    var slider_for_new = $(".range_base_ticket_for_submit").data("ionRangeSlider");

    //Create all divs with updated data
    function update_comments_new()
    {
        $.ajax({
            type: "GET",
            dataType: "json",
            url: "/tickets/get_comments/"+idTicket_data+"",
            success: function(data) {
                        var dataparsed = (data);
                        //console.log(data);
                        //alert(data.length);
                        $( ".comment_box" ).empty();
                        $.each(dataparsed, function(i, item){
                            var date = moment(item.date_data, "YYYY-MM-DD HH:mm").fromNow();
                            if (item.avatar_data)
                                {var img_parsed = item.avatar_data }
                            else
                                {var img_parsed = "user.png"}
                            if (item.delete_comment == "True"){
                              var delete_comment = '<button href="#" class="del-message btn btn-xs btn-danger pull-right" onClick="return false;">Delete comment</button>'

                            }
                            else{
                              var delete_comment = ''
                            }
                            $(".comment_box").append(
                            '<div class="row" id="comment"><div class="col-sm-1"><div class="thumbnail">'+
                            '<img alta="Avatar" class="img-responsive user-photo" src="/static/images/'+img_parsed+'"></div></div>'+
                            '<div class="col-sm-11"><div class="panel panel-default"><div class="panel-heading">'+
                            '<strong>'+item.human_name+'</strong> <span class="text-muted">commented '+date+'</span>'+
                            '<input type="hidden" id="idPMessage" name="idPMessage" value="'+item.id+'">'+delete_comment+
                            '</div><div class="panel-body"><div class="content-markdown-new">'+item.comment_data+'</div></div></div></div></div>'
                             );
                        });
                        markdownfunction();
                    }
             })
    }


    //Post new message
    $('.add-message').click(function(event){
      //console.log('am i called');
      event.preventDefault();

        $.ajax({
            type: "POST",
            url: "/tickets/add_comment/"+idTicket_data+"",
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
            data: { "message_id": idActualMessage, "ticket_id": idTicket_data},
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
            url: "/tickets/get_microtasks/"+idTicket_data+"",
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
                                        '<small>'+item.date_data+'</small>'+
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
          keyboard: "true",
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

    var slider_new_microtask = $(".range_new_mk").data("ionRangeSlider");

    //Post new microtask
    $('.add-microtask').click(function(){
        //console.log('am i called');
        //Try if ID exists and instance the variable
        //var ActualMK = $(this).closest("#microtask_modal").find("input[name='idmk']").val();
        var ActualMK = $(this).closest(".modal-footer").find("input[name='idmk']").val();
        $.ajax({
            type: "POST",
            url: "/tickets/add_microtask/"+idTicket_data+"",
            dataType: "json",
            data: { "id_mk": ActualMK,
                    "subject_text": $("#subject_mk").val(),
                    "body_text": $("#body_mk").val(),
                    "state_id": $("#state_mk").val(),
                    "percentage_num": PercentageNewMK },
            success: function(data) {
                            //Clean some inserted data
                            $("#subject_mk").val("");
                            $("#body_mk").val("");
                            //Select the firs option in select list
                            $("#state_mk").val($("#state_mk option:first").val());
                            //Reset the microtask slider state
                            slider_new_microtask.update({ from: 0 });
                            //Remove the microtask id reference from modal
                            $('.modal-footer').find('[name="idmk"]').remove();
                            //console.log(data);
                            notif('info','Success','Message added');
                            //Close the modal
                            $('#microtask_modal').modal('toggle');
                            //Get the new global average
                            //console.log(get_percentage(idTicket_data))
                            var new_percentage = get_percentage(idTicket_data);
                            //console.log(percentage)
                            //Disable the slider if its the firs microtask and update the percentage
                            slider_for_existing.update({disable: true, from: new_percentage});
                            //Update the main input value for "percentage" to avoid 0% percentage
                            update_percentage_input(new_percentage)
                            //Update all microtask from table
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
                        slider_new_microtask.update({ from: data.percentage_data });
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
            data: { "mk_id": ActualMK, "ticket_id": idTicket_data},
            success: function(data) {
                            var new_percentage = get_percentage(idTicket_data);
                            //console.log(percentage)
                            //Disable the slider if its the firs microtask and update the percentage
                            slider_for_existing.update({disable: true, from: new_percentage});
                            update_microtasks();
                            var rowCount = $('#tblmicrotasks  tr').length - 1;
                            console.log(rowCount);
                            if (rowCount == 0)
                            {
                                slider_for_existing.update({disable: false});
                            }
                            else
                            {
                                slider_for_existing.update({disable: true});
                            }
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

    function markdownfunction(){
      $(".content-markdown-new").each(function(){
        $(this).html(marked($(this).text()))
      })
    }
});

function previewMarkdown(){
  $("#id_ticket-body_preview").html(marked($("#id_ticket-body").val()))
}
