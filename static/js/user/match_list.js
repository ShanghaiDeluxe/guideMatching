(function (e) {
    var
        initialize = function () {
            $('div.guide').bind('click', function (e) {
                location.href = e.currentTarget.baseURI + $(this).data('target');
            });
            $('div.guide_status > div').bind('click', changeMatching);
        },
        changeMatching = function (e) {
            if ($(this).hasClass('active')) {
                $(this).removeClass('active');
            } else {
                $(this).siblings().removeClass('active');
                $(this).addClass('active');
            }

            if ($(this).hasClass('call')) {
                if ($('div.guides-call').hasClass('active')) {
                    $('div.guides-call').removeClass('active');
                } else {
                    $('div.guides-call').siblings().removeClass('active');
                    $('div.guides-call').addClass('active');
                }
            } else if ($(this).hasClass('receive')) {
                if ($('div.guides-receive').hasClass('active')) {
                    $('div.guides-receive').removeClass('active');
                } else {
                    $('div.guides-receive').siblings().removeClass('active');
                    $('div.guides-receive').addClass('active');
                }
            } else if ($(this).hasClass('complete')) {
                if ($('div.guides-complete').hasClass('active')) {
                    $('div.guides-complete').removeClass('active');
                } else {
                    $('div.guides-complete').siblings().removeClass('active');
                    $('div.guides-complete').addClass('active');
                }
            }
        }
    ;
    initialize();
})(jQuery);