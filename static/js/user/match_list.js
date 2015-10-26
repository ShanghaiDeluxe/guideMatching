(function (e) {
    var
        initialize = function () {
            $('div.guide').bind('click', function (e) {
                location.href = e.currentTarget.baseURI + $(this).data('target');
            });
        }
    ;
    initialize();
})(jQuery);