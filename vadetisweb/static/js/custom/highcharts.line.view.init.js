"use strict";

var VadetisHighcharts = function () {

    var initHighcharts = function (html_id, url, selectedButton) {
        var settings = settingsFromCookie();

        Highcharts.setOptions({
            global: {
                useUTC: true,
            }
        });

        // create the chart
        var highchart = new Highcharts.StockChart(html_id, {
            chart: {
                zoomType: 'x',
                height: 750,
            },

            navigator: {
                enabled: true,
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

                    var hasScore = false;
                    tooltip += '<table style="margin-top: 4px;">';
                    $.each(this.points, function (i, point) {
                        var value_color = '#000000';
                        if (point.point.marker) {
                            if (point.point.marker.fillColor) {
                                value_color = point.point.marker.fillColor;
                            }
                        }
                        tooltip += '<tr>';
                        tooltip += '<td><span style="color:' + this.series.color + '">\u25CF</span> ' + this.series.name + ': </td>'
                            + '<td style="text-align: right;"><strong style="color: ' + value_color + ';">' + this.y.toFixed(settings.round_digits) + '</strong></td>';

                        if(point.point.score !== undefined) {
                            hasScore = true;
                        }
                        tooltip += '</tr>';
                    });
                    tooltip += '</table>';

                    if(hasScore) {
                        tooltip += '<table style="margin-top: 4px;">';
                        for (var i = 0; i < this.points.length; i++) {
                            var point = this.points[i];
                            if(point.hasOwnProperty('point') && point.point.score !== undefined) {
                                tooltip += '<tr><td><strong>Score:</strong></td><td>' + point.point.score.toFixed(settings.round_digits) + '</td></tr>';
                                break;
                            }
                        }
                        tooltip += '</table>';
                    }

                    return tooltip;
                }
            },

            legend: {
                enabled: true,
                layout: 'horizontal',
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
                inputEnabled: false, // because it supports only days
                selected: selectedButton,
            },

            yAxis: [{
                floor: -40,
                title: {
                    text: '',
                },
                labels: {
                    formatter: function () {
                        return this.value;
                    }
                }
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
            series: [],
        });

        // load chart
        initSeriesForType(highchart, url, "raw");
    };
    return {
        init: function (html_id, url, selectedButton) {
            initHighcharts(html_id, url, selectedButton);
        }
    };
}();
