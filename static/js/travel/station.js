(function($) {
    var
        initailize = function () {
            $('div.guide').bind('click', function (e) {
                location.href = e.currentTarget.baseURI + $(this).data('target');
            });
        }
        ;

    initailize();
})(jQuery);