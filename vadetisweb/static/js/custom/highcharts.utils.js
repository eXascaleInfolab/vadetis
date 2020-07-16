"use strict";

/*
 * function to update the curves in highcharts for a new threshold.
 * Data must contain new threshold and series data from highcharts
 */
function updateHighchartsSeriesForThreshold(highchart, url, post_data, callback) {
    var csrftoken = Cookies.get('csrftoken');
    $.ajax({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        type: "POST",
        url: url,
        data: post_data,

        success: function (data, status, xhr) {
            handleMessages(data);
            var dataset_series_new_json = data['series'];
            var new_info = data['info'];

            setSeriesData(highchart, dataset_series_new_json);

            highchart.hideLoading();
            callback(dataset_series_new_json, new_info);
        },
        error: function (data, status, xhr) {
            printMessages([{'message': "Request failed"}], "error-request");
            handleMessages(data);
        }
    });
}

function getDatasetSeriesJson(highchart) {
    var dataset_series_json = {'series': []};
    highchart.series.forEach(function (series) {
        // the series of the navigator have to be excluded
        if (highchart.navigator === undefined || !containsObject(series, highchart.navigator.series)) {
            var series_json = {};
            series_json.id = series.options.id;
            series_json.name = series.options.name;
            series_json.unit = series.options.custom.unit;
            series_json.is_spatial = series.options.custom.is_spatial;
            series_json.detection = series.options.custom.detection;
            series_json.type = series.options.custom.type;
            series_json.data = getCleanedSeriesData(series.options.data);
            dataset_series_json.series.push(series_json);
        }
    });
    return dataset_series_json;
}

