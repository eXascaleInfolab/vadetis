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

function getDatasetSeriesJson(highchart){
    var dataset_series_json = { 'series' : [] };
    highchart.series.forEach(function(series) {
        // the series of the navigator have to be excluded
        if(highchart.navigator !== undefined && !containsObject(series, highchart.navigator.series)) {
            var series_json = {};
            series_json.id = series.options.id;
            series_json.name = series.options.name;
            series_json.unit = series.options.custom.unit;
            series_json.is_spatial = series.options.custom.is_spatial;
            series_json.type = series.options.custom.type;
            series_json.data = getCleanedSeriesData(series.options.data);
            dataset_series_json.series.push(series_json);
        }
    });
    return dataset_series_json;
}

function getCleanedSeriesData(series_data){
    var data = [];
    series_data.forEach(function(point) {
        var p = _objectWithoutProperties(point, ['marker']);
        data.push(p);
    });
    return data;
}

function _objectWithoutProperties(obj, keys) {
    var target = {};
    for (var i in obj) {
        if (keys.indexOf(i) >= 0) continue;
        if (!Object.prototype.hasOwnProperty.call(obj, i)) continue;
        target[i] = obj[i];
    }
    return target;
}

function updateTimeRange(highchart, form_id) {
    var timeRangeSelector = $('#timeRange');
    if (timeRangeSelector.length > 0) {
        var rangeStartId = "rangeStart";
        var rangeEndId = "rangeEnd";
        var rangeStartSelector = $('#' + rangeStartId);
        var rangeEndSelector = $('#' + rangeEndId);
        var range = _getExtremesForDetection(highchart, timeRangeSelector);

        _addOrReplaceRangeInput(form_id, rangeStartSelector, rangeStartId, "range_start", range.min);
        _addOrReplaceRangeInput(form_id, rangeEndSelector, rangeEndId, "range_end", range.max);
    }
}

function _getExtremesForDetection(highchart, timeRangeSelector) {
    var timeRangeVal = timeRangeSelector.val();
    var extremes_x = highchart.xAxis[0].getExtremes();
    var range = {};
    if (timeRangeVal.toLowerCase() === 'as selected in chart') {
        range.min = Math.round(extremes_x.min);
        range.max = Math.round(extremes_x.max);
    } else {
        range.min = Math.round(extremes_x.dataMin);
        range.max = Math.round(extremes_x.dataMax);
    }
    return range;
}

function _addOrReplaceRangeInput(form_id, selector, id, name, value) {
    if (selector.length > 0) {
        selector.replaceWith(
            $('<input />').attr('type', 'hidden')
                .attr('id', id)
                .attr('name', name)
                .attr('value', value));
    } else {
        $('<input />').attr('type', 'hidden')
            .attr('id', id)
            .attr('name', name)
            .attr('value', value)
            .appendTo('#' + form_id);
    }
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
        highchart.get(series.id).setData(series.data, false, true);
    });
    highchart.redraw();
}

function getDatasetSeriesFromJson(series_data) {
    var dataset_series = [];
    series_data.forEach(function (series) {
        dataset_series.push({
            type: 'line',
            visible: true,
            id: series.id,
            name: series.name,
            lineWidth: 1,
            data: series.data,
            marker: {
                enabled: true,
                symbol: 'circle',
            },
            custom: {
                type: series.type,
                is_spatial: series.is_spatial,
                unit: series.unit,
            },
            /*tooltip: {
                valueSuffix: ' ' + series.unit,
            }*/
        });
    });
    return dataset_series;
}

function loadSeries(chart, data_series) {
    // remove all series
    while (chart.series.length > 0)
        chart.series[0].remove(true);

    // add new series
    data_series.forEach(function (series) {
        chart.addSeries(series);
    });
}

function initSeriesForType(highchart, url, type, show_anomaly) {
    highchart.showLoading();
    $.getJSON(url + '?type=' + type + '&show_anomaly=' + show_anomaly, function (data) {
        var series_data = data['series'];
        var dataset_series = getDatasetSeriesFromJson(series_data);
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

function loadCnfMatrix(portlet_id, img_container_id, info) {
    // note: url is taken from global const
    var cnf_data = { data : JSON.stringify(info.cnf_matrix) };
    loadImage(img_container_id, cnf_url, cnf_data, function () {
        $('#' + portlet_id).show();
    });
}

function loadPlot(portlet_id, img_container_id, info) {
    // note: url is taken from global const
    var ts_data = { thresholds : JSON.stringify(info.thresholds), scores : JSON.stringify(info.threshold_scores) };
    loadImage(img_container_id, plot_url, ts_data, function () {
        $('#' + portlet_id).show();
    });
}
