Highcharts.chart('delivery_in_time', {
    data: {
        table: 'delivery-in-time'
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
                return this.value;
            }
        }
    },
    tooltip: {
        pointFormat: '{series.name} \: <b>{point.y:,.0f}</b>'
    },
    series: [{
            name: 'OTB mensuel',
            type: 'column',
            color: '#2748ab'
        },
        {
            name: 'OTB cumulé',
            type: 'spline',
            color: '#000000'
        },
        {
            name: 'Objectif',
            type: 'spline',
            color: '#fc0000'
        }]
});
