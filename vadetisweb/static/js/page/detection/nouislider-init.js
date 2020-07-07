"use strict";

var NoUiSliders = function() {

    var thresholdSlider = function(slider_element, value_input_selector, min, max) {

        function setValueAndUpdateRange(min, max, value) {
            updateRange(min, max);
            slider_element.noUiSlider.set(value);
        }

        function updateRange(min, max) {
            slider_element.noUiSlider.updateOptions({
                range : {
                    'min': min,
                    'max': max
                }
            });
        }

        noUiSlider.create(slider_element, {
            start: [0.5],
            connect: false,
            range: {
                'min': [min],
                'max': [max],
            },
            format: wNumb({
                decimals: 7,
            })
        });

        // slider updates text input
        slider_element.noUiSlider.on('update', function(values, handle) {
            value_input_selector.val(values[handle]);
        });

        // text input updates slider
        value_input_selector.bind('change', function(){
            // check if range has to be adapted
            var min = slider_element.noUiSlider.options.range.min;
            var max = slider_element.noUiSlider.options.range.max;
            var val = Number(this.value);
            if(this.value < min) {
                setValueAndUpdateRange(val, max, val);
            } else if (this.value > max) {
                setValueAndUpdateRange(min, val, val);
            } else {
                slider_element.noUiSlider.set(this.value);
            }
        });
    };

    return {
        //initiate the slider
        init: function(slider_element, value_input_selector, min, max) {
            thresholdSlider(slider_element, value_input_selector, min, max);
        }
    };

}();