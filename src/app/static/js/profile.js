
jQuery(document).ready(function($) {

    $('.book-condition').change(function () {
    var selectedText = $(this).find("option:selected").text();
    console.log("selected"+ selectedText);
    });

    $('#negotiation_form')
        .submit(function(e){
            var $form = $(e.target),
                transaction_id = $form.find('[name="transaction_id"]').val(),
                transaction_location = $('.meet-location').find("option:selected").text(),
                transaction_day = $('.meet-day').find("option:selected").val(),
                transaction_time = $('.meet-time').find("option:selected").text();

            $.ajax({
                url: '/negotiation/',
                type: 'POST',
                data: {
                    transaction_id : transaction_id,
                    transaction_location : transaction_location,
                    transaction_day : transaction_day,
                    transaction_time : transaction_time
                },
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
            $('#negotiation_form').find('[name="transaction_id"]').val(transaction_id).end();

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
    });

    $('#transaction_form')
        .submit(function(e){
            var $form = $(e.target),
                transaction_id = $form.find('[name="transaction_id"]').val(),
                transaction_state = $('.user-rating').find("option:selected").val(),
                listed_value = $('#listed-value').text();
                negotiation_value = $('#negotiation-value').text();
            $.ajax({
                url: '/transaction/',
                type: 'POST',
                data: {
                    transaction_id : transaction_id,
                    transaction_state : transaction_state
                },
                success: function(response){
                    if (response.status == 'Cancelled'){
                        var $button = $('button[data-id="'+ response.transaction +'"]');
                        $button.closest('tr').remove();
                        $('#negotiation-value').text(negotiation_value - 1);
                        $form.parents('.bootbox').modal('hide');
                        bootbox.alert('Transaction Cancelled! Thank you for using Stevens Marketplace.');
                    }
                    if (response.status == 'My_Cancel'){
                        var $button = $('button[data-id="'+ response.transaction +'"]');
                        $button.closest('tr').remove();
                        $('#negotiation-value').text(negotiation_value - 1);
                        $('#listed-value').text(function(i,listed_value){ return +listed_value + 1});
                        $('#my_books_listed > tbody:last-child').append('<tr class="active"><td><a href="/books/' + response.details.isbn + '">' + response.details.title  + '</a> <span class="badge pull-right">' + response.details.isbn + '</span></td><td>'+ response.details.date_listed +'</td><td>'+ response.details.condition +'</td><td>'+ response.details.price +'</td></tr>');
                        $form.parents('.bootbox').modal('hide');
                        bootbox.alert('Transaction Cancelled! Thank you for using Stevens Marketplace.');
                    }
                    if (response.status == 'Closed'){
                        $form.parents('.bootbox').modal('hide');
                        bootbox.alert('Transaction Closed! Thank you for using Stevens Marketplace.');
                        window.location.reload();
                    }
                    if (response.status == 'Pending'){
                        var $button = $('button[data-id="'+ response.transaction +'"]');
                        $button.prop("disabled",true);
                        $form.parents('.bootbox').modal('hide');
                        bootbox.alert('Transaction Pending! Thank you for using Stevens Marketplace.');
                    }
                    if (response.status == 'Unknown'){
                        $form.parents('.bootbox').modal('hide');
                        bootbox.alert('Something Bad happened');
                    }
                }
            });
            e.preventDefault();
    });
    $('.close_button')
        .click(function(){
            var transaction_id = $(this).attr('data-id');
            $('#transaction_form').find('[name="transaction_id"]').val(transaction_id).end();
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

    });

    $('.details_button')
        .click(function(){
            var transaction_id = $(this).attr('data-id');

            $.ajax({
                url: '/details/',
                type: 'POST',
                data: {
                    transaction_id : transaction_id
                },
                success: function(response, data){
                    $('#details_form').find('[name="transaction_id"]').val(transaction_id).end(),
                    $('#details_form').find('[name="location"]').val(response.details.location).end(),
                    $('#details_form').find('[name="meet_date"]').val(response.details.location_day).end(),
                    $('#details_form').find('[name="time"]').val(response.details.location_time).end(),
                    $('#details_form').find('[name="condition"]').val(response.details.condition).end();
                    bootbox
                        .dialog({
                            title: 'Details for this negotiation',
                            message: $('#details_form'),
                            show: false
                        })
                        .on('shown.bs.modal', function(){
                            $('#details_form').show();
                        })
                        .on('hide.bs.modal', function(e) {
                            $('#details_form').hide().appendTo('body');
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
