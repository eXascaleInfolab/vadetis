"use strict";

var VadetisHighcharts = function () {

    var initHighcharts = function (html_id, url, selectedButton) {
        var shows_anomalies = true;
        var current_type = 'raw';
        var dataset_series = [];

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
                var series_data_json = data[0];
                setSeriesData(highchart, series_data_json);
                highchart.hideLoading();
            });
        }

        $.getJSON(url + '?type=raw&show_anomalies=true', function (data) {
            $('#loading_screen').hide();
            $('#results_screen').show();
            var series_data = data['series'];
            dataset_series = getDatasetSeriesFromJsonValues(series_data);
            loadSeries(highchart, dataset_series);
        });

        var anomaly_detection_form = $('#anomaly_detection_form');
        anomaly_detection_form.submit(function (event) {
            if ($("#id_time_range").length > 0) {
                //var chart = $('#container').highcharts();
                var time_range = $('#id_time_range').val();
                var extremes_x = highchart.xAxis[0].getExtremes();
                var range = {};

                if (time_range == 'as selected in chart') {
                    range.min = Math.round(extremes_x.min);
                    range.max = Math.round(extremes_x.max);
                } else {
                    range.min = Math.round(extremes_x.dataMin);
                    range.max = Math.round(extremes_x.dataMax);
                }

                if ($("#rangeStart").length > 0) {
                    $("#rangeStart").replaceWith(
                        $('<input />').attr('type', 'hidden')
                            .attr('id', "id_range_start")
                            .attr('name', "range_start")
                            .attr('value', range.min));
                } else {
                    $('<input />').attr('type', 'hidden')
                        .attr('id', "id_range_start")
                        .attr('name', "range_start")
                        .attr('value', range.min)
                        .appendTo('#anomaly_detection_form');
                }

                if ($("#rangeEnd").length > 0) {
                    $("#rangeEnd").replaceWith(
                        $('<input />').attr('type', 'hidden')
                            .attr('id', "id_range_end")
                            .attr('name', "range_end")
                            .attr('value', range.max));
                } else {
                    $('<input />').attr('type', 'hidden')
                        .attr('id', "id_range_end")
                        .attr('name', "range_end")
                        .attr('value', range.max)
                        .appendTo('#anomaly_detection_form');
                }
            }
        });
    };
    return {
        init: function (html_id, url, selectedButton) {
            initHighcharts(html_id, url, selectedButton);
        }
    };
}();
