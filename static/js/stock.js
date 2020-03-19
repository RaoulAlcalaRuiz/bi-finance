Highcharts.chart('stock_chart', {
    data: {
        table: 'stock-data'
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
            name: 'stock - actuel',
            type: 'column',
            color: '#fc8d1e'
        },
        {
            name: 'stock - objectif',
            type: 'spline',
            color: '#2450ff'
        }]
});