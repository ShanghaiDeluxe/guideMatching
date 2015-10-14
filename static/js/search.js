(function($) {
    var
        initailize = function () {
            $('ul.lines > li.line').bind('click', changeSubwayLine);
        },
        changeSubwayLine = function (e) {
            var $stations = $("ul.stations > li.station"),
                $removeTarget = $('ul.lines > li.line.active').data('target'),
                $activeTarget = $(this).data('target');

            if ($(this).siblings().hasClass('active')) {
                $(this).siblings().removeClass('active');
                $('li.' + $removeTarget).removeClass('active');
            }

            $(this).addClass('active');

            if ($stations.hasClass($activeTarget)) {
                $('li.' + $activeTarget).addClass('active');
            }
        }
        ;

    initailize();
})(jQuery);