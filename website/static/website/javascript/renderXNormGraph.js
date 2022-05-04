function renderXNorm(data){

    const integrate = (xy, a, b) =>{

        let area = 0.0;
        let dx = (b-a)/(xy.length-1);
        let xy_right = xy.slice(1);
        let xy_left =  xy.slice(0,-1);
        for(let i = 0; i < xy.length; i++){
            if(a < xy[i][0] && b > xy[i][0]){
              area += ((xy_right[i][0]- xy_left[i][0])/2.0)*(xy_left[i][1] + xy_right[i][1]);
            }  
        }
        return area 
      }
    
    var optionsNorm = {
        series: [{
            name:  '|Ψ|' + '<sup>2</sup>',
            data: data,
        }],
        chart: {
            height: 350,
            type: 'area',
            toolbar: {
                tools: {
                    selection: true,
                },
                autoSelected: 'selection',
            },
            events:{
                selection: function(chartContext, { xaxis, yaxis }) {
                    let section = integrate(data, xaxis.min, xaxis.max)
                    let total = integrate(data, Normchart.w.globals.minX, Normchart.w.globals.maxX)
                    console.log(((section/total)*100).toFixed(4))
                    const div = document.querySelector("#probability-precentage");
                    div.innerHTML = ((section/total)*100).toFixed(4) + "%"; 
                }
            },
            selection: {
                enabled: true,
                type: 'x',
                fill: {
                    color: '#FFFFFF',
                    opacity: .5
                },
                stroke: {
                    width: 1,
                    dashArray: 3,
                    color: undefined,
                    opacity: 0.4
                },
                xaxis: {
                    min: 0,
                    max: 1e-9
                },
            },
        },
        colors: ['#C542E9'],
        dataLabels: {
          enabled: false
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
                opacityTo: .4
            }
        },
        legend: {
            position: 'top',
            horizontalAlign: 'left'
        },
        title: {
            text: "Position-space Probability Density",
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
            text: "Selected Enclosed Area:",
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
        xaxis: {
            type: 'numeric',
            tickAmount: 6,
            labels:{
                show: true,
                formatter: function(val){
                    return val.toPrecision(3)
                }
            },
            title:{
                text: "Position (meters)"
            }
        },
        yaxis: {
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
                text: '|Ψ|²',
                style: {
                    color: undefined,
                    fontSize: '16px',
                }
            },
        }
    };
    var Normchart = new ApexCharts(document.querySelector("#norm"), optionsNorm)
    Normchart.render();
}