$(document).ready(function () {

	$("#register-form").on('submit', function (event) {

        event.preventDefault();

		let form = $(this);
		let json = convertFormToJSON(form);
        json.role = $("#role").val()

		alert(json.toString())
		$socket.send("api:register", {data: json})
	
        $socket.connection.on('api:register', function(msg) {
            if (!msg.status) {alert(msg.item[0]); return}
    
            location.href = msg.items[0].next
        });
  	});
      $("#role").change(function (e) {
        console.log($(this).val() != "Студент")
        if ($(this).val() != "Студент") {
            $(".for_student").hide()
        } else {
            $(".for_student").show()
        }
    });
});