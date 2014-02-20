

function getUsernamePasswordFromLogin()
{
    var username = document.getElementById("username-field").value;
    var password = document.getElementById("password-field").value;
    login(username, password);
}

loggedInUser = loggedInAs();
if(loggedInUser == null)
{
    // not logged in show the username/password boxes
    document.getElementById('username-password-fields').style.display = "";
    document.getElementById('show-logged-in-user').style.display = "none";
}
else
{
    // logged in so show username and logout button
    document.getElementById('username-password-fields').style.display = "none";
    document.getElementById('show-logged-in-user').style.display = "";
    document.getElementById("logged-in-user-field").innerHTML = loggedInUser;
}







function login(username, password)
{
    alert("logging in as '" + username + "'")

    // store in local storage (session)
    localStorage.setItem('auth.loggedInUser', username);

}

function loggedInAs()
{
    // get from local storage (session)
    var loggedInUser = localStorage.getItem('auth.loggedInUser');
    return loggedInUser;
}

function logout()
{
    localStorage.removeItem('auth.loggedInUser');
}


