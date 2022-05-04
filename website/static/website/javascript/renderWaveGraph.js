function renderWave(data, expX){
    var optionsBase = {
        series: [{
            name:  'Ψ',
            type: "line",
            data: data,
        },
        ],
        chart: {
            height: 350,
            zoom: {
                type: 'x',
                enabled: true,
                autoScaleYaxis: true
            },
            toolbar: {
            autoSelected: 'zoom'
            },
        },
        dataLabels: {
            enabled: false
        },
        annotations:{
            position:"front",
            points: [{
                x: expX,
                y: 0,
                marker: {
                    size: 5,
                    fillColor: "#fff",
                    strokeColor: "red",
                    radius: 2,
                },
                label: {
                    borderColor: "#FF4560",
                    offsetY: 0,
                    style: {
                        color: "#fff",
                        background: "#FF4560"
                    },
                    text: "⟨X⟩ = " + expX.toPrecision(3)
                }
            }],
        },
        colors: ['#E01D6A', '#0000FF'],
        stroke: {
            curve: ['smooth', 'stepline'],
            width: [2, 2]
        },
        tooltip: {
            enabled: true, 
            x:{
                show: false,
                formatter: (input) => {return "Position: " + input.toPrecision(3)}
            },
            y:{
                formatter: (input) => {return input.toPrecision(3)}
            }
        },
        fill:{
            type: ["solid", "solid"],
            colors:["#ff0000", "#0000ff"],
            gradient: {
                shade: 'dark',
                type: "verticle",
                shadeIntensity: 0.5,
            },
        },
        title: {
            text: "Wavefunction",
            align: 'left',
            margin: 0,
            offsetX: 0,
            offsetY: 0,
            floating: false,
            style: {
                fontSize:  '18px',
                fontWeight:  'bold',
                fontFamily:  undefined,
                color: undefined
            },
        },
        subtitle: {
            text: "",
            align: 'left',
            margin: 0,
            offsetX: 0,
            offsetY: 30,
            floating: false,
            style: {
                fontSize:  '12px',
                fontWeight:  'normal',
                fontFamily:  undefined,
                color:  undefined
            },
        },
        grid: {
            row: {
                colors: undefined, //'#ddd', 'transparent'], // takes an array which will be repeated on columns
                opacity: 0.5
            },
        },
        xaxis: {
            type: "numeric",
            tickAmount: 6,
            labels:{
                show: true,
                formatter: function(val){
                    return val.toPrecision(3)
                }
            },
            title: {
                text: "Position (meters)"
            }
        },
        yaxis: [{
            axisBorder: {
                show: true,
                color: undefined //'#FF0000'
            },
            show: true,
            showForNullSeries: true,
            seriesName: undefined,
            tickAmount: 4,
            forceNiceScale: true,
            floating: false,
            decimalsInFloat: undefined,
            labels: {
                formatter: function(val, index){
                    return parseFloat(val.toFixed(3)).toExponential();
                }
            },
            title: {
            text: "Ψ",
                style: {
                    color: undefined,
                    fontSize: "16px"
                }
            },
        }]
    }; 
    var Basechart = new ApexCharts(document.querySelector("#base"), optionsBase)
    Basechart.render();
}