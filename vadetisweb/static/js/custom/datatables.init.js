"use strict";

var VadetisDatatables = function () {

    var initTable = function (html_id, url) {
        var table = $(html_id);

        $.ajax({
            url: url,
            type: "GET",
            success: function (result) {

                var oTable = table.DataTable({

                    // Internationalisation. For more info refer to http://datatables.net/manual/i18n
                    "language": {
                        "aria": {
                            "sortAscending": ": activate to sort column ascending",
                            "sortDescending": ": activate to sort column descending"
                        },
                        "emptyTable": "No data available in table",
                        "info": "_START_ to _END_ of _TOTAL_ entries",
                        "infoEmpty": "No entries found",
                        "infoFiltered": "(filtered1 from _MAX_ total entries)",
                        "lengthMenu": "_MENU_ entries",
                        "search": "Search:",
                        "zeroRecords": "No matching records found",
                        "loadingRecords": "Please wait - loading..."
                    },

                    // setup responsive extension: http://datatables.net/extensions/responsive/
                    responsive: true,

                    buttons: [],

                    // setup colreorder extension: http://datatables.net/extensions/colreorder/
                    colReorder: {
                        reorderCallback: function () {
                            console.log('callback');
                        }
                    },

                    "order": [
                        [0, 'asc']
                    ],

                    searching: true,

                    "lengthMenu": [
                        [10, 20, 30, 40, -1],
                        [10, 20, 30, 40, "All"] // change per page values here
                    ],

                    // set the initial value
                    "pageLength": 20,

                    data: result.data,
                    columns: result.cols,
                    rowId: 'id',

                    "dom": "<'row' <'col-md-12'B>><'row'<'col-md-6 col-sm-12'l><'col-md-6 col-sm-12'f>r><'table-scrollable't><'row'<'col-md-5 col-sm-12'i><'col-md-7 col-sm-12'p>>",
                });
            }
        });
    };

    return {
        init: function (html_id, url) {
            console.log("datatable init");
            initTable('#'+html_id, url);
        }
    };
}();