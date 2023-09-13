function get_speakerinfo(){
    $.ajax({
        url: "http://127.0.0.1:5000/get-speechesov",
        type: 'GET',
        async: true,
        dataType: "json",
        data: FormData,
        success: function (data) {
            var id = $("#search-id").val()
            var name = ""
            var party = ""
            var bday = ""
            var speech_count = 0

            for(var i=0; i < data.speeches.length; i++){
                if(id == data.speeches[i].speaker._id){
                    name = data.speeches[i].speaker.firstname + " " + data.speeches[i].speaker.lastname
                    party = data.speeches[i].speaker.party.name
                    bday = data.speeches[i].speaker.bday
                    speech_count++
                }
            }
            $("#name").append(name)
            $("#party").append(party)
            $("#bday").append(bday)
            $("#fill").append("speeches amount: " + speech_count)

        },
        failure: function(_xhr, text, error){
            console.log(text);
            console.log(error);
        }
    });
}


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



