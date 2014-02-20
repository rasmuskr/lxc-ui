
function getCurrentAdminSubPageName()
{
    var contentFile = getURLParameter("admin_page");
    if(contentFile == null)
    {
        contentFile = 'groups';
    }
    // here we keep a list of valid entries
    if(['groups', 'users'].indexOf(contentFile) >= 0)
    {
        return contentFile;
    }
    return 'groups';
}