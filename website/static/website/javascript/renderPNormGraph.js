function renderPNorm(data){
    const x_values = data.map(d=>d[0]);
    const max = Math.max(...x_values);
    const min = Math.min(...x_values);
    const shrinkFactor = (max - min)*.30

    var optionsPNorm = {
        series: [{
          name: "|ϕ|" + '<sup>2</sup>',
          type: "area",
          data: data,
        }
    
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
                    x: 0,
                    y: 0,
                    marker: {
                        size: 5,
                        fillColor: "#fff",
                        strokeColor: "purple",
                        radius: 2,
                    },
                label: {
                    borderColor: "#5C00FF",
                    offsetY: 0,
                    style: {
                        color: "#fff",
                        background: "#5C00FF"
                    },
                    text: "⟨P⟩ = " + 0.000
                }
            }],
        
        },
        colors: ['#631DE0'],
        dataLabels: {
            enabled: false
        },
        tooltip: {
            enabled: true, 
            x:{
                show: false,
                formatter: (input) => {return "Momentum: " + input.toPrecision(3)}
            },
            y:{
                formatter: (input) => {return input.toPrecision(3)}
            }
        },
        stroke: {
            width: 2,
            curve: 'smooth'
        },
        fill: {
            opacity: 2,
            type: 'gradient',
            gradient: {
                enabled: true,
                opacityFrom: 1,
                opacityTo: .7
            }
        },
        title: {
            text: "Momentum-space Probability Density",
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
            min: min + shrinkFactor,
            max: max - shrinkFactor,
            type: "numeric",
            tickAmount: 6,
            labels:{
                show: true,
                formatter: function(val){
                    return val.toPrecision(3)
                }
            },
            title:{
                text: "Momentum (eV⋅s/m)"
            }
        },
        yaxis: [{
            axisBorder: {
                show: true,
                color: undefined 
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
                text: "|ϕ|²",
                style: {
                    color: undefined,
                    fontSize: '16px',
                }
            },
        }]
    }; 
var PNormchart = new ApexCharts(document.querySelector("#pnorm"), optionsPNorm)
PNormchart.render();
}