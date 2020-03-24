Highcharts.chart('ebitda_chart', {
    data: {
        table: 'ebitda-data'
    },
    chart: {
        zoomType: 'xy'
    },
    title: {
        text: 'Objectif mensuel'
    },
    yAxis: {
        labels: {
            formatter: function () {
                return this.value/1000 + 'k';
            }
        },
    },
    xAxis: {
        tickInterval: 1,
    },
    tooltip: {
        pointFormat: '{series.name} \: <b>{point.y:,.0f} </b>'
    },
    series: [{
            name: 'Ebitda - Budget par mois',
            type: 'column',
            color: '#567bdb'
        },
        {
            name: 'Ebitda - cumulé (Budget)',
            type: 'spline',
            color: '#2450ff'
        }]
});