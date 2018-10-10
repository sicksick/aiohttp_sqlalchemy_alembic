$(document).ready(function () {
    $("form#formLogin").submit(function (event) {
        event.preventDefault();

        var formData = $("#formLogin").serializeArray();
        var data = {};
        for (var i = 0; i < formData.length; i++) {
            data[formData[i].name] = formData[i].value;
        }
        $.ajax({
            url: "/api/user/login",
            type: "POST",
            data: JSON.stringify(data),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function (data) {
                localStorage.setItem('user', JSON.stringify(data.user));
                localStorage.setItem('token', data.token);
                localStorage.setItem('roles', JSON.stringify(data.roles));
                document.location.href = URL_REDIRECT_AFTER_LOGIN
                return false;
            },
            error: function () {
                $(".alert-custom-auth-warning").addClass('show').alert();
                return false;
            }
        });
    });

});