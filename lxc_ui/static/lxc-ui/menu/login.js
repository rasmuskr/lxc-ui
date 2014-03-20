function getUsernamePasswordFromLogin() {
    var username = document.getElementById("username-field").value;
    var password = document.getElementById("password-field").value;
    login(username, password);
}

loggedInUser = loggedInAs();
if (loggedInUser == null) {
    // not logged in show the username/password boxes
    document.getElementById('username-password-fields').style.display = "";
    document.getElementById('show-logged-in-user').style.display = "none";
}
else {
    // logged in so show username and logout button
    document.getElementById('username-password-fields').style.display = "none";
    document.getElementById('show-logged-in-user').style.display = "";
    document.getElementById("logged-in-user-field").innerHTML = loggedInUser;
}


function login(username, password) {
    var post_data = {
        "username": username,
        "password": password
    };
    $.ajax({
        type: 'POST',
        url: "/users/login/",
        data: post_data,
        success: loggedInSuccess,
        dataType: "application/json",
        async: false
    });

}


function loggedInSuccess(data) {
    alert(data);
    // store in local storage (session)
    localStorage.setItem('auth.loggedInUser', username);
}


function loggedInAs() {
    // get from local storage (session)
    return localStorage.getItem('auth.loggedInUser');
}

function logout() {
    localStorage.removeItem('auth.loggedInUser');
}


