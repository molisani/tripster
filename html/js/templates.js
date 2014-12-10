var pageData = {}
var sidebarData = {}

function build_page() {
    $('body').html(Handlebars.templates['page.tmpl'](pageData));
}

function build_sidebar() {
    pageData.page_sidebar = Handlebars.templates['sidebar.tmpl'](sidebarData);
    build_page();
}

function display_error(err) {
    console.log(err);
    $('body').append(Handlebars.templates['result-modal.tmpl'](err));
    $.cookie('username', '', {expires: -1});
    $.cookie('user_id', '', {expires: -1});
    $.cookie('token', '', {expires: -1});
    $('#result-modal').modal({show: true, keyboard: true});
}

function load_sidebar() {
    var err = null;
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
            success: function(json) { 
                if (json.status == "Success") {
                    sidebarData.friends = json.friends;
                } else {
                    err = json;
                }
            }
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
            success: function(json) { 
                if (json.status == "Success") {
                    sidebarData.trips = json.trips; 
                } else {
                    err = json;
                }
            }
        })
    ).done(function() { 
        if (err != null) {
            display_error(err);
        } else build_sidebar();
    });
}
