// app specific jquery functions

$(document).ready(function() {  
    $("#navmenu li").each(function() {            
        if (document.URL.toUpperCase().indexOf($(this).attr('id').toUpperCase()) > -1) 
        {
            $(this).addClass("isSelected");
        }
    });
});

$(document).ready(function() {
    $("#garagelist li").each(function() {
        if (document.URL.toUpperCase().indexOf($(this).attr('id').toUpperCase()) > -1)
        {
            $(this).addClass("isSelected");
        }
    });
});
