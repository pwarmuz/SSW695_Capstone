
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
    $('#btn_isbn').click(function() {
        $.ajax({
            url: '/set_seller',
            type: 'POST',
            data: {
                ins_isbn : $('#ins_isbn').val(),
                ins_price : $('#ins_price').val()
            }
        })
        .done(function (data){
            if(data.error){
            $('#error_alert').show();
            $('#notice_error').text(data.error).show();
            $('#success_alert').hide();
            } else {
            $('#success_alert').show();
            $('#notice_success').text(data.item).show();
            $('#error_alert').hide();
            }
        });
        event.preventDefault();
    });
});
