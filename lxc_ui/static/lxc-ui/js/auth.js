
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