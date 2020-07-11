"use strict";

var DatasetSuggestionPage = function () {

    // private
    var init = function (url) {
        VadetisColumnHighcharts.init("highcharts_container", url);
    }
    return {
        // public
        init: function(url) {
            init(url);
        }
    };
}();