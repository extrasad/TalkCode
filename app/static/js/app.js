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
        data = JSON.parse(data);
        $('.flash-notification').removeClass("hidden").show().delay(4500).fadeOut();
        $('#anchor-notification').attr('href', data.url);
        $('#text-notification').text(data.text + '!');
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
        },

        form_answer_question: function (id_question) {
            $('#form_answer_question').submit(function (event) {
                event.preventDefault();
                answer_text = $("#form_answer_question textarea.answer-area").val();
                answer_code = $("#form_answer_question textarea.TextArea").val();
                $.ajax({
                      type: "POST",
                      url: `/question/${id_question}/answer`,
                      contentType: 'application/json;charset=UTF-8',
                      data: JSON.stringify({
                          answer_text: answer_text,
                          answer_code: answer_code
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