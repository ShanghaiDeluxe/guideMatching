(function ($){
    var
        initialize = function () {
            $('div.ask > button.cancel, div.ask > div.receive > button.cancel').bind('click', function (e) {
                if (confirm('Are you sure that you cancel a request?')) { ask(e, 'cancel/'); }
            });
            $('div.ask > button.accept, div.ask > div.receive > button.accept').bind('click', function (e) {
                if (confirm('Are you sure that you accept a request?')) { ask(e, 'accept/'); }
            });
            $('div.ask > button.complete').bind('click', function (e) {
                if (confirm('Did you finish travel with this user?')) { ask(e, 'complete/'); }
            });
            $('div.container-main > div.ask > button.review').bind('click', function (e) {
                $('nav > div.container-nav > div.title-review').removeClass('inactive');
                $('nav > div.container-nav > div.title').addClass('inactive');
                $('div.container-sub').removeClass('inactive');
                $('div.container-main').addClass('inactive');
            });
            $('div.container-sub > form > div.ask > button.later').bind('click', function (e) {
                e.preventDefault();
                $('nav > div.container-nav > div.title').removeClass('inactive');
                $('nav > div.container-nav > div.title-review').addClass('inactive');
                $('div.container-sub').addClass('inactive');
                $('div.container-main').removeClass('inactive');
                return false;
            });
            $('input.comment-submit').bind('click', addComment);
        },
        ask = function (e, uri) {
            e.preventDefault();
            $.ajax({
                type: "POST",
                url: e.currentTarget.baseURI + uri,
                data: {
                    csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()
                },
                success: function (res) {
                    //var json = JSON.parse(res);

                    $('div.ask').children('button').remove();
                    if (res['result'] == 0) {
                        $('div.ask').html('<div>Failed to request.</div>');
                    } else if (res['result'] == 1) {
                        $('div.ask').html("<div>You've canceled a  request. Maybe next time :/</div>");
                    } else if (res['result'] == 2) {
                        $('div.ask').html("<div>You've accepted a request! You can confirm a request via email.</div>");
                    } else if (res['result'] == 3) {
                        $('div.ask').html("<div>We had been travelled! Please write a review!</div>");
                    }
                },
                fail: function (res) {

                }
            });
        },
        addComment = function (e) {
            e.preventDefault();
            e.stopPropagation();
            $.ajax({
                type: "POST",
                url: e.currentTarget.baseURI + 'review/',
                data: {
                    csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
                    content: $("textarea[name='content']").val()
                },
                success: function (res) {
                    //var json = JSON.parse(res);
                    if (res['result'] == 0) {
                        alert('Failed to request.');
                    } else if (res['result'] == 1) {
                        alert('Completed!');
                    }
                },
                fail: function (res) {
                    if (res['result'] == 0) {
                        alert('Failed to request.');
                    }
                }
            });

            return false;
        }
        ;
    initialize();
})(jQuery);