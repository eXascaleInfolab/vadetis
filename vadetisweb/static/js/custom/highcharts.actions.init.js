"use strict";

var VadetisHighchartsReset = function () {

    var clearInserted = function () {
        $('#threshold_form_portlet').remove();
        $('#detection_portlets').empty();
        $('#score_portlets').empty();
    }

    var init = function (highcharts_container_id, button_id, url) {
        var button = $("#" + button_id), isLoading = false, highchart = $("#" + highcharts_container_id).highcharts();

        button.click(function () {
            if (!isLoading) {
                $(":submit").attr("disabled", true);
                button.html('Loading...').addClass('disabled');
                loadSeriesForType(highchart, url, "raw", true, function () {
                    isLoading = false;
                    $(":submit").attr("disabled", false);
                    button.html('Reset').removeClass('disabled');
                    clearInserted();
                });
            } else {
                $(":submit").attr("disabled", false);
                button.html('Reset').removeClass('disabled');
                clearInserted();
            }
        });
    };
    return {
        init: function (highcharts_container_id, button_id, url) {
            init(highcharts_container_id, button_id, url);
        }
    };
}();

var VadetisHighchartsLoad = function () {
    var init = function (highcharts_container_id, button_id, url, type) {
        var button = $("#" + button_id), isLoading = false, highchart = $("#" + highcharts_container_id).highcharts();
        var buttonTxt = type === 'raw' ? 'Raw' : (type === 'zscore' ? "Z-Score" : type);
        button.click(function () {
            if (!isLoading) {
                $(":submit").attr("disabled", true);
                button.html('Loading...').addClass('disabled');
                loadSeriesForType(highchart, url, type, true, function () {
                    isLoading = false;
                    $(":submit").attr("disabled", false);
                    button.html(buttonTxt).removeClass('disabled');
                });
            } else {
                $(":submit").attr("disabled", false);
                button.html(buttonTxt).removeClass('disabled');
            }
        });
    };
    return {
        init: function (highcharts_container_id, button_id, url, type) {
            init(highcharts_container_id, button_id, url, type);
        }
    };
}();

var VadetisHighchartsFileDownload = function () {
    var init = function (highcharts_container_id, button_id, url, type) {
        var button = $("#" + button_id), isLoading = false, highchart = $("#" + highcharts_container_id).highcharts();
        button.click(function () {
            if (!isLoading) {
                button.addClass('disabled');
                downloadDataset(highchart, url, type,function () {
                    isLoading = false;
                    button.removeClass('disabled');
                });
            } else {
                button.removeClass('disabled');
            }
        });
    };
    return {
        init: function (highcharts_container_id, button_id, url, type) {
            init(highcharts_container_id, button_id, url, type);
        }
    };
}();