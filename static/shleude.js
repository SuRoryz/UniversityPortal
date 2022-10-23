$(document).ready(function () {

	$("#shleude-form").on('submit', function (event) {
        event.preventDefault();
		let id = $("#group_id").val()
        let type = "student"

        if ($(this).hasClass("teacher")) {
            type = "teacher"
        }
		
		$socket.send("api:draw_shleude", {group_id: id, type: type})
	  
  	});

	$socket.connection.on('api:draw_shleude', function(msg) {
		if (!msg.status) return
        $(".shleude-content").html($(msg.items[0]))
        $(".shleude-content").css('display', 'flex')
	});
});