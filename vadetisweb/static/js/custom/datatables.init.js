"use strict";
var VadetisDatatables = function () {

    var initTable = function (html_id, url) {
        var table = $('#' + html_id);

        $.ajax({
            url: url,
            type: "GET",
            success: function (data) {
                var columns = [];
                if (data !== undefined && data.data !== undefined && data.data.length > 0) {
                    var columnNames = Object.keys(data.data[0]);
                    for (var i in columnNames) {
                        columns.push({
                            data: columnNames[i],
                            title: columnNames[i].replace('_', ' ')
                        });
                    }
                } else {
                    // dummy header if no data available
                    columns = [{title: '', data: null}];
                }

                var datatable = table.DataTable({

                    // Internationalisation. For more info refer to http://datatables.net/manual/i18n
                    language: {
                        "aria": {
                            "sortAscending": ": activate to sort column ascending",
                            "sortDescending": ": activate to sort column descending"
                        },
                        "emptyTable": "No data available",
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
                            //console.log('callback');
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

                    // DOM Layout
                    dom: `<'row'<'col-sm-12'tr>>
                    <'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7 dataTables_pager'lp>>`,

                    fnInitComplete: function(oSettings) {
                        if(table.DataTable().data().count() === 0)
                            $('#' + html_id + ' thead').remove();
                    }
                });

                table.on('change', 'tbody tr .kt-checkbox', function() {
                    $(this).parents('tr').toggleClass('active');
                });
            },
            error: function (data, status, xhr) {
                console.error("Loading datatable data failed: " + xhr.responseText);
            }
        });
    };
    return {
        init: function (html_id, url) {
            initTable(html_id, url);
        }
    };
}();
