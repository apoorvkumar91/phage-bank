$(function () {

  $(".js-create-signup").click(function () {
    $.ajax({
      url: '/signup',
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#myModal").modal("show");
      },
      success: function (data) {
        $("#myModal .modal-content").html(data.html_form);
      }
    });
  });

   $("#myModal").on("submit", ".js-user-create-form", function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          alert("User Registered Successfully!");  // <-- This is just a placeholder for now for testing
        }
        else {
          $("#myModal .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  });
});
