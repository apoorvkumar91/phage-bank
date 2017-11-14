$(function () {

  $(".js-create-login").click(function () {
    $.ajax({
      url: '/mylogin',
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#myModalLogin").modal("show");
      },
      success: function (data) {
        $("#myModalLogin .modal-content").html(data.html_form);
      }
    });
  });

   $("#myModalLogin").on("submit", ".js-user-login-form", function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          alert("User Logged in Successfully!");  // <-- This is just a placeholder for now for testing
        }
        else {
          $("#myModalLogin .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  });
});
