$(document).ready(function() {
    p_auth_url = p_auth_url.replace(/&amp;/g, "&")
    s_auth_url = s_auth_url.replace(/&amp;/g, "&")
    sh_auth_url = sh_auth_url.replace(/&amp;/g, "&")
    $('#plot').attr("href", p_auth_url)
    $('#sift').attr("href", s_auth_url)
    $('#shuffle').attr("href", sh_auth_url)
})
