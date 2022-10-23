$(document).ready(function () {
    $socket.send("api:join", {room: $("#sk").val(), private: 1})

    $(".messager-btn").on('click', function (e) {
        $(this).hide()
        $('.messager-window').show();
    });

    $("#messager-close").on('click', function (e) {
        $('.messager-window').hide()
        $('.messager-btn').show();
    });

	$("#messager-form").on('submit', function (event) {
        event.preventDefault();
		let text = $("#message-text").val()
		$socket.send("api:message_new", {text: text})
	  
  	});

      $socket.connection.on('api:message_history', function(msg) {
		if (!msg.status) return
        $("#messager-chat").html($(msg.items[0]))
	});

	$socket.connection.on('api:message_new', function(msg) {
		if (!msg.status) return
        $("#messager-chat").append($(msg.items[0]))
	});
});