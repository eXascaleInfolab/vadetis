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
        init: function (container_html_id, button_id, url) {
            initReload(container_html_id, button_id, url);
        }
    };
}();
