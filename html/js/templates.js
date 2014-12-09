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
                token: $.cookie('token'),
                id: $.cookie('user_id')
            },
            dataType: 'json',
            success: function(json) { sidebarData.friends = json.friends; }
        }),
        $.ajax({
            url: '../api/trip.py',
            type: 'post',
            data: {
                action: 'list',
                user_id: $.cookie('user_id'),
                token: $.cookie('token')
            },
            dataType: 'json',
            success: function(json) { sidebarData.trips = json.trips; }
        })
    ).done(function() { build_sidebar(); });
}
