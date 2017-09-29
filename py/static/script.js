function get_len() {
    $.ajax({
        type: "POST",
        url: "/get_len",
        data: $('form').serialize(),
        type: 'POST',
        success: function(response) {
            var json = jQuery.parseJSON(response)
            $('#len').html(json.len)
            console.log(response);
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function get_path_url(){
    $.ajax({
        type: "POST",
        url: "/get_path",
        data: $('form').serialize(),
        type: 'POST',
        success: load_path_url,
        error: function(error) {
            console.log(error);
        }
    });
}


function get_path(){
    $.ajax({
        type: "GET",
        url: "/get_path",
        data: {
            "start": {
                "lat":50.000,
                "lng":30.000
            }
        },
        type: 'GET',
        success: display_path,
        error: function(error) {
            console.log(error);
        }
    });
}


