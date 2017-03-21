var hide_lists = function(cb) {
    $('#posts').fadeOut(300);
    $('#projects').fadeOut(300);
    $('#aboutme').fadeOut(300);
    $('#posts-btn').removeClass('disabled');
    $('#projects-btn').removeClass('disabled')
    $('#aboutme-btn').removeClass('disabled')
};
var show_projects = function() {
    $('#posts-btn').removeClass('disabled');
    $('#aboutme-btn').removeClass('disabled');
    $('#posts').fadeOut(300, function() {
        $('#projects').fadeIn(300)
    });
    $('#aboutme').fadeOut(300, function() {
        $('#projects').fadeIn(300)
    });
    $('#projects-btn').addClass('disabled')
};
var show_posts = function() {
    $('#projects-btn').removeClass('disabled');
    $('#aboutme-btn').removeClass('disabled');
    $('#projects').fadeOut(function() {
        $('#posts').fadeIn(300)
    });
    $('#aboutme').fadeOut(function() {
        $('#posts').fadeIn(300)
    });
    $('#posts-btn').addClass('disabled')
};
var show_aboutme = function() {
    $('#posts-btn').removeClass('disabled');
    $('#projects-btn').removeClass('disabled');
    $('#posts').fadeOut(300, function() {
        $('#aboutme').fadeIn(300)
    });
    $('#projects').fadeOut(300, function() {
        $('#aboutme').fadeIn(300)
    });
    $('#aboutme-btn').addClass('disabled')
};
