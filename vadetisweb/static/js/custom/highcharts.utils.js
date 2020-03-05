/*
 * function to update the curves in highcharts for a new threshold.
 * Data must contain new threshold and series data from highcharts
 */
function updateHighchartsSeriesForThreshold(highchart, url, post_data, callback) {
    $.ajax({
        type: "POST",
        url: url,
        data: post_data,
        cache: false,

        success: function (data, status, xhr) {
            if (data.responseJSON !== undefined && data.responseJSON.hasOwnProperty('messages')) {
                print_messages(data.responseJSON.messages);
            }
            var dataset_series_new_json = data['series'];
            var new_info = data['info'];
            //dataset_series_data = generateSeriesFromJson(dataset_series_json, "{{ conf|get_item:'algorithm' }}", "{{ conf|get_item:'ts_selected' }}");
            //loadSeries(highchart, dataset_series_data);

            setSeriesData(highchart, dataset_series_new_json);

            highchart.hideLoading();
            callback(dataset_series_new_json, new_info);
        },
        error: function(data, status, xhr) {
                console.error("Sending asynchronous failed");
                if(data.responseJSON !== undefined && data.responseJSON.hasOwnProperty('messages')) {
                    print_messages(data.responseJSON.messages);
                }
                if(data.responseJSON !== undefined && data.responseJSON.hasOwnProperty('form_errors')) {
                    print_form_errors(data.responseJSON.form_errors);
                }
        }
    });
}

function getDatasetSeriesWithoutMarkerJson(dataset_series_json) {
    var clone_dataset_series_json = JSON.parse(JSON.stringify(dataset_series_json));
    clone_dataset_series_json.forEach(function(series) {
        measurements = series.measurements;
        removeMarkerFromMeasurements(measurements);
    });
    return clone_dataset_series_json;
}


function removeMarkerFromMeasurements(measurements){
    measurements.forEach(function (measurement) {
        delete measurement['marker'];
    });
}


function updateHighchartsSeriesForType(highchart, url, post_data, callback) {
    $.ajax({
        type: "POST",
        url: url,
        data: post_data,
        cache: false,

        success: function (data) {
            var dataset_series_new_json = data[0];

            //dataset_series_data = generateSeriesFromJson(dataset_series_json, "{{ conf|get_item:'algorithm' }}", "{{ conf|get_item:'ts_selected' }}");
            //loadSeries(highchart, dataset_series_data);

            setSeriesData(highchart, dataset_series_new_json);
            highchart.hideLoading();
            callback(dataset_series_new_json);
        }
    });
}

function generateSeriesFromJson(dataset_series_json, algorithm, ts_selected) {
    dataset_series_data = [];

    dataset_series_json.series.forEach(function (series) {
        if (algorithm === 'LISA') {
            var visible = false;
            if (series.id === ts_selected) {
                visible = true;
            }
            dataset_series_data.push({
                type: 'line',
                visible: visible,
                id: series.id,
                name: series.name,
                lineWidth: 1,
                data: series.measurements.raw,
                marker: {
                    enabled: true,
                    symbol: 'circle',
                },
                tooltip: {
                    valueSuffix: ' ' + series.unit,
                },
                point: {
                    events: {
                        click: function (e) {
                            if (this.series.options.id === ts_selected) {
                                getLISAComputation(e.point);
                            }
                        }
                    },
                },
            });

        } else {
            dataset_series_data.push({
                type: 'line',
                visible: true,
                id: series.id,
                name: series.name,
                lineWidth: 1,
                data: series.measurements,
                marker: {
                    enabled: true,
                    symbol: 'circle',
                },
                tooltip: {
                    valueSuffix: ' ' + series.unit,
                },
            });
        }

    });
    return dataset_series_data;
}

function setSeriesData(highchart, series_data_json) {
    series_data_json.forEach(function (series) {
        highchart.get(series.id).setData(series.measurements, false, true);
    });
    highchart.redraw();
}

function getDatasetSeriesFromJsonValues(series_data) {
    var dataset_series = [];
    series_data.forEach(function (series) {
        dataset_series.push({
            type: 'line',
            visible: true,
            id: series.id,
            name: series.name,
            lineWidth: 1,
            data: series.measurements,
            marker: {
                enabled: true,
                symbol: 'circle',
            },
            tooltip: {
                valueSuffix: ' ' + series.unit,
            }
        });
    });
    return dataset_series;
}

function loadSeries(chart, data_series) {
    //remove all series
    while (chart.series.length > 0)
        chart.series[0].remove(true);

    //add new series
    data_series.forEach(function (series) {
        chart.addSeries(series);
    });
}

function initSeriesForType(highchart, url, type, show_anomaly) {
    highchart.showLoading();
    $.getJSON(url + '?type=' + type + '&show_anomaly=' + show_anomaly, function (data) {
        var series_data = data['series'];
        dataset_series = getDatasetSeriesFromJsonValues(series_data);
        loadSeries(highchart, dataset_series);
        highchart.hideLoading();
    });
}

function loadSeriesForType(highchart, url, type, show_anomaly, callback) {
    highchart.showLoading();
    $.getJSON(url + '?type=' + type + '&show_anomaly=' + show_anomaly, function (data) {
        var series_data_json = data['series'];
        setSeriesData(highchart, series_data_json);
        highchart.hideLoading();
        callback();
    });
}
