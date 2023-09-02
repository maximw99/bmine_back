function test(){
    $.ajax({
        url: "http://127.0.0.1:5000/get-speaker",
        type: 'GET',
        async: true,
        dataType: "json",
        data: FormData,
        success: function (data) {
            console.log(data.firstname)
            $("#test").append(data.firstname + " " + data.lastname)

        },
        failure: function(_xhr, text, error){
            console.log(text);
            console.log(error);
        }
    });
}
