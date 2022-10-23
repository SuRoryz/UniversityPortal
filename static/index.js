$(document).ready(function () {
    if ($("#isemploy").attr("name") == "false") {
        $socket.send("api:join", {room: "index"})
    } else {
        $socket.send("api:join", {room: "for_employ"})
    }

    $socket.connection.on('api:update_index', function(msg) {
        if (!msg.status) return
        
        console.log(msg.items)
        switch(msg.items[0].action) {
            case(1):
                $(".app-main").append($(msg.items[0].post))
                break;
            case(2):
                post = $(msg.items[0].post)
                $(`#${post.attr("id")}`).html(post.html())
                break;
            case(0):
                $(`#post-${msg.items[0].post}`).remove()
                break;
        }
    });

    $(window).on('hashchange', function(e){
        $socket.send("api:leave", {room: "index"})
    });
});