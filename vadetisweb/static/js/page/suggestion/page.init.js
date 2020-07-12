"use strict";

var DatasetSuggestionPage = function () {

    // private
    var init = function (url) {
        VadetisColumnHighcharts.init("highcharts_container");
    }
    return {
        // public
        init: function(url) {
            init(url);
        }
    };
}();