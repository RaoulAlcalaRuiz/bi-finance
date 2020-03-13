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
        },
        min: 0,
        max: 100,
        tickInterval: 20,
    },
    tooltip: {
        pointFormat: '{series.name} \: <b>{point.y:,.0f}</b>'
    },
    series: [{
            name: 'OTD mensuel',
            type: 'column',
            color: '#2748ab'
        },
        {
            name: 'OTD cumulé',
            type: 'spline',
            color: '#000000'
        },
        {
            name: 'OTD - Objectif',
            type: 'spline',
            color: '#fc0000'
        }]
});

Highcharts.chart('delivery_quality', {
    data: {
        table: 'quality'
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
        },
        min: 0,
        max: 100,
        tickInterval: 20,
    },
    tooltip: {
        pointFormat: '{series.name} \: <b>{point.y:,.0f} </b>'
    },
    series: [{
            name: 'OQD mensuel',
            type: 'column',
            color: '#2748ab'
        },
        {
            name: 'OQD cumulé',
            type: 'spline',
            color: '#000000'
        },
        {
            name: 'OQD - Objectif',
            type: 'spline',
            color: '#fc0000'
        }]
});
