$(function () {
	
	$socket.connection.on('api:admin_get_tab', function(msg) {
			if (!msg.status) return

			msg.items.forEach((item, index) => {
				$("#menu-body").html(item)
			});
		});
	
	$socket.connection.on('api:admin_get_add_window', function(msg) {
			if (!msg.status) return

			msg.items.forEach((item, index) => {
				w = $(".window");

				if(!w.length) {
					$("body").append($(item));
					return
				};

				w.html($(item).html())
			});
		});
	
	$socket.connection.on('api:message_new', function(msg) {
		if (!msg.status) return
		$("#rektor-dialog-body").append($(msg.items[0]))
	});

	$socket.connection.on('api:admin_open_rektor_dialog', function(msg) {
		if (!msg.status) return

		msg.items.forEach((item, index) => {
			$("#menu-body").html($(item))
		});

		$socket.send("api:join", {room: $("#rektor-dialog-window").attr("name"), private: 1})
	});
		
	$("body").on("click", ".menu-tab", function () {
		action = $(this).attr("name");
		$(".menu-title").text($(this).text())
		
		$socket.send("api:admin_get_tab", {action: action})
	});
	
	$("body").on("click", ".admin-tab-add", function () {
		action = $(this).attr("id");
		
		$socket.send("api:admin_get_add_window", {action: action})
	});

	$("body").on("click", ".admin-tab-remove", function () {
		action = $(this).attr("id")
		
		$socket.send("api:admin_remove", {action: action})
	});

	
	$("body").on("click", ".rektor-dialog", function () {
		user_id = $(this).attr("name")
		$(".menu-title").text("Диалог с" + $(this).find(".dialog-header").find(".dialog-user").text())
		
		$socket.send("api:admin_open_rektor_dialog", {user_id: user_id})
	});

	$("body").on("submit", "#messager-form", function (e) {
		e.preventDefault();

		let user_id = $("#messager-form").attr("name");
		let text = $("#message-text").val()
		$("#message-text").val("")


		$socket.send("api:message_new", {text: text, to: user_id})
	});
	
	$("body").on("submit", "#admin-add-form", function (e) {
		action = $(this).attr("name");
		
		let formData;

		switch(action) {
			case("users"):
				formData = {
					email: $("#email").val(),
					password: $("#password").val(),
					username: $("#username").val(),
					last_name: $("#last_name").val(),
					first_name: $("#first_name").val(),
					role: $("#role").val(),
				};
				break;
			case("news"):
				formData = {
					label: $("#label").val(),
					text: $("#text").val(),
					user_id: $("#user_id").val(),
					type: $("#field-type").val()
				};
				break;
			case("rasp"):
				formData = new FormData();
				formData.append('file', $('#file')[0].files[0]);
				formData.append('action', 'shleude')
				formData.append('type', $('#rasp-type').val())

				$.ajax({
					   url : 'api/upload',
					   type : 'POST',
					   data : formData,
					   processData: false,  // tell jQuery not to process the data
					   contentType: false,  // tell jQuery not to set contentType
					   success : function(data) {
						   $socket.send("api:admin_get_tab", {action: action})
					   }
				});
				e.preventDefault();
				return
		}
		  
		$socket.send("api:admin_add", {action: action, formData: formData})
		$('.window').remove()
		e.preventDefault();
	});
	
  });
