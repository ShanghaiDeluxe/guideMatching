(function ($) {
    'use strict';

    var
        initailize = function () {
            $('button#code').bind('click', send_code);
            $('input[type=submit]').bind('click', resetPassword);
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
                success: function (res) {
                    //var json = JSON.parse(res);
                    alert(res['message']);
                },
                fail: function (res) {
                    //var json = JSON.parse(res);
                    alert(res['message']);
                }
            });
        },

        resetPassword = function (e) {
            e.preventDefault();

            $.ajax({
                type: "POST",
                url: 'http://127.0.0.1:8000/lost/',
                data: {
                    csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
                    username: $('#id_username').val(),
                    email: $('#id_email').val(),
                    cert_code: $('#id_cert_code').val(),
                    password: $('#id_password').val(),
                    password_check: $('#id_password_check').val()
                },
                success: function (res) {
                    //var json = JSON.parse(res);
                    alert(res['message']);
                    if (res['status']) {
                        location.href='/';
                    }
                },
                fail: function (res) {
                    //var json = JSON.parse(res);
                    alert(res['message']);
                }
            });
        };

    initailize();

})(jQuery);

