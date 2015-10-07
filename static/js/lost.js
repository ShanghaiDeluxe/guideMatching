(function ($) {
    'use strict';

    var
        initailize = function () {
            $('#code').bind('click', send_code);
            $('input[type=submit]').bind('submit', check_code);
        },

        send_code = function (e) {
            e.preventDefault();
            $.ajax({
                type: "POST",
                url: 'http://127.0.0.1:8000/send_code/',
                data: {
                    csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
                    username: $('#id_username').val(),
                    email: $('#id_email').val()
                },
                success: function (msg) {
                    //var json = JSON.parse(msg);
                    console.log(msg);
                },
                fail: function (msg) {
                    //var json = JSON.parse(msg);
                    console.log(msg);
                }
            })
        },

        check_code = function () {
            $.ajax({
                type: "POST",
                url: 'http://127.0.0.1:8000/lost/',
                data: {
                    csrfmiddlewaretoken: $('#csrfmiddlewaretoken').val(),
                    username: $('#id_username').val(),
                    email: $('#id_email').val(),
                    cert_code: $('#id_cert_code').val()
                },
                success: function (msg) {
                    //var json = JSON.parse(msg);
                    console.log(msg);
                }
            })
        };

    initailize();

})(jQuery)

