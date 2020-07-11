"use strict";

var VadetisColumnHighcharts = function () {

    var initHighcharts = function (html_id, url) {
        var dataset_series = [];
        var settings = settingsFromCookie();

        Highcharts.setOptions({
            global: {
                useUTC: true,
            }
        });

        // create the chart
        var highchart = new Highcharts.chart(html_id, {
            chart: {
                type: 'column',
                height: 750,
            },

            title: {
                text: null,
            },

            legend: {
                enabled: true,
                layout: 'horizontal',
            },
            xAxis: {
                categories: [
                    'Accuracy',
                    'F1-Score',
                    'Precision',
                    'Recall',
                ],
                crosshair: true
            },
            yAxis: {
                min: 0,
                title: {
                    text: 'Score'
                }
            },
            tooltip: {
                headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
                pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                    '<td style="padding:0"><b>{point.y:.3f}</b></td></tr>',
                footerFormat: '</table>',
                shared: true,
                useHTML: true
            },
            plotOptions: {
                column: {
                    pointPadding: 0.2,
                    borderWidth: 0
                }
            },
            series: [{
                name: 'Tokyo',
                data: [49.9, 71.5, 106.4, 129.2]

            }, {
                name: 'New York',
                data: [83.6, 78.8, 98.5, 93.4]

            }, {
                name: 'London',
                data: [48.9, 38.8, 39.3, 41.4]

            }, {
                name: 'Berlin',
                data: [42.4, 33.2, 34.5, 39.7]

            }]
        });

        // load chart
        //initSeriesForType(highchart, url, "raw");
    };
    return {
        init: function (html_id, url) {
            initHighcharts(html_id, url);
        }
    };
}();
