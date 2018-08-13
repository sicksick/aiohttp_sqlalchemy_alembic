// This is called with the results from from FB.getLoginStatus().
function statusChangeCallback(response) {
    if (response.status === 'connected') {
        var jqxhr = $.post("/api/user/login/facebook", {
            "status": response.status,
            "token": response.authResponse.accessToken
        }, function () {})
            .done(function (data) {
                localStorage.setItem('user', JSON.stringify(data.user));
                localStorage.setItem('token', data.token);
                localStorage.setItem('roles', JSON.stringify(data.roles));
                $(".alert-facebook-success").addClass('show').alert();
                document.location.href = URL_REDIRECT_AFTER_LOGIN
            })
            .fail(function () {
                $(".alert-facebook-warning").addClass('show').alert();
            });
    }
}

function checkLoginState() {
    FB.getLoginStatus(function (response) {
        statusChangeCallback(response);
    });
}

window.fbAsyncInit = function () {
    FB.init({
        appId: FACEBOOK_ID,
        cookie: true,  // enable cookies to allow the server to access
                       // the session
        xfbml: true,  // parse social plugins on this page
        version: 'v2.8' // use graph api version 2.8
    });

    FB.getLoginStatus(function (response) {
        statusChangeCallback(response);
    });
};

// Load the SDK asynchronously
(function (d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s);
    js.id = id;
    js.src = "https://connect.facebook.net/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));
