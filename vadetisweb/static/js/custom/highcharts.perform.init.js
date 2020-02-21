"use strict";

var VadetisHighcharts = function () {

    var initHighcharts = function (html_id, url, url_update_threshold, url_cnf, selectedButton, algorithm, csrf_token, round_digits) {
        var shows_anomalies = true;
        var current_type = 'raw';
        var dataset_series = [];
        var dataset_series_json;
        var info;
        var url_threshold_update_json = url_update_threshold;
        var url_cnf_img = url_cnf;
        var current_threshold;

        //init RoundSlider
        RoundSliders.init(round_digits);

        //init NoUiSlider
        var threshold_slider = $('#threshold_slider')[0]; //extracting the raw element from the jQuery object
        var selected_threshold_value = $('#selected_threshold_value')[0];
        NoUiSliders.init(threshold_slider, selected_threshold_value, round_digits);

        Highcharts.setOptions({
            global: {
                useUTC: true,
            }
        });

        // create the chart
        var highchart = new Highcharts.StockChart(html_id, {
            chart: {
                zoomType: 'x',
                height: 600, //TODO get from settings
            },

            navigator: {
                adaptToUpdatedData: true,
            },

            scrollbar: {
                liveRedraw: false,
            },

            title: {
                text: null,
            },

            tooltip: {
                shared: true,
                useHTML: true,

                formatter: function () {
                    var tooltip = '<span style="font-size: 10px;">' + Highcharts.dateFormat('%A, %b %e %Y, %H:%M', new Date(this.x)) + '</span>';

                    tooltip += '<table>';
                    $.each(this.points, function (i, point) {
                        var value_color = '#000000';
                        if (point.point.marker) {
                            if (point.point.marker.fillColor) {
                                value_color = point.point.marker.fillColor;
                            }
                        }
                        //TODO add round digits from settings
                        tooltip += '<tr>' +
                            '<td><span style="color:' + this.series.color + '">\u25CF</span> ' + this.series.name + ': </td>' +
                            '<td style="text-align: right;"><strong style="color: ' + value_color + ';">' + this.y.toFixed(2) + '</strong></td>' +
                            '<td>' + this.series.tooltipOptions.valueSuffix + '</td>' +
                            '</tr>';
                    });
                    tooltip += '</table>';
                    return tooltip;
                }
            },

            legend: {
                enabled: true,
                layout: 'horizontal',
                maxHeight: 200, // TODO add from settings
            },

            rangeSelector: {
                buttons: [{
                    type: 'minute',
                    count: 1,
                    text: '1min'
                }, {
                    type: 'hour',
                    count: 1,
                    text: '1h'
                }, {
                    type: 'day',
                    count: 1,
                    text: '1d'
                }, {
                    type: 'week',
                    count: 1,
                    text: '1w'
                }, {
                    type: 'month',
                    count: 1,
                    text: '1m'
                }, {
                    type: 'year',
                    count: 1,
                    text: '1y'
                }, {
                    type: 'all',
                    text: 'All'
                }],
                inputEnabled: false, // as it supports only days
                selected: selectedButton,
            },

            yAxis: [{
                floor: -40,
                title: {
                    text: 'Value',
                },
            }],

            plotOptions: {
                series: {
                    connectNulls: false,
                    turboThreshold: 0, // enables to display unlimited number of points
                    marker: {
                        radius: null,
                    }
                },
            },

            exporting: {
                enabled: false
            },
            series: dataset_series,
        });

        //TODO place into utils
        function loadSeriesForType(type) {
            current_type = type;
            //TODO show loading img highchart.showLoading('<img alt="" src="{% static 'img/loading.gif' %}" />');
            $.getJSON(url + '?type=' + type + '&show_anomalies=' + shows_anomalies, function (data) {
                console.log(data);
                var series_data_json = data['series'];
                setSeriesData(highchart, series_data_json);
                highchart.hideLoading();
            });
        }

        $.getJSON(url + '?type=raw&show_anomalies=true', function (data) {
            $('#loading_screen').hide();
            $('#results_screen').show();
            var series_data = data['series'];
            dataset_series_json = data['series'];
            info = data['info'];
            dataset_series = getDatasetSeriesFromJsonValues(series_data);
            loadSeries(highchart, dataset_series);
        });

        $('#threshold_form').on('submit', function(event){
            event.preventDefault();
            //highchart.showLoading('<img alt="" src="{% static 'img/loading.gif' %}" />');
            var dataset_series_without_marker_json = getDatasetSeriesWithoutMarkerJson(dataset_series_json); //reduce post size
            var post_data = { threshold : JSON.stringify($('#selected_threshold_value').val()), dataset_series_json : JSON.stringify(dataset_series_without_marker_json), info : JSON.stringify(info), algorithm : JSON.stringify(algorithm), csrfmiddlewaretoken : csrf_token, };
                updateHighchartsSeriesForThreshold(highchart, url_threshold_update_json, post_data, function (new_dataset_series_json, info) {
                dataset_series_json = new_dataset_series_json;
                var cnf_data = { data : JSON.stringify(info.cnf_matrix), csrfmiddlewaretoken : csrf_token, };
                loadImage("cnf_matrix", url_cnf_img, cnf_data);

                current_threshold = info.selected_threshold;
                $('#current_threshold').html(info.selected_threshold.toFixed(round_digits));

                RoundSliders.updateValue("#roundslider_accuracy", info.accuracy.toFixed(round_digits));
                RoundSliders.updateValue("#roundslider_f1", info.f1_score.toFixed(round_digits));
                RoundSliders.updateValue("#roundslider_precision", info.precision.toFixed(round_digits));
                RoundSliders.updateValue("#roundslider_recall", info.recall.toFixed(round_digits));

                var min = Number(info.thresholds[0].toFixed(round_digits));
                var max = Number(info.thresholds[info.thresholds.length-1].toFixed(round_digits));

                threshold_slider.noUiSlider.updateOptions({
                    range: {
                        'min': min,
                        'max': max
                    },
                });
            });
        });
    };
    return {
        init: function (html_id, url, url_threshold, url_cnf, selectedButton, algorithm, csrf_token, round_digits) {
            initHighcharts(html_id, url, url_threshold, url_cnf, selectedButton, algorithm, csrf_token, round_digits);
        }
    };
}();
