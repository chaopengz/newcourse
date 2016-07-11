$('#chat-form').on('submit', function (event) {
    event.preventDefault();

    $.ajax({
        url: '/chatpost/',
        type: 'POST',
        data: {msgbox: $('#chat-msg').val()},

        success: function (json) {
            $('#chat-msg').val('');
            $('#msg-list').append('<div class="item"><img src="http://wy.chaopengz.com/newcourse/dist/img/user4-128x128.jpg" alt="user image" class="online"><p class="message"><a href="#" class="name"><small class="text-muted pull-right"><i class="fa fa-clock-o"></i>' + 'time' + '</small>' + json.user + '</a>' + json.msg + '</p></div>');

            var chatlist = document.getElementById('msg-list-div');
            chatlist.scrollTop = chatlist.scrollHeight;
        }
    });
});

function getMessages() {
    if (!scrolling) {
        $.get('/messages/', function (messages) {
            $('#msg-list').html(messages);
            var chatlist = document.getElementById('msg-list-div');
            chatlist.scrollTop = chatlist.scrollHeight;
        });
    }
    scrolling = false;
}

var scrolling = false;
$(function () {
    $('#msg-list-div').on('scroll', function () {
        scrolling = true;
    });
    refreshTimer = setInterval(getMessages, 5000);
});

$(document).ready(function () {
    $('#send').attr('disabled', 'disabled');
    $('#chat-msg').keyup(function () {
        if ($(this).val() != '') {
            $('#send').removeAttr('disabled');
        }
        else {
            $('#send').attr('disabled', 'disabled');
        }
    });
});

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});