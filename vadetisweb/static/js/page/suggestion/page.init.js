"use strict";

var DatasetSuggestionPage = function () {

    // private
    var init = function (url, is_spatial) {
        VadetisColumnHighcharts.init("highcharts_container", url, is_spatial);
    }
    return {
        // public
        init: function(url, is_spatial) {
            init(url, is_spatial);
        }
    };
}();