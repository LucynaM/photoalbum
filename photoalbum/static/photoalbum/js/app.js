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
    function clickHandler() {
        $('.likes-indication').on('click', 'svg', function(e) {
            e.preventDefault();

            const data = {
                photo_id: $(this).closest('figure').attr('id'),
                user: $('h4').attr('id').slice(5)
            };

            if ($(this).hasClass('like')) {
                data.counter = 1
            } else {
                data.counter = -1
            }

            ajaxHandler('http://127.0.0.1:8000/ajax_counter/', data, 'GET')
        })
    }
    // click - stop

    // change likes count - start
    function likesCount(r) {

        $('figure#'+ r.id + ' .likes-count').html("Liczba polubień: " + r.photo_likes);

        const likesIndication = $('figure#'+ r.id + ' .likes-indication');
        if (likesIndication.children().hasClass('like')) {
            likesIndication.html('<i class="fas fa-thumbs-down"></i><p>lubisz to zdjęcie</p>')
        } else {
            likesIndication.html('<i class="fas fa-thumbs-up"></i>')
        }
    }
    // change likes count - stop

    clickHandler();

});