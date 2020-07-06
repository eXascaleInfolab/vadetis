var DatasetDisplayPage = function () {

    // private
    var init = function (dataset_json_url, dataset_download_file_url, selected_button) {
        VadetisHighcharts.init("highcharts_container", dataset_json_url, selected_button);

        VadetisHighchartsLoad.init("highcharts_container", "raw_btn", dataset_json_url, "raw", function () {});
        VadetisHighchartsLoad.init("highcharts_container", "zscore_btn", dataset_json_url, "zscore", function () {});

        VadetisHighchartsFileDownload.init("highcharts_container", "download_csv", dataset_download_file_url, "csv");
        VadetisHighchartsFileDownload.init("highcharts_container", "download_json", dataset_download_file_url, "json");

        switchColorLegend(false);
    }
    return {
        // public
        init: function(dataset_json_url, dataset_download_file_url, selected_button) {
            init(dataset_json_url, dataset_download_file_url, selected_button);
        }
    };
}();