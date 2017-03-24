var hide_lists = function(cb) {
    $('#posts').fadeOut(300); 
    $('#projects').fadeOut(300);
    $('#aboutme').fadeOut(300);
    $('#publications').fadeOut(300);
    $('#posts-btn').removeClass('disabled');
    $('#projects-btn').removeClass('disabled');
    $('#aboutme-btn').removeClass('disabled');
    $('#publications-btn').removeClass('disabled');
};

var show_projects = function() {

    if( $('#posts').is(':visible') ){
        $('#posts-btn').removeClass('disabled');
        $('#posts').fadeOut(300, function() { $('#projects').fadeIn(300); });
    } else if( $('#publications').is(':visible') ){
        $('#publications-btn').removeClass('disabled');
        $('#publications').fadeOut(300, function() { $('#projects').fadeIn(300); });
    } else if( $('#aboutme').is(':visible') ){
        $('#aboutme-btn').removeClass('disabled');
        $('#aboutme').fadeOut(300, function() { $('#projects').fadeIn(300); });
    } else{
        $('#projects').fadeIn(300);
    }
    $('#projects-btn').addClass('disabled')

};

var show_posts = function() {

    if( $('#projects').is(':visible') ){
        $('#projects-btn').removeClass('disabled');
        $('#projects').fadeOut(300, function() { $('#posts').fadeIn(300); });
    } else if( $('#publications').is(':visible') ){
        $('#publications-btn').removeClass('disabled');
        $('#publications').fadeOut(300, function() { $('#posts').fadeIn(300); });
    } else if( $('#aboutme').is(':visible') ){
        $('#aboutme-btn').removeClass('disabled');
        $('#aboutme').fadeOut(300, function() { $('#posts').fadeIn(300); });
    } else{
        $('#posts').fadeIn(300);
    }

    $('#posts-btn').addClass('disabled')

};



var show_aboutme = function() {

    if( $('#projects').is(':visible') ){
        $('#projects-btn').removeClass('disabled');
        $('#projects').fadeOut(300, function() { $('#aboutme').fadeIn(300); });
    } else if( $('#publications').is(':visible') ){
        $('#publications-btn').removeClass('disabled');
        $('#publications').fadeOut(300, function() { $('#aboutme').fadeIn(300); });
    }  else if( $('#posts').is(':visible') ){
        $('#posts-btn').removeClass('disabled');
        $('#posts').fadeOut(300, function() { $('#aboutme').fadeIn(300); });
    } else{
        $('#aboutme').fadeIn(300);
    }

    $('#aboutme-btn').addClass('disabled')

};

var show_publications = function() {

    if( $('#projects').is(':visible') ){
        $('#projects-btn').removeClass('disabled');
        $('#projects').fadeOut(300, function() { $('#publications').fadeIn(300); });
    } else if( $('#aboutme').is(':visible') ){
        $('#aboutme-btn').removeClass('disabled');
        $('#aboutme').fadeOut(300, function() { $('#publications').fadeIn(300); });
    }  else if( $('#posts').is(':visible') ){
        $('#posts-btn').removeClass('disabled');
        $('#posts').fadeOut(300, function() { $('#publications').fadeIn(300); });
    } else{
        $('#publications').fadeIn(300);
    }

    $('#publications-btn').addClass('disabled')

};



