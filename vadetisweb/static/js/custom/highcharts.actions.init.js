"use strict";

var VadetisHighchartsReload = function () {

    var init = function (highcharts_container_id, button_id, url) {
        var button = $("#" + button_id), isLoading = false, highchart = $("#" + highcharts_container_id).highcharts();

        button.click(function () {
            if (!isLoading) {
                button.html('Loading...').addClass('disabled');
                loadSeriesForType(highchart, url, "raw", true, function () {
                    isLoading = false;
                    button.html('Reload').removeClass('disabled');
                    // TODO better hiding
                    $('#threshold_portlet').hide();
                    $('#scores_portlet').hide();
                    $('#cnf_portlet').hide();
                    $('#plot_portlet').hide();
                });
            } else {
                button.html('Reload').removeClass('disabled');
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

var VadetisHighchartsZScore = function () {
    var init = function (highcharts_container_id, button_id, url) {
        var button = $("#" + button_id), isLoading = false, highchart = $("#" + highcharts_container_id).highcharts();

        button.click(function () {
            if (!isLoading) {
                button.html('Loading...').addClass('disabled');

                updateSeriesForType(highchart, url, "zscore", true, function () {
                    isLoading = false;
                    button.html('Z-Score').removeClass('disabled');
                });
            } else {
                button.html('Z-Score').removeClass('disabled');
            }
        });
    };
    return {
        init: function (highcharts_container_id, button_id, url) {
            init(highcharts_container_id, button_id, url);
        }
    };
}();

var VadetisHighchartsRaw = function () {
    var init = function (highcharts_container_id, button_id, url) {
        var button = $("#" + button_id), isLoading = false, highchart = $("#" + highcharts_container_id).highcharts();

        button.click(function () {
            if (!isLoading) {
                button.html('Loading...').addClass('disabled');

                updateSeriesForType(highchart, url, "raw", true, function () {
                    isLoading = false;
                    button.html('Raw').removeClass('disabled');
                });
            } else {
                button.html('Raw').removeClass('disabled');
            }
        });
    };
    return {
        init: function (highcharts_container_id, button_id, url) {
            init(highcharts_container_id, button_id, url);
        }
    };
}();