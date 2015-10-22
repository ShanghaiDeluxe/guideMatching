(function($) {
    var
        initailize = function () {
            $(document).ready(loadSubwayData);
            $('ul.lines > li.line').bind('click', changeSubwayLine);
        },
        loadSubwayData = function (e) {
            $.ajax({
                type: "GET",
                url: 'http://openapi.seoul.go.kr:8088/6f43776b756a69633130305a6f734e59/json/SearchSTNBySubwayLineService/1/700/',
                data: {},
                always: function (res) {
                    if (res['SearchSTNBySubwayLineService']['RESULT']['CODE'] != 'INFO-000') {
                        alert(res['SearchSTNBySubwayLineService']['RESULT']['MESSAGE']);
                        return -1;
                    }
                },
                success: function (res) {
                    //var json = JSON.parse(res);
                    var count = res['SearchSTNBySubwayLineService']['list_total_count'],
                        data_obj = res['SearchSTNBySubwayLineService']['row'];
                    sortingSubway(count, data_obj);
                },
                fail: function (msg) {
                    return -1;
                }
            });
        },
        sortingSubway = function (count, data_obj) {
            var sort_data_obj = [];

            for (var key in data_obj) {
                sort_data_obj.push({
                    'STATION_CD': data_obj[key]['STATION_CD'],
                    'STATION_NM' : data_obj[key]['STATION_NM'],
                    'LINE_NUM': data_obj[key]['LINE_NUM'],
                    'FR_CODE': data_obj[key]['FR_CODE']
                });
            }
            sort_data_obj.sort(function (a, b) {
                return (a.STATION_NM < b.STATION_NM) ? -1 : (a.STATION_NM > b.STATION_NM) ? 1 : 0;
            });

            addSubway(sort_data_obj);
        },
        addSubway = function (sort_data_obj) {
            for (var i=0; i < sort_data_obj.length; i++) {
                var $target_line = $('ul.lines > li.line-' + sort_data_obj[i]['LINE_NUM']),
                    $target_stations = $('ul.stations');
                if ($target_line.length > 0) {
                    $target_stations.append('<li class="station station-' + sort_data_obj[i]['LINE_NUM'] + '">' +
                        '<a href="/travel/' + sort_data_obj[i]['STATION_CD'] + '/">' +
                        sort_data_obj[i]['STATION_NM'] + '</a></li>');
                }
            }
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