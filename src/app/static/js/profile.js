
jQuery(document).ready(function($) {

    $('.book-condition').change(function () {
    var selectedText = $(this).find("option:selected").text();
    console.log("selected"+ selectedText);
});

    $(".clickable-row").click(function() {
        window.location = $(this).data("href");
    });

    $('#negotiation_form')
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

    $('.buy_button')
        .click(function(){
            var transaction_id = $(this).attr('data-id');

            $.ajax({
                url: '/negotiate/' + transaction_id,
                type: 'GET',
                success : function(response){
                    $('#negotiation_form').find('[name="name"]').val(response.negotiate.trans_id).end();

                    bootbox
                        .dialog({
                            title: 'Purchase this book',
                            message: $('#negotiation_form'),
                            show: false
                        })
                        .on('shown.bs.modal', function(){
                            $('#negotiation_form').show();
                        })
                        .on('hide.bs.modal', function(e) {
                            $('#negotiation_form').hide().appendTo('body');
                        })
                        .modal('show');
                }
            });
    });

    $('#transaction_form')
        .submit(function(e){
            var $form = $(e.target),
                transaction_id = $form.find('[name="name"]').val();

            $.ajax({
                url: '/transaction/' + transaction_id,
                type: 'POST',
                success: function(response, data){
                    var $button = $('button[data-id="'+ response.transaction +'"]');
                    $button.closest('tr').remove();
                    var selectedText = $('.user-rating').find("option:selected").val();
                    console.log("selected "+ selectedText);

                    $form.parents('.bootbox').modal('hide');

                    bootbox.alert('Transaction closed! Thank you for using Stevens Marketplace.');
                }
            });
            e.preventDefault();
    });
    $('.close_button')
        .click(function(){
            var transaction_id = $(this).attr('data-id');
            console.log(transaction_id + "value");
            $.ajax({
                url: '/transact/' + transaction_id,
                type: 'GET',
                success : function(response){
                    $('#transaction_form').find('[name="name"]').val(response.negotiate.trans_id).end();

                    bootbox
                        .dialog({
                            title: 'Rate transaction',
                            message: $('#transaction_form'),
                            show: false
                        })
                        .on('shown.bs.modal', function(){
                            $('#transaction_form').show();
                        })
                        .on('hide.bs.modal', function(e) {
                            $('#transaction_form').hide().appendTo('body');
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
    var book_condition = $('.book-condition').find("option:selected").text();

        $.ajax({
            url: '/set_seller',
            type: 'POST',
            data: {
                ins_price : $('#ins_price').val(),
                book_condition : book_condition
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
