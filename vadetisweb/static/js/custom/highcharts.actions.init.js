"use strict";

var VadetisHighchartsReset = function () {

    var init = function (highcharts_container_id, button_id, url) {
        var button = $("#" + button_id), isLoading = false, highchart = $("#" + highcharts_container_id).highcharts();

        button.click(function () {
            if (!isLoading) {
                button.html('Loading...').addClass('disabled');
                loadSeriesForType(highchart, url, "raw", true, function () {
                    isLoading = false;
                    button.html('Reset').removeClass('disabled');
                    // TODO better hiding
                    $('#threshold_portlet').hide();
                    $('#scores_portlet').hide();
                    $('#cnf_portlet').hide();
                    $('#plot_portlet').hide();
                });
            } else {
                button.html('Reset').removeClass('disabled');
                $('#threshold_portlet').hide();
                $('#scores_portlet').hide();
                $('#cnf_portlet').hide();
                $('#plot_portlet').hide();
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
                button.html('Loading...').addClass('disabled');

                loadSeriesForType(highchart, url, type, true, function () {
                    isLoading = false;
                    button.html(buttonTxt).removeClass('disabled');
                });
            } else {
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