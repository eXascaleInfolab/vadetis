"use strict";

var VadetisDatatables = function () {

    var initTable = function (html_id, url) {
        var table = $(html_id);

        $.ajax({
            url: url,
            type: "GET",
            success: function (data) {
                var columns = [];
                var columnNames = Object.keys(data.data[0]);
                for (var i in columnNames) {
                    columns.push({
                        data: columnNames[i],
                        title: capitalizeFirstLetter(columnNames[i])
                    });
                }
                $.fn.dataTableExt.oStdClasses.sWrapper = "kt-datatable kt-datatable--default kt-datatable--brand kt-datatable--loaded";
                //$.fn.dataTableExt.oStdClasses.sPaging = "kt-datatable__pager kt-datatable--paging-loaded";
                $.fn.dataTableExt.oStdClasses.sInfo = "kt-datatable__pager-detail";

                var datatable = table.DataTable({

                    // Internationalisation. For more info refer to http://datatables.net/manual/i18n
                    language: {
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

                    headerCallback: function (thead, data, start, end, display) {
                        $(thead).find('th').addClass('kt-datatable__cell kt-datatable__cell--sort');
                    },
                    createdRow: function (row, data, dataIndex) {
                        if (dataIndex > 0 && dataIndex % 2 == 0) {
                            $(row).addClass('kt-datatable__row kt-datatable__row--even');
                        } else {
                            $(row).addClass('kt-datatable__row kt-datatable__row--odd');
                        }
                    },
                    rowCallback: function (row, data) {
                        $('td', row).addClass('kt-datatable__cell');
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

                    order: [
                        [0, 'asc']
                    ],

                    searching: true,

                    lengthMenu: [
                        [10, 20, 30, 40, -1],
                        [10, 20, 30, 40, "All"] // change per page values here
                    ],

                    // set the initial value
                    pageLength: 20,

                    data: data.data,
                    columns: columns,
                    rowId: 'id',

                    dom: 't' +
                         '<"kt-datatable__pager kt-datatable--paging-loaded"li <"kt-datatable__pager-nav"p>>'
                });

                $(datatable.table().header()).addClass('kt-datatable__head');
                $(datatable.table().header()).find('tr').addClass('kt-datatable__row');

                $(datatable.table().body()).addClass('kt-datatable__body');
            },
            error: function (data, status, xhr) {
                console.error("Loading datatable data failed: " + xhr.responseText);
            }
        });
    };
    return {
        init: function (html_id, url) {
            initTable('#' + html_id, url);
        }
    };
}();
