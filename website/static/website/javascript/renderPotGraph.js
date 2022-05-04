function renderPot(data, energyLevel){
    var optionsPot = {
        series: [{
          name: "Energy-Level",
          type: "line",
          data: energyLevel,
        },{
          name: "Potential",
          type: "area",
          data: data
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
        tooltip: {
            enabled: true, 
            enabledOnSeries: [1],
            x:{
                show: false,
                formatter: (input) => {return "Position: " + input.toPrecision(3)}
            },
            y:{
                formatter: (input) => {return input.toPrecision(3)}
            }
        },
        colors: ['#FF0000', '#0000FF'],
        stroke: {
            curve: ['smooth', 'stepline'],
            width: [2, 2],
        },
        fill:{
            type: ["solid", "gradient"],
            colors:["#ff0000", "#0000ff"],
            opacity: [2],
            gradient: {
                type: 'vertical',
                enabled: true,
                opacityFrom: 1,
                opacityTo: .5
            },
        },
        title: {
            text: "Potential Well",
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
        plotOptions: {
            area: {
                fillTo: 'end',
            }
        },
        grid: {
            row: {
                colors: undefined, 
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
            }
        },
        yaxis: [
        {
            axisBorder: {
                show: true,
                color: undefined
            },
            opposite: false, 
            show: true,
            showForNullSeries: true,
            seriesName: undefined,
            tickAmount: 6,
            forceNiceScale: true,
            floating: false,
            decimalsInFloat: undefined,
            labels: {
                show: true,
                formatter: function(val){
                    return val.toFixed(2);
                }
            },
            title: {
                text: "POTENTIALS (eV)",
                style: {
                    color: undefined,
                }
            },
        }]
    }; 

    var Potchart = new ApexCharts(document.querySelector("#pot"), optionsPot)
    Potchart.render();
}