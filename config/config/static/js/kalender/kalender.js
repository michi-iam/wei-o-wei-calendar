// const directions = ["prev", "now", "next"]; - keys in django

// Switch month
jQuery(document).on('click', '.myKalSwitchMonthBtn', function(e){
    var direction = $(this).attr("direction");
    var curr_month = $(this).attr("month");
    var curr_year = $(this).attr("year");
    $.ajax({
        url: "get_prev_next_month",
        type: "GET",
        data: {
            direction:direction,
            month:curr_month,
            year:curr_year
        }, success: function(data){
            console.log(data)
            $('#calendar').html(data.content);
   
            
     
        }, failure: function(e){
            alert(e);
        }
    });
});


// add - show/edit, bc existing date + new date 
// Add event = myKalShowFormBtn
// get empty form to add event
jQuery(document).on('click', '.myKalShowFormBtn', function(e){
    // date -> get empty form
    var date = $(this).attr("date");
    var option = $(this).attr("option");
    $.ajax({
        url: "get_show_or_edit_form",
        type: "GET",
        data: {
            date: date,
            option:option
        }, success: function(data){
            $('#calendar').html(data.content);
        }, failure: function(e){
            console.log(e);
        }
    })
});

// show detail / edit = myKalEditEventBtn
// 2 btns -> 1: calender - > show
//          2: form - > edit 
jQuery(document).on('click', '.myKalEditEventBtn', function(e){
    var event_id = $(this).attr("eventid");
    var option = $(this).attr("option");
    $.ajax({
        url: "get_show_or_edit_form", // if Post/if Get in Django
        type: "GET",
        data: {
            event_id: event_id,
            option: option
        }, success: function(data) {
            $('#calendar').html(data.content);
        }, failure: function(e){
            console.log(e);
        }

    })
}); 

