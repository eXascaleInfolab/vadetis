var ComponentsMiniColors = function() {
    var handleMiniColors = function() {
        $('.minicolors-input').each(function() {
            $(this).minicolors({
                change: function(hex, opacity) {
                    if (!hex) return;
                    if (opacity) hex += ', ' + opacity;
                    if (typeof console === 'object') {
                        console.log(hex);
                    }
                },
                theme: 'bootstrap'
            });

        });
    }
    return {
        //main function to initiate the module
        init: function() {
            handleMiniColors();
        }
    };

}();

jQuery(document).ready(function() {
   ComponentsMiniColors.init();
});