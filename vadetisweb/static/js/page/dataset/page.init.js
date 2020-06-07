var DatasetPage = function () {

    // private
    var init = function (dataset_json_url, dataset_download_file_url, selected_button) {
        VadetisHighcharts.init("highcharts_container", dataset_json_url, selected_button);

        VadetisHighchartsLoad.init("highcharts_container", "raw_btn", dataset_json_url, "raw");
        VadetisHighchartsLoad.init("highcharts_container", "zscore_btn", dataset_json_url, "zscore");
        VadetisHighchartsReset.init("highcharts_container", "reset_chart_btn", dataset_json_url);

        VadetisHighchartsFileDownload.init("highcharts_container", "download_csv", dataset_download_file_url, "csv");
        VadetisHighchartsFileDownload.init("highcharts_container", "download_json", dataset_download_file_url, "json");

        // color settings
        $('#true_positive_btn').css({"background-color": getSetting('color_true_positive')});
        $('#false_positive_btn').css({"background-color": getSetting('color_false_positive')});
        $('#false_negative_btn').css({"background-color": getSetting('color_false_negative')});
    }
    return {
        // public
        init: function(dataset_json_url, dataset_download_file_url, selected_button) {
            init(dataset_json_url, dataset_download_file_url, selected_button);
        }
    };
}();