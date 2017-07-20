/**
* Created by charlyjazz on 20/07/17.
*/


var App =  (function () {

    var socket = io.connect('http://' + document.domain + ':' + location.port);

    socket.on('connect', function() {
        socket.emit('connected');
        console.log('connected')
    });

    socket.on('new_notification', function(data) {
        window.alert(data);
    });

    return {

        form_comment_snippet: function (id_snippet) {
            $('#form_comment_snippet').submit(function (event) {
                event.preventDefault();
                text = $("#form_comment_snippet input.comment-area").val();
                $.ajax({
                      type: "POST",
                      url: `/snippets/${id_snippet}/comment`,
                      contentType: 'application/json;charset=UTF-8',
                      data: JSON.stringify({
                          comment_text: text
                      }),
                      success: function(response){
                          if (response.create == true && response.socketNotification == true){
                            socket.emit('send_notification', {
                                notification: response.notification,
                                sid: response.sid
                            });
                          }
                      }
                });
            });
        }

    }

}());