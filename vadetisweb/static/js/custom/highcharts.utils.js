

function setSeriesData(highchart, series_data_json) {
    series_data_json.series.forEach(function (series) {
        highchart.get(series.id).setData(series.measurements, false, true);
    });
    highchart.redraw();
}

function getDatasetSeriesFromJsonValues(series_data) {
    var dataset_series = [];
    series_data.series.forEach(function (series) {
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

function loadSeries(chart, data_series){
    //remove all series
    while(chart.series.length > 0)
        chart.series[0].remove(true);

    //add new series
    data_series.forEach(function(series) {
        chart.addSeries(series);
    });
}