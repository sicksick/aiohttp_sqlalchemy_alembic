function onSignIn(googleUser) {

    var id_token = googleUser.getAuthResponse().id_token;

    if (id_token) {
        var profile = googleUser.getBasicProfile();
        var jqxhr = $.post("/api/user/login/google", {
            "token": id_token
        }, function () {
        }, "json")
            .done(function (data) {
                localStorage.setItem('user', JSON.stringify(data.user));
                localStorage.setItem('token', data.token);
                localStorage.setItem('roles', JSON.stringify(data.roles));
                document.location.href = URL_REDIRECT_AFTER_LOGIN
            })
            .fail(function () {
                $(".alert-google-warning").addClass('show').alert();
            });
    }
};