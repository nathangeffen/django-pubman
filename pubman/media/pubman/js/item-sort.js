/* item-sort.js */

jQuery(function($) {
    $("div.inline-group").sortable({ 
        axis: 'y',
        placeholder: 'ui-state-highlight', 
        forcePlaceholderSize: 'true', 
        items: '.row1, .row2', 
        update: update
    });
/*    $("div.inline-group").disableSelection();*/
});

function update() {
    $('.row1, .row2').each(function(i) {
        if ($(this).find('input[id$=author_or_institution]').val()) {
                    $(this).find('input[id$=order]').val(i+1);
        }
        if ($(this).find('input[id$=article]').val()) {
            $(this).find('input[id$=order]').val(i+1);
        }        
    });
}
jQuery(document).ready(function($){

    var colorholder = $('.author_or_institution img').css('background-color');  
    
    $(this).find('input[id$=order]').parent('td').hide().parent('tr').parent('tbody').parent('table').find("th:contains('Order')").hide(); 
    $(this).find('input[id$=order]').parent('td').hide().parent('tr').parent('tbody').parent('table').css('cursor','move');
    $('.author_or_institution img, .article img').hover(
        function() {
            //$(this).css('background-color','#b0c4de');
            $(this).css('background-color','black');
        },
        function() { 
            $(this).css('background-color', colorholder);
        } 
    );    
    $(':submit').click(update);         

});
