"use strict";

var VadetisHighcharts = function () {

    var initHighcharts = function (html_id, url, settings, selectedButton) {
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
                height: settings.highcharts_height,
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
                        tooltip += '<tr>' +
                            '<td><span style="color:' + this.series.color + '">\u25CF</span> ' + this.series.name + ': </td>' +
                            '<td style="text-align: right;"><strong style="color: ' + value_color + ';">' + this.y.toFixed(settings.round_digits) + '</strong></td>' +
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
                maxHeight: settings.legend_height,
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

        // load chart
        initSeriesForType(highchart, url, "raw", true);
    };
    return {
        init: function (html_id, url, settings, selectedButton) {
            initHighcharts(html_id, url, settings, selectedButton);
        }
    };
}();
