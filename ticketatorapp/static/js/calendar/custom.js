$(function() {
  // Display calendar
  $('#calendar').fullCalendar({
    defaultView: 'month',
    header: {
      left: 'today prev,next',
      center: 'title',
      right: 'month,agendaWeek'
    },
    firstDay: 1,
    events: {
      url: get_events_url,
      type: 'GET'
    },
    editable: true,
    selectable: true,
    eventRender: function(event, element) {
      element.popover({
        placement: 'top',
        html: true,
        animation: true,
        delay: 300,
        title: event.title,
        content:
          '<strong>Description: </strong>' + event.body.substr(0, 100) + '...' + '<br />' +
          '<strong>Status: </strong>' + event.state_data,
        trigger: 'hover'
      });
    },
    eventClick: function(event) {
      event.url
    }
  });
});
