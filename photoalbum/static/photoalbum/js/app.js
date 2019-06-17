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
        $('.likes-indication').on('click', '[data-type="change-likes"]', function(e) {
            e.preventDefault();
            const url = $(this).parent().data('url');
            const data = {
                photo_id: $(this).closest('figure').attr('id'),
                user: $('.user-details').eq(0).attr('id').slice(5),
            };
            data.counter = $(this).data('value');

            ajaxHandler(url, data, 'GET')
        })
    }
    // click - stop

    // change likes count - start
    function likesCount(r) {

        $('figure#'+ r.id + ' .likes-count').html("Liczba polubień: " + r.photo_likes);
        const likesIndication = $('figure#'+ r.id + ' .likes-indication');
        if (likesIndication.children().data('value') == "1") {
            likesIndication.html('<span class="btn btn-primary empty-btn-primary " data-type="change-likes" data-value="-1">nie lubię</span>')
        } else {
            likesIndication.html('<span class="btn btn-primary empty-btn-primary " data-type="change-likes" data-value="1">lubię</span>')
        }
    }
    // change likes count - stop

    clickHandler();

    // set images box height and handle img orientation
    function setImgSize () {
        const windowWidthCondition = window.innerWidth < 768;
        const containerWidth = $('.img-container').eq(0).width();
        const detailedView = $('.img-container').hasClass('landscape photo-details');

        if (windowWidthCondition) {
             $('.img-container figure').each(function() {
                $(this).css({'height': ''});
            });
            $('.img-container.landscape .img-wrapper').each(function(){
                $(this).css({'height': ''});
            });

            $('.img-container.portrait .img-wrapper').each(function(){
                $(this).css({'height': ''});
            });

        } else {

            if (!detailedView) {
                $('.img-container figure').each(function() {
                    $(this).height(containerWidth);
                });

                $('.img-container.landscape .img-wrapper').each(function(){
                    $(this).css({'height': containerWidth * 2 / 3 + 'px'})
                });

                $('.img-container.portrait .img-wrapper').each(function(){
                    $(this).css({'height': containerWidth + 'px'})
                });
            }
        }
    };

    setImgSize();
    $(window).resize(setImgSize);

    $(document).on('show.bs.modal', '#photo-modal', function (e) {
        console.log("działam");
        var url  = $(e.relatedTarget).data('src');
        $(this).find('.modal-body').html('<img class="card-body" src='+ url+'>');
    });

});