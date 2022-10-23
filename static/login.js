$(document).ready(function () {

	$("#login-form").on('submit', function (event) {

		let form = $(this);
		let json = convertFormToJSON(form);

		console.log(json)
		event.preventDefault();
		$socket.send("api:login", {data: json})
	
	  
  	});

	$socket.connection.on('api:login', function(msg) {
		if (!msg.status) {alert(msg.items[0]); return}

		Cookies.set("token", msg.items[0].token)
		Cookies.set("ref_token", msg.items[0].ref_token, { expires: msg.items[0].ref_token.exp })

		location.href = msg.items[0].next
	});
});