function getCleanedSeriesData(series_data) {
    var data = [];
    series_data.forEach(function (point) {
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

function updateTimeRangeBySelection(highchart, form_id, rangeStartId, rangeEndId) {
    var timeRangeSelector = $('#timeRange');
    if (timeRangeSelector.length > 0) {
        var rangeStartSelector = $('#' + rangeStartId);
        var rangeEndSelector = $('#' + rangeEndId);
        var range = _getExtremesForDetection(highchart, timeRangeSelector);

        _addOrReplaceRangeInput(form_id, rangeStartSelector, rangeStartId, "range_start", range.min);
        _addOrReplaceRangeInput(form_id, rangeEndSelector, rangeEndId, "range_end", range.max);
    }
}

function updateTimeRange(highchart, form_id, rangeStartId, rangeEndId) {

    var rangeStartSelector = $('#' + rangeStartId);
    var rangeEndSelector = $('#' + rangeEndId);
    var extremes_x = highchart.xAxis[0].getExtremes();
    var range = {min: Math.round(extremes_x.min), max: Math.round(extremes_x.max)}

    _addOrReplaceRangeInput(form_id, rangeStartSelector, rangeStartId, "range_start", range.min);
    _addOrReplaceRangeInput(form_id, rangeEndSelector, rangeEndId, "range_end", range.max);
}

function _getExtremesForDetection(highchart, timeRangeSelector) {
    var timeRangeVal = timeRangeSelector.val();
    var extremes_x = highchart.xAxis[0].getExtremes();
    var range = {};
    if (timeRangeVal.toLowerCase() === 'selection') {
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
    var csrftoken = Cookies.get('csrftoken');
    $.ajax({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        type: "POST",
        url: url,
        data: post_data,
        success: function (data) {
            var dataset_series_new_json = data[0];

            //dataset_series_data = generateSeriesFromJson(dataset_series_json, "{{ conf|get_item:'algorithm' }}", "{{ conf|get_item:'time_series' }}");
            //loadSeries(highchart, dataset_series_data);

            setSeriesData(highchart, dataset_series_new_json);
            highchart.hideLoading();
            callback(dataset_series_new_json);
        }
    });
}

function generateSeriesFromJson(dataset_series_json, algorithm, time_series) {
    var dataset_series_data = [];

    dataset_series_json.series.forEach(function (series) {
        if (algorithm === 'LISA') {
            var visible = false;
            if (series.id === time_series) {
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
                            if (this.series.options.id === time_series) {
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
        var highchart_series = highchart.get(series.id);

        // bugfix: sometimes markers do not get updated by highcharts, therefore we clear before setting the data
        highchart_series.setData([], false, false);

        highchart_series.setData(series.data, false, true);
        highchart_series.update({
            custom: {
                type: series.type,
                is_spatial: series.is_spatial,
                unit: series.unit,
                detection: series.detection,
            }
        }, false);
        if (series.dashStyle !== undefined) {
            highchart_series.update({dashStyle: series.dashStyle}, false);
        }
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
            dashStyle: series.dashStyle,
            marker: {
                enabled: true,
                symbol: 'circle',
            },
            custom: {
                type: series.type,
                is_spatial: series.is_spatial,
                unit: series.unit,
                detection: series.detection,
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

function initSeriesForType(highchart, url, type) {
    highchart.showLoading();
    $.getJSON(url + '?type=' + type, function (data) {
        var series_data = data['series'];
        var dataset_series = getDatasetSeriesFromJson(series_data);
        loadSeries(highchart, dataset_series);
        highchart.hideLoading();
    });
}

function loadSeriesForType(highchart, url, type, callback) {
    highchart.showLoading();
    $.getJSON(url + '?type=' + type, function (data) {
        var series_data_json = data['series'];
        setSeriesData(highchart, series_data_json);

        highchart.hideLoading();
        callback();
    });
}

function downloadDataset(highchart, url, type, callback) {
    var formData = new FormData(), dataset_series_json = getDatasetSeriesJson(highchart), csrfToken = Cookies.get('csrftoken');
    formData.append('dataset_series_json', JSON.stringify(dataset_series_json));
    $.ajax({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrfToken);
            }
        },
        type: "POST",
        url: url + '?format=' + type,
        data: formData,
        dataType: 'binary',
        processData: false,
        contentType: false,
        success: function (data, status, xhr) {
            if (data !== undefined) {
                var header = xhr.getResponseHeader('Content-Disposition');
                var filename = header.match(/filename="(.+)"/)[1];
                saveData(data, filename);
            }
            handleMessages(data);
            callback();
        },
        error: function (data, status, xhr) {
            printMessages([{'message': "Request failed: Could not download dataset."}], "error-request");
            handleMessages(data);
            callback();
        }
    });
}

//Deprecated
function updateSeriesForType(highchart, url, type, show_anomaly, callback) {
    highchart.showLoading();
    var formData = new FormData(), dataset_series_json = getDatasetSeriesJson(highchart), csrfToken = Cookies.get('csrftoken');
    formData.append('dataset_series_json', JSON.stringify(dataset_series_json));

    $.ajax({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrfToken);
            }
        },
        type: "POST",
        url: url + '?type=' + type,
        data: formData,
        processData: false,
        contentType: false,
        success: function (data, status, xhr) {
            if (data !== undefined) {
                var series_data_json = data['series'];
                setSeriesData(highchart, series_data_json);
            }
            handleMessages(data);
            highchart.hideLoading();
            callback();
        },
        error: function (data, status, xhr) {
            printMessages([{'message': "Request failed"}], "error-request");
            handleMessages(data);
            highchart.hideLoading();
            callback();
        }
    });
}

function updateScores(info) {
    RoundSliders.init(3);
    RoundSliders.updateValue("#roundslider_accuracy", info.accuracy.toFixed(3));
    RoundSliders.updateValue("#roundslider_f1", info.f1_score.toFixed(3));
    RoundSliders.updateValue("#roundslider_precision", info.precision.toFixed(3));
    RoundSliders.updateValue("#roundslider_recall", info.recall.toFixed(3));
}

function updateThreshold(thresholds, value) {
    var slider_element = $('#threshold_slider')[0]; // extracting the raw element from the jQuery object
    var threshold_input_selector = $('#threshold_value');
    // init NoUiSlider if required
    if (!slider_element.noUiSlider) {
        var min = thresholds[0], max = thresholds[thresholds.length - 1]
        NoUiSliders.init(slider_element, threshold_input_selector, min, max);
    }
    slider_element.noUiSlider.set(value);
    $('#current_threshold').html(value);
}

function requestCnfMatrix(portlet_id, img_container_id, info) {
    // note: url is taken from global const
    var cnf_data = {'cnf': JSON.stringify(info.cnf_matrix)};
    loadImage(img_container_id, cnf_url, cnf_data, function () {
        $('#' + portlet_id).show();
    });
}

function requestPlot(portlet_id, img_container_id, thresholds, threshold_scores) {
    // note: url is taken from global const
    var plot_data = {
        thresholds: thresholds,
        threshold_scores: threshold_scores
    };
    var plotData = {'plot_data': JSON.stringify(plot_data)};
    loadImage(img_container_id, plot_url, plotData, function () {
        $('#' + portlet_id).show();
    });
}

/*function setColumnSeriesData(highchart, data) {
    var highchart_series = highchart.get(series.id);
    highchart_series.setData(data, false, true);
}*/

function addColumnSeries(highchart, algorithm, maximize_score, data) {
    highchart.addSeries({
        name: algorithm,
        data: data,
        index: getIndexForAlgorithm(algorithm),
        custom: {
            maximize_score: maximize_score
        }
    });

    // reindex order
    highchart.series.forEach(function (series) {
        var index = getIndexForAlgorithm(series.name);
        series.update({index: index}, false);
    });
    highchart.redraw();
}

function getSeriesByName(highchart, name) {
    var highchartSeries = highchart.series;
    for (var i = 0; i < highchartSeries.length; i++) {
        var series = highchartSeries[i];
        if (series.hasOwnProperty('name') && series.name === name) {
            return series;
        }
    }
    return undefined;
}

function getScoresFromColumnChart(highchart) {
    var scores = {'scores': []};

    highchart.series.forEach(function (series) {
        // the series of the navigator have to be excluded
        if (highchart.navigator === undefined || !containsObject(series, highchart.navigator.series)) {
            var score_json = {};
            score_json.algorithm = series.options.name;
            score_json.accuracy = series.options.data[0];
            score_json.f1_score = series.options.data[1];
            score_json.precision = series.options.data[2];
            score_json.recall = series.options.data[3];
            scores.scores.push(score_json);
        }
    });
    return scores;
}