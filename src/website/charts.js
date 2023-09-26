function pie_chart(){
    let chart = new Chart(ctx, {
        type: "pie",
        data: {
            labels: [
                "Red",
                "Pink",
                "Yellow"
            ],
            datasets: [{
                label: "dataset",
                data: [],
                backgroundColor: [
                    'rgb(255, 99, 132)',
                    'rgb(54, 162, 235)',
                    'rgb(255, 205, 86)'
                  ],
                  hoverOffset: 4
            }]
        }
    })
}