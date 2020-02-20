
 let real_sales = cumulateGoal(getSaleValue("real"));
 let goal_sales = cumulateGoal(getSaleValue("goal"));

 function getSaleValue(id_dom){
     let real = document.getElementById(id_dom);
     let last_comma = real.innerHTML.lastIndexOf(',');
     let real_text = real.innerHTML.slice(0,last_comma) + real.innerHTML.slice(last_comma+1);
     return JSON.parse(real_text);
 }

 function cumulateGoal(array){
    let newArray = [];
    let valueCumulative = 0;
    for(let i = 0; i < array.length; i++){
        if(array[i] != null){
            valueCumulative += array[i];
            newArray[i] = valueCumulative;
        }
    }
    return newArray;
 }

 Highcharts.chart('container', {
    chart: {
        type: 'area'
    },
    title: {
        text: 'Chiffre d\'affaires Réalité/Objectif'
    },
    xAxis: {
        allowDecimals: false,
        labels: {
            formatter: function () {
                return this.value; // clean, unformatted number for year
            }
        },
        accessibility: {
            rangeDescription: 'Range: 1 to 12.'
        }
    },
    yAxis: {
        labels: {
            formatter: function () {
                return this.value / 1000 + 'k';
            }
        }
    },
    tooltip: {
        pointFormat: '{series.name} \: <b>{point.y:,.0f}</b>'
    },
    plotOptions: {
        area: {
            pointStart: 1,
            marker: {
                enabled: false,
                symbol: 'circle',
                radius: 2,
                states: {
                    hover: {
                        enabled: true
                    }
                }
            }
        }
    },
    series: [{
        name: 'Réalité',
        data: real_sales,
        color: '#2748ab',
    }, {
        name: 'Objectif',
        data: goal_sales,
        color: '#5e8fbd',
    }]
});
