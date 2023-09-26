function get_speakerinfo(){
    $.ajax({
        url: "http://127.0.0.1:5000/get-speakersov",
        type: 'GET',
        async: true,
        dataType: "json",
        data: FormData,
        success: function (data) {
            var id = $("#search-id").val()
            var name = ""
            var party = ""
            var bday = ""
            var url = ""
            var speech_count = ""

            for(var i=0; i < data.speakers.length; i++){
                if(id == data.speakers[i]._id){
                    name = data.speakers[i].firstname + " " + data.speakers[i].lastname
                    party = data.speakers[i].party
                    bday = data.speakers[i].bday
                    url = data.speakers[i].url
                    speech_count = data.speakers[i].speeches
                }
            }
            
            $("#name").html(name)
            $("#party").html(party)
            $("#bday").html(bday)
            $("#fill").html("speeches amount: " + speech_count)
            $("#speaker-port").attr("src", "http://www.bundestag.de" + url)

            var place = document.getElementById("pie")
            var chart = new Chart(place, {
                type:"pie",
                data: {
                    labels:["june", "tune"],
                    datasets: [{
                        label:"satz1",
                        data:[1,3],
                        backgroundColor:["blue", "purple"]
        }]
    }
})

        },
        failure: function(_xhr, text, error){
            console.log(text);
            console.log(error);
        }
    });
}






