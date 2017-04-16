
jQuery(document).ready(function($) {
    $(".clickable-row").click(function() {
        window.location = $(this).data("href");
    });
});

$(function() {
    $('#rate_button').click(function() {
        $.ajax({
            url: '/rate',
            type: 'POST',
            data: {
                rating_val : $('#rating_val').val()
            }
        });
    });
});

$(function() {
    $('#btn_sell_book').click(function() {
        $.ajax({
            url: '/set_seller',
            type: 'POST',
            data: {
                ins_price : $('#ins_price').val()
            }
        })
        .done(function (data){
            if(data.error){
                $('#error_alert').show();
                $('#notice_error').text(data.error).show();
                $('#success_alert').hide();
            } else {
                window.location.reload();
            }
        });
        event.preventDefault();
    });
});
