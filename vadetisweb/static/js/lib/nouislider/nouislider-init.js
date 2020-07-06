var NoUiSliders = function() {

    var thresholdSlider = function(slider_element, value_input_selector) {

        function updateRange(min, max, value) {
            slider_element.noUiSlider.updateOptions({
                range : {
                    'min': min,
                    'max': max
                }
            });
            slider_element.noUiSlider.set(value);
        }

        noUiSlider.create(slider_element, {
            start: [0],
            connect: false,
            range: {
                'min': [0],
                'max': [1],
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
                updateRange(val, max, val);
            } else if (this.value > max) {
                updateRange(min, val, val);
            } else {
                slider_element.noUiSlider.set(this.value);
            }
        });
    };

    return {
        //initiate the slider
        init: function(slider_element, value_input_selector) {
            thresholdSlider(slider_element, value_input_selector);
        }
    };

}();