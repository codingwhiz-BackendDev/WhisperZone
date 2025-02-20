$(document).ready(function () {
    $(document).on('submit', '#make_private', function (e) {
        e.preventDefault()
        $.ajax({
            type: 'POST',
            url: '/make_message_private',
            data: {
                user: $('#user').val(),
                message_id: $('#message_id').val(),
                message: $('#message').val(),
                checkbox: $('#checkbox').val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function (response) {
                //alert(response) 

            },
            error: function (response) {
                //alert('an error occured')
            }
        })
    })
})