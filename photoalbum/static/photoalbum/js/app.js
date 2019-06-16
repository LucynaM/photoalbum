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
        $('.likes-indication').on('click', 'i.fas', function(e) {
            e.preventDefault();
            const url = $(this).parent().data('url');
            const data = {
                photo_id: $(this).closest('figure').attr('id'),
                user: $('.user-details').eq(0).attr('id').slice(5),
            };

            if ($(this).hasClass('like')) {
                data.counter = 1
            } else {
                data.counter = -1
            }

            ajaxHandler(url, data, 'GET')
        })
    }
    // click - stop

    // change likes count - start
    function likesCount(r) {

        $('figure#'+ r.id + ' .likes-count').html("Liczba polubień: " + r.photo_likes);

        const likesIndication = $('figure#'+ r.id + ' .likes-indication');
        if (likesIndication.children().hasClass('like')) {
            likesIndication.html('<p>lubisz już to zdjęcie, chcesz zmienić zdanie?</p><br /><i class="fas fa-heart-broken dislike"></i>')
        } else {
            likesIndication.html('<p>jeszcze nie lubisz tego zdjęcia, chcesz zmienić zdanie?</p><br /> <i class="fas fa-heart like"></i>')
        }
    }
    // change likes count - stop

    clickHandler();

    // set images wrapper height for proper hover
    function setImgWrapperSize () {
        $('.img-wrapper').each(function() {
            const imgHeight = $(this).children().children().height();
            const wrapperHeight = $(this).height(imgHeight);
        })
    }

    //  setImgWrapperSize()

});