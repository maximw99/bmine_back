function test(){
    $.ajax({
        url: "http://127.0.0.1:5000/get-speakerov",
        type: 'GET',
        async: true,
        dataType: "json",
        data: FormData,
        success: function (data) {
            var id = $("#search-id").val()
            console.log(data.speakers[3]._id + " " + data.speakers[3].lastname)

            for(var i=0; i < data.speakers.length; i++){
                console.log("dummy")
                if(id == data.speakers[i]._id){
                    $("#name").append(data.speakers[i].firstname + " " + data.speakers[i].lastname)
                    $("#party").append(data.speakers[i].party.name)
                    $("#bday").append(data.speakers[i].bday)
                    $("#fill").append(data.speakers[i].jobs)
                    break;
                }
            }

        },
        failure: function(_xhr, text, error){
            console.log(text);
            console.log(error);
        }
        
    });
    
}
