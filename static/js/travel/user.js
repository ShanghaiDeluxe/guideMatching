(function ($){
    var
        initialize = function () {
            $('div.ask > button').bind('click', function (e) {
                if (confirm('Are you sure to request?')) {
                    askGuide(e);
                }
            })
        },
        askGuide = function (e) {
            e.preventDefault();
            $.ajax({
                type: "POST",
                url: e.currentTarget.baseURI + 'invite_guide/',
                data: {
                    csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()
                },
                success: function (res) {
                    //var json = JSON.parse(res);
                    console.log(res);
                    if (res['result'] == 1) {
                        $('div.ask').children('button').remove();
                        $('div.ask').html('<div>Successed to send a request.</div>');
                    }
                },
                fail: function (res) {
                    //var json = JSON.parse(res);
                    console.log(res);
                }
            })
        }
        ;
    initialize();
})(jQuery);