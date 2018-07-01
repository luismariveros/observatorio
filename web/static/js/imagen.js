$(function () {

    /* Functions */

    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-imagen .modal-content").html("");
                $("#modal-imagen").modal("show");
            },
            success: function (data) {
                $("#modal-imagen .modal-content").html(data.html_form);
            }
        });
    };

    var saveForm = function () {
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    $("#gallery tbody").html(data.html_imagen_list);
                    $("#modal-imagen").modal("hide");
                }
                else {
                    $("#modal-imagen .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    };


    /* Binding */

    //// Create book
    //$(".js-create-book").click(loadForm);
    //$("#modal-book").on("submit", ".js-book-create-form", saveForm);
    //
    //// Update book
    //$("#book-table").on("click", ".js-update-book", loadForm);
    //$("#modal-book").on("submit", ".js-book-update-form", saveForm);

    // Delete book
    $("#gallery").on("click", ".js-delete-book", loadForm);
    $("#modal-imagen").on("submit", ".js-book-delete-form", saveForm);

});


