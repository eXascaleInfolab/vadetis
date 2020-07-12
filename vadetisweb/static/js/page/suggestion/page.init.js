"use strict";

var DatasetSuggestionPage = function () {

    // private
    var init = function (clear_button_id) {
        VadetisColumnHighcharts.init("highcharts_container");
        VadetisHighchartsClear.init("highcharts_container", clear_button_id, function () {

        });
    }
    return {
        // public
        init: function(clear_button_id) {
            init(clear_button_id);
        }
    };
}();