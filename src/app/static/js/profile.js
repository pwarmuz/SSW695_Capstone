
jQuery(document).ready(function($) {
    $(".clickable-row").click(function() {
        window.location = $(this).data("href");
    });

    $('#userForm')
        .submit(function(e){
            var $form = $(e.target),
                transaction_id = $form.find('[name="name"]').val();

            $.ajax({
                url: '/negotiation/' + transaction_id,
                type: 'POST',
                success: function(response, data){
                    var $button = $('button[data-id="'+ response.transaction +'"]');
                    $button.closest('tr').remove();

                    $form.parents('.bootbox').modal('hide');

                    bootbox.alert('Successful! Please meet the seller to purchase this book.');
                }
            });
            e.preventDefault();
    });

    $('.editButton')
        .click(function(){
            var transaction_id = $(this).attr('data-id');

            $.ajax({
                url: '/negotiate/' + transaction_id,
                type: 'GET',
                success : function(response){
                    $('#userForm')
                        .find('[name="name"]').val(response.negotiate.trans_id).end();

                    bootbox
                        .dialog({
                            title: 'Purchase this book',
                            message: $('#userForm'),
                            show: false
                        })
                        .on('shown.bs.modal', function(){
                            $('#userForm').show();
                        })
                        .on('hide.bs.modal', function(e) {
                            $('#userForm').hide().appendTo('body');
                        })
                        .modal('show');
                }
            });
    });
});


$(function() {
    $('.currency').maskMoney();
})

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
