var pageData = {}
var sidebarData = {}

function build_page() {
    $('body').html(Handlebars.templates['page.tmpl'](pageData));
}

function build_sidebar() {
    pageData.page_sidebar = Handlebars.templates['sidebar.tmpl'](sidebarData);
    build_page();
}

function load_sidebar() {
    $.when(
        $.ajax({
            url: '../api/user.py',
            type: 'post',
            data: {
                action: 'get_friends',
                user_id: $.cookie('user_id'),
                token: $.cookie('token')
            },
            dataType: 'json',
            success: function(json) { sidebarData.friends = json.friends; }
        })
    ).done(function() { build_sidebar(); });
}
