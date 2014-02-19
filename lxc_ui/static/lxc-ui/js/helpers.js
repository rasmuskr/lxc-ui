

// nice helper function from stack overflow http://stackoverflow.com/questions/11582512/how-to-get-url-parameters-with-javascript
function getURLParameter(name)
{
    return decodeURIComponent((new RegExp('[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)').exec(location.search)||[,""])[1].replace(/\+/g, '%20'))||null
}


function getCurrentPageName()
{
    var contentFile = getURLParameter("page");
    if(contentFile == null)
    {
        contentFile = 'home';
    }
    // here we keep a list of valid entries
    if(['home', 'admin'].indexOf(contentFile) >= 0)
    {
        return contentFile;
    }
    return 'home';
}