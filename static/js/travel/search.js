(function($) {
    var
        initailize = function () {
            $('ul.lines > li.line').bind('click', changeSubwayLine);
            $('ul.stations > li.station').bind('click', selectSubway);
        },
        changeSubwayLine = function (e) {
            var $stations = $("ul.stations > li.station"),
                $removeTarget = $('ul.lines > li.line.active').data('target'),
                $activeTarget = $(this).data('target');
            if ($removeTarget == $activeTarget) {
                $(this).removeClass('active');
                if ($stations.hasClass($activeTarget)) {
                    $('li.' + $activeTarget).removeClass('active');
                }
            }
            else {
                if ($(this).siblings().hasClass('active')) {
                    $(this).siblings().removeClass('active');
                    $('li.' + $removeTarget).removeClass('active');
                }

                $(this).addClass('active');

                if ($stations.hasClass($activeTarget)) {
                    $('li.' + $activeTarget).addClass('active');
                }
            }
        },
        selectSubway = function (e) {
            location.href = $(this).data('href');
        }
        ;

    initailize();
})(jQuery);