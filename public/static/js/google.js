if (GOOGLE_SIGNIN_CLIENT_ID !== "None") {

    var clicked = false;//Global Variable

    function clickGoogleLogin() {
        clicked = true;
    }

    $(document).ready(function () {
        $(".google-auth").removeClass("d-none");
    });

    function onSignIn(googleUser) {
        if (clicked) {
            $.post("/api/user/login/google", JSON.stringify({
                "token": googleUser.getAuthResponse().id_token
            }), function () {
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
    }
}