var loc = window.location;

var token =  $('#user_token').val();

var wsStart = 'ws://';

if (loc.protocol == 'https:') {
    wsStart = 'wss://';
};

var endpoint = wsStart + loc.host + loc.pathname + '?token=' + token;

var socket = new WebSocket(endpoint);


socket.onmessage = function (event) {

     var data = JSON.parse(event.data);
     var message = data['message'];
     if (message === "reload") {
        location.reload();
     };


    var newMessage = JSON.parse(event.data);

    $('#messages').append('<hr><p>' + newMessage.body + '</p><small>' + newMessage.author + '</small><br><small>' +
        newMessage.created_on + '</small>');

};


socket.onopen = function (event) {


    $(document).ready(function () {

        var form = $('#message_add_form');

        form.submit(function (event) {

            event.preventDefault();
            var body = $('#comment_body').val();
            var adSlug = $('#hidden_input').attr('data-post');
            var authorId = $('#hidden_input').val();
            $('#comment_body').val(null);
            data = {
                'body': body,
                'ad_slug': adSlug,
                'author_id': authorId,
            };
            socket.send(JSON.stringify(data));

        });

    });


};

