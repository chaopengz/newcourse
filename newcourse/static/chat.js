$('#chat-form').on('submit', function (event) {
    event.preventDefault();

    $.ajax({
        url: '/chatpost/',
        type: 'POST',
        data: {msgbox: $('#chat-msg').val()},

        success: function (json) {
            $('#chat-msg').val('');
            $('#msg-list').append('<div class="direct-chat-msg right"><div class="direct-chat-info clearfix"><span class="direct-chat-name pull-right">' + json.user + '</span><span class="direct-chat-timestamp pull-right">' + json.time + '</span></div><img class="direct-chat-img" src="' + json.pic + '"alt="Message User Image"> <div class="direct-chat-text  pull-right">' + json.msg + '</div></div>');

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
    refreshTimer = setInterval(getMessages, 500);
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