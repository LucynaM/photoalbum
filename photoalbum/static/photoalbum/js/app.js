$(document).ready(function() {

    // ajax - start
    function ajaxHandler(url, data, type) {
        $.ajax({
            url: url,
            data: data,
            type: type,
            dataType: 'json'
        }).done(function(result){
            console.log(result);
            likesCount(result);
        }).fail(function(xhr, status, error){
            console.log(xhr, status, error);
        }).always(function(xhr, status){
            console.log(xhr, status);
        });
    }
    // ajax - stop

    // click - start
    function clickHandler(element) {
        element.on('click', function(e) {
            e.preventDefault();

            var data = {
                photo_id: $(this).parent().attr('id')
            };

            if (element.hasClass('like')) {
                data.counter = 1
            } else if (element.hasClass('dislike')) {
                data.counter = -1
            }

            ajaxHandler('http://127.0.0.1:8000/ajax_counter/', data, 'GET')
        })
    }
    // click - stop

    // change likes count - start
    function likesCount(r) {
        $('#'+ r.id + ' .likes-count').html(r.photo_likes);
    }
    // change likes count - stop

    clickHandler($('.like'));
    clickHandler($('.dislike'));


});