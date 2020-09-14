function readTextFile(file, callback) {
    console.log("Reading file "+file)
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

function getDates() {
    const twoWeeksAgo = new Date()
    const now = new Date()
    const interval = 1000 * 60 * 60;
    const duration = endDate - startDate;
    const steps = duration / interval;
    return Array.from({length: steps+1}, (v,i) => new Date(startDate.valueOf() + (interval * i)));
}

function secondsToDhms(seconds) {
    seconds = Number(seconds);
    var d = Math.floor(seconds / (3600*24));
    var h = Math.floor(seconds % (3600*24) / 3600);
    var m = Math.floor(seconds % 3600 / 60);

    var dDisplay = d > 0 ? d + (d == 1 ? " day, " : " days, ") : "";
    var hDisplay = h > 0 ? h + (h == 1 ? " hour, " : " hours, ") : "";
    var mDisplay = m > 0 ? m + (m == 1 ? " minute, " : " minutes, ") : "";
    return dDisplay + hDisplay + mDisplay;
}

function portOrStarboard(tilt){
  if ( tilt == 0 ) {
    return "level";
  }
  else if ( tilt > 0 ) {
    return tilt+"&deg; to starboard";
  }
  return Math.abs(tilt)+"&deg; to port";
}

function getUrlParameter(name) {
    name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
    var regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
    var results = regex.exec(location.search);
    return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
};

function getSerialNumber() {
    sn = window.location.pathname.split("/").pop()
    return sn
}

readTextFile("https://boatcam.io/device/"+getSerialNumber()+"/log.json", function(text){
    var DEFAULT_COLORS1 = ['#f08700', '#f49f0a', '#efca08', '#00a6a6', '#bbdef0'];
    var DEFAULT_COLORS2 = ['#7fb7be', '#357266', '#dacc3e', '#bc2c1a', '#7d1538'];

    var data = JSON.parse(text).logs;
    var l = data.length-1;
    var date = new Date(data[l].timestamp);
    var leisure_voltage = data[l].voltages.voltage1;
    var engine_voltage = data[l].voltages.voltage2;
    var latitude = data[l].position.latitude;
    var longitude = data[l].position.longitude;
    if (data[l].angles)
        var tilt = data[l].angles.roll;
    else
        var tilt = 'Unknown'
    var tide = data[l].tide;
    var ip = data[l].ip;
    var temperature = data[l].temperature
    var disk_useage = data[l].disk.percent_used
    var uptime = data[l].uptime
    var serialnumber = getSerialNumber()
    var image_url = "https://boatcam.io/device/"+serialnumber+"/images/"+data[l].timestamp+".jpg"

    var options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour: 'numeric', minute: 'numeric' }
    document.getElementById("camera").src = image_url
    document.getElementById("date").innerHTML = date.toLocaleDateString("en-GB", options)
    document.getElementById("keel").style.transform = 'rotate(' + Math.round(tilt) + 'deg)'
    document.getElementById("tilt").innerHTML = portOrStarboard(Math.round(tilt))
    document.getElementById("temperature").innerHTML = parseFloat(temperature).toFixed(1)
    document.getElementById("tide").innerHTML = parseFloat(tide).toFixed(2)
    document.getElementById("disk").innerHTML = Math.round(disk_useage)
    document.getElementById("serialnumber").innerHTML = serialnumber
    document.getElementById("uptime").innerHTML = secondsToDhms(uptime)

    var serialNumberValidation=/^[0-9a-z]{12}$/;
    if ( !serialnumber.match(serialNumberValidation)) {
        window.location.replace("/");
    }
    else {
        if ( latitude != 'Unknown' && longitude != 'Unknown' ) {
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
        }
        else {
            document.getElementById("map").innerHTML='GPS Location Unavailable'
        }
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
                {
                    label: 'Engine battery',
                    backgroundColor: window.chartColors.red,
                    borderColor: window.chartColors.red,
                    data: [
                    ],
                    fill: false,
                },
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
                    yAxisID: 'Roll angle',
                    label: 'Roll angle',
                    backgroundColor: window.chartColors.red,
                    borderColor: window.chartColors.red,
                    data: [
                    ],
                    fill: false
                    },
                    {
                    yAxisID: 'Pitch angle',
                    label: 'Pitch angle',
                    backgroundColor: window.chartColors.green,
                    borderColor: window.chartColors.green,
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
                        id: 'Roll angle',
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: 'Degrees'
                        },
                        position: 'left',
                        scalePositionLeft: true
                    },
                    {
                        id: 'Pitch angle',
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
                if (item.angles){
                    var roll = item.angles.roll;
                    var pitch = item.angles.pitch;
                }
                else {
                    var roll = 0;
                    var pitch = 0;
                }
                var tide = item.tide;

                batteryVoltageChartConfig.data.labels.push(label);
                if ( engine_voltage > 2)
                    batteryVoltageChartConfig.data.datasets[1].data.push(engine_voltage)
                if ( leisure_voltage > 2)
                    batteryVoltageChartConfig.data.datasets[0].data.push(leisure_voltage)

                tiltAngleChartConfig.data.labels.push(label);
                tiltAngleChartConfig.data.datasets[0].data.push(roll)
                tiltAngleChartConfig.data.datasets[1].data.push(pitch)
                tiltAngleChartConfig.data.datasets[2].data.push(tide)
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
                data: [engine_voltage, (14.2-engine_voltage)],
                backgroundColor: DEFAULT_COLORS1,
                label: 'Engine Battery Voltage'
            }],
            labels: ['Voltage', engine_voltage+'v']
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
                data: [leisure_voltage, (14.2-leisure_voltage)],
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
    }

});

