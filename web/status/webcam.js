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

function portOrStarboard(tilt){
  if ( tilt == 0 ) {
    return "level";
  }
  else if ( tilt > 0 ) {
    return "degrees to starboard";
  }
  return "degrees to port";
}

function getUrlParameter(name) {
    name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
    var regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
    var results = regex.exec(location.search);
    return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
};

function getSerialNumber() {
    return window.location.pathname.split("/").pop()
}

readTextFile("https://boatcam.io/status/"+getSerialNumber()+"/log", function(text){
    var DEFAULT_COLORS1 = ['#f08700', '#f49f0a', '#efca08', '#00a6a6', '#bbdef0'];
    var DEFAULT_COLORS2 = ['#7fb7be', '#357266', '#dacc3e', '#bc2c1a', '#7d1538'];

    var data = JSON.parse(text);
    var l = data.length-1;
    var date = new Date(data[l].timestamp);
    var leisure_voltage = data[l].voltages.voltage1;
    var engine_voltage = data[l].voltages.voltage2;
    var latitude = data[l].position.latitude;
    var longitude = data[l].position.longitude;
    var tilt = data[l].x;
    var tide = data[l].tide;
    var ip = data[l].ip;
    var temperature = data[l].temperature
    var disk_useage = data[l].disk.percent_used

    var options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour: 'numeric', minute: 'numeric' }
    document.getElementById("camera").src = "https://whqprggu22.execute-api.eu-west-2.amazonaws.com/beta/boatcam/"+getSerialNumber()+"/images/"+data[l].timestamp
    document.getElementById("date").innerHTML = date.toLocaleDateString("en-GB", options)
    document.getElementById("keel").style.transform = 'rotate(' + Math.round(tilt) + 'deg)'
    document.getElementById("tilt").innerHTML = Math.abs(Math.round(tilt))
    document.getElementById("tiltdirection").innerHTML = portOrStarboard(Math.round(tilt))
    document.getElementById("temperature").innerHTML = parseFloat(temperature).toFixed(1)
    document.getElementById("tide").innerHTML = parseFloat(tide).toFixed(2)
    document.getElementById("disk").innerHTML = Math.round(disk_useage)
    document.getElementById("serialnumber").innerHTML = getSerialNumber()

    var mymap = L.map('map').setView([latitude, longitude], 15);
    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 19,
        id: 'mapbox/streets-v11',
        tileSize: 512,
        zoomOffset: -1,
        accessToken: 'pk.eyJ1IjoiY3J5c3RhbG1hcmsiLCJhIjoiY2tiOWJpenY4MDZqODJ6bndyZjc3eTA2dSJ9.mITzzn_vH7IV56_CYA-Itg'
    }).addTo(mymap);
    var marker = L.marker([latitude, longitude]).addTo(mymap);   

        window.chartColors = {
        red: 'rgb(255, 99, 132)',
        orange: 'rgb(255, 159, 64)',
        yellow: 'rgb(255, 205, 86)',
        green: 'rgb(75, 192, 192)',
        blue: 'rgb(54, 162, 235)',
        blue_transparent: 'rgb(54, 162, 235, 0.2)',
        purple: 'rgb(153, 102, 255)',
        grey: 'rgb(201, 203, 207)'
    };

    var batteryVoltageChartConfig = {
        type: 'line',
        data: {
            labels: [],
            datasets: [
//            {
//                label: 'Engine battery',
//                backgroundColor: window.chartColors.red,
//                borderColor: window.chartColors.red,
//                data: [
//                ],
//                fill: false,
//            },
            {
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
                yAxisID: 'Tilt angle',
                label: 'Tilt angle',
                backgroundColor: window.chartColors.red,
                borderColor: window.chartColors.red,
                data: [                        
                ],
                fill: false
                },
                {
                    yAxisID: 'Tide height',
                    label: 'Tide height',
                    backgroundColor: window.chartColors.blue_transparent,
                    borderColor: window.chartColors.blue_transparent,
                    data: [                        
                    ],
                    fill: true
                }
            ]
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
                    id: 'Tilt angle',
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Degrees'
                    },
                    position: 'left',
                    scalePositionLeft: true
                },
                {
                    id: 'Tide height',
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'metres'
                    },
                    position: 'right',
                    scalePositionLeft: false,
                    min: 0,
                    max: 6
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
            var tide = item.tide;

            batteryVoltageChartConfig.data.labels.push(label);
//            batteryVoltageChartConfig.data.datasets[0].data.push(engine_voltage)
//            batteryVoltageChartConfig.data.datasets[1].data.push(leisure_voltage)
            batteryVoltageChartConfig.data.datasets[0].data.push(leisure_voltage)

            tiltAngleChartConfig.data.labels.push(label);
            tiltAngleChartConfig.data.datasets[0].data.push(tilt)
            tiltAngleChartConfig.data.datasets[1].data.push(tide)
        }
    });


    var vctx = document.getElementById('voltagecanvas').getContext('2d');
    window.batteryVoltageLine = new Chart(vctx, batteryVoltageChartConfig);
    var tctx = document.getElementById('tiltanglecanvas').getContext('2d');
    window.tiltAngleLine = new Chart(tctx, tiltAngleChartConfig);

    var evctx = document.getElementById('enginevoltagecanvas').getContext('2d');
    new Chart(evctx, {
    type: 'doughnut',
    data: {
        datasets: [{
            data: [engine_voltage, (12.8-engine_voltage)],
            backgroundColor: DEFAULT_COLORS1,
            label: 'Engine Battery Voltage'
        }],
        labels: ['Current Voltage', leisure_voltage+'v']
    },
    options: {
        responsive: true,
        legend: {
            display: false,
            position: 'top',
        },
        title: {
            display: false,
            fontSize: 20,
            text: 'Engine Voltage'
        },
        animation: {
            animateScale: true,
            animateRotate: true
        },
        plugins: {
            doughnutlabel: {
                labels: [
                    {
                        text: 'Engine Battery',
                        font: {
                            size: '40'
                        }
                    },
                    {
                        text: engine_voltage+'v',
                        font: {
                            size: 60
                        },
                        color: 'green'
                    }
                ]
            }
        }
    }
});

    var lvctx = document.getElementById('leisurevoltagecanvas').getContext('2d');
    new Chart(lvctx, {
    type: 'doughnut',
    data: {
        datasets: [{
            data: [leisure_voltage, (12.8-leisure_voltage)],
            backgroundColor: DEFAULT_COLORS1,
            label: 'Leisure Battery Voltage'
        }],
        labels: ['Current Voltage', leisure_voltage+'v']
    },
    options: {
        responsive: true,
        legend: {
            display: false,
            position: 'top',
        },
        title: {
            display: false,
            fontSize: 20,
            text: 'Leisure Voltage'
        },
        animation: {
            animateScale: true,
            animateRotate: true
        },
        plugins: {
            doughnutlabel: {
                labels: [
                    {
                        text: 'Leisure Battery',
                        font: {
                            size: '40'
                        }
                    },
                    {
                        text: leisure_voltage+'v',
                        font: {
                            size: 60
                        },
                        color: 'green'
                    }
                ]
            }
        }
    }
});

});

