(function ($){
    var
        initialize = function () {
            $('div.ask > button.cancel').bind('click', function (e) {
                if (confirm('정말 취소하실껀가요?')) { ask(e, 'cancel/'); }
            });
            $('div.ask > button.accept').bind('click', function (e) {
                if (confirm('수락 하실껀가요?')) { ask(e, 'accept/'); }
            });
            $('div.ask > button.complete').bind('click', function (e) {
                if (confirm('여행이 끝나셨나요?')) { ask(e, 'complete/'); }
            });
            $('div.container > div.ask > button.review').bind('click', function (e) {
                $('div.comment-container').removeClass('inactive');
                $('div.container').addClass('inactive');
            });
            $('div.comment-container > div.ask > button.review').bind('click', function (e) {
                $('div.comment-container').addClass('inactive');
                $('div.container').removeClass('inactive');
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
                        $('div.ask').html('<div>요청이 실패했습니다.</div>');
                    } else if (res['result'] == 1) {
                        $('div.ask').html('<div>취소 되었습니다.</div>');
                    } else if (res['result'] == 2) {
                        $('div.ask').html('<div>수락 되었습니다.</div>');
                    } else if (res['result'] == 3) {
                        $('div.ask').html('<div>여행이 끝났습니다.</div>');
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
                        alert('<div>요청이 실패했습니다.</div>');
                    } else if (res['result'] == 1) {
                        alert('저장 되었습니다.');
                    }
                },
                fail: function (res) {

                }
            });

            return false;
        }
        ;
    initialize();
})(jQuery);