function readTextFile(file, callback) {
    var rawFile = new XMLHttpRequest();
    rawFile.overrideMimeType("application/json");
    rawFile.open("GET", file, true);
    rawFile.onreadystatechange = function() {
        if (rawFile.readyState === 4 && rawFile.status == "200") {
            callback(rawFile.responseText);
        }
    }
    rawFile.send(null);
}

readTextFile("./capture.json", function(text){
    var data = JSON.parse(text);
    var l = data.length-1;
    var filename = data[l].filename;
    var date = new Date(data[l].timestamp);
    var ip = data[l].ip;
    var leisure_voltage = data[l].voltages.voltage1;
    var engine_voltage = data[l].voltages.voltage2;
    var latitude = data[l].position.latitude;
    var longitude = data[l].position.longitude;
    var tilt = data[l].x;
    var ip = data[l].ip;

    window.chartColors = {
        red: 'rgb(255, 99, 132)',
        orange: 'rgb(255, 159, 64)',
        yellow: 'rgb(255, 205, 86)',
        green: 'rgb(75, 192, 192)',
        blue: 'rgb(54, 162, 235)',
        purple: 'rgb(153, 102, 255)',
        grey: 'rgb(201, 203, 207)'
    };

    var batteryVoltageChartConfig = {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Engine battery',
                backgroundColor: window.chartColors.red,
                borderColor: window.chartColors.red,
                data: [                        
                ],
                fill: false,
            }, {
                label: 'Leisure battery',
                fill: false,
                backgroundColor: window.chartColors.blue,
                borderColor: window.chartColors.blue,
                data: [
                ],
            }]
        },
        options: {
            responsive: true,
            title: {
                display: true,
                text: 'Battery Voltages'
            },
            tooltips: {
                mode: 'index',
                intersect: false,
            },
            hover: {
                mode: 'nearest',
                intersect: true
            },
            scales: {
                xAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Hour'
                    }
                }],
                yAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Voltage'
                    }
                }]
            }
        }
    };

    var tiltAngleChartConfig = {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Tilt angle',
                backgroundColor: window.chartColors.red,
                borderColor: window.chartColors.red,
                data: [                        
                ],
                fill: false,
            }]
        },
        options: {
            responsive: true,
            title: {
                display: true,
                text: 'Tilt angle'
            },
            tooltips: {
                mode: 'index',
                intersect: false,
            },
            hover: {
                mode: 'nearest',
                intersect: true
            },
            scales: {
                xAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Hour'
                    }
                }],
                yAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Degrees'
                    }
                }]
            }
        }
    };

    data.forEach(function (item, index) {
        var options = { day: 'numeric', hour: 'numeric', minute: 'numeric' };
        var date = new Date(item.timestamp);
        var label = date.toLocaleDateString("en-GB", options)
        if ( label != 'Invalid Date' ){
            var leisure_voltage = item.voltages.voltage1;
            var engine_voltage = item.voltages.voltage2;
            var tilt = item.x;


            batteryVoltageChartConfig.data.labels.push(label);
            batteryVoltageChartConfig.data.datasets[0].data.push(engine_voltage)
            batteryVoltageChartConfig.data.datasets[1].data.push(leisure_voltage)

            tiltAngleChartConfig.data.labels.push(label);
            tiltAngleChartConfig.data.datasets[0].data.push(tilt)
        }
    });


    var vctx = document.getElementById('voltagecanvas').getContext('2d');
    window.batteryVoltageLine = new Chart(vctx, batteryVoltageChartConfig);
    var tctx = document.getElementById('tiltanglecanvas').getContext('2d');
    window.tiltAngleLine = new Chart(tctx, tiltAngleChartConfig);
      
});

