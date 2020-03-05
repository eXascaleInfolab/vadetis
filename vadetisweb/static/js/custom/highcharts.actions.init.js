"use strict";

var VadetisHighchartsActionsReload = function () {
    var initReload = function (container_html_id, button_id, url) {
        var button = $("#" + button_id), isLoading = false, highchart = $("#" + container_html_id).highcharts();

        button.click(function () {
            if (!isLoading) {
                button.html('Loading...').addClass('disabled');
                loadSeriesForType(highchart, url, "raw", true, function () {
                    isLoading = false;
                    button.html('Reload').removeClass('disabled');
                });
            } else {
                button.html('Reload').removeClass('disabled');
            }
        });
    };
    return {
        init: function (container_html_id, button_id, url) {
            initReload(container_html_id, button_id, url);
        }
    };
}();
